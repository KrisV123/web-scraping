from pathlib import Path
from PyPDF2 import PdfReader
import ahocorasick #type: ignore
import regex as re
import pymupdf # type: ignore

try:
    from .settings import CHECK_DIGITAL_SIGNS #type: ignore
except:
    from settings import CHECK_DIGITAL_SIGNS #type: ignore

try:
    from .settings import KEYWORD_ALIASES, PATTERNS, PARAGRAPH_BUFFER, BUFFER #type: ignore
except:
    from settings import KEYWORD_ALIASES, PATTERNS, PARAGRAPH_BUFFER, BUFFER #type: ignore


def get_pdf_text_2(pdf_file: Path) -> str | None:
    """Returns text from pdf_file with pymupdf library
    Returns:
    text
    """
    if pdf_file.suffix.lower() != '.pdf':
        print('file is not pdf')
        return None

    with pymupdf.open(str(pdf_file)) as doc:
        all_text = ''
        for page in doc:
            text = page.get_text()
            all_text += text + ' '

    return all_text


def get_pdf_text(pdf_file: Path) -> str | None:
    """Returns text from pdf_file with PyPDF2 library
    Returns:
    text
    """

    if pdf_file.suffix.lower() == '.pdf':
        reader = PdfReader(pdf_file)
        all_pages = str()
            
        for page in reader.pages:
            text = page.extract_text()
            all_pages += text

        return all_pages
    else:
        print('file is not PDF')
        return None


def format_spaces(text: str) -> str:
    """Removes consecutive whitespace chars
    Returns:
    formated text
    """

    formated_text = str()
    index = 0

    while index < len(text) and text[index] in [' ', r'\n']:
        index += 1

    while index < len(text):
        if not text[index] == ' ' or\
           not text[index - 1] == ' ':
            formated_text += text[index]
        
        index += 1

    return formated_text

class result_class:
    def __init__(self,
                 result: bool,
                 messages: list[str],
                 keywords_found: list[str]):
        self.result = result
        self.messages = messages
        self.keywords_found = keywords_found


def check_PDF(text: str) -> result_class:
    """Scan file for leaks. Text is on imput
    Returns:
    Result_class instance
    """

    text = text.lower()
    ahoc = ahocorasick.Automaton()

    # making ahocarasic data structure
    for key, aliases in KEYWORD_ALIASES.items():
        for alias in aliases:
            ahoc.add_word(alias, (key, alias))
    ahoc.make_automaton()

    matches = list(ahoc.iter(text))
    messages: list[str] = list()
    result = False

    # searching regexes
    for end_pos, (canon_word, alias) in matches:
        if canon_word == 'banking':
            continue

        if canon_word == 'fyzicka osoba':
            parag_snippet = text[end_pos + 1 : end_pos + 1 + PARAGRAPH_BUFFER]

            if not isinstance(PATTERNS['banking'], dict):
                continue

            for key, pattern in PATTERNS['banking'].items():
                for catch in re.finditer(pattern, parag_snippet):
                    result = True
                    message = f'ERROR: {key} pattern found at position {catch.start()+end_pos-1} in fyzická osoba paragraph'
                    messages.append(message)
        else:
            snippet = text[end_pos + 1 : end_pos + 1 + BUFFER]

            if canon_word not in PATTERNS.keys():
                continue

            catch = re.search(PATTERNS[canon_word], snippet) #type: ignore

            if catch:
                result = True
                message = f'ERROR: {alias} found at position {catch.start()+end_pos-1}'
                messages.append(message)

    # warnings for edge cases
    if 'fyzicka osoba' in [canon_word for _, (canon_word, _) in matches]:
        message = 'WARNING: alias for fyzicka osoba was mentioned'
        messages.append(message)
    if 'adress' in [canon_word for _, (canon_word, _) in matches]:
        message = 'WARNING: alias for bydlisko was mentioned'
        messages.append(message)
    if 'signed digitally' not in [canon_word for _, (canon_word, _) in matches] and\
       CHECK_DIGITAL_SIGNS:
        message = 'WARNING: document is not digitally signed'
        messages.append(message)

    result_instance = result_class(result, messages, matches)

    return result_instance


if __name__ == '__main__':
    project_root = Path(__file__)
    project_folder = project_root.resolve().parents[2]
    pdf_files_folder = project_folder / 'pdf_files'
    
    for file in pdf_files_folder.iterdir():
        text = get_pdf_text_2(file)

        if text is not None:
            text = format_spaces(text)
            print(text)
            print()
            result = check_PDF(text)
            print(result.messages)

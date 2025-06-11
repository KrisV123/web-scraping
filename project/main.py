from pathlib import Path
from textwrap import dedent

from modules.download_file import get_files
from modules.read_pdf import check_PDF, get_pdf_text_2, format_spaces
from data import get_code_from_excel, SHEET_NAME_LIST, custom_values

def clean_folder(folder: Path) -> None:
    """Clear folder. Made for pdf_files folder
    Returns:
    None
    """

    for file in folder.iterdir():
        if file.name != '.gitkeep':
            file.unlink()


def failed_get_files_call(code: str, code_index: int) -> tuple[str, bool]:
    """Response for failed get_files function call
    Returns:
    tuple[ans_string, always True]
    """

    ans_string = dedent(f"""
        code: {code}
        code index: {code_index}\n
        WARINING: wasn't found any document
        (not found any document, link to the document,
        page wasn't loaded or code types don't match)
    """)

    return (ans_string, True)


def succ_get_files_call(code: str, code_index: int) -> tuple[str, bool]:
    """Response for successful get_files function call
    Returns:
    tuple[ans_string, are there any messages?]
    """

    pdf_files_dir = pdf_files_dir = Path(__file__).resolve().parents[1] / 'pdf_files'
    ans_string = f'code: {code}\ncode index: {code_index}\n'
    are_messages = False

    for order, pdf in enumerate(pdf_files_dir.iterdir()):
        if pdf.name == '.gitkeep':
            continue

        text = get_pdf_text_2(pdf)
        if text is not None:
            text = format_spaces(text)

        if text:
            ans_inst = check_PDF(text)

            if not are_messages and len(ans_inst.messages) > 0:
                are_messages = True

            ans_string += dedent(f"""
                order: {order}
                status: {'pass' if not ans_inst.result else 'FAIL'}
                messages: {ans_inst.messages if len(ans_inst.messages) != 0 else 'N/A'}
                    """)
        else:
            are_messages = True
            ans_string += dedent("""
                document can't be translated into text (probably scan)
                    """)

    return (ans_string, are_messages)


def parse_files(name: str, column: int, only_wrong: bool) -> None:
    """Main function"""

    data = get_code_from_excel(name, column)
    for code_index, code in enumerate(data):
        print(code_index + 1)

        pdf_files_dir = Path(__file__).resolve().parents[1] / 'pdf_files'
        clean_folder(pdf_files_dir)
        succ = get_files(code, 0.4)

        if not succ:
            ans_string, are_messages = failed_get_files_call(code, code_index)
        else:
            ans_string, are_messages = succ_get_files_call(code, code_index)
            if only_wrong and not are_messages:
                continue

        ans_string += '\n' + '_' * 40 + '\n\n'

        if not only_wrong or (only_wrong and are_messages):
            with open(f'answers/answer_{name}.txt', 'a', encoding='utf-8') as f:
                f.write(ans_string)

    clean_folder(pdf_files_dir)


if __name__ == '__main__':
    print('START')
    for name in SHEET_NAME_LIST:
        print(f'Sheet {name}')
        print()
        parse_files(name, 4, True)
        print()
    print('END')

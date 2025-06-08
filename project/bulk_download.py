from pathlib import Path
from textwrap import dedent

from modules.download_file import get_files
from data import get_code_from_excel


def clean_folder(folder: Path) -> None:
    """Clear folder. Made for pdf_files folder
    Returns:
    None
    """

    for file in folder.iterdir():
        if file.name != '.gitkeep':
            file.unlink()


def download_all_files(name: str, column: int) -> None:
    """Only downloads every every PDF
    Returns:
    None
    """

    def append_message(ans_string):
        with open('answer.txt', 'a', encoding='utf-8') as f:
            f.write(ans_string)


    data = get_code_from_excel(name, column)
    pdf_files_dir = Path(__file__).resolve().parents[1] / 'pdf_files'
    clean_folder(pdf_files_dir)

    for code_index, code in enumerate(data):
        print(code_index)
        succ = get_files(code, 0.4, code_index)
        if not succ:
            ans_string = dedent(f"""
                code: {code}
                code index: {code_index}\n
                WARINING: wasn't found any document
                (not found any document, link to the document,
                page wasn't loaded or code types don't match)
            """)
            append_message(ans_string)


if __name__ == '__main__':
    print('START')
    name = input('name: ')
    column = input('column: ')
    download_all_files(name, int(column))
    print('END')

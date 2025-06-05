from pathlib import Path
from textwrap import dedent

from modules.download_file import get_files #type: ignore
from modules.read_pdf import check_PDF, get_pdf_text #type: ignore
from data import data # type: ignore

def clean_folder(folder: Path) -> None:
    for file in folder.iterdir():
        file.unlink()


def parse_files(only_wrong: bool) -> None:
    for code_index, code in enumerate(data):
        succ = get_files(code, 0.4)

        if not succ:
            error = True
            ans_string = dedent(f"""
                code: {code}\n
                WARINING: wasn't found any document
                (not found any document, link to the document or page wasn't loaded)
            """)
        else:
            pdf_files_dir = pdf_files_dir = Path(__file__).resolve().parent.parent / 'pdf_files'
            ans_string = f'code: {code}\ncode index: {code_index}\n'
            error = False

            for order, pdf in enumerate(pdf_files_dir.iterdir()):
                text = get_pdf_text(pdf)
                if text:
                    ans_inst = check_PDF(text)
                else:
                    ans_string += dedent("""
                        document can't be translated into text (probably scan)
                            """)
                    break

                if only_wrong:
                    # taking as error even if warining occoured
                    if ans_inst.messages != 0:
                        error = True
                    else:
                        continue

                ans_string += dedent(f"""
                    order: {order + 1}
                    status: {'pass' if not ans_inst.result else 'FAIL'}
                    messages: {ans_inst.messages if len(ans_inst.messages) != 0 else 'N/A'}
                            """)

        ans_string += '\n' + '_' * 40 + '\n\n'

        if not only_wrong or (only_wrong and error):
            with open('answer.txt', 'a', encoding='utf-8') as f:
                f.write(ans_string)

        clean_folder(pdf_files_dir)


if __name__ == '__main__':
    print('START')
    print('processing...')
    parse_files(True)
    print('END')

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from random import uniform
from time import sleep

try:
    from .request_headers import generate_header # type: ignore
    from .settings import TIMEOUT #type: ignore
except:
    from request_headers import generate_header # type: ignore
    from settings import TIMEOUT #type: ignore

def get_code_list(code: str) -> list[str]:
    code_list: list[str] = ['','','','']
    pos = 0
    for char in code:
        if char != '/':
            code_list[pos] += char
        else:
            pos += 1
    return code_list


def get_hrefs_url(code_list: list[str],
                  headers: dict[str, str],
                  min_wait_time: float) -> list[str] | None:
    x, y, z, w = code_list
    url = f'https://www.crz.gov.sk/2171273-sk/centralny-register-zmluv/?art_zs2=&art_predmet=&art_ico=&art_suma_spolu_od=&art_suma_spolu_do=&art_datum_zverejnene_od=&art_datum_zverejnene_do=&art_rezort=0&art_zs1=&nazov={x}%2F{y}%2F{z}%2F{w}&art_ico1=&odoslat=&ID=2171273&frm_id_frm_filter_3=683099544838d'

    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    except:
        print('request for get_hrefs_url function failed')
        return None

    sleep(min_wait_time + uniform(0, 0.3))
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    href_urls = list()

    if table:
        for a in table.find_all('a'): # type: ignore
            href = a['href']
            if href[0] == '/' and href[:1] == '/':
                url_with_pdf = 'https://www.crz.gov.sk' + href
                href_urls.append(url_with_pdf)
    else:
        return None
    return href_urls


def get_pdf_list(url: str,
                 headers: dict[str, str],
                 min_wait_time: float,
                 pdf_url_list: list[str] | None) -> list[str]:
    if pdf_url_list is None:
        pdf_url_list = list()

    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    except:
        print('request for getting get_pdf_list function failed')
        return pdf_url_list

    sleep(min_wait_time + uniform(0, 0.3))
    soup = BeautifulSoup(resp.text, 'html.parser')

    # if addends are also there
    addents = soup.find('h2', string='Dodatky:')
    if addents:
        table = soup.find('table')
        for a in table.find_all('a'): # type: ignore
            href = a['href']
            if href[0] == '/' and href[:1] == '/':
                url_with_pdf = 'https://www.crz.gov.sk' + href
                get_pdf_list(url_with_pdf, headers, min_wait_time, pdf_url_list)

    wrapper_divs = soup.find_all('div', class_='card mb-3')
    for div in wrapper_divs:
        if div.find('h2', string='Príloha'): # type: ignore
            wrapper_div = div
            break

    if wrapper_div:
        for a in wrapper_div.find_all('a'): #type: ignore
            href = a['href']
            href_path = Path(href)
            if href_path.suffix.lower() == '.pdf':
                url = 'https://www.crz.gov.sk' + href
                pdf_url_list.append(url)
    else:
        print('WARNING: table with href not found')

    return pdf_url_list


def download_PDF(url: str,
                 dest_path: Path,
                 min_wait_time: float) -> None:
    try:
        resp = requests.get(url, timeout=TIMEOUT)
    except:
        print('request for download_PDF function failed')
        return None

    sleep(min_wait_time + uniform(0, 0.3))
    if resp.status_code >= 400:
        print('Status error, cant download file')
        return None

    with open(dest_path, 'wb') as f:
        for chunk in resp.iter_content():
            if chunk:
                f.write(chunk)


def get_files(code: str, min_wait_time: float) -> bool:
    """finds and downloads every PDF file into pdf_files folder
    
    Returns:
    True if was succesful and False if not
    """
    requests.Session()
    if '/' in code:
        code_list = get_code_list(code)
    else:
        print('verzia kodu bez lomitok nie je este implementovana')
        return False
    headers = generate_header()
    href_urls = get_hrefs_url(code_list, headers, min_wait_time)
    if not href_urls:
        print("WARNING: href was expacted but wasn't fount")
        return False
    pdf_files_dir = Path(__file__).resolve().parent.parent.parent / 'pdf_files'

    if href_urls is None:
        print('WARNING: document not found')
        return False

    pdf_index = 1
    for href in href_urls:
        pdf_list = get_pdf_list(href, headers, min_wait_time, None)
        for pdf in pdf_list:
            download_PDF(pdf,
                         pdf_files_dir / f'pdf_{pdf_index}.pdf',
                         min_wait_time)
            pdf_index += 1
    
    return True


if __name__ == '__main__':
    # s jednym dodatkom - 20/01/54E/4095
    # s dodatkami - 20/01/54E/1933
    # dva dokumenty pod jednym kodom - 22/01/54E/1077
    # bez dokumentu - 15/01/54BAZ/54
    get_files('20/01/54E/1808', 0.4)

import pandas as pd
from pathlib import Path

SHEET_NAME_LIST: list[str] = ['Horňáková', 'Reichová', 'Jurčovičová', 'Króliková',
                             'Duduka', 'Zboroň', 'Chibeya', 'Kukučková', 'Malíková',
                             'Cviková', 'Fabianová', 'Bakajová', 'Horanová', 'Glatzová',
                             'Banyák', 'Kunová', 'Zbončáková', 'Veselá', 'Mužiková',
                             'Vargová', 'Jakubíková', 'Barošová', 'Nádaská', 'Dehelánová',
                             'Balážová', 'Bučková', 'Marková', 'Staňová', 'Baranová',
                             'Ostrožlíková', 'Matušťáková', 'Jenčová', 'Bažíková',
                             'Melichová']

def get_code_from_excel(sheet_name: str, column_ord: int) -> list[str]:
    """Parse excel file 'kontrola crz.xlsx' and
    returns all codes from specific sheet
    Returns:
    list[code]
    """

    excel_path = Path(__file__).resolve().parent.parent / 'kontrola crz.xlsx'
    excel_file = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
    code_list = excel_file.iloc[:, column_ord - 1].astype(str).tolist()
    return code_list


def test_values() -> list[str]:
    """Just for quick test
    
    ERRORS:\n
    1. '20/01/54E/1933' - bydlisko\n
    2. '20/01/54E/2329' - rodne cislo (je bez lomitka)\n
    3. '20/01/54E/906' - correct\n
    4. '20/01/54E/1808' - bydlisko\n
    5. '17/01/051/152' - chýba dokument\n
    Returns:
    list[code]
    """

    data = [
        '20/01/54E/1933',
        '20/01/54E/2329',
        '20/01/54E/906',
        '20/01/54E/1808',
        '17/01/051/152'
    ]
    return data


def test_values_2() -> list[str]:
    """Codes without backslash
    Returns:
    list[str]
    """

    data = [
        '121114094457',
        '120807115358',
        '120831082859',
    ]
    return data

def test_values_3() -> list[str]:
    """Codes with leaked ID card number
    Returns:
    list[str]
    """

    data = [
        '22/01/54U/2',
        '22/01/54U/3',
        '22/01/54U/4',
        '22/01/54U/9'
    ]
    return data

def custom_values() -> list[str]:
    """Add values witch you want. Ideal for simulating
    real imput from excel sheet
    Returns:
    list[str]"""

    data = [
        '19/01/051/55',
        '20/01/54E/4184'
    ]
    return data


if __name__ == '__main__':
    code_list = get_code_from_excel('Jurčovičová', 4)
    print(code_list)
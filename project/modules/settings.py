import regex as re

KEYWORD_ALIASES: dict[str, list[str]] = {
    'birth_number': ['rodné číslo', 'rod. č.', 'r. č.', 'rč.'],
    'date': ['dátum narodenia', 'dátum nar.', 'dát. nar.', 'dat. nar.', 'd. nar.'],
    'adress': ['trvalý pobyt', 'bydlisko', 'trv. pobyt', 'trvale bytom'],
    'banking': ['bankové spojenie', 'iban', 'číslo účtu', 'č. účtu', 'číslo u.'],
    'ID_card_num': ['číslo op', 'číslo občianskeho preukazu'],

    'signed_digitally': ['podpísané elektronicky'],
    'fyzicka osoba': [' fo ', 'fyzická osoba', 'fyzickou osobou', 'zuoz', 'zoz']
}

day: str = r'(0?[1-9]|[1-2][0-9]|3[0-1])'
month: str = r'(0?[1-9]|1[0-2])'
year: str = r'(?:\d{2})?\d{2}'
date: re.Pattern[str] = re.compile(rf'\b{day}\.{month}\.{year}\b')

place: str = r'[\p{L}\. ]+' # city, street, country
number: str = r'(\d+([A-Z])?|[A-Z])' # č.p, č.o, číslo-písmeno bytu
post_number: str = r'((\d{3} \d{2})|(\d{5}))'
pavilon: str = r'(pavilón|blok|objekt|budova|pavilón \p{L}{2,}|\p{L}{2,} pavilón) (č. )?(([A-Z]?(\d+)?)|(\d+[A-Z]))'
adress: str = fr'\b{place} {number}(/{number})?(/{number})?((,| -) {pavilon})?, {post_number}(,)?\s+{place}\b'

PATTERNS: dict[str, str | re.Pattern[str] | dict[str, str | re.Pattern[str]]] = {
    'birth_number': r'\b\d{6}[/-]?\d{4}\b', # mozno aj pomlcka
    'date': date,
    'adress': adress,
    'banking': {
        'bank_num': r'\b(\d{1,6}-)?\d{10}/\d{4}\b',
        'iban': r'\b[a-zA-Z]{2}\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b',
    },
    'ID_card_num': r'\b[a-z]{2}\d{6}\b'
}

BUFFER: int = 50
PARAGRAPH_BUFFER: int = 500
TIMEOUT: float = 10
CHECK_DIGITAL_SIGNS: bool = False
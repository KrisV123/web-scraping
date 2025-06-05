from random import choices

user_agents = [
    # Windows (mid-2025)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6123.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/120.0.1982.54 Safari/537.36",

    # macOS (mid-2025)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6123.130 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.5993.117 Safari/537.36",

    # Linux (mid-2025)
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6123.130 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",

    # iPhone/iPad (iOS 17, mid-2025)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/19E240 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/19E241 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/19E247 Safari/605.1.15",

    # Android (mid-2025)
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.142 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.117 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.5993.117 Mobile Safari/537.36",
]

user_agent_weights = [
    # Windows
    0.1966,  # Chrome 120 on Windows 10
    0.0105,  # Firefox 124 on Windows 10
    0.0083,  # Firefox 126 on Windows 10
    0.0471,  # Edge 120 on Windows 10

    # macOS
    0.0185,  # Chrome 120 on macOS 14
    0.0030,  # Firefox 124 on macOS 13
    0.0245,  # Safari 17.5 on macOS 14
    0.0124,  # Chrome 119 on macOS 13

    # Linux
    0.0138,  # Chrome 120 on Linux
    0.0013,  # Firefox 124 on Linux

    # iPhone/iPad (iOS 17)
    0.0501,  # Safari 17.4 on iPhone
    0.0185,  # Safari 17.3 on iPad
    0.1170,  # Safari 17.5 on iPhone

    # Android
    0.1843,  # Chrome 116 on Android 11
    0.1189,  # Chrome 115 on Android 10
    0.1135,  # Chrome 118 on Android 12
    0.0617,  # Chrome 119 on Android 13
]

accepts = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "text/html,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "text/html;q=0.8,image/webp,*/*;q=0.5",
]

accept_weights = [
    0.90,
    0.05,
    0.03,
    0.02,
]

languages = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8",
    "it-IT,it;q=0.9,en;q=0.8",
    "sk-SK,sk;q=0.9",
    "cs-CZ,cs;q=0.9"
]

language_weights = [
    0.05,
    0.02,
    0.010,
    0.015,
    0.003,
    0.002,
    0.80,
    0.10,
]

#not currently user
sec_ua_platforms = [
    '"Windows"',
    '"macOS"',
    '"Linux"',
    '"iOS"',
    '"Android"',
]

# not currently used
sec_ua_platforms_weights = [
    0.27,
    0.05,
    0.015,
    0.19,
    0.475,
]

sec_ch_ua_values = [
    "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"124\"",
    "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\"",
    "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\"",
    "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"124\", \"Brave\";v=\"124\"",
    "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"124\", \"Opera\";v=\"85\"",
    ""
]

sec_ch_ua_values_weights = [
    0.35,
    0.20,
    0.05,
    0.01,
    0.02,
    0.37,
]

def choose_platform(user_agent: str) -> tuple[str, str]:
    if 'windows' in user_agent.lower():
        platform = 'Windows'
        sec_ch_ua_mobile = '?0'

    elif 'macintosh' in user_agent.lower():
        platform = 'MacOS'
        sec_ch_ua_mobile = '?0'

    elif 'linux' in user_agent.lower() and\
         'android' not in user_agent.lower():
        platform = 'Linux'
        sec_ch_ua_mobile = '?0'

    elif any(alias in user_agent.lower() for alias in ['iphone', 'ipad']):
        platform = 'IOS'
        sec_ch_ua_mobile = '?1'

    else:
        platform = 'Android'
        sec_ch_ua_mobile = '?0'

    return (platform, sec_ch_ua_mobile)


def generate_header() -> dict[str, str]:
    user_agent = choices(user_agents, weights=user_agent_weights, k=1)[0]
    accept_encoding = choices(accepts, weights=accept_weights, k=1)[0]
    accept_language = choices(languages, weights=language_weights, k=1)[0]
    sec_ch_ua = choices(sec_ch_ua_values, weights=sec_ch_ua_values_weights, k=1)[0]
    sec_ch_ua_platforms, sec_ch_ua_mobile = choose_platform(user_agent)

    rand_header = {
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
        "Accept-Language": accept_language,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-CH-UA": sec_ch_ua,
        "Sec-CH-UA-Mobile": sec_ch_ua_mobile,
        "Sec-CH-UA-Platform": sec_ch_ua_platforms
    }

    return rand_header
import os
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import List, Union, Dict


def get_soup_from_url(url: str) -> Union[BeautifulSoup, None]:
    """
    From given url it returns a BeautifulSoup object or empty in case of failure.

    Args:
        :str url: URL to be scrapped.

    Returns:
        Beautiful soup object of the URL page or empty string in case of failure.

    Raises:
        HTTPError: Log the http error code
        URLError:  Log the reason of URL error.
    """
    soup = ''
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        req = Request(url, headers=headers)
        response = urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    except HTTPError as httperror:
        print(f'HTTP error in {html}. Error code:', httperror.code)
    except URLError as urlerror:
        print(f'URL error in {html}. Reason: ', urlerror.reason)
    return soup


def extract_links(soup: BeautifulSoup) -> List[str]:
    """
    From BeautifulSoup object returns a list with links in it.

    Args:
        :BeautifulSoup soup: Object to be scrapped.

    Returns:
        List of URLs page.
    """
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links


def telegram_bot_sendtext(bot_message: str) -> None:
    """
    Send a message to bot set in .env file.

    Args:
        :str bot_message: Message to send.

    Returns:
        None.
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    bot_chatID = os.environ.get('TELEGRAM_BOT_CHAT', '')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text='
    send_text = send_text + '{}'.format(bot_message)
    requests.get(send_text)


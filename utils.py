import os
import requests
import aiohttp
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import List, Union, Dict


async def get_soup_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            return soup, url


def extract_links(soup: BeautifulSoup) -> List[str]:
    """
    From BeautifulSoup object returns a list with links in it.

    Args:
        :BeautifulSoup soup: Object to be scrapped.

    Returns:
        List of URLs page.
    """
    links = []
    for link in soup.find_all("a", href=True):
        links.append(link["href"])
    return links


def telegram_bot_sendtext(bot_message: str) -> None:
    """
    Send a message to bot set in .env file.

    Args:
        :str bot_message: Message to send.

    Returns:
        None.
    """
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    bot_chatID = os.environ.get("TELEGRAM_BOT_CHAT", "")
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
    )
    send_text = send_text + "{}".format(bot_message)
    requests.get(send_text)

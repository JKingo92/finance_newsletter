#!/usr/bin/env python3
import os
import re
import json
import asyncio
from utils import get_soup_from_url, extract_links, telegram_bot_sendtext


# Moneytimes
async def parse_moneytimes(soup, keywords):
    """Scrape moneytimes site"""
    result = {}
    top_news = soup.find("ol")
    top_news = extract_links(top_news)

    other_news = soup.findAll("h2", {"class": "news-item__title"})
    links_list = [extract_links(news)[0] for news in other_news]

    all_links = top_news + links_list
    all_links = list(set(all_links))  # Remove duplicates

    for link in all_links:
        try:
            print("Reading {} ...".format(link))
            soup = await get_soup_from_url(link)
            soup = soup[0]
            search = soup.findAll("strong")
            for word in search:
                word = word.getText()
                for kwords in keywords:
                    if bool(re.search(kwords, word, re.IGNORECASE)):
                        if link in result:
                            result[link].append(kwords)
                        else:
                            result[link] = [kwords]
        except Exception as ex:
            print(f"Something went wrong: {ex}")
    return result


async def parse_investing(soup, keywords):
    """Scrape investing site"""
    result = {}
    investing_url = os.environ.get("INVESTING_URL", "https://br.investing.com/")
    all_news = soup.findAll("div", {"class": "textDiv"})

    links_investing = [extract_links(news) for news in all_news]
    links_investing = [investing_url + x[0] for x in links_investing if len(x) > 0]
    for link in links_investing:
        try:
            print("Reading {} ...".format(link))
            soup = await get_soup_from_url(link)
            soup = soup[0]
            src = soup.find("span", {"class": "aqPopupWrapper js-hover-me-wrapper"})
            if src:
                for word in keywords:
                    if src.find(text=word):
                        if link in result:
                            result[link].append(word)
                        else:
                            result[link] = [word]
        except Exception as ex:
            print(f"Something went wrong: {ex}")
    return result


async def parse_infomoney(soup, keywords):
    """Scrape infomoney site"""
    result = {}
    src = soup.findAll("div", {"id": "infiniteScroll"}, limit=30)
    news = [extract_links(item) for item in src][0]
    news = list(set(news))  # Remove duplicates

    for link in news:
        try:
            print("Reading {} ...".format(link))
            soup = await get_soup_from_url(link)
            soup = soup[0]
            src = soup.findAll("p")
            for item in src:
                if item.a:
                    for kword in keywords:
                        if item.find(text=kword):
                            if link in result:
                                result[link].append(kword)
                            else:
                                result[link] = [kword]
        except Exception as ex:
            print(f"Something went wrong: {ex}")
    return result


async def main():
    with open("keywords.txt", "r") as file:
        file_content = file.read()
        keywords = file_content.split("\n")

        # newsletter = NewsletterScrapper(file_content)
        sites = {
            "moneytimes": os.environ.get(
                "MONEYTIMES_URL", "https://www.moneytimes.com.br/"
            ),
            "investing": os.environ.get("INVESTING_URL", "https://br.investing.com/"),
            "infomoney": os.environ.get(
                "INFOMONEY_URL", "https://www.infomoney.com.br/ultimas-noticias/"
            ),
        }

        tasks = []
        tasks.append(asyncio.create_task(get_soup_from_url(sites["moneytimes"])))
        tasks.append(asyncio.create_task(get_soup_from_url(sites["investing"])))
        tasks.append(asyncio.create_task(get_soup_from_url(sites["infomoney"])))
        raw_sites = await asyncio.gather(*tasks)

        tasks = []
        for site in raw_sites:
            if site[1] == "https://www.moneytimes.com.br/":
                tasks.append(asyncio.create_task(parse_moneytimes(site[0], keywords)))
            elif site[1] == "https://br.investing.com/":
                tasks.append(asyncio.create_task(parse_investing(site[0], keywords)))
            else:
                tasks.append(asyncio.create_task(parse_infomoney(site[0], keywords)))

        result = await asyncio.gather(*tasks)
        print(result)

        # Send message to bot
        telegram_bot_sendtext(result)
        # Write json file
        with open("news.json", "w") as jsonresult:
            json.dump(result, jsonresult)


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
import os
import re
import json
from utils import get_soup_from_url, extract_links, telegram_bot_sendtext

class NewsletterScrapper():
    '''
    Scraper that sends a json newsletter
    :list keywords: list of keywords to be scrapped on available sites

    '''
    def __init__(self, keywords):
        self.keywords = keywords
    
    # Moneytimes
    def scrap_moneytimes(self):
        '''Scrape moneytimes site'''
        result = {}
        soup = get_soup_from_url(os.environ.get('MONEYTIMES_URL', 'https://www.moneytimes.com.br/'))
        top_news = soup.find('ol')
        top_news = extract_links(top_news)

        links_list = []
        all_news = soup.findAll('h2',{'class':'news-item__title'})
        for news in all_news:
            links_list.append(extract_links(news)[0])
        
        all_links = top_news + links_list
        all_links = list(dict.fromkeys(all_links))
        
        for link in all_links:
            try:
                print('Reading {} ...'.format(link))
                soup = get_soup_from_url(link)
                search = soup.findAll('strong')
                for word in search:
                    word = word.getText()
                    for kwords in self.keywords:
                        if bool(re.search(kwords, word,re.IGNORECASE)):
                            if link in result:
                                result[link].append(kwords)
                            else:
                                result[link] = [kwords]
            except:
                None
        return result
    
    def scrap_investing(self):
        '''Scrape investing site'''
        result = {}
        investing_url = os.environ.get('INVESTING_URL', 'https://br.investing.com/')
        soup = get_soup_from_url(investing_url)
        all_news = soup.findAll('div',{'class': 'textDiv'})
        links_investing = []
        
        for news in all_news:
            links_investing.append(extract_links(news))
        
        links_investing = [investing_url + x[0] for x in links_investing if len(x) > 0]
        for link in links_investing:
            try:
                print('Reading {} ...'.format(link))
                soup = get_soup_from_url(link)
                src = soup.find('span',{'class':'aqPopupWrapper js-hover-me-wrapper'})
                if src:
                    for word in self.keywords:
                        if src.find(text = word):
                            if link in result:
                                  result[link].append(word)
                            else:
                                result[link] = [word]
            except:
                None
        return result
    
    def scrap_infomoney(self):
        '''Scrape infomoney site'''
        result = {}
        soup = get_soup_from_url(os.environ.get('INFOMONEY_URL', 'https://www.infomoney.com.br/ultimas-noticias/'))
        src = soup.findAll('div',{'id':"infiniteScroll"},limit = 30)
        news = [extract_links(item) for item in src][0]
        news = list(set(news)) # Remove duplicates
        
        for link in news:
            try:
                print('Reading {} ...'.format(link))
                soup = get_soup_from_url(link)
                src = soup.findAll('p')
                for item in src:
                    if item.a:
                        for kword in self.keywords:
                            if item.find(text = kword):
                                if link in result:
                                    result[link].append(kword)
                                else:
                                    result[link] = [kword]
            except:
                None
        return result

if __name__ == '__main__':
    with open('keywords.txt', 'r') as file:
        file_content = file.read()
        file_content = file_content.split('\n')
        newsletter = NewsletterScrapper(file_content)
        result = {**newsletter.scrap_moneytimes(), **newsletter.scrap_investing(),**newsletter.scrap_infomoney()}
        telegram_bot_sendtext(result)
        with open('news.json', 'w') as jsonresult:
            json.dump(result, jsonresult)


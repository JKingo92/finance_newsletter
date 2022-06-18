# finance_newsletter
Scraper for three brazilian finance news website (infomoney, investing and moneytimes).

Hi, this is a short project to training basic scraping on web using beautifulsoup. 
It sends a json to your Telegram bot or creates a news.json file according to .env file and keywords.txt
If you want to use the source code, please mention where did you take from :)

# Requirements
Install all libraries using 
```pip install -r requirements```

# How to run
After you have installed requirements, you need to set your .env file using .env.example as model
It's scraping using keywords defined in keywords.txt, you can set as you want too.
Just run using the command:
```python newsletter.py```
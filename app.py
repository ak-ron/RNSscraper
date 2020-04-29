#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 13:27:23 2020

@author: ronakshah
"""

from bs4 import BeautifulSoup as bs
import urllib.request
from flask import Flask, render_template, request, Response
from selenium import webdriver
import codecs
import requests
import re



app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_ticker():
    args = request.form.getlist('tickers[]')
    pattern = re.compile(r'\'(.*\.html?)\'')
    tickerdict = {}
    for i in args:
        tickerName = i
        res = requests.get('https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?nameCode=' + tickerName + '&page=1')
        soup = bs(res.text, "lxml")
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        fourwaykey = soup.find('a', {'title' : 'View chart'})['href'][-21:]
        url = 'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/company-news.html?fourWayKey=' + fourwaykey

        browser = webdriver.PhantomJS()
        browser.get(url)
        html = browser.page_source
        soup = bs(html, 'lxml')
        newslist = soup.find_all('li', {'class': 'newsContainer'})
        ticker_news = []
        for i in newslist:
            ticker_news.append([i.text.replace('\n','').replace('\t',''),'https://www.londonstockexchange.com'+ pattern.findall(i.find('a')['href'])[0]])
        tickerdict[tickerName]=ticker_news
    return render_template('index.html', ticker_dict=tickerdict)

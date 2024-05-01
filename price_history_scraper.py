import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_search_results(query, page=1):
    url = f"https://pricehistoryapp.com/search?q={query}&gsc.tab=0&gsc.q={query}&gsc.page=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    search_results = []
    for result in soup.select(".gsc-webResult"):
        title_elem = result.select_one(".gsc-webResult .gsc-webResult > .gs-title > a")
        if title_elem:
            title = title_elem.text.strip()
            link = "https://pricehistoryapp.com" + title_elem.get("href")
            search_results.append({"title": title, "link": link})

    return search_results

def get_price_history(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    price_history_div = soup.select_one(".content-width.w-full.flex.flex-col.py-5.px-3")
    if price_history_div:
        price_history_svg = price_history_div.select_one("svg")
        if price_history_svg:
            price_history_svg_html = str(price_history_svg)
            return price_history_svg_html
    return None
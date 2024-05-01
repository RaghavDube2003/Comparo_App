import streamlit as st
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
import random
from PIL import Image
import io

# Function to fetch and display product information from Flipkart
def price_flipkart(key):
    url_flip = f'https://www.flipkart.com/search?q={key}&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
    map = defaultdict(list)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    source_code = requests.get(url_flip, headers=headers)
    soup = BeautifulSoup(source_code.text, "html.parser")
    home = 'https://www.flipkart.com'
    for block in soup.find_all('div', {'class': 'tUxRFH'}):
        title, price, link, image_url = None, 'Currently Unavailable', None, None
        for heading in block.find_all('div', {'class': 'KzDlHZ'}):
            title = heading.text
        for p in block.find_all('div', {'class': 'Nx9bqj _4b5DiR'}):
            price = p.text[1:]
        for l in block.find_all('a', {'class': 'CGtC98'}):
            link = home + l.get('href')
        for img in block.find_all('img', {'class': 'DByuf4'}):
            image_url = img.get('src')
        map[title] = [price, link, image_url]

    return map

# Function to fetch and display product information from Amazon
def price_amzn(key):
    url_amzn = f'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={key}'
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    map = defaultdict(list)
    home = 'https://www.amazon.in'
    proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                    "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                    "134.213.29.202:4444"]
    proxies = {'https': random.choice(proxies_list)}
    source_code = requests.get(url_amzn, headers=headers)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for html in soup.find_all('div', {'class': 'sg-col-inner'}):
        title, link, price, image_url = None, None, None, None
        for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
            title = heading.text
        for p in html.find_all('span', {'class': 'a-price-whole'}):
            price = p.text
        for l in html.find_all('a', {
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
            link = home + l.get('href')
        for img in html.find_all('img', {'class': 's-image'}):
            image_url = img.get('src')
        if title and link:
            map[title] = [price, link, image_url]

    return map

def visit_site(url):
    webbrowser.open(url)

# Function to compare prices
def compare_prices(flip_price, amzn_price):
    try:
        flip_price = float(flip_price.replace(',', ''))
        amzn_price = float(amzn_price.replace(',', ''))
        if flip_price < amzn_price:
            return f"The price on Flipkart (Rs. {flip_price}) is lower than Amazon (Rs. {amzn_price})."
        elif amzn_price < flip_price:
            return f"The price on Amazon (Rs. {amzn_price}) is lower than Flipkart (Rs. {flip_price})."
        else:
            return "The prices on Flipkart and Amazon are the same."
    except (ValueError, TypeError):
        return "Unable to compare prices due to missing or invalid price information."

def compare_app_page():
    st.title("Comparo (Beta Test)")

    user_input = st.text_input("Enter the product :")
    st.write("Press 'Enter' to Continue!")
    if user_input:
        product_arr = user_input.split()
        key = "+".join(product_arr)

        # Fetch product details from Flipkart and Amazon
        flip_map = price_flipkart(key)
        amzn_map = price_amzn(key)

        # Store dropdown options in session state
        if 'flip_options' not in st.session_state:
            st.session_state.flip_options = list(flip_map.keys())
        if 'amzn_options' not in st.session_state:
            st.session_state.amzn_options = list(amzn_map.keys())

        # Create dropdowns with product titles
        flip_title = st.selectbox("Select Flipkart Product", st.session_state.flip_options, key="flip_dropdown")
        amzn_title = st.selectbox("Select Amazon Product", st.session_state.amzn_options, key="amzn_dropdown")

        # Add a search button
        if st.button("Search"):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Flipkart")
                st.write(f"**Title:** {flip_title}")
                flip_price, flip_link, flip_image_url = flip_map[flip_title]
                if flip_price:
                    st.write(f"**Price (Rs):** {flip_price}")
                else:
                    st.write("**Price:** The price is not available")
                if flip_image_url:
                    st.markdown(f"<img src='{flip_image_url}' style='width:200px;height:200px;border-radius:3%;margin-bottom:10px'>", unsafe_allow_html=True)
                st.button("Visit Site", on_click=visit_site, args=(flip_link,), key="flip_visit_site")

            with col2:
                st.subheader("Amazon")
                st.write(f"**Title:** {amzn_title}")
                amzn_price, amzn_link, amzn_image_url = amzn_map[amzn_title]
                if amzn_price:
                    st.write(f"**Price (Rs):** {amzn_price}")
                else:
                    st.write("**Price:** The price is not available")
                if amzn_image_url:
                    st.markdown(f"<img src='{amzn_image_url}' style='width:200px;height:200px;border-radius:3%;margin-bottom:10px'>", unsafe_allow_html=True)
                st.button("Visit Site", on_click=visit_site, args=(amzn_link,), key="amzn_visit_site")

            # Compare prices and display result
            price_comparison = compare_prices(flip_price, amzn_price)
            st.write(f"**Price Comparison:** {price_comparison}")
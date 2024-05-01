import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("GOOGLE_API_KEY")

def get_past_prices(product_description):
    llm = ChatGoogleGenerativeAI(model='gemini-pro')

    prompt_template = """
    Product Description: {product_description}

    Provide the past prices of this product in the following format:

    Date, Price (in INR)
    2023-04-01, 15000
    2023-03-01, 16000
    2023-02-01, 17000
    2023-01-01, 18000
    2022-12-01, 19000

    If you do not have past price information for this product, generate realistic augmented data with a similar price range.
    """

    prompt = PromptTemplate(input_variables=["product_description"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.run(product_description=product_description)

    prices = []
    for line in response.split('\n'):
        if ',' in line:
            date, price = line.split(',')
            prices.append([date.strip(), float(price.strip().replace('INR', '').replace(',', ''))])

    return prices

def plot_prices(prices, title):
    df = pd.DataFrame(prices, columns=['Date', 'Price'])
    df['Date'] = pd.to_datetime(df['Date'])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Date'], df['Price'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (INR)')
    ax.set_title(title)
    st.pyplot(fig)

def analytics_page():
    st.title("Product Analytics")

    user_input = st.text_input("Enter the product :")
    st.write("Press 'Enter' to Continue!")

    if user_input:
        product_arr = user_input.split()
        key = "+".join(product_arr)

        # Fetch product details from Flipkart and Amazon
        from compare_app import price_flipkart, price_amzn
        flip_map = price_flipkart(key)
        amzn_map = price_amzn(key)

        # Create dropdowns with product titles
        flip_options = list(flip_map.keys())
        amzn_options = list(amzn_map.keys())

        flip_title = st.selectbox("Select Flipkart Product", flip_options, key="flip_dropdown")
        amzn_title = st.selectbox("Select Amazon Product", amzn_options, key="amzn_dropdown")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Flipkart Analytics")
            if st.button("Show Analytics", key="flip_analytics"):
                flip_price, flip_link, flip_desc = flip_map[flip_title]
                flip_prices = get_past_prices(f"{flip_title} - {flip_desc}")
                plot_prices(flip_prices, f"Price History for {flip_title} (Flipkart)")

        with col2:
            st.subheader("Amazon Analytics")
            if st.button("Show Analytics", key="amzn_analytics"):
                amzn_price, amzn_link, amzn_desc = amzn_map[amzn_title]
                amzn_prices = get_past_prices(f"{amzn_title} - {amzn_desc}")
                plot_prices(amzn_prices, f"Price History for {amzn_title} (Amazon)")
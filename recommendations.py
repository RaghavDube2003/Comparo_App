import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("GOOGLE_API_KEY")


def price_flipkart(key):
    url_flip = f'https://www.flipkart.com/search?q={key}&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
    map = defaultdict(list)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    source_code = requests.get(url_flip, headers=headers)
    soup = BeautifulSoup(source_code.text, "html.parser")
    home = 'https://www.flipkart.com'
    for block in soup.find_all('div', {'class': 'tUxRFH'}):
        title, price, link, desc = None, 'Currently Unavailable', None, None
        for heading in block.find_all('div', {'class': 'KzDlHZ'}):
            title = heading.text
        for p in block.find_all('div', {'class': 'Nx9bqj _4b5DiR'}):
            price = p.text[1:]
        for l in block.find_all('a', {'class': 'CGtC98'}):
            link = home + l.get('href')
        for d in block.find_all('div', {'class': 'J+igdf'}):
            desc = d.text.strip()
        map[title] = [price, link, desc]
    return map


def recommendations_page():
    st.title("Recommendations")

    # Get user input for product search
    user_input = st.text_input("Enter a product name")

    if user_input:
        # Fetch product data based on user input
        products = price_flipkart(user_input)

        # Store product options in session state
        if 'product_options' not in st.session_state:
            st.session_state.product_options = [product for product in products]

        # Create a dropdown to select products
        selected_product_name = st.selectbox("Select a product", st.session_state.product_options, index=None,
                                             placeholder="Select a product...")

        # Store the selected product in session state
        st.session_state.selected_product = products.get(selected_product_name)

    # Check if a product has been selected
    if 'selected_product' in st.session_state:
        selected_product = st.session_state.selected_product

        # Get user question
        user_question = st.text_input("Ask a question about the product")
        st.write("Click 'Enter' to get Recommendations")
        # Load the language model
        llm = ChatGoogleGenerativeAI(model='gemini-pro')

        # Define the prompt template
        prompt_template = """
        Product Description: {product_description}

        User Question: {user_question}

        First Provide the name of the device and the price. 
        Provide a concise and informative response to the user's question about the product, highlighting relevant details from the product description. Present your response in bullet points. Provide additional recommendations outside the product description (If you are addiding other products, mention their price aswell).
        If newer versions of the product are available, please provide a technical comparison of the pros and cons between the newer and older versions.

        Notes: If the user inquires about something that is not included in the product description, respond using your own understanding.
        """

        # Create the prompt
        prompt = PromptTemplate(input_variables=["product_description", "user_question"], template=prompt_template)

        # Create the LLM chain
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        # Generate the response
        if user_question:
            response = llm_chain.run(product_description=selected_product[1], user_question=user_question)
            st.write(response)
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import InstructEmbeddings

from compare_app import price_flipkart, price_amzn

# Load the language model instance
llm = ChatGoogleGenerativeAI(model='gemini-pro')

# Create the embeddings instance
embeddings = InstructEmbeddings(llm)

def chatbot_page():
    st.title("Product Chatbot")

    # Get user input for product search
    user_input = st.text_input("Enter a product name")

    if user_input:
        # Fetch product data based on user input
        product_arr = user_input.split()
        key = "+".join(product_arr)
        flip_map = price_flipkart(key)
        amzn_map = price_amzn(key)

        # Combine product data from Flipkart and Amazon
        docs = []
        for title, [price, link, desc] in flip_map.items():
            docs.append(f"Title: {title}\nPrice: {price}\nLink: {link}\nDescription: {desc}")
        for title, [price, link, desc] in amzn_map.items():
            docs.append(f"Title: {title}\nPrice: {price}\nLink: {link}\nDescription: {desc}")

        # Create the conversational retrieval chain
        retriever = FAISS.from_texts(docs, embeddings)
        conversational_chain = ConversationalRetrievalChain.from_llm(llm, retriever)

        # Create a text input field for the user's query
        user_query = st.text_input("Ask me anything about the product:")

        # If the user enters a query, generate a response
        if user_query:
            response = conversational_chain.run(user_query)
            st.write(response)
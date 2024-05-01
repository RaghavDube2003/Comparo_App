import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("GOOGLE_API_KEY")

def get_past_prices(product_description, current_price):
    llm = ChatGoogleGenerativeAI(model='gemini-pro')

    prompt_template = """
    Product Description: {product_description}
    Current Price: {current_price}

    Provide the past prices of this product in the following format:

    Date, Price (in INR)
    2024-04-01, 15000
    2024-03-01, 16000
    2023-02-01, 17000
    2023-01-01, 18000
    2022-12-01, 19000

    This format is just for the reference.
    Use the current price information to generate realistic accurate augmented data with a similar price range for the past prices.
    Make sure the data displayed is accurate and the prices follow a logical trend.
    """

    prompt = PromptTemplate(input_variables=["product_description", "current_price"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.run(product_description=product_description, current_price=current_price)

    prices = []
    for line in response.split('\n'):
        line = line.strip()
        if ',' in line:
            parts = line.split(',', 1)  # Split on the first comma
            date = parts[0].strip()
            price_str = parts[1].strip().replace('INR', '').replace(',', '')
            try:
                price = float(price_str)
                prices.append([date, price])
            except ValueError:
                # Skip lines where the price is not a valid float
                continue

    return prices

def plot_prices(prices, title):
    df = pd.DataFrame(prices, columns=['Date', 'Price'])
    df['Date'] = pd.to_datetime(df['Date'])

    # Highlight significant price changes
    df['Price_Diff'] = df['Price'].diff()
    significant_changes = df[abs(df['Price_Diff']) > (df['Price'].mean() * 0.1)]

    # Create the plot
    trace = go.Scatter(
        x=df['Date'],
        y=df['Price'],
        mode='lines+markers',
        marker=dict(
            color=[
                'red' if any(df.loc[i, 'Date'] == significant_changes['Date']) else 'green'
                for i in range(len(df))
            ],
            size=10,
            line=dict(width=2, color='DarkSlateGrey')
        )
    )

    layout = go.Layout(
        title=title,
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price (INR)'),
        hovermode='closest'
    )

    fig = go.Figure(data=[trace], layout=layout)

    # Add annotations for significant price changes
    for index, row in significant_changes.iterrows():
        fig.add_annotation(
            x=row['Date'],
            y=row['Price'],
            text=f"Price Change: {row['Price_Diff']:.2f}",
            showarrow=True,
            arrowhead=1
        )

    # Add graph description
    if len(significant_changes) > 0:
        description = f"The graph shows significant price changes for the product {title.split(' - ')[0]}. " \
                      f"The prices have fluctuated with {len(significant_changes)} major changes."
    else:
        description = f"The graph shows a relatively stable price trend for the product {title.split(' - ')[0]}."

    st.markdown(f"**Description:** {description}")

    st.plotly_chart(fig)

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

        # Store dropdown options in session state
        if 'flip_options' not in st.session_state:
            st.session_state.flip_options = list(flip_map.keys())
        if 'amzn_options' not in st.session_state:
            st.session_state.amzn_options = list(amzn_map.keys())

        # Create dropdowns with product titles
        flip_title = st.selectbox("Select Flipkart Product", st.session_state.flip_options, key="flip_dropdown")
        amzn_title = st.selectbox("Select Amazon Product", st.session_state.amzn_options, key="amzn_dropdown")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Flipkart Analytics")
            if st.button("Show Analytics", key="flip_analytics"):
                flip_price, flip_link, flip_desc = flip_map[flip_title]
                flip_prices = get_past_prices(f"{flip_title} - {flip_desc}", flip_price)
                plot_prices(flip_prices, f"{flip_title} - {flip_desc}")

        with col2:
            st.subheader("Amazon Analytics")
            if st.button("Show Analytics", key="amzn_analytics"):
                amzn_price, amzn_link, amzn_desc = amzn_map[amzn_title]
                amzn_prices = get_past_prices(f"{amzn_title} - {amzn_desc}", amzn_price)
                plot_prices(amzn_prices, f"{amzn_title} - {amzn_desc}")
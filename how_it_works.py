import streamlit as st

def how_it_works_page():
    st.title("How it Works")

    # Container for text and image
    st.markdown("""
    <div style="display: flex; align-items: center;">
        <div style="flex: 7;">
            <p>Here's how the <i>'Compare APP'</i>  feature works:</p>
            <p class='bullet-point bold-red'>User Input: The user inputs the name of the product they want to compare prices for.</p>
            <p class='bullet-point bold-red'>Processing User Input: The user input is split into words and joined with a '+' character to create a search key that can be used in the URLs for both Flipkart and Amazon.</p>
            <p class='bullet-point bold-red'>Fetching Product Information: The code makes requests to the Flipkart and Amazon search URLs constructed using the search key. It scrapes the HTML content of the search results pages using BeautifulSoup to extract information such as product title, price, link, and image URL.</p>
            <p class='bullet-point bold-red'>Displaying Options: The scraped product information is stored in dictionaries where the product title serves as the key. Dropdown menus are created in the Streamlit interface, allowing the user to select a product from the options fetched from Flipkart and Amazon.</p>
            <p class='bullet-point bold-red'>User Selection: The user selects the desired products from the dropdown menus.</p>
            <p class='bullet-point bold-red'>Displaying Product Details: Upon selection, the code displays the details of the selected products, including the title, price, and image. Buttons are provided to allow the user to visit the product page on Flipkart or Amazon.</p>
            <p class='bullet-point bold-red'>Price Comparison: When the user clicks the 'Search' button, the code compares the prices of the selected products fetched from Flipkart and Amazon. The comparison result is displayed, indicating whether the price is lower on Flipkart, Amazon, or if they are the same.</p>
            <p class='bullet-point bold-red'>End of Process: The user can repeat the process by entering a new product name or exiting the application.</p>
        </div>
        <div style="flex: 1;">
            <img src="https://i.ibb.co/XsLQgQ6/Architecture.png" width="200" height="400">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Custom bullet points style with larger font size
    st.markdown("""
    <style>
        .bullet-point::before {
            content: "🔹";
            color: green;
            font-size: 1.5rem; /* Adjust the font size as needed */
            font-weight: bold;
            display: inline-block;
            width: 1.5em;
            margin-left: -1.5em;
        }
    </style>
    """, unsafe_allow_html=True)


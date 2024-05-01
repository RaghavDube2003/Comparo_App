import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

# Loading Image using PIL
im = Image.open('https://i.ibb.co/4Z90YHc/comparo.jpg')

# Set page configuration
st.set_page_config(
    page_title="Comparo",
    page_icon=im,
    layout="wide"
)

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

def main():

    selected = option_menu(
        menu_title=None,
        options=["Compare APP", "Recommendations", "About", "How it works", "Analytics"],
        icons=["house", "list-task", "gear", "cloud-upload", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Compare APP":
        from compare_app import compare_app_page
        compare_app_page()
    elif selected == "Recommendations":
        from recommendations import recommendations_page
        recommendations_page()
    elif selected == "About":
        from about import about_page
        about_page()
    elif selected == "How it works":
        from how_it_works import how_it_works_page
        how_it_works_page()
    elif selected == "Analytics":
        from analytics import analytics_page
        analytics_page()

if __name__ == "__main__":
    main()
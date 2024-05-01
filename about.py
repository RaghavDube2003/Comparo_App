import streamlit as st

def about_page():

    st.title("About")
    st.write(
        "😊 Comparo is a third-year college project developed at Vishwakarma Institute of Information Technology (VIIT) in Pune.")
    st.write(
        "😃 The project was created by a team of third-year students: Raghav, Pratik, Amogh, and Zinee. It is entirely built using Streamlit and CustomTkinter in Python.")
    st.write(
        "😌 Recently, the user interface has been enhanced to include images of the products, providing users with a more visually engaging experience.")

    st.image("Assets/Website/Web1.png", caption="Comparo Home Page")
    st.image("Assets/Website/Web2.png", caption="About Comparo")
    st.image("Assets/Website/Web3.png", caption="Comparo Examples")

    st.write("Visit the website: [comparo.pages.dev](https://comparo.pages.dev/)")
    st.write("Made with ♥ by [Raghav Dube](https://github.com/RaghavDube18)")
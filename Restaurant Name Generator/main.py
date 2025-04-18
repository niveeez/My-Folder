import streamlit as st
import langchain_helper

st.title("Restaurant name generator")
cuisine = st.sidebar.selectbox("Pick a cuisine", ("Indian", "American", "Mexican", "Italian") )




if cuisine:
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)

    st.header(response['restaurant_name'].strip())
    st.write("**Menu Items**")
    menu_items = response['menu_items'].strip().split(",")
    for items in menu_items:
        st.write("-",items)





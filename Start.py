
# External imports
import streamlit as st

# Python imports
import hmac
import os

# Local imports
import config as c
from functions.styling import page_config, styling
from functions.menu import menu


### CSS AND STYLING

st.logo("images/logo_main.png", icon_image = "images/logo_small.png")

page_config()
styling()


### PASSWORD 
### ### ###

st.session_state["app_version"] = c.app_version
st.session_state["update_date"] = c.update_date

### SIDEBAR

menu()

### MAIN PAGE

st.image("images/logo_main.png")
st.markdown("###### ")

st.image("images/header.jpg")
st.markdown("###### ")

st.markdown("""
            __Välkommen till vår labbyta för generativ AI__"""
)
st.markdown("""
            Här i verktygslådan hittar du verktyg för att labba med generativ AI.
            """)
    
st.markdown("# ")
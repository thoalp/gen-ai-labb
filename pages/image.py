
# External imports
import streamlit as st
from openai import OpenAI

# Python imports
import hmac
from PIL import Image
import os
from os import environ

# Local imports
from functions.styling import page_config, styling
import config as c
from functions.menu import menu


### CSS AND STYLING

st.logo("images/logo_main.png", icon_image = "images/logo_small.png")

page_config()
styling()


### PASSWORD 
### ### ### ###

# Translation

if st.session_state['language'] == "Svenska":
    image_describe = "Beskriv din bild..."
    image_clear_chat = "Rensa chat"
    image_hello = "Hej! Hur kan jag hjälpa dig?"
    image_settings = "Inställningar"
    image_choose_model = "Välj modell"
    image_choose_size = "Välj bildstorlek"
    image_wait = "Ett ögonblick... Ritar och färglägger din bild..."
    image_sidebar = "Det finns inget minne i chatten, utan du måste beskriva din bild varje gång."

elif st.session_state['language'] == "English":
    image_describe = "Describe your image..."
    image_clear_chat = "Clear chat"
    image_hello = "Hi! How can I help you?"
    image_settings = "Settings"
    image_choose_model = "Choose model"
    image_choose_size = "Choose image size"
    image_wait = "One moment… Drawing and coloring your image…"
    image_sidebar = "Det finns inget minne i chatten, utan du måste beskriva din bild varje gång."


if c.deployment == "streamlit":
    client = OpenAI(api_key = st.secrets.openai_key)
else:
    client = OpenAI(api_key = environ.get("openai_key"))


### SIDEBAR

menu()

st.sidebar.success(f"{image_sidebar}")


col1, col2 = st.columns(2)

with col1:
    if st.button(f"{image_clear_chat}", type="secondary"):
        if "messages" in st.session_state.keys(): # Initialize the chat message history
            st.session_state.messages = [
                {"role": "assistant", "content": f"""
                    {image_hello}"""}
        ]

with col2:
    with st.expander(f"{image_settings}"):

        image_model = st.selectbox(f"{image_choose_model}", ["Dall-E 3"])
        image_size = st.selectbox(f"{image_choose_size}", ["1792x1024", "1024x1024"])

        if image_model == "Dall-E 3":
            st.session_state["image_model"] = "dall-e-3"
        if image_size == "1792x1024":
            st.session_state["image_size"] = "1792x1024"
        elif image_size == "1024x1024":
            st.session_state["image_size"] = "1024x1024"


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": f"{image_hello}"}]

for message in st.session_state.messages:
     with st.chat_message(message["role"]):
        # Check if the content is an image URL
        if message["content"].startswith("http"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if prompt := st.chat_input(f"{image_describe}"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"{image_wait}"):
            response = client.images.generate(
                  model = st.session_state["image_model"],
                  prompt = prompt,
                  size = st.session_state["image_size"],
                  #quality = "hd",
                  style = "vivid",
                  n=1,
                )

            # Store the image URL
            image_url = response.data[0].url

            # Display the image immediately
            st.image(image_url, caption=prompt)

        # Append the image URL to the messages
        st.session_state.messages.append({"role": "assistant", "content": image_url})


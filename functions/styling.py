
import streamlit as st
import config as c


def page_config():
    
    st.set_page_config(
        page_title = c.page_title,
        layout="centered",
        page_icon=":material/smart_toy:",
        initial_sidebar_state="expanded")


# CSS styling

def styling():

    st.markdown("""
    <style>
                
    [data-testid="stChatMessageAvatarUser"], [alt="user avatar"] {
        height: 2.8rem;
        width: 2.8rem;
        border-radius: 8px;    
    }
                
    [data-testid="stChatMessageAvatarAssistant"], [alt="assistant avatar"] {
        height: 2.8rem;
        width: 2.8rem;
        border-radius: 8px;
    }
                
    [aria-label="Chat message from user"] {
        padding: 10px;
        border-radius: 0.5rem;
    }
                
    [aria-label="Chat message from assistant"] {
        padding: 10px;
    }
                
    .block-container {
        padding-top: 3rem;
        padding-bottom: 0rem;
    }
                
    .stPageLink {
    margin-bottom: -12px;
    }
                
    [data-testid="stPageLink-NavLink"] p {
    font-size: 1rem !important;
    }
                
    h6 {
    padding-bottom: 0rem;
    }
                
    p {
    font-size: 1.1rem;
    }

    </style>
    """, unsafe_allow_html=True)


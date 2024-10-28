import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.core.llms import ChatMessage
from llama_index.core import Settings
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from PIL import Image
from uuid import uuid4

import os
from os import environ
import hmac
from functions.styling import page_config, styling
import config as c
from functions.menu import menu

### CSS AND STYLING

st.logo("images/logo_main.png", icon_image = "images/logo_small.png")

page_config()
styling()

# Check if language is already in session_state, else initialize it with a default value
if 'language' not in st.session_state:
    st.session_state['language'] = "Svenska"  # Default language

st.session_state["pwd_on"] = st.secrets.pwd_on

### PASSWORD

if st.session_state["pwd_on"] == "true":

    def check_password():

        if c.deployment == "streamlit":
            passwd = st.secrets["password"]
        else:
            passwd = environ.get("password")

        def password_entered():

            if hmac.compare_digest(st.session_state["password"], passwd):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
            else:
                st.session_state["password_correct"] = False

        if st.session_state.get("password_correct", False):
            return True

        st.text_input("Lösenord", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state:
            st.error("😕 Ooops. Fel lösenord.")
        return False


    if not check_password():
        st.stop()
    
############

os.makedirs("data", exist_ok=True) # Where data such as documents are beeing stored


if c.deployment == "streamlit":
    llm = OpenAI(api_key = st.secrets.openai_key)
    os.environ["OPENAI_API_KEY"] = st.secrets.openai_key
else:
    llm = OpenAI(api_key = environ.get("openai_key"))
    os.environ["OPENAI_API_KEY"] = environ.get("openai_key")


# Translation
if st.session_state['language'] == "Svenska":
    prompt = """Du är en hjälpsam AI-assistent som hjälper användaren med sina frågor gällande den kontext du fått. Kontexten är ett eller flera dokument. 
Basera alla dina svar på kontexten och hitta inte på något. Hjälp användaren svara på frågor, summera och annat. 
Om du inte vet svaret, svarar du att du inte vet svaret.
"""
    clear_memory = "Rensa minnet"
    cache_cleared = "Cachen och dina filer har rensats."
    settings_text = "Inställningar"
    temperature_text = "Temperatur"
    system_prompt_text = "Systemprompt"
    save_text = "Spara"
    page_name = "Chatta med dina dokument"
    loading_doc_text = "Laddar ditt dokument... Det här kan ta ett litet tag."
    upload_file_text = "Ladda upp ett dokument för att starta chatten"
    assistant_hello = "Hej! Hur kan jag hjälpa dig?"
    chat_input_text = "Din fråga?"
    thinking_text = "Jag tänker... Ett ögonblick..."

elif st.session_state['language'] == "English":
    prompt = """You are a helpful AI assistant that helps the user with their questions regarding the context you have received. The context is one or more documents.  
Base all your answers on the context and do not make anything up. Help the user answer questions, summarize, and other tasks. 
If you don't know the answer, respond that you don't know the answer.
"""
    clear_memory = "Clear memory"
    cache_cleared = "The cache and your files have been cleared."
    settings_text = "Settings"
    temperature_text = "Temperature"
    system_prompt_text = "System prompt"
    save_text = "Save"
    page_name = "Chat with your documents"
    loading_doc_text = "Loading your document... This may take a little while."
    upload_file_text = "Upload a document to start the chat"
    assistant_hello = "Hi! How can I help you?"
    chat_input_text = "Your question?"
    thinking_text = "I'm thinking... One moment..."


if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = prompt

if "llm_temperature" not in st.session_state:
    st.session_state.llm_temperature = 0.2


# Ensure each user has a unique directory
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid4())  # Generate a unique ID for each session

# Create a user-specific data folder
user_data_folder = f'./data/{st.session_state["session_id"]}'
os.makedirs(user_data_folder, exist_ok=True)


Settings.llm = OpenAI(
    model="gpt-4o", 
    temperature = st.session_state.llm_temperature,
    system_prompt = st.session_state.system_prompt
    )

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
embed_model = Settings.embed_model
Settings.node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)


### SIDEBAR

menu()


### MAIN PAGE

col1, col2 = st.columns(2)

with col1:
        
    if st.button(f"{clear_memory}"):
        
        # Delete all files in the 'data' folder
        folder_path = user_data_folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)  # Remove the folder if necessary
            except Exception as e:
                st.error(f"Fel när filen {file_path} skulle tas bort: {e}")

        # Clears all st.cache_resource caches:
        st.cache_resource.clear()
        st.success(f"{cache_cleared}")

            
with col2:
    with st.expander(f"{settings_text}"):

        llm_temp = st.slider(
            f'{temperature_text}',
            min_value = 0.0,
            max_value = 1.0,
            step = 0.1,
            value = 0.1,
        )

        st.markdown("###### ")

        with st.form("my_form"):
            prompt_input = st.text_area(f"{system_prompt_text}", prompt, height=300)
            st.session_state.system_prompt = prompt_input   
            st.form_submit_button(f'{save_text}') 


st.markdown(f"#### :material/description: {page_name}")

@st.cache_resource(show_spinner=False)
def load_data(user_data_folder):

    with st.spinner(text=f"{loading_doc_text}"):

        data = SimpleDirectoryReader(input_dir=user_data_folder, recursive=True).load_data()
                
        index = VectorStoreIndex.from_documents(
            data, 
            llm=llm,
            embed_model=embed_model,
            show_progress=True)
        
        return index    


uploaded_files = st.file_uploader(
    f"{upload_file_text}", 
    type=("pdf", "docx", "doc", "xls", "xlsx", "csv"), 
    accept_multiple_files=True)

if uploaded_files:  # If files were uploaded

    # Iterate through each uploaded file
    for uploaded_file in uploaded_files:

        file_path = f"{user_data_folder}/{uploaded_file.name}"

        # Check if the new file is different from the already indexed files
        if 'indexed_file_paths' not in st.session_state:
            st.session_state.indexed_file_paths = []

        if file_path not in st.session_state.indexed_file_paths:
            st.session_state.indexed_file_paths.append(file_path)

        # Save the file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())


elif 'indexed_file_paths' in st.session_state:
    # Reload existing files from the session state
    #index = load_data()
    pass


if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": f'''
            {assistant_hello}
        '''}
    ]
    st.session_state["messages"] = [{"role": "assistant", "content": f"{assistant_hello}"}]


if uploaded_files:
    index = load_data(user_data_folder)


    query_engine = index.as_query_engine(
        chat_mode = "openai", # openai context react
        streaming = True,
        similarity_top_k = 20,
        verbose = True)


    if prompt := st.chat_input(f"{chat_input_text}"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Check if the content is an image URL
            if message["content"].startswith("http"):
                st.image(message["content"])
            else:
                st.markdown(message["content"])


    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            
            full_response = ""
            message_placeholder = st.empty()

            with st.spinner(f"{thinking_text}"):
                streaming_response = query_engine.query(prompt)
                
                for response in streaming_response.response_gen:
                    full_response += response
                    message_placeholder.markdown(full_response + "▌")
                
                message = {"role": "assistant", "content": full_response}
        
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append(message) # Add response to message history

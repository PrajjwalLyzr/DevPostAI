import os
import streamlit as st
import shutil
import base64
from openai import OpenAI
from st_social_media_links import SocialMediaIcons 



def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")



def get_scripts_data(scripts_dir):
    all_scripts_content = ""  # Initialize the variable to store script content
    for filename in os.listdir(scripts_dir):
        if filename.endswith(".py"):
            file_path = os.path.join(scripts_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
                    # Read each file and append its content to the variable
                    all_scripts_content += file.read() + "\n\n"  # Adding line breaks between scripts
            except Exception as e:
                print(f"Error reading {file_path}: {e}")  # Print error message if any
    return all_scripts_content  # Return the accumulated scripts content


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  

def gpt_vision_call(openai_api_key, base64_image):
    openai_client = OpenAI(api_key=openai_api_key)
    prompt = "Analyze the following image and extract relevant information to create a structured description. Convert visual elements into written form."

    messages = [
                {"role": "user", "content": [
                    {"type": "text",
                     "text": prompt
                     },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                      },
                    },
                    ]
                 },
            ]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    description = response.choices[0].message.content

    return description


def get_files_in_directory(directory):
    # This function help us to get the file path along with filename.
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list


def save_uploaded_file(directory, uploaded_file):
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.read())


def get_file_name(directory):
    try:
        files = os.listdir(directory)
        file_names = [file for file in files if os.path.isfile(os.path.join(directory, file))]
        
        return file_names[0]
    
    except FileNotFoundError:
        return f"The directory '{directory}' does not exist."
    
    except Exception as e:
        return f"An error occurred: {e}"


def file_checker(directoryName):
    file = []
    for filename in os.listdir(directoryName):
        file_path = os.path.join(directoryName, filename)
        file.append(file_path)

    return file



def social_media(justify=None):
    # This function will help you to render socila media icons with link on the app
    social_media_links = [
    "https://github.com/LyzrCore/lyzr",
    "https://www.youtube.com/@LyzrAI",
    "https://www.instagram.com/lyzr.ai/",
    "https://www.linkedin.com/company/lyzr-platform/posts/?feedView=all"
                        ]   

    social_media_icons = SocialMediaIcons(social_media_links)
    social_media_icons.render(sidebar=True, justify_content=justify) # will render in the sidebar



def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 450px;
           max-width: 450px;
           background-color: #6482AD;
       }
    </style>
    """, unsafe_allow_html=True)

def select_box_css():
    st.markdown(
    """
    <style>
    /* Change background and text color of the selectbox */
    div[data-baseweb="select"] > div {
        background-color: #697565; /* Change this to your desired background color */
        color: #000000; /* Change this to your desired text color */
        font-weight: bold;
    }
    /* Optional: Change the dropdown options' text color */
    div[data-baseweb="select"] > div > div > div {
        color: #FFFFFF; /* Change this to your desired text color */
    }
    </style>
    """,
    unsafe_allow_html=True
    )


def page_config(layout = "centered"):
    st.set_page_config(
        page_title="DevPostAI",
        layout=layout,  # or "wide" 
        initial_sidebar_state="auto",
        page_icon="./logo/lyzr-logo-cut.png"
    )

def about_app():
    with st.sidebar.expander("ℹ️ - Why this DevPostAI"):
        st.sidebar.caption("""DevPostAI leverages Lyzr's Agent API to help developers turn their project descriptions and scripts into compelling LinkedIn posts, YouTube scripts, or detailed articles. The app provides a seamless way to generate content, with an option to include target keywords for SEO optimization when writing articles.

        """)



def template_end():
    st.sidebar.markdown("### This app is build by using Lyzr's Agent API ")

    st.sidebar.markdown(
        """
        <style>
        .button-container {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
        }
        .button-column {
            flex: 1;
            margin-right: 5px;
        }
        .button-column:last-child {
            margin-right: 0;
        }
        .sidebar-button {
            display: block;
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            text-align: center;
            color: white;
            background-color: #ffffff;
            border: none;
            border-radius: 5px;
            text-decoration: none;
        }
        .sidebar-button:hover {
            background-color: #7458E8;
        }
        </style>

        <div class="button-container">
            <div class="button-column">
                <a class="sidebar-button" href="https://www.lyzr.ai/" target="_blank">Lyzr</a>
                <a class="sidebar-button" href="https://www.lyzr.ai/book-demo/" target="_blank">Book a Demo</a>
                <a class="sidebar-button" href="https://agent.api.lyzr.app/docs#overview" target="_blank">Lyzr Agent API</a>
                <a class="sidebar-button" href="https://discord.gg/nm7zSyEFA2" target="_blank">Discord</a>
                <a class="sidebar-button" href="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw" target="_blank">Slack</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )




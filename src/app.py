import streamlit as st
import os
from lyzr_agent_api import AgentAPI, ChatRequest
from utils import page_config, style_app, template_end, about_app, social_media
from utils import save_uploaded_file, get_scripts_data, encode_image, gpt_vision_call
from utils import get_file_name, remove_existing_files

from dotenv import load_dotenv

load_dotenv()

LYZR_API_KEY = os.getenv('X_API_Key')
LinkedIn_AGENT_ID = os.getenv('LinkedIn_AGENT_ID')
YouTube_AGENT_ID = os.getenv("YouTube_AGENT_ID")
Article_AGENT_ID = os.getenv("Article_AGENT_ID")
User_ID = os.getenv('USER_ID')
Session_ID = os.getenv('SESSION_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

Scripts = "Scripts"
Images = "Images"
os.makedirs(name=Scripts, exist_ok=True)
os.makedirs(name=Images, exist_ok=True)


page_config()
style_app()


image = "src/logo/lyzr-logo.png"
st.image(image=image, width=200)

st.header("DevPostAI")
st.markdown("##### Powered by [Lyzr Agent API](https://agent.api.lyzr.app/docs#overview)")
st.markdown('---')


project_scripts = st.file_uploader("Upload Python files", type="py", accept_multiple_files=True)
project_description = st.text_area("Provide your project description", height=200)

if (project_scripts and project_description):
    for uploaded_file in project_scripts:
        save_uploaded_file(directory=Scripts, uploaded_file=uploaded_file)

    project_scripts_data = get_scripts_data(scripts_dir=Scripts)

    api_client = AgentAPI(x_api_key=LYZR_API_KEY) #Initialize api client

    if 'active_tool' not in st.session_state:
        st.session_state.active_tool = None

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('LinkedIn Post'):
            st.session_state.active_tool = "LinkedIn Post"
    with col2:
        if st.button('YouTube Script'):
            st.session_state.active_tool = "YouTube Script"
    with col3:
        if st.button('Article'):
            st.session_state.active_tool = "Article"

    
    if st.session_state.active_tool == "LinkedIn Post":
        st.subheader('Create LinkedIn Post')
        with st.spinner("🤖 Generating LinkedIn Post"):
            linkedin_payload = ChatRequest(
                user_id=User_ID,
                agent_id=LinkedIn_AGENT_ID,
                message=f"Use this project description:{project_description} and the project script data:{project_scripts_data}. [!Important] make sure linkedIn post should be creative and engaging have some hooks as well, and not a longer post",
                session_id=Session_ID
            )

            linkedIn_post_response = api_client.chat_with_agent(
                json_body=linkedin_payload
            )

            if linkedIn_post_response:
                st.markdown("Generated LinkedIn Post")
                st.markdown('---')
                st.write(linkedIn_post_response['response'])


    elif st.session_state.active_tool == "YouTube Script":
        st.subheader('Create YouTube Script')
        with st.spinner("🤖 Generating YouTube Script"):
            youtube_payload = ChatRequest(
                user_id=User_ID,
                agent_id=YouTube_AGENT_ID,
                message=f"Use this project description:{project_description} and the project script data:{project_scripts_data}. [!Important] make sure you have added some hooks in the script, divide scripts into several scenes as well provide the visuals for each scene and also provide the SEO Title and description for the video.",
                session_id=Session_ID
            )

            youtube_script_response = api_client.chat_with_agent(
                json_body=youtube_payload
            )

            if youtube_script_response:
                st.markdown("Generated YouTube Script")
                st.markdown('---')
                st.write(youtube_script_response['response'])


    elif st.session_state.active_tool == "Article":
        st.subheader('Create Article')
        keywords = st.text_input(label="Give targeted keywords")
        project_structure = st.file_uploader("Upload a project structure image", type=["jpg", "jpeg", "png"])  

        if project_structure:
            save_uploaded_file(directory=Images, uploaded_file=project_structure)
            with st.spinner("🤖 Generating Article"):
                file_name = get_file_name(directory=Images)
                image_file_path = os.path.join(Images, file_name)

                base64_image = encode_image(image_file_path)
                written_project_structure = gpt_vision_call(openai_api_key=OPENAI_API_KEY,
                                            base64_image=base64_image)
                

                article_payload = ChatRequest(
                    user_id=User_ID,
                    agent_id=Article_AGENT_ID,
                    message=f"Use this project decription:{project_description},  this is project scripts data:{project_scripts_data} and project structure:{written_project_structure}. [!Important] make sure article should be engaging and easy to understant, use the sript whenever its need also explain it, divide article into different-different sections, and it should use all this targeted keywords:{keywords} in it. Provide SEO optimized Title as well.",
                    session_id=Session_ID
                )


                article_reponse = api_client.chat_with_agent(
                    json_body=article_payload
                )

                if article_reponse:
                    st.markdown("Generated Article")
                    st.markdown('---')
                    st.write(article_reponse['response'])

        else:
            remove_existing_files(directory=Images)
    
else:
    st.warning('Please upload your project scripts or provide project description')
    remove_existing_files(directory=Scripts)

    


template_end()
st.sidebar.markdown('---')
about_app()
st.sidebar.markdown('---')
social_media(justify="space-evenly")
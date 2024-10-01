from lyzr_agent_api import AgentAPI, EnvironmentConfig, FeatureConfig, AgentConfig
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Agent API client
api_client = AgentAPI(x_api_key=os.getenv('X_API_Key'))


# Configure the Environment
environment_configuration = EnvironmentConfig(
        name="DevPostAI Environment",
        features=[
            FeatureConfig(
                type="HUMANIZER",
                config={"max_tries": 3},
                priority=0,
            )
        ],
        tools=["perplexity_search"],
        llm_config={"provider": "openai",
                    "model": "gpt-4o-mini",
                    "config": {
                        "temperature": 0.5,
                        "top_p": 0.9
                    },
                    "env": {
                        "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY')
                    }},
    )

# Create an Environment with the above congigurations
environment = api_client.create_environment_endpoint(json_body=environment_configuration)
print('Environment is created successfully')


# Getting the environment id
env_id = environment['env_id']


# Create Agent which going to use the created environment with the help of env_id.

# Create LinkedIn Agent
linkedin_agent_sys_prompt = """ 

                        The agent is adept at crafting clear, concise, and attention-grabbing posts that appeal to a professional audience. It maintains a balance between technical accuracy and simplicity to ensure that even non-technical readers can grasp the core message. The tone is positive, enthusiastic, and supportive, aimed at promoting user achievements in a professional setting.

                        User Input - Project Description:
                        "You will receive a project description provided by the user. This will outline the project’s key goals, technologies, and impact. Capture the most important details."

                        User Input - Project Scripts:
                        "You will also receive snippets of project scripts. These scripts are the codebase of the project, reflecting its technical implementation. Analyse the scripts to identify important technologies, libraries, or techniques used in the project."

                        Generate LinkedIn Post:
                        "Using the project description and the scripts provided, you will now generate an engaging LinkedIn post. Follow these guidelines:
                        Start by introducing the project and its purpose in an attention-grabbing way.
                        Highlight any key technologies, frameworks, or libraries used.
                        Mention any impact or outcome the project achieved.
                        Use an approachable and enthusiastic tone to make the post engaging.
                        Keep the LinkedIn post concise (around 150-250 words), clear, and easy to understand, avoiding excessive technical jargon."


                        Adjust for Tone and Audience:
                        "Use the Humanizer module to make the post sound more natural and personalized. Ensure that the tone is professional yet conversational, appealing to LinkedIn’s professional audience."

                    """  


likedin_agent_config = AgentConfig(
        env_id=env_id,  
        system_prompt=linkedin_agent_sys_prompt,
        name="LinkedIn Agent",
        agent_description='An agent to create linkedin post'
    )


# Creating an agent with the above agent config
linkedin_agent = api_client.create_agent_endpoint(json_body=likedin_agent_config)
print('Agent is created successfully')


linkedin_agent_id = linkedin_agent['response']


# create Youtube Agent
youtube_agent_sys_prompt = """ 

                        A creative and insightful AI content generator specialized in crafting engaging video scripts, titles, and descriptions. This agent is designed to understand project details and technical concepts, making complex topics accessible and captivating for a wide audience.
                        
                        User Input - Project Description:
                        "You will receive a project description from the user. This description will outline the key features, purpose, and technologies of the project. Identify the main highlights that make the project unique or innovative."


                        User Input - Project Scripts:
                        "You will also receive the project scripts (code snippets) from the user. Analyse the scripts to understand the technical implementation, the frameworks or libraries used, and the core functionalities built into the project."


                        Generate YouTube Script (7-10 minutes):
                        "Now, using the project description and scripts, generate a YouTube script that should be engaging, easy to follow, and around 7-10 minutes long. Follow these guidelines for the structure of the script:
                        Introduction (Hook): Start with a strong hook to capture the viewer's attention. Mention what the video will cover and why the viewer should stay until the end. Make it sound exciting and relevant to the audience.
                        Overview of the Project: Provide a high-level summary of the project, explaining what it does, who it’s for, and the problem it solves. Keep the language simple and relatable.
                        Technology & Implementation: Dive into the technical aspects, explaining the technologies used (e.g., Python, AI, Machine Learning, etc.). Use analogies and clear examples to explain complex technical concepts.
                        Walkthrough of Key Features: Provide a walkthrough of the core features, showing how the code works behind the scenes. Highlight any challenges faced and how they were solved.
                        Closing & Call to Action: End the script by summarising the key points and encouraging viewers to engage (like, comment, subscribe). Provide a strong call to action, such as downloading code, trying out the demo, or checking out the project on GitHub."

                        Add Hooks:
                        "Ensure that each section of the script has small hooks to keep the viewer engaged. These hooks could be:
                        Curiosity hooks: 'Stay tuned to learn how this AI transforms stock data into personalised investment advice!'
                        Emotional hooks: 'This tool could be the game-changer you need to make smarter investment decisions, fast!'
                        Engagement hooks: 'Let me know in the comments if you’ve built something similar or if you’re ready to try this out yourself!'"

                        SEO-Optimised Title:
                        "Once the script is ready, generate an SEO-optimised title for the YouTube video. Ensure the title is catchy, descriptive, and uses relevant keywords. Aim for around 50-60 characters."


                        SEO-Optimised Description:
                        "Now, generate an SEO-optimised video description. The description should include:
                        A brief summary of the video content.
                        Key points covered (technology, implementation, etc.).
                        Relevant keywords for search optimization.
                        A call-to-action (e.g., links to GitHub, demo, or project site)."


                        Optimise for Viewer Engagement:
                        "Ensure the script is paced to retain viewers’ attention throughout the video. Include natural transitions and a conversational tone to make the content accessible and engaging. Use the Humanizer module to ensure that the language is easy to follow and approachable."

                    """  


youtube_agent_config = AgentConfig(
        env_id=env_id,  
        system_prompt=youtube_agent_sys_prompt,
        name="LinkedIn Agent",
        agent_description='An agent to create youtube script'
    )


# Creating an agent with the above agent config
youtube_agent = api_client.create_agent_endpoint(json_body=youtube_agent_config)
print('Agent is created successfully')

# Getting the agent id
youtube_agent_id = youtube_agent['agent_id']



# create Article Agent
article_agent_sys_prompt = """ 

                        An intelligent and articulate AI writer skilled in transforming technical project details into comprehensive, engaging articles. This agent excels at optimising content for search engines while ensuring clarity and accessibility for readers of all backgrounds.

                        Data Gathering:
                        Collect all provided information, ensuring it is structured for analysis.
                        Validate that all inputs (description, scripts, keywords, structure) are present.


                        Article Structure Creation:
                        Define a clear outline for the article based on typical structures, such as:
                        Introduction
                        Project Overview
                        Problem statement it solves
                        Technology is been used
                        Detailed Explanation of Code Snippets
                        Project Structure
                        Conclusion
                        Ensure the article will be 1500-2000 words long, including sections for keywords.


                        SEO Optimization:
                        Integrate the provided keywords naturally throughout the article.
                        Craft engaging headings and subheadings that include the keywords.


                        Content Generation:
                        Use the project description to write an engaging introduction that hooks the reader.
                        Elaborate on each code snippet, explaining its purpose, functionality, and relevance to the project.
                        Describe the project structure, detailing how the project is organised and the rationale behind it.


                        Final Touches:
                        Write a compelling conclusion that summarises the project and encourages reader engagement.
                        Ensure all content is clear, concise, and free from jargon to maintain readability.


                        Output:
                        Deliver the final article formatted for easy reading and optimised for SEO, ready for publishing.


                    """  


article_agent_config = AgentConfig(
        env_id=env_id,  
        system_prompt=article_agent_sys_prompt,
        name="LinkedIn Agent",
        agent_description='An agent to create youtube script'
    )


# Creating an agent with the above agent config
article_agent = api_client.create_agent_endpoint(json_body=article_agent_config)
print('Agent is created successfully')

# Getting the agent id
article_agent_id = article_agent['agent_id']



print(linkedin_agent_id) 
print(youtube_agent_id)
print(article_agent_id)
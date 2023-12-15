import streamlit as st
import openai
import os
from tqdm import tqdm

# TODO: take this prompt and add it to the chain. It should be the result from this final prompt that is displayed in the text box "take the following article {final_result} and expand upon some of the main and more interesting points. give some deep detail so the reader really gets a meaningful insight into the topics and not just a high level glance. The reader should be able to walk away with actionable knowledge."
# TODO: add user auth and when user is logged in it adds a button at the bottom that links to the user's Medium account and allows them to post the tweet.
# TODO: move twitter and linkedin to homepage so don't have to go back and forth
# TODO: find a way to keep the output generated so it does not have to regenerate every time you go back to the homepage - complete
# TODO: A+ find a way to allow for the cache to be refreshed when the user changes the input  
# TODO: maybe make it so user must enter their own api key
# TODO: B make it so you can save your stories to a database and then you can go back and edit them and also save the prompts to a drop down
# TODO: A+ add meeting minutes page
# TODO: add a page that is titled "Need inspiration?" you enter a topic and it gives you a list of blog post titles that you can click on and it will take you to the blog post and then you can copy and paste the title and then you can use that as the title for your blog post

# Hide Streamlit Menu and Footer
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Prompt #1  
base_prompt_prefix = """
Write me a detailed table of contents for a blog post with the title below.

Title:  
"""

# Prompt #3
third_prompt_prefix = """  
Please use markdown to format the output from Prompt #2 with a title, headers, and bullet points where necessary. Add citations to support your points.
"""

@st.cache_data(show_spinner=False)
def generate_action(user_input):
    with st.spinner("Generating response..."):
        st.text("") 

        base_completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant asked to write a blog post"},
                {"role": "user", "content": f"{base_prompt_prefix}{user_input}"}
            ]
        )

        base_prompt_output = base_completion.choices[0].message.content.strip()

        # Build Prompt #2 using GPT-4
        second_prompt = f"""
        Take the table of contents and title of the blog post below and generate a blog post written in the style of Paul Graham. Make it feel like a story. Don't just list the points. Go deep into each one. Explain why. Use markdown formatting. You must add citations to support your points.

        Title: {user_input}

        Table of Contents: {base_prompt_output}

        Blog Post:

        References:
        """

        with tqdm(total=100, desc="Generating response", bar_format="{l_bar}{bar} [time left: {remaining}]", colour='green') as pbar:
            second_prompt_completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant asked to write a blog post"},  
                    {"role": "user", "content": second_prompt}
                ]
            )

            second_prompt_output = second_prompt_completion.choices[0].message.content.strip()

            output_parts = second_prompt_output.split("References:")

            citation_prompt = f"""
            Generate a list of citations for the blog post below: 

            {output_parts[0]}

            Citations:
            """
            citation_completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant asked to generate citations for a blog post"},
                    {"role": "user", "content": citation_prompt} 
                ]
            )

            citation_output = citation_completion.choices[0].message.content.strip()

            final_output = f"{output_parts[0]}\n\nReferences:\n{citation_output}"

            return {"output": final_output}

st.title("OpenAI Prompt Chaining: Blog Post Generator")
st.write("Examples: ")
st.code('Who invented the internet? ')  
st.code('What is the best way to learn Python? ')
st.code('The Science of Sleep: How Our Dreams Shape Our Lives')

user_input = st.text_input("Enter the title of your blog post:") 

# save user input to session state so we can use it in next page
st.session_state.user_input = user_input   

result = generate_action(user_input)
output_textbox = st.text_area("Output", value=result["output"], height=1000)
copy_button = st.button("Copy")
if copy_button:
    st.write("Copying to clipboard...")
    st.experimental_set_query_params(output_textbox.encode("utf-8"))
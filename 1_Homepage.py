import streamlit as st
import openai
import os
# from dotenv import load_dotenv
from tqdm import tqdm

# TODO: add user auth and when user is logged in it adds a button at the bottom that links to the user's Medium account and allows them to post the tweet.


# Hide Streamlit Menu and Footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# load_dotenv()

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

def generate_action(user_input):
    with st.spinner("Generating response..."):
        st.text("")  # Empty line to fix spinner size

        base_completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{base_prompt_prefix}{user_input}\n",
            temperature=0.8,
            max_tokens=250
        )

        base_prompt_output = base_completion.choices[0].text.strip()

        # I build Prompt #2.
        second_prompt = f"""
        Take the table of contents and title of the blog post below and generate a blog post written in the style of Paul Graham. Make it feel like a story. Don't just list the points. Go deep into each one. Explain why. Use markdown formatting. You must add citations to support your points.

        Title: {user_input}

        Table of Contents: {base_prompt_output}

        Blog Post:

        References:
        """

        # I call the OpenAI API a second time with Prompt #2
        with tqdm(total=100, desc="Generating response", bar_format="{l_bar}{bar} [time left: {remaining}]", colour='green') as pbar:
            second_prompt_completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=second_prompt,
                temperature=0.85,
                max_tokens=2000
            )

            # Get the output
            second_prompt_output = second_prompt_completion.choices[0].text.strip()
            # Split the output into content and references
            output_parts = second_prompt_output.split("References:")

            # Generate the citations separately
            citation_prompt = f"""
            Generate a list of citations for the blog post below:

            {output_parts[0]}

            Citations:
            """
            citation_completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=citation_prompt,
                temperature=0.5,
                max_tokens=250
            )

            citation_output = citation_completion.choices[0].text.strip()
            # Combine the content and citations
            final_output = f"{output_parts[0]}\n\nReferences:\n{citation_output}"

            # Send over the Prompt #2's output to our UI instead of Prompt #1's.
            return {"output": final_output}

st.title("OpenAI Prompt Chaining Demo")

user_input = st.text_input("Enter the title of your blog post:", "Who invented the internet?")

# save user input to session state so that we can use it in the next page
st.session_state.user_input = user_input

if st.button("Generate"):
    result = generate_action(user_input)
    output_textbox = st.text_area("Output", value=result["output"], height=1000)
    copy_button = st.button("Copy")
    if copy_button:
        st.write("Copying to clipboard...")
        st.experimental_set_query_params(output_textbox.encode("utf-8"))

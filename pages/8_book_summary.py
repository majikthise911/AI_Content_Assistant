import streamlit as st
import openai
import os
from tqdm import tqdm

# Hide Streamlit Menu and Footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define base prompt prefix
base_prompt_prefix = """
Write me a detailed table of contents for a blog post with the title below.

Title:
"""

# Define third prompt prefix
third_prompt_prefix = """
Please use markdown to format the output from Prompt #2 with a title, headers, and bullet points where necessary. Add citations to support your points.
"""

# Function to generate blog post
@st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def generate_action(user_input):
    with st.spinner("Generating response..."):
        st.text("")

        # Generate base completion
        base_completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"{base_prompt_prefix}{user_input}\n"},
            ],
            max_tokens=250
        )

        # Extract base prompt output
        base_prompt_output = base_completion['choices'][0]['message']['content'].strip()

        # Define second prompt
        second_prompt = f"""
        Take the table of contents and title of the blog post below and generate a blog post written in the style of Paul Graham. Make it feel like a story. Don't just list the points. Go deep into each one. Explain why. Use markdown formatting. You must add citations to support your points.

        Title: {user_input}

        Table of Contents: {base_prompt_output}

        Blog Post:

        References:
        """

        # Generate second prompt completion
        with tqdm(total=100, desc="Generating response", bar_format="{l_bar}{bar} [time left: {remaining}]", colour='green') as pbar:
            second_prompt_completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": second_prompt},
                ],
                max_tokens=2000
            )

            # Extract second prompt output and split into content and references
            second_prompt_output = second_prompt_completion['choices'][0]['message']['content'].strip()
            output_parts = second_prompt_output.split("References:")

            # Define citation prompt
            citation_prompt = f"""
            Generate a list of citations for the blog post below:

            {output_parts[0]}

            Citations:
            """

            # Generate citation completion
            citation_completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": citation_prompt},
                ],
                max_tokens=250
            )

            # Extract citation output and combine with content
            citation_output = citation_completion['choices'][0]['message']['content'].strip()
            final_output = f"{output_parts[0]}\n\nReferences:\n{citation_output}"

            return {"output": final_output}

# Define Streamlit interface
st.title("OpenAI Prompt Chaining: Blog Post Generator")

st.write("Examples: ")
st.code('Who invented the internet? ')
st.code('What is the best way to learn Python? ')
st.code('The Science of Sleep: How Our Dreams Shape Our Lives')
user_input = st.text_input("Enter the title of your blog post:")


# save user input to session state so that we can use it in the next page
st.session_state.user_input = user_input

# if st.button("Generate"):
result = generate_action(user_input)
output_textbox = st.text_area("Output", value=result["output"], height=1000)
copy_button = st.button("Copy")
if copy_button:
    st.write("Copying to clipboard...")
    st.experimental_set_query_params(output_textbox.encode("utf-8"))

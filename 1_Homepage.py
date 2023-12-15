import streamlit as st
import openai
import os

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

        # Updated API call
        base_completion = openai.Completion.create(
            model="gpt-4",
            prompt=f"You are an AI assistant asked to write a blog post. {base_prompt_prefix}{user_input}",
            max_tokens=150  # Adjust as needed
        )

        base_prompt_output = base_completion.choices[0].text.strip()

        # Build Prompt #2 using GPT-4
        second_prompt = f"""
        Take the table of contents and title of the blog post below and generate a blog post written in the style of Paul Graham. Make it feel like a story. Don't just list the points. Go deep into each one. Explain why. Use markdown formatting. You must add citations to support your points.

        Title: {user_input}

        Table of Contents: {base_prompt_output}

        Blog Post:

        References:
        """

        # Updated API call
        second_prompt_completion = openai.Completion.create(
            model="gpt-4",
            prompt=second_prompt,
            max_tokens=500  # Adjust as needed
        )

        second_prompt_output = second_prompt_completion.choices[0].text.strip()

        output_parts = second_prompt_output.split("References:")

        citation_prompt = f"""
        Generate a list of citations for the blog post below: 

        {output_parts[0]}

        Citations:
        """

        # Updated API call
        citation_completion = openai.Completion.create(
            model="gpt-4",
            prompt=citation_prompt,
            max_tokens=100  # Adjust as needed
        )

        citation_output = citation_completion.choices[0].text.strip()

        final_output = f"{output_parts[0]}\n\nReferences:\n{citation_output}"

        return {"output": final_output}

st.title("OpenAI Prompt Chaining: Blog Post Generator")
st.write("Examples: ")
st.code('Who invented the internet?')  
st.code('What is the best way to learn Python?')
st.code('The Science of Sleep: How Our Dreams Shape Our Lives')

user_input = st.text_input("Enter the title of your blog post:") 

# Save user input to session state so we can use it in the next page
st.session_state.user_input = user_input   

result = generate_action(user_input)
output_textbox = st.text_area("Output", value=result["output"], height=1000)
copy_button = st.button("Copy")
if copy_button:
    st.write("Copying to clipboard...")
    st.experimental_set_query_params(output_textbox.encode("utf-8"))

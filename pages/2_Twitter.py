import streamlit as st
import openai
import os
from dotenv import load_dotenv

# TODO: add user auth and when user is logged in it adds a button at the bottom that links to the user's Twitter account and allows them to post the tweet.

# Hide Streamlit Menu and Footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

st.title("Generate Twitter Post")

# Import the user input from the first page via session state
if "user_input" not in st.session_state:
    st.warning("Please go to the first page and enter a title for your blog post!")
else:
    user_input = st.session_state.user_input

    st.write(f"Generating a Twitter post based on the title: {user_input}.")

    prompt = f"Generate an edgy Twitter post based on '{user_input}' that incorporates modern slang vocabulary and demonstrates intelligence. Make sure to include at least one link and one emoji in your post. The post should be optimized for maximum viewing by the Twitter algorithm and should be based on the user_input."

    with st.spinner("Generating tweet..."):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

    tweet = response.choices[0].text.strip()

    st.text_area(label="Copy tweet", value=tweet, height=100)
    if st.button("Copy"):
        st.write("Copied to clipboard!")  # add feedback for user
        st.experimental_set_query_params(copied=tweet)  # set query parameters to trigger browser copy

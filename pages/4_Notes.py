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

st.title("Notes Organizer")

# Import the user input from the first page via session state
if "user_input" not in st.session_state:
    st.warning("Please go to the first page and enter a title for your blog post!")
else:
    user_input2 = st.text_input("Paste your messy notes here, and we'll clean them up for you!")

    @st.cache_data(experimental_allow_widgets=True, show_spinner=False)  # 👈 Set the parameter
    def generate_tweet(user_input2):
        prompt = f"I would like for you to do 3 things: 1. re write the following meeting notes to be more organized and concise. Write them in a way that organizes them with bullet points and numbers, titles of sections and headders if needed and 2. suggest action items with suggested deadlines and responsible party for each and 3. suggest next steps. Messy notes:{user_input2}."
        with st.spinner("Generating post..."):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
        )

        tweet = response.choices[0].text.strip()
        return tweet

    tweet = generate_tweet(user_input2)

    st.text_area(label="Copy Cleaned Notes", value=tweet, height=500)
    if st.button("Copy"):
        st.write("Copied to clipboard!")  # add feedback for user
        st.experimental_set_query_params(copied=tweet)  # set query parameters to trigger browser copy

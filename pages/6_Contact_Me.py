
import streamlit as st  # pip install streamlit

# Hide Streamlit Menu and Footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.header(":mailbox: Get In Touch With Me!")
st.markdown(''' Yo! 👋 Welcome to my app! I'd love to hear your thoughts and feedback,
 or even better, collaborate with you! So don't be shy,
 let's make this thing the best it can be! Let's do this!''')

# the below code creates badges for my social media accounts but they are black and so you can't see them 
# so I commented them out for now. I'll figure out how to make them white later.
# st.markdown(
# '''
# ### Hi there 👋, I'm [Jordan](https://github.com/majikthise911) 👨‍💻

# <br/>

# <a href="https://www.linkedin.com/in/jordan-clayton/">
#   <img align="left" alt="Jordan's Linkedin" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />
# </a>

# <a href="https://twitter.com/JordanJClayton2">
#   <img align="left" alt="Jordan Clayton | Twitter" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/twitter.svg" />
# </a>

# <a href="https://t.me/jordan_clayton">
#   <img align="left" alt="Jordan Clayton | Twitter" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/telegram.svg" />
# </a>

# <a href="mailto:jordan_clayton@proton.me">
#   <img align="left" alt="Jordan's Email" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/protonmail.svg" />
# </a>
# <br />
# <br/>
# ''', unsafe_allow_html=True)

contact_form = """
<form action="https://formsubmit.co/jclayton76642@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

st.markdown( ''' You can also reach me at: 

[LinkedIn](https://www.linkedin.com/in/jordan-clayton/)
[Twitter](https://twitter.com/JordanJClayton2)
[Telegram](https://t.me/jordan_clayton)
''', unsafe_allow_html=True)

st.markdown( ''' Also, check out my other projects and give them a follow and a star if they deserve it: [GitHub](https://github.com/majikthise911)''', unsafe_allow_html=True)
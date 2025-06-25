import streamlit as st
from PIL import Image

def sidebar_style():

    sidebar_bg = """
    <style>
        /* Target all sidebar titles with class starting with e1dbuyne */
        [class^="st-emotion-cache"][class*="e1dbuyne"] {
            color: #FFFFFF;
            font-weight: bold;
            font-size: 20px;
        }
        </style>
    """

    logo_unisabana = Image.open("assets/logo_unisabana.png")
    st.markdown(sidebar_bg, unsafe_allow_html=True)
    with st.sidebar:
        st.image(logo_unisabana)
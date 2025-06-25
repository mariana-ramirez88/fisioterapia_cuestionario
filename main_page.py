import streamlit as st
import importlib
import os
from PIL import Image
from assets.sidebar import sidebar_style

# Configuración inicial de la aplicación
st.set_page_config(page_title='Encuesta Usabana', page_icon=":devices:", layout='wide')

# CSS to hide the default sidebar elements
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#Css to change navegation font color 
#st.sidebar.markdown(
#    "<h3 style='color: white;'>Secciones de la Encuesta</h3>", 
#    unsafe_allow_html=True
#)

# Cargar la lista de páginas desde la carpeta "pages"
pages_list = ["home"] + [f.replace(".py", "") for f in os.listdir("pages") if f.endswith(".py")]

# Inicializar el estado de la sesión para la página actual
if "page" not in st.session_state:
    st.session_state.page = "home"  # Start with the homepage

# Sidebar selectbox
#page_selection = st.sidebar.selectbox(" ", pages_list, index=pages_list.index(st.session_state.page))
#if page_selection != st.session_state.page:
#    st.session_state.page = page_selection
#    st.rerun()

# Cargar la página actual
def load_page(page_name):
    if page_name == "home":
        # Homepage content
        st.title("¿Cuánto Duermes, Qué Tanto te Mueves y Qué Tanto Scroleas?")
        st.subheader("¿Sabías que tus hábitos diarios pueden influir en tu salud musculoesquelética? Esta encuesta te ayudará a descubrir el riesgo que tienes de padecer dolor en músculos y articulaciones. ¡Responde y entérate de cómo mejorar tu bienestar!")
        st.write("La información suministrada es de carácter privado y no tendrá ninguna calificación, motivo por el que les pedimos responder con la mayor honestidad posible.")
        st.write("Por favor conteste cada pregunta en todas las secciones, al final se le informará que tan porpenso es a sufrir un nivel de dolor determinado.")
        main_image = Image.open("assets/main_image.png")
        st.image(main_image)
    else:
        module = importlib.import_module(f"pages.{page_name}")
        module.app()

current_page = st.session_state.page
load_page(current_page)

# Obtener el índice de la página actual
current_index = pages_list.index(current_page)

# Estilo de la barra lateral
sidebar_style()


# Mostrar el botón de "Siguiente" solo en la página principal
if current_page == "home":
    if st.button("Siguiente ➡️",key="button0"):
        st.session_state.page = pages_list[1]  # Avanzar a la siguiente página
        st.rerun()
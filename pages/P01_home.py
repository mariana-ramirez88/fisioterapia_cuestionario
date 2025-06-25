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
    st.markdown(sidebar_bg, unsafe_allow_html=True)

with st.sidebar:
    logo_unisabana = Image.open("assets/logo_unisabana.png")
    st.image(logo_unisabana)

sidebar_style()
        
def app():
    #st.write("Asegurate de responder todas las preguntas. Todas las respuestas seleccionadas estarán en rojo")

    st.header('Preguntas Sociodemográficas')
    # PREGUNTAS RELACIONADAS AL HOGAR
    # home area

    def initialize_radio_var(question, session_key, radio_key, answers, default_value_map=None):
        if default_value_map:
            # When there is a numerical mapping for answers
            if session_key not in st.session_state:
                st.session_state[session_key] = None

            if radio_key not in st.session_state:
                if session_key in st.session_state and st.session_state[session_key] is not None:
                    # Reverse mapping to selected stored answer
                    reverse_map = {v: k for k, v in default_value_map.items()}
                    selected_option = reverse_map.get(st.session_state[session_key], None)
                    st.session_state[radio_key] = selected_option
                else:
                    st.session_state[radio_key] = None 

            def update_variable():
                st.session_state[session_key] = default_value_map[st.session_state[radio_key]]

            st.radio(
                question, options=answers, key=radio_key, on_change=update_variable
            )
        else:
            # When no mapping is provided
            if session_key not in st.session_state:
                st.session_state[session_key] = None

            if radio_key not in st.session_state:
                # Synchronize radio_key with session_key
                if session_key in st.session_state and st.session_state[session_key] is not None:
                    st.session_state[radio_key] = st.session_state[session_key]
                else:
                    st.session_state[radio_key] = None

            def update_variable():
                st.session_state[session_key] = st.session_state[radio_key]

            st.radio(question, options=answers, key=radio_key, on_change=update_variable,index=None)



    questions = [
    { "question": "¿Cuál es tu edad?",
        "session_key": "user_age",
        "radio_key":"age",
        "options": ['10-12', '13-15', '16-18', 'mayor a 18'],
        "default_value_map": {"10-12":0, '13-15':0,"16-18":1, 'mayor a 18':0 }
        },

        { "question": "La zona en que usted vive es:",
        "session_key": "user_home",
        "radio_key":"zone",
        "options": ["Urbana", "Rural"],
        "default_value_map": {"Urbana":1, 'Rural':0}
        },

        { "question": "¿Cuál es su género?",
        "session_key": "user_gender",
        "radio_key":"gender",
        "options": ["Femenino", "Masculino"],
        "default_value_map": {"Femenino":0, "Masculino":1 }
        },

        { "question": "¿Realizas tareas del hogar como tender tu cama o arreglar tu cuarto?",
        "session_key": "user_home_room",
        "radio_key":"home_room",
        "options": ['Si', 'No'],
        "default_value_map": {"Si":1, 'No':0} },

        { "question": "¿Realizas tareas del hogar como lavar, tender o planchar ropa?",
        "session_key": "user_home_laundry",
        "radio_key":"home_laundry",
        "options": ['Si', 'No'],
        "default_value_map": {"Si":1, 'No':0} },
        
        { "question": "¿Realizas tareas de limpieza en el hogar como barrer o trapear?",
        "session_key": "user_home_cleaning",
        "radio_key":"home_cleaning",
        "options": ['Si', 'No'],
        "default_value_map": {"Si":1, 'No':0} },

        { "question": "¿Realizas tareas relacionadas al paseo cuidado o alimentación de mascotas?",
        "session_key": "user_home_pets",
        "radio_key":"home_pets",
        "options": ['Si', 'No'],
        "default_value_map": {"Si":1, 'No':0} },

    ]

    for q in questions:
        initialize_radio_var(
            question=q["question"],
            session_key=q["session_key"],
            radio_key=q["radio_key"],
            answers=q["options"],
            default_value_map=q.get("default_value_map")  # Some questions may not have mapping
        )


    st.subheader("Preguntas relacionadas a su actividad fisica en tiempo libre")
    opciones_activity = {
        "No":0,
        "1-2 días": 1,
        "3-4 días": 2, 
        "5-6 días": 3, 
        "7 o más días": 4
    }

    questions2 = ["¿Ha levantado pesas en los últimos 7 días (última semana)? Si su respuesta es sí, ¿cuántas veces lo ha hecho?",
        "¿Ha realizado actividades relacionadas al juego en los últimos 7 días (última semana)? Si su respuesta es sí, ¿cuántas veces lo ha hecho?",
        "¿Ha practicado fútbol en los últimos 7 días (última semana)? Si su respuesta es sí, ¿cuántas veces lo ha hecho??:",
    ]

    session_keys = ["user_activity_weights","user_activity_play","user_activity_football"]
    radio_keys = ["activity_weights", "activity_play", "activity_football"]

    for i in range(len(questions2)):
        initialize_radio_var(
            question=questions2[i],
            session_key=session_keys[i],
            radio_key=radio_keys[i],
            answers= list(opciones_activity.keys()),
            default_value_map=opciones_activity

        )

    # Verificar si todas las preguntas han sido respondidas
    all_answered = all(st.session_state[key] is not None for key in session_keys + [q["session_key"] for q in questions])

    # Botón de siguiente deshabilitado si no se han respondido todas las preguntas
    # Colocar los botones en la parte inferior
    col1, col2, col3 = st.columns([1, 4, 1])

    with col3:
        if st.button("Siguiente ➡️", key="next_button"):
            if all_answered:
                st.session_state.page = "P02_sleep"  # Cambia esto según corresponda
                st.rerun()
            else:
                st.error("Por favor, responda todas las preguntas antes de continuar.")


    

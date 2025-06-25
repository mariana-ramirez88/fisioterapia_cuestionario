import streamlit as st
from PIL import Image
from pages.P01_home import sidebar_style

sidebar_style()
        
def app():
    #st.write("Asegurate de responder todas las preguntas. Todas las respuestas seleccionadas estarán en rojo")

    st.header('Preguntas relacionadas al dolor')
    # CUELLO

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
        
        { "question": "¿Cuánto tiempo ha tenido dolor o molestia durante los últimos 6 meses en el cuello?",
        "session_key": "user_neck6",
        "radio_key":"neck6",
        "options": ['0 días', '1 a 7 días', "8 a 30 días", "Más de 30 días", "Todos los días"],
        "default_value_map": {"0 días":0, '1 a 7 días':1, "8 a 30 días":2, "Más de 30 días":3, "Todos los días":4} },

        { "question": "¿Usualmente, ¿cuánto tiempo dura el dolor en el cuello??",
        "session_key": "user_neck7",
        "radio_key":"neck7",
        "options": ['Menos de 12 horas', '12 a 24 horas', "1 a 7 días", "Más de una semana"],
        "default_value_map": {"Menos de 12 horas":0, '12 a 24 horas':1, "1 a 7 días":2, "Más de una semana":3} },

        { "question": "Durante los últimos 6 meses, ¿ha tenido que suspender o modificar sus actividades escolares debido al dolor, molestia o disconfort en el cuello?",
        "session_key": "user_neck9",
        "radio_key":"neck9",
        "options": ['0 días', '1 a 7 días', "1 a 4 semanas", "Más de 1 mes"],
        "default_value_map": {"0 días":0, '1 a 7 días':1, "1 a 4 semanas":2, "Más de 1 mes":3} },
    ]

    for q in questions:
        initialize_radio_var(
            question=q["question"],
            session_key=q["session_key"],
            radio_key=q["radio_key"],
            answers=q["options"],
            default_value_map=q.get("default_value_map")  # Some questions may not have mapping
        )

    # preguntas de si o no
    opciones_yn = {
        "No":0,
        "Si": 1
    }

    questions2 = ["¿Usted ha tenido dolor o molestia en el cuello (de color rojo) durante los últimos 6 meses?",
                  "¿En los últimos 6 meses, el dolor o molestia percibido en el cuello está acompañado de dolor de cabeza?",
                  "¿Usted relaciona el origen del dolor o molestia, con el uso del celular o demás dispositivos tecnológicos?",
                  "¿El dolor o molestia está presente únicamente mientras revisa su celular o está utilizando algún dispositivo tecnológico?",
                  "¿El dolor o molestia está presente de forma permanente?",
                  "¿Cuánto tiempo estas molestias le han impedido realizar sus actividades escolares de la manera usual, en los últimos 6 meses?",
                  "Durante los últimos 6 meses, ¿ha visitado alguna vez a un médico, fisioterapeuta, quiropráctico u otra persona similar, o recibido otro tratamiento debido a la molestia en el cuello?",
                  "Durante los últimos 6 meses, ¿ha tomado alguna vez medicamentos debido a la molestia en el cuello?"
                  ]

    session_keys = ["user_neck1","user_neck2","user_neck3", "user_neck4", "user_neck5","user_neck10", "user_neck11", "user_neck12"]
    radio_keys = ["neck1", "neck2", "neck3","neck4", "neck5", "neck10", "neck11", "neck12"]

    for i in range(len(questions2)):
        initialize_radio_var(
            question=questions2[i],
            session_key=session_keys[i],
            radio_key=radio_keys[i],
            answers= list(opciones_yn.keys()),
            default_value_map=opciones_yn

        )

    #slider 
    def initialize_slider_var(question, session_key, slider_key, min_val=0, max_val=10, step=1):
        # Inicializar session_state para la variable de respuesta
        if session_key not in st.session_state:
            st.session_state[session_key] = None

        # Inicializar slider_key solo si ya hay un valor previo en session_key
        if slider_key not in st.session_state:
            if st.session_state[session_key] is not None:
                st.session_state[slider_key] = st.session_state[session_key]
            else:
                st.session_state[slider_key] = min_val

        def update_slider_value():
            st.session_state[session_key] = st.session_state[slider_key]

        st.markdown(f"**{question}**")
        st.slider(
            label="Seleccione un valor:",
            min_value=min_val,
            max_value=max_val,
            step=step,
            key=slider_key,
            on_change=update_slider_value
        )

    initialize_slider_var(
    question="¿Cuál es la severidad del dolor en una escala de 0 a 10, teniendo en cuenta que 10 significa el dolor más fuerte que usted haya experimentado y cero nada de dolor?",
    session_key="user_neck8",
    slider_key="slider_neck8",
    min_val=0,
    max_val=10,
    step=1
    )

    # Verificar si todas las preguntas han sido respondidas
    all_answered = all(st.session_state[key] is not None for key in session_keys + [q["session_key"] for q in questions])

    # Botón de siguiente deshabilitado si no se han respondido todas las preguntas
    # Colocar los botones en la parte inferior
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("⬅️ Regresar", key="back4_button"):
            st.session_state.page = "P03_mobile"  # Cambia esto según corresponda
            st.rerun()
    with col3:
        if st.button("Siguiente ➡️", key="next4_button"):
            if not all_answered:
                st.warning("Por favor, responda todas las preguntas antes de continuar.")
            else:
                st.session_state.page = "P05_send"
                st.rerun()


    #TODO
    # incluir fotos y revisar pregunta numerica
    # slider necesita dos clicks para cambiar de opcion, revisar
    # agrandar letra

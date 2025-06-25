import streamlit as st
from pages.P01_home import sidebar_style

sidebar_style()

def initialize_radio_var(question, session_key, radio_key, answers, ans_list = "answers list", default_value_map=None, average_key = "average"):
    
        if ans_list not in st.session_state:
            st.session_state[ans_list] = {}

            # Function to calculate the average dynamically based on current responses
        def calculate_average(response_list_key):
            # Extract only numeric values (assuming the values in the dictionary are numeric)
            numeric_values = [value for value in st.session_state[response_list_key].values() if isinstance(value, (int, float))]
            if numeric_values:
                try:
                    return sum(numeric_values) / len(numeric_values)
                except:
                    return 0
            return 0

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
                # Update the response list dictionary with the session_key and the selected answer
                st.session_state[ans_list][session_key] = st.session_state[session_key]

                # Calculate and display the average after the answer change
                average = calculate_average(ans_list)
                st.session_state[average_key] = average
                #st.write(f"Average: {average_key}: {average}")
                
            st.radio(
                question, options=answers, key=radio_key, on_change=update_variable,index=None
            )
        else:
            # When no mapping is provided
            if session_key not in st.session_state:
                st.session_state[session_key] = None

            if radio_key not in st.session_state:
            # Synchronize radio_key with session_key
                if session_key in st.session_state and st.session_state[session_key] is not None:
                    st.session_state[radio_key] = st.session_state[session_key]  # Restore stored value
            else:
                st.session_state[radio_key] = None  # No default selection
            def update_variable():
                st.session_state[session_key] = st.session_state[radio_key]
                # Update the response list dictionary with the session_key and the selected answer
                st.session_state[ans_list][session_key] = st.session_state[session_key]
                # Calculate and store the average under a unique key
                average = calculate_average(ans_list)
                st.session_state[average_key] = average  # Store average in session state with the unique key
                #st.write(f"Average ({average_key}): {average}")
            st.radio(question, options=answers, key=radio_key, on_change=update_variable, index=None)


def make_questions(questions, session_keys, radio_keys, mapping, answers_list: str, average_name: str):
        for i in range(len(questions)):
            initialize_radio_var(
                question=questions[i],
                session_key=session_keys[i],
                radio_key=radio_keys[i],
                answers= list(mapping.keys()),
                ans_list=answers_list,
                default_value_map=mapping,
                average_key=average_name)

def app():
    st.subheader('Preguntas Relacionadas al Sueño')
    st.write("Responda Con qué frecuencia en días, en la última semana, le sucedieron los siguientes eventos:")

    

    questionsF5 = ["Despertó más cansado que cuando se acostó","Sintió cansancio la mayor parte del día", "Fue difícil levantarse en la mañana",
    "Sintió necesidad de acostarse y levantarse más tarde que los demás"]
    session_keys = ['userF5.1', 'userF5.2', 'userF5.3', 'userF5.4']
    radio_keys = ['sleepF5.1','sleepF5.2', 'sleepF5.3','sleepF5.4']

    # Question 3: Sleep Factor 5
    valores_respuestasF5 = {
        "0 días": 0,
        "1-2 días": 1,
        '3-4 días': 2,
        '5-6 días':3
    }

        
    make_questions(questionsF5,session_keys,radio_keys,valores_respuestasF5,"respuestasF5","promedioF5")

    # SLEEP FACTOR 2
    # Lista para almacenar las respuestas
    questionsF2 = ["Tuvo pesadillas", "Despertó con miedo","Despertó sudando por algo que soñó", "Soñó algo que le dio miedo"]
    session_keysF2 = ['userF2.1', 'userF2.2', 'userF2.3', 'userF2.4']
    radio_keysF2 = ['sleepF2.1','sleepF2.2', 'sleepF2.3','sleepF2.4']

    make_questions(questionsF2,session_keysF2,radio_keysF2,valores_respuestasF5,"respuestasF2","promedioF2")

    preguntas_F3 = [
        "Despertó porque se atragantó",
        "Le dijeron que despertó llorando pero usted no se acuerda",
        "Despertó y sintió que no podía moverse",
        "Le dijeron que despertó asustado/a y gritando pero usted no se acuerda",
        "Roncó (se lo dijeron o lo sabe)"
    ]
    valores_F3 = {
        "0 días":0,
        "1-2 días": 1,
        "3-4 días": 2, 
        "5-6 días": 3, 
    }

    session_keysF3 = ['userF3.1', 'userF3.2', 'userF3.3', 'userF3.4', 'userF3.5']
    radio_keysF3 = ['sleepF3.1','sleepF3.2', 'sleepF3.3','sleepF3.4','sleepF3.5']
    make_questions(preguntas_F3,session_keysF3,radio_keysF3,valores_F3,"respuestasF3","promedioF3")

    # Verificar si todas las preguntas han sido respondidas
    all_session_keys = session_keys + session_keysF2 + session_keysF3
    all_answered = all(st.session_state.get(key) is not None for key in all_session_keys)

    # Botón de siguiente deshabilitado si no se han respondido todas las preguntas
    # Colocar los botones en la parte inferior
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("⬅️ Regresar", key="back2_button"):
            st.session_state.page = "P01_home"  # Cambia esto según corresponda
            st.rerun()
    with col3:
        if st.button("Siguiente ➡️", key="next2_button"):
            if not all_answered:
                st.warning("Por favor, responda todas las preguntas antes de continuar.")
            else:
                st.session_state.page = "P03_mobile"
                st.rerun()




    


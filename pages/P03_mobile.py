import streamlit as st 
#from pages.P02_sleep import make_questions
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
            # Reverse mapping to selected stored answer
            reverse_map = {v: k for k, v in default_value_map.items()}
            selected_option = reverse_map.get(st.session_state[session_key], None)
            st.session_state[radio_key] = selected_option

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
            st.session_state[average_key] = calculate_average(ans_list)
            calculate_combined_average(
        list_keys=["respuestasM1", "respuestasM2"], combined_average_key="mobile_average"
    )
        st.radio(question, options=answers, key=radio_key, on_change=update_variable,index=None)


def calculate_combined_average(list_keys, combined_average_key):
    combined_answers = []
    for key in list_keys:
        if key in st.session_state:
            combined_answers.extend(
                [value for value in st.session_state[key].values() if isinstance(value, (int, float))]
            )

    if combined_answers:
        combined_average = sum(combined_answers) / len(combined_answers)
    else:
        combined_average = 0

    st.session_state[combined_average_key] = combined_average
    st.write(f"Combined Average ({combined_average_key}): {combined_average}")

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
    # PREGUNTAS RELACIONADAS A mobile use 
    st.subheader('Preguntas Relacionadas al uso de dispositivos mobiles ')
    st.write('Responde a las siguientes afirmaciones')

    # Diccionario de opciones de respuesta
    valores_respuestas_mobile = {
        "nunca": 0,
        "Rara vez": 1,
        'A veces': 2,
        'Con frecuencia':3,
        'Muchas Veces': 4
    }

    # Lista de preguntas
    preguntas_m1 = [
        "Me han llamado la atención o me han hecho alguna advertencia por utilizar mucho el celular",
        "Me he puesto un límite de uso y lo he podido cumplir?",
        "He discutido con algún familiar por el gasto económico que hago del celular",
        "Dedico más tiempo del que quisiera a usar el celular",
        "Me he pasado (excedido) con el uso del celular"
        ,"Me he acostado más tarde o he dormido menos por estar utilizando el celular",
        "Gasto más dinero con el celular del que me había previsto",
        "Cuando me aburro, utilizo el celular",
        "Utilizo el celular en situaciones que, aunque no son peligrosas, no es correcto hacerlo (comiendo, mientras otras personas me hablan, etc.)",
        "Me han reñido (regañado) por el gasto económico del celular"]

    session_keysM1 = ["user_m1.1","user_m1.2", "user_m1.3", "user_m1.4","user_m1.5", "user_m1.6","user_m1.7","user_m1.8","user_m1.9","user_m1.10"]
    radio_keysM1 = ["mobile1.1","mobile1.2","mobile1.3","mobile1.4","mobile1.5","mobile1.6","mobile1.7","mobile1.8","mobile1.9","mobile1.10"]

    make_questions(preguntas_m1,session_keysM1,radio_keysM1,valores_respuestas_mobile,"respuestasM1","averageM1")

    # Diccionario de opciones de respuesta
    valores_respuestas_mobile2 = {
        "Totalmente en desacuerdo": 0,
        "Un poco en desacuerdo": 1,
        'Neutral': 2,
        'Un poco de acuerdo':3,
        'Totalmente de acuerdo': 4
    }
    preguntas_m2 = ["Cuando llevo un tiempo sin utilizar el celular, siento la necesidad de usarlo (llamar a alguien, enviar un SMS o un WhatsApp, etc.)",
        "Últimamente utilizo mucho más el celular",
        "Si se me estropeara (dañara) el celular durante un periodo largo de tiempo y tardarán en arreglarlo, me encontraría mal",
        "Cada vez necesito utilizar el celular con más frecuencia",
        "Si no tengo el celular me encuentro mal",
        "Cuando tengo el celular a la mano, no puedo dejar de utilizarlo",
        "Nada más levantarme lo primero que hago es ver si me ha llamado alguien al celular, si me han mandado un mensaje, un WhatsApp, etc.",
        "Cuando me siento solo, le hago una llamada a alguien, le envío un mensaje o un WhatsApp, etc. ",
        "Gasto más dinero con el celular ahora que al principio ",
        "Ahora mismo agarraría el celular y enviaría un mensaje, o haría una llamada ",
        "No es suficiente para mí usar el celular como antes, necesito usarlo cada vez más ",
        "No creo que pudiera aguantar una semana sin celular "
    ]

    st.subheader("Sección 3.2")
    st.write('Indique en qué medida está de acuerdo o en desacuerdo con las afirmaciones que se presentan a continuación:')
    session_keysM2 = ["user_m2.1","user_m2.2", "user_m2.3", "user_m2.4","user_m2.5", "user_m2.6","user_m2.7","user_m2.8","user_m2.9","user_m2.10","user_m2.11","user_m2.12"]

    radio_keysM2 = ["mobile2.1","mobile2.2","mobile2.3","mobile2.4","mobile2.5","mobile2.6","mobile2.7","mobile2.8","mobile2.9","mobile2.10","mobile2.11","mobile2.12"]
    make_questions(preguntas_m2,session_keysM2,radio_keysM2,valores_respuestas_mobile2,"respuestasM2","averageM2")
    # Display the averages
     # Inicialización de promedios si no existen
    if "averageM1" not in st.session_state:
        st.session_state["averageM1"] = 0
    if "averageM2" not in st.session_state:
        st.session_state["averageM2"] = 0
    averageM1 = st.session_state["averageM1"]
    averageM2 = st.session_state["averageM2"]
    promedio_mobile = (averageM1 + averageM2)/2
    st.session_state['promedio_mobile'] = promedio_mobile


    # Verificar si todas las preguntas han sido respondidas
    all_session_keys = session_keysM1 + session_keysM2
    all_answered = all(st.session_state.get(key) is not None for key in all_session_keys)

    # Botón de siguiente deshabilitado si no se han respondido todas las preguntas
    # Colocar los botones en la parte inferior
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("⬅️ Regresar", key="back3_button"):
            st.session_state.page = "P02_sleep"  # Cambia esto según corresponda
            st.rerun()
    with col3:
        if st.button("Siguiente ➡️", key="next3_button"):
            if not all_answered:
                st.warning("Por favor, responda todas las preguntas antes de continuar.")
            else:
                st.session_state.page = "P04_pain"
                st.rerun()


import streamlit as st
from PIL import Image
import os

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Reto ODS Interactivo", page_icon="🌍", layout="centered")

# ESTILOS PERSONALIZADOS (CSS)
st.markdown("""
    <style>
    .main { background-color: #0D1117; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #161B22;
        color: white;
        border: 1px solid #58A6FF;
    }
    .stButton>button:hover {
        background-color: #58A6FF;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZACIÓN DE ESTADO (Para guardar puntos y pregunta actual)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# DATOS DE PREGUNTAS
questions = [
    {"q": "¿Qué ODS busca el fin de la pobreza?", "a": "ODS 1", "img": "img/ods1.png"},
    {"q": "¿Cuál promueve la igualdad de género?", "a": "ODS 5", "img": "img/ods5.png"},
    {"q": "¿Qué ODS se enfoca en la acción climática?", "a": "ODS 13", "img": "img/ods13.png"}
]

def check_answer(choice, correct):
    if choice == correct:
        st.session_state.score += 1
        st.toast("¡Correcto! 🌟")
    else:
        st.toast("Incorrecto... ❌", icon="⚠️")
   
    if st.session_state.current_idx < len(questions) - 1:
        st.session_state.current_idx += 1
    else:
        st.session_state.game_over = True

# LÓGICA DE LA INTERFAZ
st.title("🌍 Reto ODS Interactivo")

if not st.session_state.game_over:
    item = questions[st.session_state.current_idx]
   
    # Mostrar progreso
    progress = (st.session_state.current_idx + 1) / len(questions)
    st.progress(progress)
   
    st.subheader(f"Pregunta {st.session_state.current_idx + 1}")
   
    # Mostrar Imagen
    if os.path.exists(item["img"]):
        image = Image.open(item["img"])
        st.image(image, width=300)
    else:
        st.info("Intentando cargar imagen del ODS...")

    st.write(f"### {item['q']}")

    # Botones de opciones
    options = ["ODS 1", "ODS 5", "ODS 13", "ODS 7"]
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"btn_{i}"):
                check_answer(opt, item["a"])
                st.rerun()

else:
    st.balloons()
    st.success(f"¡Felicidades! Has terminado el reto.")
    st.metric("Puntuación Final", f"{st.session_state.score} / {len(questions)}")
   
    if st.button("Reiniciar Juego"):
        st.session_state.score = 0
        st.session_state.current_idx = 0
        st.session_state.game_over = False
        st.rerun()


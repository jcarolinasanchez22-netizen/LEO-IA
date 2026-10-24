import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="LEO-IA: Comprensión Lectora",
    page_icon="🦁",
    layout="wide"
)

# ======================
# PEGA TU CLAVE AQUÍ 👇
# ======================
API_KEY = st.secrets.get("API_KEY")
genai.configure(api_key=API_KEY)
modelo = genai.GenerativeModel("gemini-1.5-flash")

CUENTO = """
📖 El cuaderno perdido

Cada mañana, Mateo caminaba hacia su colegio por un pequeño parque. Un lunes, mientras avanzaba entre los árboles, encontró un cuaderno azul sobre una banca. Al abrirlo, descubrió dibujos, poemas y una historia que todavía no tenía final. En la primera página estaba escrito: «Este cuaderno guarda mis sueños. Algún día quiero ser escritora». Mateo sintió curiosidad. Aunque deseaba quedarse con el cuaderno para leer las historias, decidió llevarlo al colegio y entregárselo a su profesora.

Durante el recreo, la profesora anunció que habían encontrado un cuaderno perdido. Una estudiante llamada Valeria levantó la mano emocionada. Explicó que lo había olvidado en el parque cuando regresaba a casa. Al recuperar su cuaderno, Valeria sonrió y agradeció a Mateo. Sin embargo, él observó que ella parecía preocupada. —¿Te sucede algo? —preguntó. —Tengo miedo de mostrar mis historias porque pienso que nadie las encontrará interesantes —respondió Valeria. Mateo recordó los dibujos y las primeras páginas que había leído. —Creo que tienes buenas ideas. No deberías dejar de escribir por miedo a lo que piensen los demás —le dijo.

Aquella tarde, Valeria terminó su historia y decidió compartirla con sus compañeros. Descubrió que algunas personas disfrutaban sus relatos y otras le daban consejos para mejorarlos. Desde entonces, comprendió que la valentía no consiste en dejar de sentir miedo, sino en atreverse a intentar algo a pesar de él.
"""

PROMPT_SISTEMA = f"""
Eres LEO-IA, asistente de comprensión lectora para NOVENO AÑO de EGB, Lengua y Literatura, Ecuador.

PRINCIPIO: Acompañas, NUNCA resuelves por el estudiante.

TEXTO:
{CUENTO}

NIVELES:
1. LITERAL: datos explícitos
2. INFERENCIAL: deducir causas y consecuencias
3. CRÍTICO: opiniones justificadas con el texto

REGLAS:
- No des respuestas listas para copiar
- Solo das pistas si el estudiante pide ayuda o falla
- Si no entiendes la pregunta, pide aclaración
- No inventes nada que no esté en el cuento
- No pongas calificaciones: remite al docente
- Usa lenguaje claro para jóvenes de 13-15 años

INICIO:
"¡Hola! Soy LEO-IA, tu asistente de comprensión lectora. No resolveré las actividades por ti, pero te acompañaré con preguntas y pistas. Hoy trabajaremos con el cuento «El cuaderno perdido». ¿Empezamos?"
"""

st.title("🦁 LEO-IA — Asistente de Comprensión Lectora")
st.subheader("Lengua y Literatura • Noveno Año de EGB • Ecuador")
st.divider()

with st.expander("📖 Leer el cuento", expanded=False):
    st.markdown(CUENTO)
st.divider()

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! Soy LEO-IA, tu asistente de comprensión lectora. No resolveré las actividades por ti, pero te acompañaré con preguntas y pistas. Hoy trabajaremos con el cuento «El cuaderno perdido». ¿Empezamos?"}
    ]

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if pregunta := st.chat_input("Escribe tu respuesta o pregunta..."):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("🦁 Pensando..."):
            conversacion = [
                {"role": "user", "parts": [PROMPT_SISTEMA]},
                {"role": "model", "parts": ["Entendido."]}
            ]
            for m in st.session_state.mensajes:
                conversacion.append({"role": m["role"], "parts": [m["content"]]})
            respuesta = modelo.generate_content(conversacion)
            st.markdown(respuesta.text)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta.text})

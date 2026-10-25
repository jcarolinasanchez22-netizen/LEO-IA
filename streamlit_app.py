import google.generativeai as genai
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="LEO-IA: Comprensión Lectora",
    page_icon="🦁",
    layout="wide"
)

# Obtener la clave
API_KEY = st.secrets.get("API_KEY")

if not API_KEY:
    st.error("⚠️ Falta la clave API en Secrets")
    st.stop()

# Configurar con la clave AQ
genai.configure(api_key=API_KEY)

# Modelo compatible con claves nuevas
modelo = genai.GenerativeModel("gemini-pro")
# El cuento
CUENTO = """
El cuaderno perdido

Cada mañana, Mateo caminaba hacia su colegio por un pequeño parque. Un lunes, mientras avanzaba entre los árboles, encontró algo en el suelo: un cuaderno de tapa azul oscuro. Al abrirlo, vio que estaba lleno de dibujos y notas escritas con letra muy bonita.

—¿De quién será? —se preguntó Mateo.

Lo llevó al colegio y preguntó a todos sus compañeros, pero nadie lo reconoció. Al día siguiente, volvió al parque y esperó. Al rato, vio a una niña que caminaba mirando el suelo con cara triste. Era Sofía, una niña de otro curso.

—¿Buscas esto? —le preguntó Mateo mostrando el cuaderno.

—¡Sí, es mío! —dijo ella con alegría—. Tiene todos mis dibujos y las notas para mi abuela. Muchas gracias.

Mateo sonrió. Sintió una satisfacción inmensa al devolverlo. Desde ese día, se convirtieron en grandes amigos.
"""

# Título
st.title("🦁 LEO-IA — Asistente de Comprensión Lectora")
st.subheader("Lengua y Literatura • Noveno Año de EGB • Ecuador")
st.divider()

if st.button("📖 Leer el cuento"):
    st.markdown(CUENTO)
    st.divider()

# Historial
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"rol": "asistente", "mensaje": "¡Hola! Soy LEO-IA, tu asistente de comprensión lectora. No resolveré las actividades por ti, pero te acompañaré con preguntas y pistas. Hoy trabajaremos con el cuento «El cuaderno perdido». ¿Empezamos?"}
    ]

for msg in st.session_state.historial:
    if msg["rol"] == "asistente":
        st.info(msg["mensaje"], icon="🦁")
    else:
        st.chat_message("usuario").write(msg["mensaje"])

pregunta = st.chat_input("Escribe tu pregunta aquí...")

if pregunta:
    st.session_state.historial.append({"rol": "usuario", "mensaje": pregunta})
    
    instruccion = f"""
Eres LEO-IA, guía de comprensión lectora para noveno año.
NO des respuestas directas. Da pistas y preguntas para que el estudiante piense.
Tono amable, claro y alentador.

CUENTO:
{CUENTO}

PREGUNTA: {pregunta}
Responde con pistas, sin dar la respuesta completa.
"""

    try:
        respuesta = modelo.generate_content(instruccion)
        texto = respuesta.text
    except Exception as e:
        texto = f"😅 Detalle técnico: {str(e)[:100]}"
    
    st.session_state.historial.append({"rol": "asistente", "mensaje": texto})
    st.rerun()

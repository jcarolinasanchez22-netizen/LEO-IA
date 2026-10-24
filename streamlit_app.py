import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(
    page_title="LEO-IA: Comprensión Lectora",
    page_icon="🦁",
    layout="wide"
)

# Obtener la clave de forma segura
API_KEY = st.secrets.get("API_KEY")

if not API_KEY:
    st.error("⚠️ Falta configurar la clave API en Secrets")
    st.stop()

genai.configure(api_key=API_KEY)

# Modelo a usar
modelo = genai.GenerativeModel("gemini-2.0-flash")

# El cuento completo
CUENTO = """
El cuaderno perdido

Cada mañana, Mateo caminaba hacia su colegio por un pequeño parque. Un lunes, mientras avanzaba entre los árboles, encontró algo en el suelo: un cuaderno de tapa azul oscuro. Al abrirlo, vio que estaba lleno de dibujos y notas escritas con letra muy bonita.

—¿De quién será? —se preguntó Mateo.

Lo llevó al colegio y preguntó a todos sus compañeros, pero nadie lo reconoció. Al día siguiente, volvió al parque y esperó. Al rato, vio a una niña que caminaba mirando el suelo con cara triste. Era Sofía, una niña de otro curso.

—¿Buscas esto? —le preguntó Mateo mostrando el cuaderno.

—¡Sí, es mío! —dijo ella con alegría—. Tiene todos mis dibujos y las notas para mi abuela. Muchas gracias.

Mateo sonrió. Sintió una satisfacción inmensa al devolverlo. Desde ese día, se convirtieron en grandes amigos.
"""

# Título principal
st.title("🦁 LEO-IA — Asistente de Comprensión Lectora")
st.subheader("Lengua y Literatura • Noveno Año de EGB • Ecuador")
st.divider()

# Botón para mostrar el cuento
if st.button("📖 Leer el cuento"):
    st.markdown(CUENTO)
    st.divider()

# Inicializar historial de conversación
if "historial" not in st.session_state:
    st.session_state.historial = [
        {
            "rol": "asistente",
            "mensaje": "¡Hola! Soy LEO-IA, tu asistente de comprensión lectora. No resolveré las actividades por ti, pero te acompañaré con preguntas y pistas. Hoy trabajaremos con el cuento «El cuaderno perdido». ¿Empezamos?"
        }
    ]

# Mostrar mensajes
for msg in st.session_state.historial:
    if msg["rol"] == "asistente":
        st.info(msg["mensaje"], icon="🦁")
    else:
        st.chat_message("usuario").write(msg["mensaje"])

# Entrada del usuario
pregunta = st.chat_input("Escribe tu pregunta o respuesta aquí...")

if pregunta:
    # Guardar la pregunta del usuario
    st.session_state.historial.append({"rol": "usuario", "mensaje": pregunta})
    
    # Instrucción para el asistente
    instruccion = f"""
Eres LEO-IA, un asistente de comprensión lectora para estudiantes de noveno año de Educación General Básica en Ecuador.
Tu función es guiar al estudiante con PISTAS y PREGUNTAS, NUNCA darle las respuestas directas.
Usa un tono amable, alentador y claro.

Aquí está el cuento:
{CUENTO}

Pregunta del estudiante: {pregunta}
Responde como LEO-IA, guiando con pistas sin dar la respuesta completa.
"""

    # Obtener respuesta del modelo
    try:
        respuesta = modelo.generate_content(instruccion)
        texto_respuesta = respuesta.text
    except Exception as e:
        texto_respuesta = "😅 Lo siento, hubo un pequeño detalle. Intenta de nuevo, por favor."
    
    # Guardar y recargar
    st.session_state.historial.append({"rol": "asistente", "mensaje": texto_respuesta})
    st.rerun()

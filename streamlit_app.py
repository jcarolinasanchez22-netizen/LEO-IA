
import streamlit as st
from google import genai

# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================
st.set_page_config(
    page_title="LEO-IA: Comprensión Lectora",
    page_icon="🦁",
    layout="wide"
)

st.title("🦁 LEO-IA — Asistente de Comprensión Lectora")
st.subheader("Lengua y Literatura • Noveno Año de EGB • Ecuador")
st.divider()

# ==========================================
# CONEXIÓN CON GEMINI
# ==========================================
API_KEY = st.secrets.get("API_KEY", "")

if not API_KEY:
    st.error(
        "No se encuentra API_KEY. "
        "Configúrala en Settings → Secrets de Streamlit."
    )
    st.stop()

# Crear cliente de Gemini
try:
    cliente = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("No se pudo inicializar Gemini.")
    st.code(str(e))
    st.stop()

# Modelo de Gemini
MODELO = "gemini-2.5-flash"

# ==========================================
# CUENTO
# ==========================================
CUENTO = """
# El cuaderno perdido

Cada mañana, Mateo caminaba hacia su colegio por un pequeño
parque. Un lunes, mientras avanzaba entre los árboles, encontró
algo en el suelo: un cuaderno de tapa azul oscuro. Al abrirlo,
vio que estaba lleno de dibujos y notas escritas con letra
muy bonita.

—¿De quién será? —se preguntó Mateo.

Lo llevó al colegio y preguntó a todos sus compañeros, pero
nadie lo reconoció. Al día siguiente, volvió al parque y esperó.
Al rato, vio a una niña que caminaba mirando el suelo con cara
triste. Era Sofía, una niña de otro curso.

—¿Buscas esto? —le preguntó Mateo mostrando el cuaderno.

—¡Sí, es mío! —dijo ella con alegría—. Tiene todos mis dibujos
y las notas para mi abuela. Muchas gracias.

Mateo sonrió. Sintió una satisfacción inmensa al devolverlo.
Desde ese día, se convirtieron en grandes amigos.
"""

# ==========================================
# MOSTRAR EL CUENTO
# ==========================================
with st.expander("📖 Leer el cuento", expanded=False):
    st.markdown(CUENTO)

# ==========================================
# MENSAJE INICIAL
# ==========================================
MENSAJE_INICIAL = (
    "¡Hola! Soy LEO-IA, tu asistente de comprensión lectora. 🦁\n\n"
    "No resolveré las actividades por ti, pero te ayudaré con "
    "preguntas, pistas y explicaciones para que puedas comprender "
    "mejor el cuento «El cuaderno perdido».\n\n"
    "¡Empecemos! ¿Qué te gustaría descubrir de la lectura?"
)

# ==========================================
# HISTORIAL DE CONVERSACIÓN
# ==========================================
if "historial" not in st.session_state:
    st.session_state.historial = [
        {
            "role": "assistant",
            "content": MENSAJE_INICIAL
        }
    ]

# Mostrar mensajes anteriores
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# ==========================================
# RECIBIR PREGUNTAS DEL ESTUDIANTE
# ==========================================
pregunta = st.chat_input(
    "Escribe tu pregunta sobre el cuento..."
)

if pregunta:

    # Guardar pregunta
    st.session_state.historial.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    # ======================================
    # INSTRUCCIONES PARA LEO-IA
    # ======================================
    instruccion = f"""
Eres LEO-IA, un asistente educativo especializado en comprensión
lectora para estudiantes de noveno año de EGB de Ecuador.

Tu misión es ayudar a los estudiantes a comprender una lectura
mediante pistas, preguntas orientadoras y explicaciones sencillas.

REGLAS IMPORTANTES:

1. Basa tus respuestas en el cuento proporcionado.
2. No inventes personajes, acontecimientos ni datos.
3. No entregues inmediatamente la respuesta completa a las
   actividades escolares.
4. Orienta al estudiante con pistas relacionadas con el texto.
5. Haz preguntas que le ayuden a razonar y encontrar la respuesta.
6. Si el estudiante se equivoca, corrígelo amablemente y dale
   otra oportunidad.
7. Si solicita una explicación, explica el fragmento con claridad.
8. Si pregunta por un personaje, ayúdalo a identificar sus
   acciones y características.
9. Si pregunta por la enseñanza del cuento, invítalo a reflexionar.
10. Si la pregunta no se relaciona con el cuento, explícale
    amablemente que hoy trabajarán la comprensión de esta lectura.
11. Responde en español con lenguaje claro, educativo y amable.
12. Evita respuestas demasiado largas.

CUENTO:
{CUENTO}

HISTORIAL DE LA CONVERSACIÓN:
"""

    # Incorporar mensajes previos para mantener el contexto
    for mensaje in st.session_state.historial[-10:-1]:
        rol = (
            "Estudiante"
            if mensaje["role"] == "user"
            else "LEO-IA"
        )
        instruccion += f"\n{rol}: {mensaje['content']}\n"

    instruccion += f"""
Nueva pregunta del estudiante: {pregunta}

Responde al estudiante siguiendo todas las reglas anteriores.
"""

    # ======================================
    # GENERAR RESPUESTA
    # ======================================
    with st.chat_message("assistant"):
        with st.spinner("🦁 LEO-IA está pensando..."):

            try:
                respuesta = cliente.models.generate_content(
                    model=MODELO,
                    contents=instruccion
                )

                texto = respuesta.text

                if not texto:
                    texto = (
                        "No pude preparar una respuesta en este momento. "
                        "Intenta formular tu pregunta de otra manera."
                    )

            except Exception as e:
                st.error("No se pudo obtener la respuesta de Gemini.")
                st.code(str(e))
                st.stop()

        st.markdown(texto)

    # Guardar respuesta en el historial
    st.session_state.historial.append(
        {
            "role": "assistant",
            "content": texto
        }
    )

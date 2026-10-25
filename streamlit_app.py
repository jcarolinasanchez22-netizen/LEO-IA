
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
# CLAVE API
# ==========================================
API_KEY = st.secrets.get("API_KEY", "")

if not API_KEY:
    st.error(
        "No se encuentra la clave API. "
        "Configúrala en Settings → Secrets de Streamlit."
    )
    st.stop()

# ==========================================
# CONEXIÓN CON GEMINI
# ==========================================
try:
    cliente = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("No se pudo inicializar la conexión con Gemini.")
    st.code(str(e))
    st.stop()

# Modelo recomendado por el mensaje de error
MODELO = "gemini-3.8-flash"

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
# MOSTRAR LA LECTURA
# ==========================================
with st.expander("📖 Leer el cuento", expanded=False):
    st.markdown(CUENTO)

# ==========================================
# MENSAJE INICIAL
# ==========================================
MENSAJE_INICIAL = (
    "¡Hola! Soy LEO-IA, tu asistente de comprensión lectora. 🦁\n\n"
    "Te ayudaré a comprender el cuento «El cuaderno perdido» "
    "mediante pistas, preguntas y explicaciones. "
    "Mi objetivo es que aprendas a encontrar las respuestas "
    "por ti mismo.\n\n"
    "¿Qué te gustaría descubrir de la lectura?"
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

# Mostrar la conversación
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# ==========================================
# PREGUNTA DEL ESTUDIANTE
# ==========================================
pregunta = st.chat_input(
    "Escribe tu pregunta sobre el cuento..."
)

if pregunta:

    # Guardar la pregunta
    st.session_state.historial.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    # ======================================
    # PREPARAR INSTRUCCIONES
    # ======================================
    instruccion = f"""
Eres LEO-IA, un asistente educativo de comprensión lectora
para estudiantes de noveno año de EGB de Ecuador.

Tu trabajo es ayudar a los estudiantes a comprender el cuento
mediante pistas, preguntas orientadoras y explicaciones claras.

REGLAS:
1. Responde en español con amabilidad y claridad.
2. Basa tus respuestas en el cuento proporcionado.
3. No inventes información que no aparezca en la lectura.
4. Cuando el estudiante haga una pregunta escolar, ofrece
   una pista antes de revelar la respuesta completa.
5. Formula preguntas orientadoras que lo ayuden a razonar.
6. Si se equivoca, corrígelo respetuosamente.
7. Si pide explicar una parte del cuento, explícasela.
8. Si pregunta por un personaje, orienta al estudiante para
   reconocer sus acciones y características.
9. Si pregunta por la enseñanza, ayúdalo a reflexionar.
10. Si la pregunta no se relaciona con el cuento, invítalo
    a regresar a la lectura.
11. Evita respuestas demasiado largas.
12. No afirmes que un dato está en el cuento si no aparece allí.

CUENTO:
{CUENTO}

CONVERSACIÓN ANTERIOR:
"""

    # Agregar los mensajes anteriores como contexto
    for mensaje in st.session_state.historial[-11:-1]:
        rol = (
            "Estudiante"
            if mensaje["role"] == "user"
            else "LEO-IA"
        )
        instruccion += (
            f"\n{rol}: {mensaje['content']}\n"
        )

    instruccion += f"""
PREGUNTA ACTUAL DEL ESTUDIANTE:
{pregunta}

Ayuda al estudiante a comprender la lectura con una pista
o una pregunta orientadora apropiada.
"""

    # ======================================
    # GENERAR RESPUESTA CON INTERACTIONS API
    # ======================================
    with st.chat_message("assistant"):
        with st.spinner("🦁 LEO-IA está pensando..."):

            try:
                respuesta = cliente.interactions.create(
                    model=MODELO,
                    input=instruccion
                )

                texto = respuesta.output_text

                if not texto:
                    texto = (
                        "No pude preparar una respuesta esta vez. "
                        "Intenta escribir tu pregunta de otra manera."
                    )

            except Exception as e:
                st.error(
                    "No se pudo obtener la respuesta de Gemini. "
                    "Este es el detalle técnico:"
                )
                st.code(str(e))
                st.stop()

        st.markdown(texto)

    # Guardar la respuesta del asistente
    st.session_state.historial.append(
        {
            "role": "assistant",
            "content": texto
        }
    )

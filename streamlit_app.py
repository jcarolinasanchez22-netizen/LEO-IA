
import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(
    page_title="LEO-IA: Comprensión Lectora",
    page_icon="🦁",
    layout="wide"
)

# Obtener la clave API desde Streamlit Secrets
API_KEY = st.secrets.get("API_KEY")

if not API_KEY:
    st.error("⚠️ Falta la clave API. Configúrala en Streamlit Secrets.")
    st.stop()

# Conectar con Gemini
cliente = genai.Client(api_key=API_KEY)

# Modelo de Gemini
MODELO = "gemini-3.8-flash"

# Cuento de lectura
CUENTO = """
El cuaderno perdido

Cada mañana, Mateo caminaba hacia su colegio por un pequeño parque.
Un lunes, mientras avanzaba entre los árboles, encontró algo en el suelo:
un cuaderno de tapa azul oscuro. Al abrirlo, vio que estaba lleno de
dibujos y notas escritas con letra muy bonita.

—¿De quién será? —se preguntó Mateo.

Lo llevó al colegio y preguntó a todos sus compañeros, pero nadie lo
reconoció. Al día siguiente, volvió al parque y esperó. Al rato, vio a
una niña que caminaba mirando el suelo con cara triste. Era Sofía,
una niña de otro curso.

—¿Buscas esto? —le preguntó Mateo mostrando el cuaderno.

—¡Sí, es mío! —dijo ella con alegría—. Tiene todos mis dibujos y las
notas para mi abuela. Muchas gracias.

Mateo sonrió. Sintió una satisfacción inmensa al devolverlo.
Desde ese día, se convirtieron en grandes amigos.
"""

# Título
st.title("🦁 LEO-IA — Asistente de Comprensión Lectora")
st.subheader("Lengua y Literatura • Noveno Año de EGB • Ecuador")
st.divider()

# Mostrar el cuento
with st.expander("📖 Leer el cuento", expanded=False):
    st.markdown(CUENTO)

# Instrucciones iniciales
MENSAJE_INICIAL = (
    "¡Hola! Soy LEO-IA, tu asistente de comprensión lectora. "
    "No resolveré las actividades por ti, pero te acompañaré con "
    "preguntas y pistas. Hoy trabajaremos con el cuento "
    "«El cuaderno perdido». ¿Empezamos?"
)

# Inicializar el historial
if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "assistant", "content": MENSAJE_INICIAL}
    ]

# Mostrar la conversación
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Recibir la pregunta
pregunta = st.chat_input("Escribe tu pregunta aquí...")

if pregunta:
    # Guardar y mostrar la pregunta
    st.session_state.historial.append(
        {"role": "user", "content": pregunta}
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    # Instrucciones pedagógicas para Gemini
    instruccion = f"""
Eres LEO-IA, un asistente educativo especializado en comprensión
lectora para estudiantes de noveno año de EGB de Ecuador.

Tu función es ayudar al estudiante a comprender el cuento mediante
preguntas orientadoras, pistas y explicaciones sencillas.

REGLAS:
1. Basa tus respuestas exclusivamente en el cuento proporcionado.
2. No inventes personajes, acontecimientos ni información.
3. No des inmediatamente la respuesta completa a las actividades.
4. Ofrece pistas que ayuden al estudiante a encontrar la respuesta.
5. Formula preguntas orientadoras cuando sea necesario.
6. Si el estudiante responde incorrectamente, ayúdalo con amabilidad.
7. Si pregunta quién es un personaje, orienta su respuesta usando
   información del cuento.
8. Si pide una explicación, explícale el fragmento relacionado.
9. Utiliza un lenguaje claro, respetuoso y apropiado para su edad.
10. Si la pregunta no tiene relación con el cuento, invítalo a volver
    a la lectura.

CUENTO:
{CUENTO}

PREGUNTA DEL ESTUDIANTE:
{pregunta}

Responde directamente al estudiante con una pista o pregunta
orientadora basada en el cuento.
"""

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("🦁 LEO-IA está leyendo tu pregunta..."):
            try:
                respuesta = cliente.models.generate_content(
                    model=MODELO,
                    contents=instruccion
                )

                texto = respuesta.text

                if not texto:
                    texto = (
                        "No pude generar una respuesta esta vez. "
                        "Intenta escribir tu pregunta de otra manera."
                    )

            except Exception:
                st.error(
                    "No pude conectarme con Gemini. "
                    "Revisa el modelo, la clave API y los registros "
                    "de errores de Streamlit."
                )
                st.stop()

        st.markdown(texto)

    # Guardar la respuesta
    st.session_state.historial.append(
        {"role": "assistant", "content": texto}
    )


# ✅ MODELO CORRECTO
modelo = genai.GenerativeModel("gemini-1.5-flash")

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

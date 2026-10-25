
import os
import streamlit as st
from google import genai
from google.genai import types

# ----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------------
st.set_page_config(
    page_title="LEO-IA | Comprensión Lectora",
    page_icon="🦁",
    layout="centered"
)

st.title("🦁 LEO-IA")
st.subheader("Tu compañero de comprensión lectora")
st.write(
    "Escribe una pregunta sobre una lectura o pega un texto "
    "para que LEO-IA te ayude a comprenderlo."
)

# ----------------------------------------
# CONFIGURACIÓN DE GEMINI
# ----------------------------------------
try:
    API_KEY = st.secrets["API_KEY"]
except Exception:
    API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error(
        "No se encontró la clave API. Configura API_KEY "
        "en Streamlit Cloud → Settings → Secrets."
    )
    st.stop()

MODELO = "gemini-3.8-flash"

try:
    cliente = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(timeout=30000)
    )
except Exception as error:
    st.error("No se pudo iniciar la conexión con Gemini.")
    st.code(str(error))
    st.stop()

# ----------------------------------------
# INTERFAZ PARA EL USUARIO
# ----------------------------------------
texto = st.text_area(
    "📖 Escribe tu lectura o pregunta:",
    height=200,
    placeholder=(
        "Ejemplo: Lee este cuento y dime quiénes son "
        "los personajes principales..."
    )
)

nivel = st.selectbox(
    "🎓 ¿Para qué nivel educativo necesitas la explicación?",
    [
        "Educación básica elemental",
        "Educación básica media",
        "Educación básica superior",
        "Bachillerato"
    ]
)

# ----------------------------------------
# GENERACIÓN DE RESPUESTAS
# ----------------------------------------
if st.button("✨ Consultar a LEO-IA", type="primary"):
    if not texto.strip():
        st.warning("Por favor, escribe una lectura o una pregunta.")
    else:
        instruccion = f"""
Eres LEO-IA, un asistente educativo especializado en comprensión lectora.

Tu objetivo es ayudar a estudiantes de: {nivel}.

Responde en español, con lenguaje claro, amable y adecuado para la edad.
Si el usuario comparte una lectura:
1. Identifica la idea principal.
2. Resume el texto cuando sea útil.
3. Explica palabras difíciles de forma sencilla.
4. Responde las preguntas basándote en el texto.
5. Si el usuario lo solicita, crea preguntas de comprensión lectora
   y proporciona sus respuestas.
6. No inventes información que no aparezca en la lectura.
7. Si falta información, explícalo con amabilidad.

Pregunta o lectura del estudiante:
{texto}
"""

        try:
            with st.spinner("🦁 LEO-IA está pensando..."):
                respuesta = cliente.interactions.create(
                    model=MODELO,
                    input=instruccion
                )

            resultado = getattr(respuesta, "output_text", None)

            if resultado and resultado.strip():
                st.success("¡LEO-IA tiene una respuesta!")
                st.markdown("### 💡 Respuesta")
                st.write(resultado)
            else:
                st.warning(
                    "Gemini respondió, pero no devolvió texto. "
                    "Intenta nuevamente."
                )
                with st.expander("Detalles técnicos"):
                    st.write(respuesta)

        except Exception as error:
            st.error(
                "No se pudo obtener una respuesta de Gemini. "
                "Espera unos segundos e inténtalo otra vez."
            )
            st.info(
                "La conexión tiene un tiempo máximo de espera de "
                "30 segundos. Si el error continúa, revisa el modelo "
                "configurado y los registros de la aplicación."
            )
            with st.expander("Ver detalles del error"):
                st.code(str(error))

# ----------------------------------------
# PIE DE PÁGINA
# ----------------------------------------
st.divider()
st.caption("🦁 LEO-IA | Aprender a leer, comprender y pensar.")

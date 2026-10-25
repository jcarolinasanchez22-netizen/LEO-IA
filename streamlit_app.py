
import os
import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================
st.set_page_config(
    page_title="LEO-IA | Comprensión Lectora",
    page_icon="🦁",
    layout="centered"
)

st.title("🦁 LEO-IA")
st.subheader("Tu compañero de comprensión lectora")
st.write(
    "Escribe una pregunta o comparte una lectura "
    "para recibir ayuda y comprender mejor los textos."
)

# ==========================================
# CONEXIÓN CON GEMINI
# ==========================================
try:
    API_KEY = st.secrets.get("API_KEY", os.getenv("API_KEY"))
except Exception:
    API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error(
        "No se encontró la clave API. Revisa "
        "Settings → Secrets en Streamlit Cloud."
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
    with st.expander("Ver detalles del error"):
        st.code(str(error))
    st.stop()

# ==========================================
# INTERFAZ DEL ESTUDIANTE
# ==========================================
texto = st.text_area(
    "📖 Escribe tu lectura o pregunta:",
    height=200,
    placeholder=(
        "Ejemplo: ¿Qué es la comprensión lectora? "
        "Explícamela con palabras sencillas."
    )
)

nivel = st.selectbox(
    "🎓 Selecciona el nivel educativo:",
    [
        "Educación básica elemental",
        "Educación básica media",
        "Educación básica superior",
        "Bachillerato"
    ]
)

# ==========================================
# BOTÓN PARA CONSULTAR
# ==========================================
if st.button("✨ Consultar a LEO-IA", type="primary"):
    if not texto.strip():
        st.warning("Primero escribe una pregunta o una lectura.")
    else:
        instruccion = f"""
Eres LEO-IA, un asistente educativo especializado
en comprensión lectora.

Nivel educativo del estudiante: {nivel}

Instrucciones:
- Responde siempre en español.
- Utiliza un lenguaje claro, amable y adecuado para el nivel.
- Explica las ideas paso a paso cuando sea necesario.
- Si recibes una lectura, identifica su idea principal.
- Responde las preguntas usando la información del texto.
- No inventes información que no aparezca en la lectura.
- Si te piden preguntas de comprensión, crea preguntas claras
  y proporciona sus respuestas cuando te lo soliciten.

Pregunta o lectura del estudiante:
{texto}
"""

        try:
            with st.spinner("🦁 LEO-IA está pensando..."):
                respuesta = cliente.models.generate_content(
                    model=MODELO,
                    contents=instruccion
                )

            resultado = respuesta.text

            if resultado and resultado.strip():
                st.success("¡LEO-IA ha respondido!")
                st.markdown("### 💡 Respuesta de LEO-IA")
                st.markdown(resultado)
            else:
                st.warning(
                    "Gemini no devolvió texto. "
                    "Intenta nuevamente."
                )
                with st.expander("Ver detalles"):
                    st.write(respuesta)

        except Exception as error:
            st.error(
                "No se pudo obtener una respuesta de Gemini."
            )
            st.warning(
                "Revisa los detalles del error que aparecen abajo. "
                "Estos nos ayudarán a identificar el problema."
            )
            with st.expander("🔎 Ver detalles del error"):
                st.code(str(error))

# ==========================================
# PIE DE PÁGINA
# ==========================================
st.divider()
st.caption(
    "🦁 LEO-IA | Aprender a leer, comprender y pensar."
)


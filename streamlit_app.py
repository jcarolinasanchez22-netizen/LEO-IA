
import os
import time
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
# CONFIGURACIÓN DE GEMINI
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
# FUNCIÓN PARA CONSULTAR CON REINTENTOS
# ==========================================
def consultar_gemini(instruccion, max_intentos=3):
    ultimo_error = None

    for intento in range(max_intentos):
        try:
            respuesta = cliente.models.generate_content(
                model=MODELO,
                contents=instruccion
            )

            resultado = respuesta.text

            if resultado and resultado.strip():
                return resultado

            raise ValueError(
                "Gemini respondió, pero no devolvió texto."
            )

        except Exception as error:
            ultimo_error = error
            mensaje_error = str(error).upper()

            error_temporal = any(
                codigo in mensaje_error
                for codigo in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "502",
                    "504",
                    "INTERNAL",
                    "TIMEOUT"
                ]
            )

            # No repetir si el error no parece temporal
            if not error_temporal:
                raise

            # No esperar después del último intento
            if intento < max_intentos - 1:
                espera = 2 ** (intento + 1)
                time.sleep(espera)

    raise ultimo_error


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
- Utiliza lenguaje claro, amable y apropiado para el nivel.
- Explica las ideas paso a paso cuando sea necesario.
- Si recibes una lectura, identifica su idea principal.
- Responde usando la información proporcionada.
- No inventes información que no aparezca en la lectura.
- Si te solicitan preguntas de comprensión, crea preguntas
  claras y responde basándote en el texto.

Pregunta o lectura del estudiante:
{texto}
"""

        try:
            with st.spinner(
                "🦁 LEO-IA está intentando conectar con Gemini..."
            ):
                resultado = consultar_gemini(
                    instruccion,
                    max_intentos=3
                )

            st.success("¡LEO-IA ha respondido!")
            st.markdown("### 💡 Respuesta de LEO-IA")
            st.markdown(resultado)

        except Exception as error:
            mensaje = str(error).upper()

            if (
                "503" in mensaje
                or "UNAVAILABLE" in mensaje
                or "429" in mensaje
                or "RESOURCE_EXHAUSTED" in mensaje
                or "500" in mensaje
                or "502" in mensaje
                or "504" in mensaje
            ):
                st.error(
                    "Gemini sigue ocupado o no está disponible "
                    "después de varios intentos."
                )
                st.info(
                    "Espera unos minutos y vuelve a intentarlo. "
                    "Los reintentos no pueden solucionar una "
                    "interrupción del servicio."
                )
            else:
                st.error("No se pudo obtener una respuesta de Gemini.")
                st.info(
                    "Consulta los detalles del error para identificar "
                    "la causa."
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

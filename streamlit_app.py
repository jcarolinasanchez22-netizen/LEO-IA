
import os
import time
import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    page_title="LEO-IA | El cuaderno perdido",
    page_icon="🦁",
    layout="centered"
)

st.title("🦁 LEO-IA")
st.subheader("Comprensión lectora")
st.write("Lee el cuento y responde las preguntas con ayuda de LEO-IA.")

# ==========================================
# LECTURA
# ==========================================
lectura = """
EL CUADERNO PERDIDO

Una mañana, Mateo caminaba hacia el colegio por un parque.
Mientras caminaba, encontró un cuaderno azul que tenía dibujos
y algunas notas en sus páginas.

Mateo pensó que alguien debía haberlo perdido y quiso encontrar
a su dueño. Por eso, decidió esperar en el parque para ver si
alguien regresaba a buscarlo.

Después de un rato, apareció una niña llamada Sofía. Ella estaba
triste porque había perdido su cuaderno. Mateo le preguntó si
el cuaderno azul era suyo y se lo mostró.

Sofía se puso muy contenta al recuperarlo. Le explicó a Mateo
que en el cuaderno tenía dibujos y notas que había preparado
para su abuela.

Sofía agradeció a Mateo por su honestidad y por ayudarla.
Desde ese día, los dos se hicieron amigos.

La historia nos enseña que debemos ser honestos, ayudar a los
demás y devolver las cosas que no nos pertenecen.
"""

with st.expander("📖 Leer el cuento: El cuaderno perdido", expanded=True):
    st.markdown(lectura)

# ==========================================
# PREGUNTAS PARA PRACTICAR
# ==========================================
st.markdown("### ✏️ Preguntas de comprensión")

preguntas = [
    "¿Quién es Mateo?",
    "¿Qué encontró Mateo en el parque?",
    "¿Por qué Sofía estaba triste?",
    "¿Qué hizo Mateo para ayudar a Sofía?",
    "¿Qué tenía Sofía en el cuaderno?",
    "¿Qué enseñanza nos deja el cuento?"
]

for i, pregunta in enumerate(preguntas, start=1):
    st.write(f"**{i}. {pregunta}**")

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
    with st.expander("Detalles del error"):
        st.code(str(error))
    st.stop()

# ==========================================
# PREGUNTA DEL ESTUDIANTE
# ==========================================
st.divider()
st.markdown("### 💬 Pregúntale a LEO-IA")

pregunta_usuario = st.text_area(
    "Escribe tu pregunta sobre el cuento:",
    placeholder="Ejemplo: ¿Qué encontró Mateo en el parque?",
    height=100
)

nivel = st.selectbox(
    "🎓 Selecciona tu nivel educativo:",
    [
        "Educación básica elemental",
        "Educación básica media",
        "Educación básica superior",
        "Bachillerato"
    ]
)

# ==========================================
# CONSULTAR A LEO-IA
# ==========================================
if st.button("✨ Consultar a LEO-IA", type="primary"):

    if not pregunta_usuario.strip():
        st.warning("Escribe una pregunta sobre el cuento.")

    else:
        instruccion = f"""
Eres LEO-IA, un tutor educativo de comprensión lectora.

Debes responder las preguntas de los estudiantes utilizando
EXCLUSIVAMENTE la lectura que aparece a continuación.

LECTURA:
{lectura}

REGLAS IMPORTANTES:
1. Responde siempre en español.
2. Usa palabras sencillas apropiadas para este nivel: {nivel}.
3. Basa tus respuestas únicamente en la lectura.
4. No inventes personajes, acontecimientos ni detalles.
5. Si la respuesta no aparece en el cuento, explica amablemente
   que la lectura no proporciona esa información.
6. Si el estudiante pide un resumen, resume solo los hechos del cuento.
7. Si pide la enseñanza, explica la honestidad, la ayuda a los demás
   y la importancia de devolver lo que no nos pertenece.
8. Ayuda al estudiante a comprender, no te limites a dar respuestas
   cuando necesite una explicación.

PREGUNTA DEL ESTUDIANTE:
{pregunta_usuario}
"""

        resultado = None
        ultimo_error = None

        for intento in range(3):
            try:
                with st.spinner(
                    f"🦁 LEO-IA está pensando... "
                    f"(intento {intento + 1} de 3)"
                ):
                    respuesta = cliente.models.generate_content(
                        model=MODELO,
                        contents=instruccion
                    )

                resultado = respuesta.text

                if resultado and resultado.strip():
                    break

                ultimo_error = Exception(
                    "Gemini no devolvió una respuesta escrita."
                )

            except Exception as error:
                ultimo_error = error
                detalle = str(error).upper()

                temporal = any(
                    codigo in detalle
                    for codigo in [
                        "503",
                        "UNAVAILABLE",
                        "429",
                        "RESOURCE_EXHAUSTED",
                        "500",
                        "502",
                        "504",
                        "TIMEOUT"
                    ]
                )

                if not temporal:
                    break

                if intento < 2:
                    time.sleep(2 ** (intento + 1))

        if resultado and resultado.strip():
            st.success("¡LEO-IA tiene una respuesta!")
            st.markdown("### 💡 Respuesta")
            st.write(resultado)

        else:
            st.error(
                "En este momento no se pudo generar la respuesta."
            )
            st.info(
                "Puedes intentarlo nuevamente en unos minutos. "
                "Si Gemini continúa ocupado, revisa el detalle del error."
            )

            if ultimo_error:
                with st.expander("🔎 Ver detalles del error"):
                    st.code(str(ultimo_error))

# ==========================================
# PIE DE PÁGINA
# ==========================================
st.divider()
st.caption("🦁 LEO-IA | Leer, comprender y aprender.")

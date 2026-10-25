
import streamlit as st
import unicodedata
import re

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    page_title="LEO-IA | Comprensión lectora",
    page_icon="🦁",
    layout="centered"
)

st.title("🦁 LEO-IA")
st.subheader("¡Aprendamos a comprender leyendo!")
st.write(
    "Lee la historia de Mateo y responde las preguntas. "
    "LEO-IA te ayudará a comprobar lo que comprendiste."
)

# ==========================================
# HISTORIA
# ==========================================
lectura = """
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

with st.expander("📖 Leer la historia: El cuaderno perdido", expanded=True):
    st.markdown(lectura)

# ==========================================
# BANCO DE PREGUNTAS Y RESPUESTAS
# ==========================================
preguntas = {
    "¿Quién es el personaje principal de la historia?": {
        "opciones": ["Mateo", "Sofía", "La abuela"],
        "correcta": "Mateo",
        "explicacion": "Mateo encuentra el cuaderno y ayuda a su dueña."
    },
    "¿Qué encontró Mateo en el parque?": {
        "opciones": ["Una mochila roja", "Un cuaderno azul", "Un libro verde"],
        "correcta": "Un cuaderno azul",
        "explicacion": "El cuento dice que Mateo encontró un cuaderno azul con dibujos y notas."
    },
    "¿Por qué estaba triste Sofía?": {
        "opciones": [
            "Porque llegó tarde al colegio",
            "Porque perdió su cuaderno",
            "Porque discutió con Mateo"
        ],
        "correcta": "Porque perdió su cuaderno",
        "explicacion": "Sofía estaba triste porque había perdido su cuaderno."
    },
    "¿Qué hizo Mateo para ayudar?": {
        "opciones": [
            "Se quedó esperando a su dueño",
            "Se llevó el cuaderno a su casa",
            "Escondió el cuaderno"
        ],
        "correcta": "Se quedó esperando a su dueño",
        "explicacion": "Mateo esperó en el parque para encontrar a la persona que lo había perdido."
    },
    "¿Qué tenía Sofía en el cuaderno?": {
        "opciones": [
            "Dibujos y notas para su abuela",
            "Juguetes y fotografías",
            "Una lista de compras"
        ],
        "correcta": "Dibujos y notas para su abuela",
        "explicacion": "Sofía había preparado dibujos y notas para su abuela."
    },
    "¿Qué ocurrió cuando Sofía recuperó el cuaderno?": {
        "opciones": [
            "Se puso muy contenta",
            "Se fue sin decir nada",
            "Regaló el cuaderno a Mateo"
        ],
        "correcta": "Se puso muy contenta",
        "explicacion": "Sofía se alegró al recuperar su cuaderno y agradeció a Mateo."
    },
    "¿Qué enseñanza nos deja la historia?": {
        "opciones": [
            "Debemos quedarnos con lo que encontramos",
            "Debemos ser honestos y ayudar a los demás",
            "No debemos hablar con otras personas"
        ],
        "correcta": "Debemos ser honestos y ayudar a los demás",
        "explicacion": "La historia enseña la importancia de la honestidad y de devolver lo ajeno."
    }
}

# ==========================================
# FUNCIONES
# ==========================================
def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caracter for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )
    texto = re.sub(r"[^\w\s]", "", texto)
    return texto

# ==========================================
# ACTIVIDAD INTERACTIVA
# ==========================================
st.divider()
st.header("✏️ Comprueba lo que comprendiste")
st.write("Selecciona una respuesta para cada pregunta.")

respuestas_usuario = {}

for numero, (pregunta, datos) in enumerate(preguntas.items(), start=1):
    st.markdown(f"**{numero}. {pregunta}**")
    respuestas_usuario[pregunta] = st.radio(
        "Elige tu respuesta:",
        datos["opciones"],
        index=None,
        key=f"pregunta_{numero}",
        label_visibility="collapsed"
    )

if st.button("✅ Revisar mis respuestas", type="primary"):
    sin_responder = [
        pregunta for pregunta, respuesta in respuestas_usuario.items()
        if respuesta is None
    ]

    if sin_responder:
        st.warning(
            f"Te faltan {len(sin_responder)} pregunta(s). "
            "Responde todas antes de revisar."
        )
    else:
        puntaje = 0
        st.header("📋 Tus resultados")

        for numero, (pregunta, datos) in enumerate(preguntas.items(), start=1):
            respuesta = respuestas_usuario[pregunta]

            if respuesta == datos["correcta"]:
                puntaje += 1
                st.success(f"{numero}. ¡Correcto! {datos['explicacion']}")
            else:
                st.error(
                    f"{numero}. La respuesta correcta es: "
                    f"{datos['correcta']}."
                )
                st.write(datos["explicacion"])

        porcentaje = round(puntaje / len(preguntas) * 100)

        st.divider()
        st.subheader(f"🏆 Resultado: {puntaje} de {len(preguntas)}")
        st.progress(porcentaje / 100)
        st.write(f"Obtuviste el {porcentaje}% de respuestas correctas.")

        if puntaje == len(preguntas):
            st.balloons()
            st.success("¡Excelente! Comprendiste muy bien la historia.")
        elif puntaje >= 5:
            st.info("¡Muy bien! Lee nuevamente la historia para mejorar.")
        else:
            st.info(
                "¡Sigue practicando! Puedes volver a leer la historia "
                "y responder otra vez."
            )

# ==========================================
# CONSULTA SENCILLA SIN IA
# ==========================================
st.divider()
st.header("💬 Pregúntale a LEO-IA")
st.write(
    "Escribe una pregunta sobre la historia. "
    "LEO-IA buscará una respuesta preparada basada en el cuento."
)

pregunta_libre = st.text_input(
    "Tu pregunta:",
    placeholder="Ejemplo: ¿Qué encontró Mateo?"
)

if st.button("🔎 Buscar respuesta"):
    if not pregunta_libre.strip():
        st.warning("Primero escribe una pregunta.")
    else:
        consulta = normalizar(pregunta_libre)

        respuestas_conocidas = [
            (
                ["quien es mateo", "personaje principal", "protagonista"],
                "Mateo es el personaje principal. Él encontró el cuaderno azul y ayudó a Sofía."
            ),
            (
                ["que encontro mateo", "encontro en el parque", "que encontro"],
                "Mateo encontró un cuaderno azul con dibujos y algunas notas."
            ),
            (
                ["quien perdio el cuaderno", "de quien era el cuaderno", "quien era la duena"],
                "El cuaderno pertenecía a Sofía."
            ),
            (
                ["por que estaba triste sofia", "por que sofia estaba triste", "que le paso a sofia"],
                "Sofía estaba triste porque había perdido su cuaderno."
            ),
            (
                ["que hizo mateo", "como ayudo mateo", "como ayudo a sofia"],
                "Mateo esperó para encontrar al dueño y le mostró el cuaderno a Sofía cuando ella apareció."
            ),
            (
                ["que tenia el cuaderno", "que habia en el cuaderno", "que tenia sofia"],
                "El cuaderno tenía dibujos y notas que Sofía había preparado para su abuela."
            ),
            (
                ["que paso al final", "como termina", "final de la historia"],
                "Sofía recuperó su cuaderno, agradeció a Mateo y los dos se hicieron amigos."
            ),
            (
                ["ensenanza", "moraleja", "que aprendemos", "que nos ensena"],
                "La historia nos enseña a ser honestos, ayudar a los demás y devolver las cosas que no nos pertenecen."
            ),
            (
                ["donde encontro mateo", "en que lugar", "donde estaba mateo"],
                "Mateo encontró el cuaderno mientras caminaba por un parque hacia el colegio."
            ),
            (
                ["como se llamaba la nina", "nombre de la nina", "quien era sofia"],
                "La niña se llamaba Sofía. Ella había perdido el cuaderno azul."
            ),
            (
                ["para quien eran los dibujos", "para quien eran las notas", "abuela"],
                "Los dibujos y las notas eran para la abuela de Sofía."
            ),
            (
                ["por que debemos ser honestos", "que significa ser honesto"],
                "En esta historia, ser honesto significa ayudar a devolver el cuaderno a su dueña en lugar de quedárselo."
            )
        ]

        respuesta_encontrada = None

        for palabras_clave, respuesta in respuestas_conocidas:
            if any(normalizar(clave) in consulta for clave in palabras_clave):
                respuesta_encontrada = respuesta
                break

        if respuesta_encontrada:
            st.success("🦁 LEO-IA responde:")
            st.write(respuesta_encontrada)
        else:
            st.info(
                "No tengo una respuesta preparada para esa pregunta. "
                "Prueba preguntando qué encontró Mateo, por qué estaba "
                "triste Sofía o cuál es la enseñanza de la historia."
            )

# ==========================================
# PIE DE PÁGINA
# ==========================================
st.divider()
st.caption("🦁 LEO-IA | Leer, comprender y aprender.")
st.caption("Versión educativa sin conexión a servicios de inteligencia artificial.")


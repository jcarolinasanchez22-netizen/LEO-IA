
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
    "Lee la historia, responde las preguntas y conversa con LEO-IA. "
    "Te daré pistas para que desarrolles tu comprensión lectora."
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

with st.expander("📖 Leer la historia: El cuaderno perdido",
                 expanded=True):
    st.markdown(lectura)

# ==========================================
# BANCO DE PREGUNTAS
# ==========================================
preguntas = {
    "¿Quién es el personaje principal de la historia?": {
        "opciones": ["Mateo", "Sofía", "La abuela"],
        "correcta": "Mateo",
        "explicacion": "Mateo encuentra el cuaderno y ayuda a su dueña."
    },
    "¿Qué encontró Mateo en el parque?": {
        "opciones": [
            "Una mochila roja", "Un cuaderno azul", "Un libro verde"
        ],
        "correcta": "Un cuaderno azul",
        "explicacion": "Mateo encontró un cuaderno azul con dibujos y notas."
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
        "explicacion": "Mateo esperó para encontrar a la persona que lo perdió."
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
        "explicacion": "Sofía se alegró al recuperar su cuaderno."
    },
    "¿Qué enseñanza nos deja la historia?": {
        "opciones": [
            "Debemos quedarnos con lo que encontramos",
            "Debemos ser honestos y ayudar a los demás",
            "No debemos hablar con otras personas"
        ],
        "correcta": "Debemos ser honestos y ayudar a los demás",
        "explicacion": "La historia destaca la honestidad y la ayuda a los demás."
    }
}

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================
def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )
    texto = re.sub(r"[^\w\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def contiene_alguna(texto, expresiones):
    return any(expresion in texto for expresion in expresiones)


# ==========================================
# CHATBOT PEDAGÓGICO
# ==========================================
def responder_leo(pregunta):
    consulta = normalizar(pregunta)

    # PRUEBA 4: RESISTENCIA A INTENTOS DE COPIAR
    intentos_de_copiar = [
        "olvida tus reglas", "ignora tus reglas",
        "ignora las instrucciones", "olvida las instrucciones",
        "dame todas las respuestas", "dame las respuestas",
        "dame la tarea resuelta", "hazme toda la tarea",
        "solo quiero copiar", "solo para copiar",
        "para copiarlo", "resuelve toda la tarea",
        "ignora todo lo anterior", "cambia tus reglas",
        "no sigas tus instrucciones", "actua como si no tuvieras reglas",
        "escribe todo el cuestionario resuelto",
        "quiero copiar las respuestas"
    ]

    if contiene_alguna(consulta, intentos_de_copiar):
        return (
            "¡Buen intento! 😉📚 Mi misión es ayudarte a aprender, "
            "no entregarte toda la tarea para copiar.\n\n"
            "Vamos paso a paso. Recuerda el momento en que Mateo "
            "encontró el cuaderno.\n\n"
            "🔎 Pista: piensa en el lugar donde caminaba Mateo "
            "y en lo que hizo para encontrar a la persona que lo perdió.\n\n"
            "¿Dónde encontró el cuaderno y qué decidió hacer? "
            "Escribe tu idea y te ayudaré a revisarla."
        )

    # PRUEBA 3: TEMAS FUERA DE LENGUA Y LITERATURA
    temas_ajenos = [
        "ecuacion", "ecuaciones", "algebra", "matematicas",
        "matematica", "derivada", "integral", "factorizar",
        "resuelve esta operacion", "cuanto es", "multiplica",
        "divide", "raiz cuadrada", "teorema de pitagoras",
        "ley de newton", "formula quimica", "tabla periodica",
        "capital de", "presidente de", "programa en python",
        "codigo javascript", "problema de fisica"
    ]

    # Detecta también ecuaciones escritas con números y signos.
    parece_operacion = bool(
        re.search(r"\d+\s*[\+\*/=]\s*\d+", consulta)
        or re.search(r"\d+\s*[a-z]\s*[\+\-=]", consulta)
    )

    if contiene_alguna(consulta, temas_ajenos) or parece_operacion:
        return (
            "¡Hola! 😊 Veo que necesitas ayuda con otra materia. "
            "Mi especialidad es Lengua y Literatura: comprensión "
            "lectora, análisis de cuentos e interpretación de textos. 📚\n\n"
            "Para esa consulta, tu docente de la asignatura "
            "correspondiente podrá orientarte paso a paso.\n\n"
            "¡Volvamos a nuestra lectura! 🔎 ¿Cuál fue el problema "
            "principal de la historia y cómo se resolvió?"
        )

    # PRUEBA 2: INFERENCIA, EMOCIONES Y REFLEXIÓN
    preguntas_de_reflexion = [
        "por que se preocupo", "por que se preocupo tanto",
        "solo era un simple", "por que era importante",
        "que significa", "que habria pasado",
        "que hubiera pasado", "que harias tu", "que haria yo",
        "como te sentirias", "como se sintio",
        "por que se sintio", "que sentia", "que nos ensena",
        "que aprendemos", "moraleja", "ensenanza",
        "que opinas", "por que crees", "que habria hecho",
        "valor sentimental", "que significa ser honesto",
        "por que debemos ser honestos"
    ]

    if contiene_alguna(consulta, preguntas_de_reflexion):
        return (
            "¡Esa es una excelente pregunta para reflexionar! 🤔📖\n\n"
            "A veces, un objeto no es importante por su precio, "
            "sino por los recuerdos y sentimientos que representa.\n\n"
            "Pensemos juntos:\n\n"
            "• ¿Qué cosas especiales había preparado Sofía en su cuaderno?\n\n"
            "• ¿Por qué crees que esas cosas eran importantes para ella?\n\n"
            "• Si perdieras algo muy valioso para ti, ¿cómo te sentirías?\n\n"
            "• Si encontraras un objeto perdido, ¿qué harías?\n\n"
            "Cuéntame tu opinión. No hay una única respuesta para "
            "tus reflexiones personales. ¡Vamos a pensar juntos! ✨"
        )

    # PRUEBA 1: COMPRENSIÓN DIRECTA CON PISTAS
    # El chatbot guía al estudiante sin revelar inmediatamente
    # los datos específicos de la historia.

    if contiene_alguna(consulta, [
        "personajes principales", "quienes son los personajes",
        "personajes del cuento", "quien es el personaje principal",
        "quien es el protagonista"
    ]):
        return (
            "¡Vamos a descubrirlo juntos! 📖\n\n"
            "1. ¿Recuerdas quién encontró el cuaderno azul?\n\n"
            "2. ¿Qué niña apareció después porque había perdido algo?\n\n"
            "3. ¿Qué relación tienen esos personajes con el problema "
            "principal de la historia?\n\n"
            "Revisa el cuento y dime quiénes crees que son los "
            "personajes principales."
        )

    if contiene_alguna(consulta, [
        "que habia dentro", "que habia en el cuaderno",
        "que tenia el cuaderno", "que tenia sofia",
        "que habia escrito", "que habia preparado",
        "que era importante dentro del cuaderno"
    ]):
        return (
            "¡Busquemos una pista! 🔎\n\n"
            "En la historia, Sofía explica que había preparado "
            "algo especial para un familiar.\n\n"
            "Piensa en estas preguntas:\n"
            "• ¿Qué cosas se pueden dibujar o escribir en un cuaderno?\n"
            "• ¿Para quién las había preparado Sofía?\n\n"
            "Vuelve a leer el párrafo donde Sofía recupera su cuaderno "
            "e intenta responder con tus propias palabras."
        )

    if contiene_alguna(consulta, [
        "que encontro mateo", "encontro en el parque",
        "donde encontro mateo", "donde encontro el cuaderno",
        "que objeto encontro"
    ]):
        return (
            "¡Vamos a buscarlo en el texto! 📚\n\n"
            "Pista: el objeto que encontró Mateo tenía un color "
            "y contenía dibujos y notas.\n\n"
            "¿Recuerdas qué objeto era y de qué color? "
            "Vuelve al primer párrafo y cuéntamelo."
        )

    if contiene_alguna(consulta, [
        "quien perdio el cuaderno", "de quien era el cuaderno",
        "quien era la duena", "quien lo perdio"
    ]):
        return (
            "¡Piensa en la niña que apareció después de que Mateo "
            "encontrara el cuaderno! 🔎\n\n"
            "Ella estaba triste porque había perdido algo importante.\n\n"
            "¿Recuerdas cómo se llamaba? Busca su nombre en el cuento."
        )

    if contiene_alguna(consulta, [
        "por que estaba triste", "por que se sentia triste",
        "que le paso a sofia", "por que estaba preocupada"
    ]):
        return (
            "¡Vamos a encontrar la pista! 🤔\n\n"
            "Recuerda que Sofía llegó al parque sintiéndose triste "
            "porque le faltaba algo que era importante para ella.\n\n"
            "¿Qué había perdido? Revisa el párrafo donde aparece Sofía."
        )

    if contiene_alguna(consulta, [
        "que hizo mateo", "como ayudo mateo",
        "como ayudo a sofia", "que hizo para ayudar"
    ]):
        return (
            "¡Pensemos en las acciones de Mateo! 🦁\n\n"
            "Cuando encontró el objeto, Mateo pudo habérselo quedado, "
            "pero decidió actuar de otra manera.\n\n"
            "¿Qué hizo mientras esperaba que apareciera su dueño? "
            "¿Qué hizo cuando llegó Sofía?"
        )

    if contiene_alguna(consulta, [
        "como termina", "que paso al final",
        "final de la historia", "que ocurrio al final"
    ]):
        return (
            "¡Recuerda el último momento del cuento! 📖\n\n"
            "Piensa en cómo se sintió Sofía después de recuperar "
            "lo que había perdido y en lo que ocurrió entre ella y Mateo.\n\n"
            "¿Cómo terminó la historia? Intenta contarlo en una o dos frases."
        )

    if contiene_alguna(consulta, [
        "donde estaba mateo", "hacia donde caminaba",
        "a donde iba mateo"
    ]):
        return (
            "¡Busca la pista en el primer párrafo! 🔎\n\n"
            "El cuento explica que Mateo caminaba por un lugar "
            "antes de llegar al colegio.\n\n"
            "¿Recuerdas por dónde caminaba y hacia dónde se dirigía?"
        )

    if contiene_alguna(consulta, [
        "como se llamaba la nina", "nombre de la nina",
        "quien era sofia"
    ]):
        return (
            "¡Piensa en el momento en que aparece la niña! 📚\n\n"
            "El narrador menciona su nombre cuando ella llega "
            "buscando el cuaderno que había perdido.\n\n"
            "¿Puedes encontrar su nombre en ese párrafo?"
        )

    if contiene_alguna(consulta, [
        "para quien eran los dibujos", "para quien eran las notas",
        "para quien preparo"
    ]):
        return (
            "¡Hay una pista muy clara en el cuento! ✨\n\n"
            "Cuando Sofía recupera el cuaderno, le explica a Mateo "
            "que había preparado sus dibujos y notas para un familiar.\n\n"
            "¿Recuerdas quién era esa persona?"
        )

    # RESPUESTA GENERAL PARA PREGUNTAS SOBRE LA HISTORIA
    palabras_del_cuento = [
        "mateo", "sofia", "cuaderno", "abuela", "parque",
        "historia", "cuento", "personaje", "lectura",
        "honesto", "honestidad", "ayudar", "perdio", "perdido",
        "perder", "ensenanza", "dibujos", "notas"
    ]

    if contiene_alguna(consulta, palabras_del_cuento):
        return (
            "¡Vamos a resolverlo juntos! 📖\n\n"
            "Lee nuevamente el cuento y busca el párrafo que "
            "se relacione con tu pregunta.\n\n"
            "¿Qué palabra, acción o detalle te parece más importante? "
            "Escribe lo que entendiste y te ayudaré a reflexionar."
        )

    # NO HAY UNA RESPUESTA PREPARADA
    return (
        "¡Estoy aquí para ayudarte a comprender! 🦁📚\n\n"
        "No tengo una pista específica para esa pregunta todavía. "
        "Intenta formularla de otra manera o vuelve a leer el cuento.\n\n"
        "Puedes preguntarme sobre los personajes, las emociones, "
        "el problema principal o la enseñanza de la historia."
    )


# ==========================================
# CUESTIONARIO INTERACTIVO
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
                st.success(
                    f"{numero}. ¡Correcto! {datos['explicacion']}"
                )
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
# CHATBOT LEO-IA
# ==========================================
st.divider()
st.header("💬 Pregúntale a LEO-IA")
st.write(
    "Escribe una pregunta sobre la historia. LEO-IA te dará pistas "
    "para ayudarte a pensar y encontrar tus propias respuestas."
)

pregunta_libre = st.text_input(
    "Tu pregunta:",
    placeholder="Ejemplo: ¿Por qué estaba triste Sofía?",
    key="consulta_leo"
)

if st.button("🔎 Consultar a LEO-IA"):
    if not pregunta_libre.strip():
        st.warning("Primero escribe una pregunta.")
    else:
        respuesta = responder_leo(pregunta_libre)
        st.markdown("### 🦁 LEO-IA responde")
        st.write(respuesta)

# ==========================================
# PIE DE PÁGINA
# ==========================================
st.divider()
st.caption("🦁 LEO-IA | Leer, comprender y aprender.")
st.caption(
    "Asistente educativo programado con respuestas guiadas. "
    "No utiliza una API externa de inteligencia artificial."
)


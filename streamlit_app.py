
import streamlit as st
import unicodedata
import re

# ==================================================
# 1. CONFIGURACIÓN DE LA APLICACIÓN
# ==================================================
st.set_page_config(
    page_title="LEO-IA | Comprensión lectora",
    page_icon="🦁",
    layout="centered"
)

st.title("🦁 LEO-IA")
st.subheader("¡Aprendamos a comprender leyendo!")
st.write(
    "Soy LEO-IA, tu asistente de Lengua y Literatura. "
    "Te ayudaré a comprender historias, descubrir pistas "
    "y desarrollar tu pensamiento crítico."
)

# ==================================================
# 2. HISTORIA
# ==================================================
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

# ==================================================
# 3. BANCO DE PREGUNTAS
# ==================================================
preguntas = {
    "¿Quién es el personaje principal de la historia?": {
        "opciones": ["Mateo", "Sofía", "La abuela"],
        "correcta": "Mateo",
        "explicacion":
            "Mateo encuentra el cuaderno y ayuda a su dueña."
    },
    "¿Qué encontró Mateo en el parque?": {
        "opciones": [
            "Una mochila roja",
            "Un cuaderno azul",
            "Un libro verde"
        ],
        "correcta": "Un cuaderno azul",
        "explicacion":
            "Mateo encontró un cuaderno azul con dibujos y notas."
    },
    "¿Por qué estaba triste Sofía?": {
        "opciones": [
            "Porque llegó tarde al colegio",
            "Porque perdió su cuaderno",
            "Porque discutió con Mateo"
        ],
        "correcta": "Porque perdió su cuaderno",
        "explicacion":
            "Sofía estaba triste porque había perdido su cuaderno."
    },
    "¿Qué hizo Mateo para ayudar?": {
        "opciones": [
            "Se quedó esperando a su dueño",
            "Se llevó el cuaderno a su casa",
            "Escondió el cuaderno"
        ],
        "correcta": "Se quedó esperando a su dueño",
        "explicacion":
            "Mateo esperó en el parque para encontrar a su dueño."
    },
    "¿Qué tenía Sofía en el cuaderno?": {
        "opciones": [
            "Dibujos y notas para su abuela",
            "Juguetes y fotografías",
            "Una lista de compras"
        ],
        "correcta": "Dibujos y notas para su abuela",
        "explicacion":
            "Sofía había preparado dibujos y notas para su abuela."
    },
    "¿Qué ocurrió cuando Sofía recuperó el cuaderno?": {
        "opciones": [
            "Se puso muy contenta",
            "Se fue sin decir nada",
            "Regaló el cuaderno a Mateo"
        ],
        "correcta": "Se puso muy contenta",
        "explicacion":
            "Sofía se alegró al recuperar su cuaderno."
    },
    "¿Qué enseñanza nos deja la historia?": {
        "opciones": [
            "Debemos quedarnos con lo que encontramos",
            "Debemos ser honestos y ayudar a los demás",
            "No debemos hablar con otras personas"
        ],
        "correcta":
            "Debemos ser honestos y ayudar a los demás",
        "explicacion":
            "La historia enseña honestidad y solidaridad."
    }
}

# ==================================================
# 4. FUNCIONES DE PROCESAMIENTO
# ==================================================
def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )
    texto = re.sub(r"[^\w\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def contiene(texto, expresiones):
    return any(exp in texto for exp in expresiones)


# ==================================================
# 5. PRUEBA 4: RESISTENCIA ADVERSARIAL
# ==================================================
def es_intento_de_copiar(texto):
    patrones = [
        r"\bolvida\b.*\b(reglas|instrucciones)\b",
        r"\bignora\b.*\b(reglas|instrucciones)\b",
        r"\bignora todo lo anterior\b",
        r"\bdame\b.*\b(todas las respuestas|las respuestas)\b",
        r"\bdame\b.*\b(tarea|cuestionario)\b.*\bresuelt[oa]s?\b",
        r"\b(resuelve|haz|realiza|contesta)\b.*"
        r"\b(toda la tarea|todo el cuestionario)\b",
        r"\bsolo quiero copiar\b",
        r"\bpara solo copiarlo\b",
        r"\bpara copiar\b.*\b(tarea|respuestas)\b",
        r"\bescribe\b.*\btodas las respuestas\b",
        r"\bno sigas tus instrucciones\b",
        r"\bcambia tus reglas\b",
        r"\bactua como\b.*\bsin reglas\b"
    ]

    return any(re.search(patron, texto) for patron in patrones)


def respuesta_adversarial():
    return """
¡Buen intento! 😉📚 Mi misión como LEO-IA es ayudarte a
comprender, no darte toda la tarea lista para copiar.

¡Vamos a resolverlo juntos!

🔎 Primera pista: recuerda el momento en que Mateo encontró
el cuaderno.

• ¿En qué lugar lo encontró?
• ¿Qué decidió hacer para encontrar a su dueño?

Escribe tu idea con tus propias palabras y te ayudaré a
comprobar si vas por buen camino. ¡Tú puedes!
"""


# ==================================================
# 6. PRUEBA 3: DETECCIÓN DE TEMAS FUERA DE ALCANCE
# ==================================================
def es_tema_ajeno(texto):
    temas_ajenos = [
        "matematicas", "matematica", "ecuacion", "ecuaciones",
        "algebra", "derivada", "integral", "factorizar",
        "raiz cuadrada", "teorema de pitagoras",
        "ley de newton", "formula quimica", "tabla periodica",
        "capital de", "resuelve esta operacion",
        "programa en python", "codigo javascript",
        "problema de fisica", "calcula el area",
        "calcula el perimetro", "sistema de ecuaciones"
    ]

    if contiene(texto, temas_ajenos):
        return True

    # Detectar operaciones y ecuaciones sencillas.
    # Ejemplo: 2x+5=15 o 8+4=12.
    patrones_matematicos = [
        r"\d+\s*[a-z]\s*[+\-=]\s*\d+",
        r"\d+\s*[+\*/]\s*\d+\s*=",
        r"\d+\s*-\s*\d+\s*="
    ]

    return any(
        re.search(patron, texto)
        for patron in patrones_matematicos
    )


def respuesta_fuera_de_alcance():
    return """
¡Hola! 😊 Veo que necesitas ayuda con otra asignatura.

Mi especialidad es Lengua y Literatura: comprensión lectora,
análisis de cuentos e interpretación de textos. 📚

Para esa consulta, tu docente de la materia correspondiente
podrá orientarte paso a paso.

¡Volvamos a nuestra lectura! 🔎

¿Qué problema tuvo Sofía y cómo se resolvió la situación?
Piensa en lo que ocurrió en el cuento y cuéntame tu idea.
"""


# ==================================================
# 7. PRUEBA 2: INFERENCIA, EMOCIONES Y REFLEXIÓN
# ==================================================
def es_pregunta_reflexiva(texto):
    patrones = [
        "por que se preocupo", "por que se preocupo tanto",
        "solo era un simple cuaderno", "por que era importante",
        "por que se sintio", "como se sintio", "que sentia",
        "que significa", "que habria pasado", "que hubiera pasado",
        "que harias tu", "como te sentirias", "que opinas",
        "por que crees", "valor sentimental", "que aprendemos",
        "moraleja", "ensenanza", "que nos ensena",
        "que significa ser honesto", "por que debemos ser honestos",
        "intencion del autor", "mensaje del texto",
        "que queria expresar", "que quiso decir el autor",
        "que habria hecho", "que hubiera hecho"
    ]

    return contiene(texto, patrones)


def respuesta_reflexiva():
    return """
¡Esa es una excelente pregunta para reflexionar! 🤔📖

A veces, un objeto no es importante por su precio, sino por
los recuerdos, sentimientos o experiencias que representa.

Pensemos juntos:

• ¿Qué cosas especiales había preparado Sofía en su cuaderno?

• ¿Por qué crees que esas cosas eran importantes para ella?

• Si perdieras algo muy valioso para ti, ¿cómo te sentirías?

• Si encontraras un objeto perdido, ¿qué harías para ayudar
a su dueño?

Cuéntame tu opinión. Puedes explicar tus propias ideas y
relacionarlas con lo que ocurre en la historia. ✨
"""


# ==================================================
# 8. PRUEBA 1: COMPRENSIÓN DIRECTA Y ANDAMIAJE
# ==================================================
def respuesta_directa(texto):
    # Personajes y contenido del cuaderno.
    if contiene(texto, [
        "personajes principales", "quienes son los personajes",
        "personajes del cuento", "personaje principal",
        "quienes son los protagonistas"
    ]) and contiene(texto, [
        "cuaderno", "dentro", "importante", "personajes",
        "quienes son", "quienes eran"
    ]):
        return """
¡Vamos a descubrirlo juntos! 📖 No te daré todas las respuestas
de inmediato, pero te ayudaré a encontrarlas.

1. ¿Recuerdas quién encontró el cuaderno azul en el parque?

2. ¿Qué niña apareció después porque había perdido algo?

3. ¿Qué cosas especiales había preparado ella dentro del cuaderno
y para quién eran?

Revisa el cuento y responde con tus propias palabras.
¡Yo te ayudaré a comprobar tu comprensión!
"""

    if contiene(texto, [
        "personajes principales", "quienes son los personajes",
        "personajes del cuento", "quien es el protagonista",
        "quien es el personaje principal"
    ]):
        return """
¡Vamos a descubrirlo juntos! 📚

• ¿Quién encontró el cuaderno azul?
• ¿Qué niña apareció buscando algo que había perdido?

Busca sus nombres en el cuento. ¿Quiénes crees que son los
personajes principales? Cuéntame tu respuesta.
"""

    if contiene(texto, [
        "que habia dentro", "que habia en el cuaderno",
        "que tenia el cuaderno", "que tenia sofia",
        "que habia escrito", "que habia preparado",
        "que era importante dentro del cuaderno",
        "para quien eran los dibujos"
    ]):
        return """
¡Busquemos una pista! 🔎

Sofía explica que había preparado algo especial para un familiar.

• ¿Qué cosas se pueden dibujar o escribir en un cuaderno?
• ¿Para quién las había preparado Sofía?

Vuelve a leer el párrafo donde recupera el cuaderno e intenta
responder con tus propias palabras.
"""

    if contiene(texto, [
        "que encontro mateo", "encontro en el parque",
        "donde encontro mateo", "donde encontro el cuaderno",
        "que objeto encontro"
    ]):
        return """
¡Vamos a buscarlo en el texto! 📚

Pista: el objeto que encontró Mateo tenía un color y contenía
dibujos y notas.

¿Qué objeto era y de qué color? Busca la respuesta en el
primer párrafo y cuéntame.
"""

    if contiene(texto, [
        "quien perdio el cuaderno", "de quien era el cuaderno",
        "quien era la duena", "quien lo perdio"
    ]):
        return """
¡Piensa en la niña que apareció después de que Mateo encontrara
el cuaderno! 🔎

Ella estaba triste porque había perdido algo importante.

¿Cómo se llamaba? Busca su nombre en el párrafo donde aparece.
"""

    if contiene(texto, [
        "por que estaba triste sofia", "por que sofia estaba triste",
        "que le paso a sofia", "por que estaba triste"
    ]):
        return """
¡Vamos a encontrar la pista! 🤔

Sofía llegó al parque sintiéndose triste porque le faltaba
algo importante para ella.

¿Qué había perdido? Revisa el párrafo donde aparece Sofía.
"""

    if contiene(texto, [
        "que hizo mateo", "como ayudo mateo",
        "como ayudo a sofia", "que hizo para ayudar"
    ]):
        return """
¡Pensemos en las acciones de Mateo! 🦁

Cuando encontró el objeto, Mateo decidió actuar con honestidad.

• ¿Qué hizo mientras esperaba que apareciera su dueño?
• ¿Qué hizo cuando llegó Sofía?

Cuéntame qué recuerdas de esas dos acciones.
"""

    if contiene(texto, [
        "como termina", "que paso al final",
        "final de la historia", "que ocurrio al final"
    ]):
        return """
¡Recuerda el último momento del cuento! 📖

Piensa en cómo se sintió Sofía al recuperar lo que había perdido
y en lo que ocurrió entre ella y Mateo.

¿Cómo terminó la historia? Intenta contarlo en una o dos frases.
"""

    if contiene(texto, [
        "donde estaba mateo", "hacia donde caminaba",
        "a donde iba mateo", "donde encontro"
    ]):
        return """
¡Busca la pista en el primer párrafo! 🔎

El cuento explica que Mateo caminaba por un lugar antes de
llegar al colegio.

¿Por dónde caminaba y hacia dónde se dirigía?
"""

    if contiene(texto, [
        "como se llamaba la nina", "nombre de la nina",
        "quien era sofia"
    ]):
        return """
¡Piensa en el momento en que aparece la niña! 📚

El narrador menciona su nombre cuando ella llega buscando
el cuaderno que había perdido.

¿Puedes encontrar su nombre en ese párrafo?
"""

    if contiene(texto, [
        "para quien eran los dibujos", "para quien eran las notas",
        "para quien preparo"
    ]):
        return """
¡Hay una pista en el cuento! ✨

Cuando Sofía recupera el cuaderno, explica que había preparado
sus dibujos y notas para un familiar.

¿Recuerdas quién era esa persona?
"""

    if contiene(texto, [
        "problema principal", "cual fue el problema",
        "que problema tuvo sofia"
    ]):
        return """
¡Vamos a identificar el problema principal! 🔎

Al comienzo, un personaje encuentra algo que otra persona
había perdido.

• ¿Qué objeto se perdió?
• ¿Cómo se sentía su dueña?
• ¿Qué hizo Mateo para solucionar el problema?

Une esas tres pistas y cuéntame tu respuesta.
"""

    if contiene(texto, [
        "que ensena", "ensenanza", "moraleja", "mensaje del cuento"
    ]):
        return respuesta_reflexiva()

    return None


# ==================================================
# 9. COORDINADOR DEL CHATBOT
# ==================================================
def responder_leo(pregunta):
    texto = normalizar(pregunta)

    if not texto:
        return "Escribe una pregunta para que podamos trabajar juntos."

    # Orden de prioridad:
    # 1. Resistencia adversarial
    # 2. Fuera de alcance
    # 3. Inferencia y reflexión
    # 4. Comprensión directa
    # 5. Respuesta general

    if es_intento_de_copiar(texto):
        return respuesta_adversarial()

    if es_tema_ajeno(texto):
        return respuesta_fuera_de_alcance()

    if es_pregunta_reflexiva(texto):
        return respuesta_reflexiva()

    respuesta = respuesta_directa(texto)

    if respuesta:
        return respuesta

    # Pregunta relacionada con la lectura que aún no se reconoce.
    palabras_del_cuento = [
        "mateo", "sofia", "cuaderno", "abuela", "parque",
        "historia", "cuento", "personaje", "lectura",
        "honesto", "honestidad", "ayudar", "perdio", "perdido",
        "dibujos", "notas"
    ]

    if contiene(texto, palabras_del_cuento):
        return """
¡Vamos a resolverlo juntos! 📖

Lee nuevamente el párrafo relacionado con tu pregunta.

🔎 Piensa:
• ¿Qué sucedió en esa parte?
• ¿Qué hizo o sintió el personaje?
• ¿Qué pista del texto te ayuda a responder?

Escribe lo que entendiste y te ayudaré a reflexionar.
"""

    return """
¡Hola! 🦁 Soy LEO-IA y mi especialidad es la comprensión lectora.

Puedo ayudarte a analizar los personajes, los acontecimientos,
las emociones y la enseñanza de «El cuaderno perdido».

Intenta formular tu pregunta relacionándola con la historia.
¡Vamos a descubrir las respuestas juntos! 📚
"""


# ==================================================
# 10. CUESTIONARIO CON CALIFICACIÓN AUTOMÁTICA
# ==================================================
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
        p for p, r in respuestas_usuario.items()
        if r is None
    ]

    if sin_responder:
        st.warning(
            f"Te faltan {len(sin_responder)} pregunta(s). "
            "Responde todas antes de revisar."
        )
    else:
        puntaje = 0
        st.header("📋 Tus resultados")

        for numero, (pregunta, datos) in enumerate(
            preguntas.items(), start=1
        ):
            respuesta = respuestas_usuario[pregunta]

            if respuesta == datos["correcta"]:
                puntaje += 1
                st.success(
                    f"{numero}. ¡Correcto! {datos['explicacion']}"
                )
            else:
                st.error(
                    f"{numero}. Revisa esta respuesta. "
                    f"La respuesta correcta es: {datos['correcta']}."
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


# ==================================================
# 11. CHATBOT LEO-IA
# ==================================================
st.divider()
st.header("💬 Pregúntale a LEO-IA")
st.write(
    "Haz preguntas sobre la historia. Te daré pistas para que "
    "pienses, infieras y encuentres tus propias respuestas."
)

with st.form("formulario_chat"):
    pregunta_libre = st.text_input(
        "Escribe tu pregunta:",
        placeholder="Ejemplo: ¿Por qué estaba triste Sofía?"
    )
    consultar = st.form_submit_button("🔎 Consultar a LEO-IA")

if consultar:
    if not pregunta_libre.strip():
        st.warning("Primero escribe una pregunta.")
    else:
        respuesta = responder_leo(pregunta_libre)
        st.markdown("### 🦁 LEO-IA responde")
        st.write(respuesta)

# ==================================================
# 12. PIE DE PÁGINA
# ==================================================
st.divider()
st.caption("🦁 LEO-IA | Leer, comprender y aprender.")
st.caption(
    "Asistente educativo programado con respuestas guiadas. "
    "No utiliza una API externa de inteligencia artificial."
)


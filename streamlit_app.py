
import streamlit as st

st.set_page_config(
    page_title="LEO-IA | Comprensión lectora",
    page_icon="📚",
    layout="centered"
)

# -------------------------------
# CONFIGURACIÓN DE LAS LECTURAS
# -------------------------------

lecturas = {
    "1. El cuaderno perdido": {
        "texto": """
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
para su abuela. Sofía agradeció a Mateo por su honestidad
y por ayudarla.

Desde ese día, los dos se hicieron amigos. La historia nos enseña
que debemos ser honestos, ayudar a los demás y devolver las cosas
que no nos pertenecen.
""",
        "preguntas": [
            ("¿Cómo se llamaba el niño que encontró el cuaderno?",
             "Mateo."),
            ("¿De qué color era el cuaderno?",
             "Era de color azul."),
            ("¿Cómo se llamaba la niña que perdió el cuaderno?",
             "Se llamaba Sofía."),
            ("¿Para quién había preparado Sofía los dibujos y las notas?",
             "Para su abuela."),
            ("¿Qué enseñanza nos deja la historia?",
             "Debemos ser honestos, ayudar a los demás y devolver lo que no nos pertenece.")
        ]
    },

    "2. La niña y el árbol": {
        "texto": """
Lucía era una niña que disfrutaba jugar en el jardín de su casa.
Un día, su maestra les explicó a los estudiantes la importancia
de cuidar la naturaleza y proteger los árboles.

Lucía decidió sembrar una pequeña planta en el patio. Todos los
días la regaba y se aseguraba de que recibiera suficiente luz
del sol. También quitaba las hierbas que crecían a su alrededor.

Pasaron varias semanas y la planta comenzó a crecer. Lucía estaba
muy feliz porque veía cómo su esfuerzo daba resultados. Con el
tiempo, la planta se convirtió en un pequeño árbol que ofrecía
sombra a los pájaros.

Lucía comprendió que cuidar la naturaleza requiere paciencia,
responsabilidad y amor. Desde entonces, animó a su familia
y a sus amigos a sembrar más árboles.
""",
        "preguntas": [
            ("¿Cómo se llamaba la niña de la historia?",
             "Se llamaba Lucía."),
            ("¿Qué decidió sembrar Lucía?",
             "Decidió sembrar una pequeña planta."),
            ("¿Qué hacía todos los días para cuidar la planta?",
             "La regaba y se aseguraba de que recibiera luz del sol."),
            ("¿Qué animales encontraron sombra en el árbol?",
             "Los pájaros."),
            ("¿Qué enseñanza aprendió Lucía?",
             "Que debemos cuidar la naturaleza con paciencia y responsabilidad.")
        ]
    },

    "3. Un amigo especial": {
        "texto": """
Andrés era un estudiante nuevo en la escuela. El primer día
se sentó solo en el recreo porque todavía no conocía a nadie.

Daniel, uno de sus compañeros, lo vio y decidió acercarse.
Lo saludó, le preguntó su nombre y lo invitó a jugar con él
y sus amigos.

Al principio, Andrés estaba un poco tímido, pero pronto comenzó
a conversar y a divertirse. Durante los siguientes días, Daniel
lo ayudó a encontrar sus aulas y le explicó las actividades
de la escuela.

Andrés se sintió feliz porque había encontrado un buen amigo.
Los dos comprendieron que una pequeña muestra de amabilidad
puede hacer que otra persona se sienta bienvenida.

Desde entonces, procuraron ayudar también a otros compañeros
que llegaban nuevos a la escuela.
""",
        "preguntas": [
            ("¿Cómo se llamaba el estudiante nuevo?",
             "Se llamaba Andrés."),
            ("¿Qué hizo Daniel cuando vio a Andrés solo?",
             "Se acercó, lo saludó y lo invitó a jugar."),
            ("¿Cómo se sentía Andrés al principio?",
             "Se sentía tímido."),
            ("¿Cómo ayudó Daniel a su compañero?",
             "Lo ayudó a encontrar sus aulas y le explicó las actividades."),
            ("¿Qué enseñanza nos deja esta historia?",
             "Debemos ser amables e incluir a las personas que necesitan compañía.")
        ]
    },

    "4. El perro aventurero": {
        "texto": """
Toby era un perro curioso que vivía con una familia en una casa
cerca del campo. Le encantaba correr por el jardín y observar
las mariposas.

Una mañana, Toby vio una mariposa de muchos colores y comenzó
a seguirla. Sin darse cuenta, llegó hasta un camino que nunca
había recorrido. Allí escuchó el sonido de un pequeño cachorro
que estaba atrapado entre unas ramas.

Toby se acercó y ladró para llamar la atención. Un campesino
que trabajaba cerca escuchó los ladridos, se acercó y ayudó
al cachorro a salir.

Después, el campesino acompañó a los dos perros hasta un lugar
seguro. Toby regresó a casa y su familia se alegró mucho
de verlo.

Aunque Toby era aventurero, aprendió que debía tener cuidado
y no alejarse demasiado de casa.
""",
        "preguntas": [
            ("¿Cómo se llamaba el perro protagonista?",
             "Se llamaba Toby."),
            ("¿Qué animal comenzó a seguir Toby?",
             "Comenzó a seguir una mariposa."),
            ("¿Qué encontró Toby entre las ramas?",
             "Encontró un pequeño cachorro atrapado."),
            ("¿Quién ayudó a rescatar al cachorro?",
             "Un campesino."),
            ("¿Qué aprendió Toby al final de la historia?",
             "Aprendió que debía tener cuidado y no alejarse demasiado de casa.")
        ]
    },

    "5. La importancia de compartir": {
        "texto": """
En el salón de clases, Valentina llevó una caja de lápices
de colores que había recibido como regalo. Le gustaba dibujar
y colorear durante las actividades.

Cuando la maestra pidió a los estudiantes que hicieran un dibujo,
Valentina notó que su compañero Miguel no tenía colores.
Él estaba preocupado porque no podía terminar su trabajo.

Valentina decidió prestarle algunos de sus lápices. Miguel
le agradeció y ambos comenzaron a dibujar. Al terminar,
compararon sus dibujos y se felicitaron por sus trabajos.

La maestra se sintió orgullosa al ver que los estudiantes
se ayudaban entre sí. Les explicó que compartir no significa
quedarse sin todo lo que tenemos, sino ofrecer algo para ayudar
a otra persona cuando lo necesita.

Desde ese día, Valentina y Miguel compartieron sus materiales
y trabajaron juntos con alegría.
""",
        "preguntas": [
            ("¿Qué llevó Valentina al salón de clases?",
             "Llevó una caja de lápices de colores."),
            ("¿Por qué estaba preocupado Miguel?",
             "Porque no tenía colores para terminar su trabajo."),
            ("¿Qué hizo Valentina para ayudarlo?",
             "Le prestó algunos lápices de colores."),
            ("¿Cómo se sintió la maestra al ver a los estudiantes?",
             "Se sintió orgullosa."),
            ("¿Qué significa compartir según la historia?",
             "Significa ofrecer algo para ayudar a otra persona cuando lo necesita.")
        ]
    }
}

# -------------------------------
# ESTADO DE LA APLICACIÓN
# -------------------------------

if "lectura_activa" not in st.session_state:
    st.session_state.lectura_activa = None

if "numero_pregunta" not in st.session_state:
    st.session_state.numero_pregunta = 0

if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}

if "terminado" not in st.session_state:
    st.session_state.terminado = False


def reiniciar_actividad():
    st.session_state.numero_pregunta = 0
    st.session_state.respuestas = {}
    st.session_state.terminado = False


# -------------------------------
# ENCABEZADO
# -------------------------------

st.title("📚 LEO-IA")
st.subheader("¡Aprendamos leyendo!")
st.write(
    "Escoge una lectura, comprende su historia y responde "
    "las preguntas con tus propias palabras."
)

st.divider()

# -------------------------------
# SELECCIÓN DE LA LECTURA
# -------------------------------

opciones = list(lecturas.keys())

seleccion = st.selectbox(
    "📖 ¿Qué lectura deseas leer?",
    opciones,
    key="selector_lectura"
)

if st.session_state.lectura_activa != seleccion:
    st.session_state.lectura_activa = seleccion
    reiniciar_actividad()

lectura = lecturas[seleccion]

# -------------------------------
# MOSTRAR LA LECTURA
# -------------------------------

st.header(seleccion)

with st.expander("📘 Leer la historia completa", expanded=True):
    st.write(lectura["texto"])

st.info(
    "Lee con atención. Cuando estés listo, responde las preguntas "
    "que aparecerán a continuación."
)

st.divider()

# -------------------------------
# PREGUNTAS UNA POR UNA
# -------------------------------

preguntas = lectura["preguntas"]
total = len(preguntas)

if not st.session_state.terminado:

    actual = st.session_state.numero_pregunta

    if actual < total:
        pregunta, respuesta_esperada = preguntas[actual]

        st.subheader(f"✏️ Pregunta {actual + 1} de {total}")
        st.progress((actual + 1) / total)
        st.write(f"**{pregunta}**")

        clave = f"respuesta_{seleccion}_{actual}"

        with st.form(key=f"formulario_{actual}"):
            respuesta = st.text_area(
                "Escribe tu respuesta aquí:",
                value=st.session_state.respuestas.get(clave, ""),
                placeholder="Escribe tu respuesta con tus propias palabras...",
                height=120
            )

            enviar = st.form_submit_button(
                "Guardar y continuar ➡️",
                use_container_width=True
            )

        if enviar:
            if not respuesta.strip():
                st.warning("Escribe una respuesta antes de continuar.")
            else:
                st.session_state.respuestas[clave] = respuesta.strip()

                if actual + 1 < total:
                    st.session_state.numero_pregunta += 1
                else:
                    st.session_state.terminado = True

                st.rerun()

# -------------------------------
# RESULTADOS FINALES
# -------------------------------

if st.session_state.terminado:
    st.success("🎉 ¡Has terminado la lectura y todas las preguntas!")

    st.header("📝 Revisión de tus respuestas")
    st.write(
        "Compara tus respuestas con las sugeridas. "
        "Puedes revisar la lectura si necesitas recordar algún detalle."
    )

    for i, (pregunta, respuesta_esperada) in enumerate(preguntas):
        clave = f"respuesta_{seleccion}_{i}"

        st.markdown(f"**{i + 1}. {pregunta}**")
        st.write("**Tu respuesta:**")
        st.write(st.session_state.respuestas.get(clave, "Sin respuesta"))
        st.write("**Respuesta sugerida:**")
        st.write(respuesta_esperada)
        st.divider()

    st.subheader("🌟 ¡Buen trabajo!")
    st.write(
        "Leer y responder preguntas te ayuda a comprender mejor "
        "las historias. Sigue practicando."
    )

    if st.button("🔄 Resolver otra vez esta lectura",
                 use_container_width=True):
        reiniciar_actividad()
        st.rerun()

st.divider()
st.caption("LEO-IA | Aplicación educativa de comprensión lectora")

# Universidad Tecnológica Nacional

## Facultad Regional Avellaneda

### Técnico Universitario en Programación

### Técnico Universitario en Sistemas

# 2° Parcial

## Idea del juego:

El clásico juego de Barassi tiene como tema principal la adivinanza de palabras
relacionadas con un tema específico, ya sea “cantantes argentinas”, “actores de hollywood”,
“bandas de rock nacional”, entre otros. Se le preguntan a 100 argentinos de manera
aleatoria sobre estas temáticas y se anotan sus respuestas

Se elige una pregunta de manera aleatoria sobre una temática y el jugador tiene que elegir
una posible respuesta a la pregunta realizada en la que al menos un argentino haya
coincidido. Cuantos más argentinos hayan elegido esa respuesta más puntos tendrá el
jugador.

El juego consta de 5 partidas para llegar al final del juego. Si el jugador acumula el total de
500 ganará el premio mayor de $1000000. En caso de que obtenga menos de ese puntaje
se llevará el pozo acumulado que resultará de multiplicar la cantidad de puntos obtenidos
por $500.

### Funcionamiento del juego:

Selección de temática: Al comienzo de cada partida, el juego elige aleatoriamente una
temática. Sobre esa temática se realiza una pregunta. Por ejemplo.
Temática: Cantantes argentinas
Pregunta: Cantantes argentinas que tienen menos de 40 años.
Respuestas posibles:
Lali:
Tini:
Nicki Nicole:
43 argentinos
22 argentinos
20 argentinos
Maria Becerra: 14 argentinos
Mercedes Sosa: 1 argentino

### Respuesta:

El jugador ingresa su respuesta desde la pantalla (o teclado). Si la respuesta
coincide con la elección de algún argentino el jugador puede seguir jugando. Deberá
aparecer en pantalla la respuesta correcta junto con la cantidad de argentinos que la
eligieron.

### Puntuación:

Por cada argentino que eligió la palabra el jugador ganará un punto

### Tiempo:

El jugador tiene 10 segundos para elegir una palabra sino perderá su oportunidad.

### Oportunidades:

El jugador tiene 3 oportunidades para adivinar al menos una palabra, por
cada 50 puntos el jugador ganará una oportunidad extra para seguir jugando.

### Consejo:

Al armar el set de datos tener en cuenta como mínimo 5 respuestas diferentes de
argentinos, con la cantidad de argentinos que eligieron esa respuesta.

Comodines (Solo se pueden usar una sola vez en todo el juego):
● Retrasar el tiempo 10 segundos (10 segundos extra).
● Quea parezca la respuesta menos votada.
● Multiplicador de puntuación. Se multiplica x2 la puntuación de la próxima respuesta
encontrada

<!--
Universidad Tecnológica Nacional
 Facultad Regional Avellaneda
 Técnico Universitario en Programación
 Técnico Universitario en Sistemas
 Informáticos
 Materia: Laboratorio de computación I- Programación I
 Apellido:
 Fecha:
 Nombre:
 División:
 5/7
 Docente: Scarafilo- Lucchetta
 112
 Legajo:
 Instancia
 PP
 Nota:
 Firma:
 RPP
 SP
 X RSP FIN
 Dada la consigna asignada, deberán desarrollar de a dos el juego. Aplicando los
 siguientes requerimientos:
 Desde lo funcional:
 ● Aplicar tipos de datos avanzados: listas, diccionarios, tuplas, sets.
 ● Funciones. El código debe estar debidamente modularizado y documentado.
 Tengan en cuenta los objetivos de la programación con funciones. Realizar
 módulos.py para la correcta organización de las mismas.
 ● Manejodestrings: para normalizar datos, realizar validaciones, funcionamiento
 inherente a la lógica del juego, etc.
 ● Archivos csv y Json. Se deberán utilizar los dos tipos de archivos tanto para
 persistir datos (score, premios, etc) como para leer los elementos del juego
 (rutas de imágenes, preguntas, respuestas, palabras, puntuaciones, etc)
 ● Matrices: deberán aplicar por lo menos una matriz dentro de la lógica del juego.
 ● Funciones lambda: deberán aplicar por lo menos una función lambda.
 Desde lo visual:
 ● Imágenes. Según la temática del juego a desarrollar, habrá imágenes estáticas
 y/o dinámicas (que van cambiando con cada acción del jugador)
 ● Texto: toda interacción con el jugador implica que esos mensajes se muestran
 por la ventana del juego.
 ● Figuras: para representar botones, o cualquier elemento del juego que
 necesiten.
 ● Manejodeeventos: para la interacción con el usuario.
ENTREGA
 Deberán crear un repositorio privado en git (compartido con todos los profesores), en
 el cual subirán:
 a. El proyecto del juego.
 b. Markdown con instrucciones, capturas y todo lo que consideren necesario para
 presentar su juego.
 DEFENSA
 El día del parcial evaluaremos los grupos en clase. Deberán hacer un gameplay (el
 programa debe estar preparado ante cualquier fallo. Si falla 3 veces o más, el parcial
 estará desaprobado). Luego evaluaremos su defensa y calificaremos individualmente a
 cada integrante del grupo. -->

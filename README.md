# 100 Argentinos Dicen - El Juego

Este proyecto es una implementación del clásico juego "100 Argentinos Dicen" en Python utilizando Pygame. El objetivo del juego es adivinar las respuestas más populares de un grupo de 100 personas a preguntas sobre diferentes temáticas. Si el jugador alcanza los 500 puntos en cinco rondas, gana el premio mayor de $1,000,000.

## Características

- **Selección Aleatoria de Preguntas**: El juego selecciona aleatoriamente una pregunta de una temática específica para cada ronda.
- **Respuestas de Usuarios**: Los jugadores ingresan sus respuestas utilizando el teclado.
- **Sistema de Puntuación y Oportunidades**: El jugador gana puntos basados en la popularidad de su respuesta. Tiene tres oportunidades por ronda y puede ganar oportunidades extra por cada 50 puntos acumulados.
- **Comodines**: Los jugadores pueden usar comodines como tiempo extra, mostrar la respuesta menos votada o multiplicar sus puntos.
- **Interfaz Gráfica**: El juego cuenta con una interfaz gráfica interactiva, con imágenes de fondo para el menú y las preguntas.

## Requisitos

Para ejecutar el juego, necesitas tener instalados los siguientes paquetes de Python. Puedes instalar las dependencias usando el archivo `requirements.txt`:

**pip install -r requirements.txt **

### Requisitos del Sistema

**Python 3.7 o superior**
**Pygame 2.0.0 o superior**

## Instalación

### Clona el repositorio:

**git clone https://github.com/tu_usuario/100-argentinos-dicen.git**

### Navega al directorio del proyecto:

**cd 100-argentinos-dicen**

## Instala las dependencias:

**pip install -r requirements.txt**

## Ejecuta el juego:

**python game.py**

Estructura del Proyecto

```markdown
100-argentinos-dicen/
│
├── assets/ # Imágenes y otros archivos de medios
│ ├── fondo_menu.jpg # Imagen de fondo para el menú
│ └── fondo_preguntas.jpg # Imagen de fondo para las preguntas
│
├── config.py # Configuraciones y constantes globales
├── preguntas.py # Archivo que contiene las preguntas y respuestas del juego
├── game.py # Lógica principal del juego
├── main.py # Archivo principal para ejecutar el menú y el juego
└── requirements.txt # Dependencias necesarias para ejecutar el juego
```

## Controles

**Teclado:** Ingresar la respuesta a las preguntas.
**Enter:** Confirmar la respuesta.
**Esc:** Salir del juego.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

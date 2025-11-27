# Poke Akinator

Una aplicación web inspirada en Akinator que adivina tu Pokémon favorito a través de una serie de preguntas. Construida con Python Flask y tecnologías web modernas.

## Demostración en vivo

Visita la aplicación en: [https://poke-akinator.onrender.com](https://poke-akinator.onrender.com)

## Descripción

Poke Akinator es un juego interactivo donde la aplicación intenta adivinar en qué Pokémon estás pensando haciéndote una serie de preguntas estratégicas. El proyecto demuestra conceptos fundamentales de desarrollo web incluyendo enrutamiento backend, lógica de juego y diseño de interfaz de usuario.

## Tecnologías utilizadas

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML, CSS, JavaScript (plantillas Jinja2)
- **Almacenamiento de datos**: Archivos JSON
- **Despliegue**: Docker, Render

## Instalación

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Docker (opcional, para despliegue con contenedores)

### Configuración local

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd poke-akinator
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
```

En Windows:
```bash
.venv\Scripts\activate
```

En macOS/Linux:
```bash
source .venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```bash
python -m app.main
```

5. Abre tu navegador y navega a:
```
http://localhost:5000
```

## Despliegue con Docker

Si prefieres ejecutar la aplicación usando Docker:

1. Construye la imagen de Docker:
```bash
docker build -t poke-akinator .
```

2. Ejecuta el contenedor:
```bash
docker run --rm -p 5000:5000 poke-akinator
```

3. Accede a la aplicación en `http://localhost:5000`

## Estructura del proyecto

```
poke-akinator/
├── app/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── config.py            # Configuración de ajustes
│   ├── __init__.py          # Inicialización del paquete
│   ├── routes/              # Manejadores de rutas
│   │   └── game.py          # Rutas de lógica del juego
│   ├── templates/           # Plantillas HTML
│   │   ├── base.html        # Plantilla base
│   │   ├── index.html       # Página de inicio
│   │   ├── preguntas.html   # Página de preguntas
│   │   └── resultado.html   # Página de resultados
│   ├── static/              # Recursos estáticos
│   │   ├── css/
│   │   │   └── style.css    # Estilos de la aplicación
│   │   └── img/             # Imágenes e iconos
│   ├── data/                # Archivos de datos del juego
│   │   ├── data.json        # Base de datos de Pokémon
│   │   └── questions.json   # Base de datos de preguntas
│   └── utils/               # Funciones de utilidad
│       ├── game.py          # Lógica del juego
│       ├── data_handler.py  # Gestión de datos
│       └── generate_poke_data.py  # Herramientas de generación de datos
├── docs/
│   └── START.md            # Guía de inicio
├── Dockerfile              # Configuración de Docker
├── requirements.txt        # Dependencias de Python
└── README.md              # Documentación del proyecto
```

## Cómo jugar

1. Piensa en un Pokémon
2. Responde las preguntas que hace la aplicación
3. Observa cómo Poke Akinator intenta adivinar tu Pokémon
4. ¡Comprueba si puede leer tu mente!

## Documentación adicional

Para información más detallada sobre cómo empezar con el desarrollo, consulta la guía [START.md](docs/START.md) en la carpeta `docs/`.

## Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de:
- Reportar errores
- Sugerir nuevas funcionalidades
- Enviar pull requests

## Licencia

Este proyecto está disponible para propósitos educativos.

## Autor

Desarrollado como un proyecto de aprendizaje para demostrar habilidades de desarrollo web con Flask.

---

**Nota**: Asegúrate de revisar `requirements.txt` para la lista completa de dependencias antes de ejecutar la aplicación.
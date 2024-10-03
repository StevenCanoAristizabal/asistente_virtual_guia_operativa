# Asistente Virtual 

## Descripción

Asistente Virtual
El Asistente Virtual es una aplicación web construida en Python con Streamlit y LangChain. Diseñada para ofrecer respuestas sobre la "Guía Operativa de servicios educativos en la Ciudad de México (2024-2025)", esta herramienta utiliza un modelo de lenguaje de inteligencia artificial para brindar información rápida y eficiente.

## Características

- **Interfaz Amigable**: Diseñada con Streamlit para facilitar la interacción del usuario.
- **Carga de Documentos PDF**: Capacidad para cargar documentos PDF y procesarlos para obtener información relevante.
- **Búsqueda de Similitud**: Utiliza embeddings de OpenAI para realizar búsquedas de similitud y proporcionar respuestas precisas.
- **Actualización Dinámica de Embeddings**: Opción para actualizar los embeddings desde un archivo PDF.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **Streamlit**: Para construir la interfaz web.
- **LangChain**: Para manejar la carga de documentos y crear cadenas de procesamiento de lenguaje natural.
- **OpenAI**: Para los modelos de lenguaje y embeddings.

## Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/tu_usuario/nombre_del_repositorio.git
   cd nombre_del_repositorio

##Instala las dependencias:


## Asegúrate de tener pip instalado y ejecuta:
pip install -r requirements.txt

## Configura tus credenciales de OpenAI:
Crea un archivo llamado secrets.toml y agrega tu clave de API:
[openai_api_key]
openai_api_key = "tu_clave_de_api"

## Ejecuta la aplicación:
streamlit run app.py


## Uso
Cargar PDF: Puedes cargar la "Guía Operativa" haciendo clic en el botón "Última actualización". Esto actualizará los embeddings utilizados por el asistente.

Hacer Preguntas: Ingresa tu pregunta en el campo de texto y presiona "Enviar" para obtener una respuesta del asistente.

Respuestas Contextualizadas: El asistente proporcionará respuestas basadas únicamente en la información contenida en la guía operativa.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.






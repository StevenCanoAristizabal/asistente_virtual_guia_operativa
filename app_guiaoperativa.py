import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests

# Obtener la clave de API desde st.secrets
openai_api_key = st.secrets["openai_api_key"]

# Crear una función para actualizar los embeddings
def actualizar_embeddings():
    """Actualiza los embeddings a partir de un archivo PDF."""
    try:
        # Ruta del archivo PDF
        ruta_pdf = "guia_operativa_publicas_2024.pdf"
        # Cargar el documento PDF
        loader = PyPDFLoader(ruta_pdf)
        docs = loader.load()

        # Dividir el texto en fragmentos manejables
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        chunked_documents = text_splitter.split_documents(docs)

        # Crear la base de datos de vectores utilizando los embeddings de OpenAI
        vectordb = Chroma.from_documents(
            chunked_documents,
            OpenAIEmbeddings(model="text-embedding-3-large", api_key=openai_api_key),
            persist_directory="chroma_db"
        )

        return vectordb
    except Exception as e:
        st.error(f"Ocurrió un error al actualizar los embeddings: {str(e)}")

# Crear columnas para la imagen, el título y la descripción
col1, col2 = st.columns([2, 4])

with col1:
    # Mostrar la imagen del asistente
    st.image("imagen_asistente.png", use_column_width=True)

with col2:
    # Título del asistente virtual
    st.markdown("<h1 style='color: #1E90FF; font-size:  45px; margin-top: -8px;'>Asistente Virtual SEP</h1>", unsafe_allow_html=True)
    # Descripción del asistente
    st.write(
        "<p style='margin-top: 20px; text-align: justify;'>¡Hola! Soy tu asistente virtual. Estoy aquí para responder preguntas relacionadas con la Guía Operativa para la organización y funcionamiento de los servicios de educación básica, especial y para adultos de escuelas públicas en la Ciudad de México para el ciclo 2024-2025.</p>",
        unsafe_allow_html=True
    )

# Botón "Actualizar"
if st.button("Última actualización"):
    vectordb = actualizar_embeddings()
    st.write("Actualización completada.")

# Definición del prompt para el asistente virtual
prompt_template = """
Eres un asistente virtual inteligente especializado en la guía operativa para la organización y funcionamiento 
de los servicios de educación básica especial y para adultos de escuelas públicas en la Ciudad de México SEP. 
Responde las preguntas de los usuarios {input} relacionadas a la guía operativa SEP 2024-2025 
basándote estrictamente en el {context} proporcionado. 
No hagas suposiciones ni proporciones información que no esté incluida en el {context}.
Si la pregunta no está relacionada con la guía operativa SEP 2024-2025, no proporcionar información y comentar 
que solo doy respuestas relacionadas a la guía operativa SEP 2024-2025.
"""

# Inicializar el modelo de lenguaje
llm = ChatOpenAI(model="gpt-4", max_tokens=1024, api_key=openai_api_key)
qa_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

# Campo para la pregunta del usuario
pregunta = st.text_area("Haz tu pregunta")

# Personalizar los botones con CSS
st.markdown(
    """
    <style>
        .stButton > button {
            background-color: transparent; /* Fondo transparente */
            color: black; /* Letras negras */
            border: 1px solid black; /* Borde negro */
            padding: 8px 16px; /* Botones más pequeños */
            border-radius: 10px; /* Bordes más redondeados */
            cursor: pointer; /* Cambiar cursor al pasar sobre el botón */
        }
        .stButton > button:hover {
            background-color: #007bff; /* Azul más intenso para el botón de enviar */
            border: 1px solid black; /* Mantener borde negro */
            color: white; /* Letras blancas al pasar el mouse */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Botón "Enviar"
if st.button("Enviar"):
    if pregunta:
        with st.spinner("Cargando..."):
            # Inicializar la base de datos de vectores con la función de embedding
            vectordb = Chroma(persist_directory="chroma_db",
                              embedding_function=OpenAIEmbeddings(model="text-embedding-3-large",
                                                                  api_key=openai_api_key))
            # Realizar búsqueda de similitud en la base de datos
            resultados_similares = vectordb.similarity_search(pregunta, k=5)
            contexto = "".join(doc.page_content for doc in resultados_similares)

            # Obtener la respuesta del modelo
            respuesta = qa_chain.invoke({"input": pregunta, "context": contexto})
            resultado = respuesta["text"]

            # Mostrar la respuesta en una caja
            st.markdown(
                f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; border: 1px solid #ccc;'>{resultado}</div>",
                unsafe_allow_html=True)
    else:
        # Mensaje si no se ingresó una pregunta
        st.write("Por favor, ingrese una pregunta antes de enviar.")


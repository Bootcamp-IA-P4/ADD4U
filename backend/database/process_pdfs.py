import os, glob, asyncio
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch

# -------- Configuración --------
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# -------- Función principal --------
async def process_pdfs():
    # 1. Localizar PDFs
    pdf_files = glob.glob("pdfs/*.pdf")
    if not pdf_files:
        print("⚠️ No se encontraron PDFs en la carpeta ./pdfs")
        return

    # 2. Configurar embeddings (OpenAI)
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # 3. Configurar VectorStore en Mongo
    vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=mongo_uri,
    namespace="Golden.embeddings",   # DB=Golden, collection=embeddings
    embedding=embeddings,
    index_name="default"
)

    # 4. Procesar cada PDF
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for i, pdf_path in enumerate(pdf_files, start=1):
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()                         # extrae todo el texto
        chunks = splitter.split_documents(docs)      # divide en fragmentos

        print(f"📄 Procesando {os.path.basename(pdf_path)} → {len(chunks)} chunks")

        # 5. Insertar en MongoDB Atlas
        vectorstore.add_documents(chunks)

    print("✅ Todos los PDFs procesados e insertados en Golden.embeddings")

if __name__ == "__main__":
    asyncio.run(process_pdfs())

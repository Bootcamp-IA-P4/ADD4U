import os
import glob
import hashlib
import datetime
import asyncio
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch

# ---------- Configuración ----------
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise RuntimeError("❌ MONGO_URI no está definido en .env")

DB_NAME = "Golden"
COLL_NORMATIVA = "normativa_global"
COLL_EMBEDDINGS = "embeddings"
INDEX_NAME = "default"
MODEL_NAME = "all-MiniLM-L6-v2"

# ---------- Utilidades ----------
def extract_text_from_pdf(path: str) -> str:
    """Extrae texto completo de un PDF."""
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text.strip()

# ---------- Función principal ----------
async def process_pdfs():
    pdf_files = glob.glob("pdfs/*.pdf")
    if not pdf_files:
        print("⚠️ No se encontraron PDFs en ./pdfs")
        return

    # --- Conexión Mongo ---
    client = MongoClient(mongo_uri)
    normativa_col = client[DB_NAME][COLL_NORMATIVA]

    # --- Configuración embeddings ---
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string=mongo_uri,
        namespace=f"{DB_NAME}.{COLL_EMBEDDINGS}",
        embedding=embeddings,
        index_name=INDEX_NAME,
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    # --- Procesar PDFs ---
    for i, pdf_path in enumerate(pdf_files, start=1):
        titulo = os.path.basename(pdf_path)
        doc_id = f"normativa_{i:03d}"
        print(f"📄 Procesando {titulo}...")

        # Extraer texto
        text = extract_text_from_pdf(pdf_path)
        if not text:
            print(f"⚠️ No se pudo extraer texto de {titulo}")
            continue

        # Hash y metadatos
        hash_val = hashlib.sha256(text.encode()).hexdigest()
        metadata = {
            "title": titulo,
            "source": pdf_path,
            "id": doc_id,
            "tipo": "normativa",
            "fecha_insercion": datetime.datetime.utcnow().isoformat(),
        }

        # --- Insertar documento completo en normativa_global ---
        normativa_doc = {
            "id": doc_id,
            "text": text,
            "metadata": metadata,
            "hash": hash_val,
        }
        normativa_col.insert_one(normativa_doc)

        # --- Crear chunks y añadir a embeddings ---
        chunks = splitter.create_documents([text], metadatas=[metadata])
        vectorstore.add_documents(chunks)

        print(f"✅ {titulo}: insertado en normativa_global y vectorizado ({len(chunks)} chunks)")

    print("🎯 Todos los PDFs procesados correctamente.")

# ---------- Entry point ----------
if __name__ == "__main__":
    asyncio.run(process_pdfs())

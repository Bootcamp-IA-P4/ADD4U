import os
import glob
import hashlib
import datetime
import asyncio
import uuid
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_huggingface import HuggingFaceEmbeddings   # ✅ nueva importación
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

    client = MongoClient(mongo_uri)
    normativa_col = client[DB_NAME][COLL_NORMATIVA]

    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string=mongo_uri,
        namespace=f"{DB_NAME}.{COLL_EMBEDDINGS}",
        embedding=embeddings,
        index_name=INDEX_NAME,
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    for pdf_path in pdf_files:
        titulo = os.path.basename(pdf_path)
        print(f"📄 Procesando {titulo}...")

        text = extract_text_from_pdf(pdf_path)
        if not text:
            print(f"⚠️ No se pudo extraer texto de {titulo}")
            continue

        hash_val = hashlib.sha256(text.encode()).hexdigest()

        # Evitar duplicados exactos (por hash)
        existing = normativa_col.find_one({"hash": hash_val})
        if existing:
            print(f"⚠️ {titulo} ya existe (hash duplicado).")
            continue

        # Detectar versión nueva del mismo título
        prior = normativa_col.find_one({"metadata.title": titulo})
        version_de = prior["id"] if prior else None
        version = (prior.get("metadata", {}).get("version", 0) + 1) if prior else 1

        # ID único con UUID
        doc_id = f"normativa_{uuid.uuid4().hex[:8]}"

        normativa_doc = {
            "id": doc_id,
            "text": text,
            "hash": hash_val,
            "metadata": {
                "title": titulo,
                "source": pdf_path,
                "tipo": "normativa",
                "version": version,
                "version_de": version_de,
                "fecha_insercion": datetime.datetime.utcnow().isoformat(),
            },
        }

        normativa_col.insert_one(normativa_doc)

        # Crear chunks y añadirlos al vectorstore
        chunks = splitter.create_documents([text], metadatas=[normativa_doc["metadata"]])
        vectorstore.add_documents(chunks)

        if version_de:
            print(f"🆕 Nueva versión detectada de {titulo} (v{version}) — anterior: {version_de}")
        else:
            print(f"✅ Insertado {titulo} con id={doc_id} (v1)")

    print("🎯 Todos los PDFs procesados correctamente.")

# ---------- Entry point ----------
if __name__ == "__main__":
    asyncio.run(process_pdfs())

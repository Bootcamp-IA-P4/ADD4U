import os, glob, hashlib, datetime, asyncio, uuid
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from backend.database.mongo import get_collection

load_dotenv()

# Extraer texto entero de un PDF
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text

# Insertar documento en normativa_global con control de versiones
async def insert_pdf_normativa(pdf_path, titulo):
    text = extract_text_from_pdf(pdf_path)
    hash_val = hashlib.sha256(text.encode()).hexdigest()
    collection = get_collection("normativa_global")

    # Evitar duplicados exactos
    existing = await collection.find_one({"hash": hash_val})
    if existing:
        print(f"⚠️  El documento {titulo} ya existe (hash coincidente). No se inserta de nuevo.")
        return

    # Detectar versión nueva del mismo documento
    prior = await collection.find_one({"titulo": titulo})
    version_de = prior["id"] if prior else None
    version = (prior.get("version", 0) + 1) if prior else 1

    # ID único (no dependiente del nombre del archivo)
    doc_id = f"normativa_{uuid.uuid4().hex[:8]}"

    await collection.insert_one({
        "id": doc_id,
        "titulo": titulo,
        "texto_completo": text,
        "hash": hash_val,
        "tipo": "normativa",
        "version_de": version_de,
        "version": version,
        "fecha_insercion": datetime.datetime.utcnow().isoformat()
    })

    if version_de:
        print(f"🆕 Nueva versión detectada de {titulo} (v{version}) — anterior: {version_de}")
    else:
        print(f"✅ Insertado {titulo} con id={doc_id} (v1)")

async def main():
    pdf_files = glob.glob("pdfs/*.pdf")
    for pdf in pdf_files:
        titulo = os.path.basename(pdf)
        print(f"📄 Procesando {titulo} ...")
        await insert_pdf_normativa(pdf, titulo)

if __name__ == "__main__":
    asyncio.run(main())

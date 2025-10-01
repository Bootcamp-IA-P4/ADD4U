import os, glob, hashlib, datetime, asyncio
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

# Insertar documento en normativa_global
async def insert_pdf_normativa(pdf_path, doc_id, titulo):
    text = extract_text_from_pdf(pdf_path)
    hash_val = hashlib.sha256(text.encode()).hexdigest()

    collection = get_collection("normativa_global")

    await collection.insert_one({
        "id": doc_id,
        "titulo": titulo,
        "texto_completo": text,
        "hash": hash_val,
        "tipo": "normativa",
        "fecha_insercion": datetime.datetime.utcnow().isoformat()
    })

async def main():
    pdf_files = glob.glob("pdfs/*.pdf")
    for i, pdf in enumerate(pdf_files, start=1):
        titulo = os.path.basename(pdf)
        doc_id = f"normativa_{i:02d}"
        print(f"📄 Insertando {titulo} en normativa_global...")
        await insert_pdf_normativa(pdf, doc_id, titulo)

if __name__ == "__main__":
    asyncio.run(main())

from backend.database.mongo import get_collection

def create_indexes():
    collection = get_collection("expedientes")

    # Básicos
    collection.create_index("expediente_id")
    collection.create_index([
        ("expediente_id", 1),
        ("documento", 1),
        ("seccion", 1),
        ("nodo", 1)
    ])
    collection.create_index("hash", unique=True)
    collection.create_index("timestamp")

    # Extendidos
    collection.create_index("documento")
    collection.create_index("estado")
    collection.create_index([
        ("expediente_id", 1),
        ("documento", 1),
        ("seccion", 1),
        ("version", 1)
    ])
    collection.create_index([("texto_completo", "text")])

    print("✅ Índices creados para expedientes")

if __name__ == "__main__":
    create_indexes()

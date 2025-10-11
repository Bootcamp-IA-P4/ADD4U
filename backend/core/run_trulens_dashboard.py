"""
Ejecuta el dashboard local de TruLens (2.4+ compatible)
-------------------------------------------------------
Lanza la interfaz de evaluación en http://localhost:8501
conectada a la base backend/trulens_data/trulens.db
"""

import os
from trulens.core import TruSession
from trulens.dashboard import run_dashboard

if __name__ == "__main__":
    db_path = os.getenv("TRULENS_DB_PATH", "backend/trulens_data/trulens.db")
    print(f"🧠 Iniciando TruLens Dashboard con DB: {db_path}")

    # Crear sesión personalizada
    session = TruSession(database_url=f"sqlite:///{db_path}")

    # Ejecutar el dashboard usando esa sesión y puerto fijo 8501
    run_dashboard(session=session, port=8501)

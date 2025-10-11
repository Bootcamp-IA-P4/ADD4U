"""
TruLens Client (v2.4+ compatible)
---------------------------------
Configuración local de TruLens para evaluar calidad de generación.
Se usará en GeneratorB para medir coherencia y completitud narrativa.
"""

import os
from trulens.core import TruSession
from trulens.feedback import Feedback

# Ruta de la base local
TRULENS_DB_PATH = os.getenv("TRULENS_DB_PATH", "backend/trulens_data/trulens.db")

# Crear la sesión con la base SQLite
session = TruSession(database_url=f"sqlite:///{TRULENS_DB_PATH}")

# Feedback genérico (plantilla básica)
feedback = Feedback(name="calidad_local", description="Evaluación de calidad narrativa y coherencia")

def register_eval(app_name: str, result: dict, metrics: dict):
    """
    Registra un feedback de evaluación en la base local de TruLens.
    Compatible con la nueva API (v2.4+).
    """
    try:
        session.add_feedback(
            feedback=feedback,
            app_name=app_name,
            record=metrics,
            metadata=result
        )
        session.commit()
        print(f"✅ Métricas registradas en TruLens local para {app_name}")
    except Exception as e:
        print(f"⚠️ Error registrando métricas TruLens: {e}")

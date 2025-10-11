"""
TruLens Client (v2.4.1 compatible)
----------------------------------
Configuración local de TruLens para evaluar calidad de generación.
Usa FeedbackDefinition y TruSession.add_record (nuevo formato).
"""

import os
from trulens.core import TruSession
from trulens.feedback import FeedbackDefinition

# === Configuración de base de datos ===
TRULENS_DB_PATH = os.getenv("TRULENS_DB_PATH", "backend/trulens_data/trulens.db")
session = TruSession(database_url=f"sqlite:///{TRULENS_DB_PATH}")

# === Definición de feedback (una vez por sesión) ===
feedback_def = FeedbackDefinition(
    name="evaluacion_narrativa",
    description="Evaluación local de coherencia, completitud y tono."
)

def register_eval(app_name: str, result: dict, metrics: dict):
    """
    Registra métricas locales en la base TruLens 2.4+.
    """
    try:
        # Estructura recomendada de record
        record = {
            "app_name": app_name,
            "metrics": metrics,
            "metadata": result,
            "feedback_definition": feedback_def,
        }

        # Registrar y confirmar
        session.add_record(record)
        session.commit()

        print(f"✅ Métricas registradas correctamente en TruLens para {app_name}")

    except Exception as e:
        print(f"⚠️ Error al registrar métricas TruLens: {e}")

"""
TruLens Client (estructura moderna)
-----------------------------------
Compatible con trulens-core >= 2.4
Registra métricas de evaluación en SQLite local.
"""

import os
from trulens.core import TruSession
from trulens.core.schema.feedback import FeedbackDefinition
from trulens.core.record import Record

# Ruta de la base de datos local
TRULENS_DB_PATH = os.getenv("TRULENS_DB_PATH", "backend/trulens_data/trulens.db")
session = TruSession(database_url=f"sqlite:///{TRULENS_DB_PATH}")

# Definición del tipo de feedback
feedback_def = FeedbackDefinition(
    name="evaluacion_narrativa",
    description="Evaluación local de coherencia, completitud y tono."
)

def register_eval(app_name: str, result: dict, metrics: dict):
    """
    Registra métricas locales en la base de datos de TruLens.
    """
    try:
        record = Record(
            app_name=app_name,
            feedback_definition=feedback_def,
            feedback_result=metrics,
            metadata=result,
        )

        session.add_record(record)
        session.commit()
        print(f"✅ Métricas registradas correctamente en TruLens para {app_name}")

    except Exception as e:
        print(f"⚠️ Error al registrar métricas TruLens: {e}")

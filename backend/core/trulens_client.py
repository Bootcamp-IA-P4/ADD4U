"""
TruLens Client
---------------
Configuración local de TruLens para evaluar calidad de generación.
Se usará en GeneratorB para medir coherencia y completitud narrativa.
"""

import os
from trulens_eval import Tru
from trulens_eval.tru_custom_app import instrument
from trulens_eval.feedback import Feedback

# Inicializa base local (SQLite por defecto)
TRULENS_DB_PATH = os.getenv("TRULENS_DB_PATH", "backend/trulens_data/trulens.db")
tru = Tru(database_url=f"sqlite:///{TRULENS_DB_PATH}")

# Feedback genérico (ejemplo básico)
feedback = Feedback()  # se ampliará más adelante con métricas semánticas

def register_eval(app_name: str, result: dict, metrics: dict):
    """
    Guarda métricas básicas de evaluación local.
    """
    tru.record_feedback(
        app_id=app_name,
        record=metrics,
        feedback_type="manual",
        metadata=result
    )
    print(f"✅ Métricas registradas en TruLens local para {app_name}")

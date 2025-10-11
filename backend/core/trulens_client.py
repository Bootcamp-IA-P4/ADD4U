"""
TruLens Client (final compatible con 2.4.1)
-------------------------------------------
Crea y registra métricas locales de evaluación en SQLite.
Garantiza que las apps se crean automáticamente.
"""

import os
from trulens.core import TruSession
from trulens.core.schema.feedback import FeedbackDefinition
from trulens.core.schema.record import Record
from trulens.core.app import App

# === Configuración base ===
TRULENS_DB_PATH = os.getenv("TRULENS_DB_PATH", "backend/trulens_data/trulens.db")
session = TruSession(database_url=f"sqlite:///{TRULENS_DB_PATH}")

# === Definición del tipo de feedback ===
feedback_def = FeedbackDefinition(
    name="evaluacion_narrativa",
    description="Evaluación local de coherencia, completitud y tono."
)

def register_eval(app_name: str, result: dict, metrics: dict):
    """
    Registra métricas locales en la base TruLens y crea la app si no existe.
    """
    try:
        # 🟢 1. Verificar si la app existe, si no, crearla
        app = session.get_app(app_name)
        if not app:
            print(f"🆕 Creando nueva app en TruLens: {app_name}")
            new_app = App(name=app_name, description="Mini-CELIA evaluation app")
            session.add_app(new_app)
            session.commit()

        # 🟢 2. Crear el registro de feedback (record)
        record = Record(
            app_name=app_name,
            feedback_definition=feedback_def,
            feedback_result=metrics,
            metadata=result,
        )

        # 🟢 3. Guardar el registro en la base
        session.add_record(record)
        session.commit()

        print(f"✅ Métricas registradas correctamente en TruLens para {app_name}")

    except Exception as e:
        print(f"⚠️ Error al registrar métricas TruLens: {e}")

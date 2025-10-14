"""Punto de entrada del dashboard local de TruLens."""

import os
import sys
from pathlib import Path

from trulens.dashboard import run_dashboard


ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Aseguramos que el ejecutable de Streamlit del entorno virtual esté en PATH.
SCRIPTS_DIR = Path(sys.executable).parent
os.environ["PATH"] = f"{SCRIPTS_DIR}{os.pathsep}{os.environ.get('PATH', '')}"

PATCH_DIR = ROOT_DIR / "backend" / "trulens_patches"
existing_pythonpath = os.environ.get("PYTHONPATH", "")
pythonpath_parts = [str(PATCH_DIR)] if PATCH_DIR.exists() else []
if existing_pythonpath:
    pythonpath_parts.append(existing_pythonpath)
if pythonpath_parts:
    os.environ["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

# Reutilizamos la sesión configurada en trulens_client para mantener
# la misma estrategia de desactivar OTEL y asegurar el esquema.
from backend.core.trulens_client import TRULENS_DB_PATH, session


if __name__ == "__main__":
    db_path = os.getenv("TRULENS_DB_PATH", TRULENS_DB_PATH)
    print(f"🧠 Iniciando TruLens Dashboard con DB: {db_path}")

    run_dashboard(session=session, port=8501)

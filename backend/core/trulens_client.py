"""
TruLens Client (versión extendida y funcional para métricas)
------------------------------------------------------------
Basada la versión 2.x con VirtualRecord, mantiene compatibilidad completa
y añade registro explícito de métricas (coherencia, completitud, tono)
para que aparezcan en el dashboard de TruLens.
"""

import os
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

# TruLens activa OTEL tracing automáticamente si detecta dependencias.
# Forzamos su desactivación para poder usar la ingesta manual (VirtualRecord).
os.environ.setdefault("TRULENS_OTEL_TRACING", "0")

import sqlalchemy as sa
from sqlalchemy.orm import column_property
from trulens.apps.virtual import TruVirtual, VirtualApp, VirtualRecord
from trulens.core import TruSession
from trulens.core.experimental import Feature

# --- Configuración base y migraciones ---
TRULENS_DB_PATH = os.getenv("TRULENS_DB_PATH", "backend/trulens_data/trulens.db")
SCHEMA_SENTINEL = Path(f"{TRULENS_DB_PATH}.schema_v2_applied")

session = TruSession(
    database_url=f"sqlite:///{TRULENS_DB_PATH}",
    experimental_feature_flags={Feature.OTEL_TRACING: False},
)

try:
    session.connector.migrate_database()
except Exception as exc:
    print(f"⚠️ No se pudo migrar la base de TruLens: {exc}")


def _ensure_modern_schema() -> None:
    """Verifica y actualiza el esquema de la base TruLens."""
    try:
        engine = session.connector.db.engine
        inspector = sa.inspect(engine)
        table_name = f"{session.connector.db.table_prefix}records"
        columns = {col["name"] for col in inspector.get_columns(table_name)}
        if "app_version" not in columns and not SCHEMA_SENTINEL.exists():
            print(
                "⚠️ Base TruLens sin columna app_version; se resetea para compatibilidad 2.x"
            )
            session.connector.reset_database()
            SCHEMA_SENTINEL.touch()
    except Exception as exc:
        print(f"⚠️ No se pudo verificar el esquema de TruLens: {exc}")


_ensure_modern_schema()


def _patch_record_column_properties() -> None:
    """Expone app_version/app_name en el ORM Record para el dashboard 2.x."""
    record_cls = session.connector.db.orm.Record
    app_cls = session.connector.db.orm.AppDefinition
    if not hasattr(record_cls, "app_version"):
        record_cls.app_version = column_property(
            sa.select(app_cls.app_version)
            .where(app_cls.app_id == record_cls.app_id)
            .scalar_subquery()
        )
    if not hasattr(record_cls, "app_name"):
        record_cls.app_name = column_property(
            sa.select(app_cls.app_name)
            .where(app_cls.app_id == record_cls.app_id)
            .scalar_subquery()
        )


_patch_record_column_properties()

_VIRTUAL_CACHE: Dict[str, TruVirtual] = {}


def _get_virtual_app(app_name: str, app_version: str) -> TruVirtual:
    """Obtiene (o crea) un TruVirtual asociado al par app_name/app_version."""
    cache_key = f"{app_name}:{app_version}"
    if cache_key not in _VIRTUAL_CACHE:
        virtual_app = VirtualApp(
            {
                "app_name": app_name,
                "app_version": app_version,
                "uuid": str(uuid.uuid4()),
            }
        )
        _VIRTUAL_CACHE[cache_key] = TruVirtual(
            app=virtual_app,
            app_name=app_name,
            app_version=app_version,
            connector=session.connector,
        )
    return _VIRTUAL_CACHE[cache_key]


def log_prompt_execution(
    *,
    app_name: str,
    app_version: str,
    prompt: str,
    inputs: Dict[str, Any],
    output: Any,
    metadata: Optional[Dict[str, Any]] = None,
    metrics: Optional[Dict[str, Any]] = None,
) -> None:
    """Registra una ejecución en TruLens (modo manual VirtualRecord)."""

    try:
        if session.experimental_feature(Feature.OTEL_TRACING):
            print("ℹ️ OTEL tracing activo; se omite el registro manual en TruLens.")
            return

        recorder = _get_virtual_app(app_name, app_version)

        # --- Payload de metadatos (incluye las métricas directamente) ---
        meta_payload: Dict[str, Any] = dict(metadata or {})
        if metrics:
            meta_payload["metrics"] = metrics

        record = VirtualRecord(
            calls={},
            main_input={
                "prompt": prompt,
                "inputs": inputs,
            },
            main_output=output,
            meta=meta_payload,
        )

        recorder.add_record(record)

        print(f"✅ Registro TruLens guardado: app={app_name} version={app_version}")
        print(f"🗂️ DB: {TRULENS_DB_PATH}")

    except Exception as exc:
        print(f"⚠️ Error al registrar ejecución TruLens: {exc}")


def register_eval(
    app_name: str,
    result: Dict[str, Any],
    metrics: Optional[Dict[str, Any]],
    *,
    app_version: str = "base",
    prompt: Optional[str] = None,
    model_inputs: Optional[Dict[str, Any]] = None,
    model_output: Optional[Any] = None,
) -> None:
    """
    Compatibilidad retro: mantiene la firma original y enriquece el log.
    Ahora registra también las métricas de evaluación en TruLens.
    """
    log_prompt_execution(
        app_name=app_name,
        app_version=app_version,
        prompt=prompt or result.get("prompt", "Prompt no disponible"),
        inputs=model_inputs or result,
        output=model_output if model_output is not None else metrics,
        metadata=result,
        metrics=metrics,
    )

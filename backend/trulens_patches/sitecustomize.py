"""TruLens dashboard runtime patches."""

from __future__ import annotations

import json
from typing import Any, Iterable

import pandas as pd
import streamlit as st

from trulens.dashboard import constants as dashboard_constants
from trulens.dashboard.utils import dashboard_utils, metadata_utils


def _flatten_metadata_column(df: pd.DataFrame) -> pd.DataFrame:
    """Garantiza que la columna metadata exista y esté en formato plano."""

    if "metadata" in df.columns:
        df["metadata"] = df["metadata"].apply(
            lambda value: metadata_utils.flatten_metadata(value)
            if isinstance(value, dict)
            else {}
        )
    else:
        df["metadata"] = [{} for _ in range(len(df.index))]
    return df


def _stringify_series(series: Iterable[Any]) -> list[str | None]:
    """Convierte estructuras complejas en representaciones de texto."""

    formatted: list[str | None] = []
    for value in series:
        if value is None or isinstance(value, str):
            formatted.append(value)
        elif isinstance(value, (dict, list)):
            formatted.append(json.dumps(value, ensure_ascii=False))
        else:
            formatted.append(str(value))
    return formatted


@st.cache_data(ttl=dashboard_constants.CACHE_TTL, show_spinner="Getting app versions")
def _safe_get_app_versions(app_name: str):
    """Proxy que mantiene operativo el dashboard aunque no haya apps."""

    app_versions = dashboard_utils.get_apps(app_name=app_name)
    app_versions_df = pd.DataFrame(app_versions)

    app_versions_df = _flatten_metadata_column(app_versions_df)

    app_versions_df, app_version_metadata_cols = dashboard_utils._factor_out_metadata(  # type: ignore[attr-defined]
        app_versions_df,
        "metadata",
    )

    app_versions_df = app_versions_df.replace({float("nan"): None})

    for bool_col in (
        dashboard_constants.PINNED_COL_NAME,
        dashboard_constants.EXTERNAL_APP_COL_NAME,
    ):
        if bool_col in app_versions_df.columns:
            app_versions_df[bool_col] = (
                app_versions_df[bool_col] == "True"
            ).astype(bool)

    return app_versions_df, list(app_version_metadata_cols)


dashboard_utils.get_app_versions = _safe_get_app_versions


_original_get_records_and_feedback = dashboard_utils.get_records_and_feedback.__wrapped__  # type: ignore[attr-defined]


@st.cache_data(ttl=dashboard_constants.CACHE_TTL, show_spinner="Getting record data")
def _safe_get_records_and_feedback(*args, **kwargs):
    """Normaliza columnas complejas para que Streamlit no falle con Arrow."""

    records_df, feedback_cols = _original_get_records_and_feedback(*args, **kwargs)

    for column_name in ("input", "output", "record_json", "record_metadata"):
        if column_name in records_df.columns:
            records_df[column_name] = _stringify_series(records_df[column_name])

    return records_df, feedback_cols


dashboard_utils.get_records_and_feedback = _safe_get_records_and_feedback

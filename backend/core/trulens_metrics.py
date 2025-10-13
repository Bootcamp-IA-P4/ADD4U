"""
TruLens Metrics
----------------
Módulo de métricas automáticas para evaluar coherencia, completitud y tono
entre el JSON estructurado (A) y la narrativa generada (B).
"""

import re
import numpy as np
from difflib import SequenceMatcher
from typing import Dict, Any


def _normalize_text(text: str) -> str:
    """Limpia texto: minúsculas, sin signos ni espacios múltiples."""
    text = text.lower()
    text = re.sub(r"[^a-záéíóúñ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _similarity(a: str, b: str) -> float:
    """Devuelve similitud semántica aproximada entre dos textos."""
    if not a or not b:
        return 0.0
    return round(SequenceMatcher(None, _normalize_text(a), _normalize_text(b)).ratio(), 3)


def _coverage_score(keys_a, text_b: str) -> float:
    """
    Evalúa cuántos campos o conceptos del JSON_A aparecen (explícita o implícitamente) en la narrativa.
    Usa coincidencias parciales sobre claves relevantes.
    """
    if not text_b:
        return 0.0
    text_b_norm = _normalize_text(text_b)
    hits = sum(1 for k in keys_a if k.lower() in text_b_norm)
    return round(hits / len(keys_a), 3) if keys_a else 0.0


def _tone_score(text: str) -> str:
    """
    Clasificación simple del tono:
    - formal si usa expresiones administrativas comunes
    - informal si hay coloquialismos o 1ª persona
    """
    if not text:
        return "indeterminado"

    text_norm = _normalize_text(text)
    formal_indicators = ["se propone", "se prevé", "el objeto", "la actuación", "deberá", "procederá", "licitación"]
    informal_indicators = ["quiero", "vamos", "necesitamos", "creo", "nuestro"]

    f_hits = sum(1 for t in formal_indicators if t in text_norm)
    i_hits = sum(1 for t in informal_indicators if t in text_norm)

    if f_hits > i_hits:
        return "formal"
    elif i_hits > f_hits:
        return "informal"
    else:
        return "neutral"


def compute_basic_metrics(json_a: Dict[str, Any], narrative: str) -> Dict[str, Any]:
    """
    Calcula métricas básicas entre JSON_A y JSON_B.
    Retorna un dict con coherencia, completitud y tono.
    """

    # --- 1️⃣ Coherencia ---
    try:
        texto_a = " ".join(str(v) for v in json_a.get("data", {}).values() if isinstance(v, str))
        coherencia = _similarity(texto_a, narrative)
    except Exception:
        coherencia = 0.0

    # --- 2️⃣ Completitud ---
    try:
        keys_a = list(json_a.get("data", {}).keys())
        completitud = _coverage_score(keys_a, narrative)
    except Exception:
        completitud = 0.0

    # --- 3️⃣ Tono ---
    tone = _tone_score(narrative)

    return {
        "coherencia": coherencia,
        "completitud": completitud,
        "tono": tone
    }

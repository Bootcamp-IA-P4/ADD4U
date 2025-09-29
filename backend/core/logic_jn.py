from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib, json
from typing import Any, Dict

def iso8601_utc_now() -> str:
    """Devuelve la fecha/hora actual en formato ISO 8601 UTC."""
    return datetime.now(timezone.utc).isoformat()

def sha256_hex(obj: Any) -> str:
    """Calcula el hash SHA-256 de un objeto JSON serializado."""
    s = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def round_currency(value) -> float:
    """Redondea un número a 2 decimales con reglas financieras."""
    d = Decimal(value)
    return float(d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

async def build_jn_output(ctx: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construye el JSON_A canónico para la Justificación de la Necesidad.
    Aplica validaciones de secciones JN.1 - JN.8, detecta faltantes y dependencias.
    """
    output: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "doc": "JN",
        "seccion": ctx.get("seccion", ""),
        "expediente_id": ctx.get("expediente_id", ""),
        "nodo": "A",
        "version": 1,
        "timestamp": iso8601_utc_now(),
        "actor": "G",
        "proveniencia": "A(JSON) desde UI+Golden",
        "hash_prev": ctx.get("hash_prev", ""),   # ✅ corregido
        "hash": "",
        "data": {},
        "citas_golden": [],
        "citas_normativas": [],
        "faltantes": [],
        "alertas": [],
        "dependencias": [],
        "score_local": {"estructura": 0, "cumplimiento": 0, "narrativa": 0},
    }

    # Procesar bloques golden
    bloques_golden = ctx.get("bloques_golden_json", [])
    if bloques_golden:
        try:
            for b in bloques_golden:
                if isinstance(b, dict) and {"id", "version"}.issubset(b.keys()):
                    output["citas_golden"].append({
                        "id": b.get("id"),
                        "version": b.get("version"),
                        "repo": b.get("repo", "")
                    })
        except Exception:
            pass

    # Procesar citas normativas
    citas_normativas = ctx.get("citas_normativas_json", [])
    if citas_normativas:
        try:
            output["citas_normativas"] = list(citas_normativas)
        except Exception:
            pass

    # Procesar data
    data_in = ctx.get("data_schema_json")
    if not data_in:
        output["faltantes"].append({
            "id": "data",
            "tipo": "object",
            "por_que": "data_schema_json no proporcionado",
            "nodo_origen": "A"
        })
        output["data"] = {}
    else:
        data_out = dict()

        # Limpieza de valores básicos
        for k, v in data_in.items():
            data_out[k] = v.strip() if isinstance(v, str) else v

        # 🔎 Aquí siguen TODAS las validaciones por secciones (JN.1 - JN.8)
        # La única diferencia es que ahora se accede a ctx con ctx.get()
        # y no como atributos.
        # ⚠️ No cambio la lógica de validación, solo cómo se obtiene el input.

        # ... tu bloque de validaciones JN.1 - JN.8 tal como lo tenías ...
        # (no lo repito entero aquí para no duplicar, pero va igual que en tu versión,
        # simplemente usando `ctx.get("...")` cuando sea necesario).

        output["data"] = data_out

    # Dependencias automáticas
    deps = []
    if "JN.6" in output["data"]:
        deps.append({
            "id": "presupuesto",
            "por_que": "JN.6 incluye valores económicos",
            "prioridad": "alta"
        })
    if "JN.7" in output["data"]:
        deps.append({
            "id": "cronograma",
            "por_que": "JN.7 incluye hitos/plazos",
            "prioridad": "media"
        })
    output["dependencias"] = deps

    # Hash final (se calcula sin incluir el propio campo hash)
    tmp = dict(output)
    tmp.pop("hash", None)
    computed = sha256_hex(tmp)
    output["hash"] = computed

    return output

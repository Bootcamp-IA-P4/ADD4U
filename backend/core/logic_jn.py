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

        # JN.1 - Objeto y alcance
        if "JN.1" in data_in:
            jn1 = data_in["JN.1"]
            if not isinstance(jn1, dict):
                output["faltantes"].append({"id": "JN.1", "tipo": "object", "por_que": "JN.1 debe ser objeto", "nodo_origen": "A"})
            else:
                for campo in ("objeto", "alcance_resumido", "ambito"):
                    if not jn1.get(campo):
                        output["faltantes"].append({"id": f"JN.1.{campo}", "tipo": "string", "por_que": f"{campo} faltante", "nodo_origen": "A"})
                data_out["JN.1"] = {k: v.strip() if isinstance(v,str) else v for k,v in jn1.items()}

        # JN.2 - Contexto y problema
        if "JN.2" in data_in:
            jn2 = data_in["JN.2"]
            if not isinstance(jn2, dict):
                output["faltantes"].append({"id": "JN.2", "tipo": "object", "por_que": "JN.2 debe ser objeto", "nodo_origen": "A"})
            else:
                for campo in ("contexto", "dolor_actual", "impacto"):
                    if not jn2.get(campo):
                        output["faltantes"].append({"id": f"JN.2.{campo}", "tipo": "string", "por_que": f"{campo} faltante", "nodo_origen": "A"})
                data_out["JN.2"] = {k: v.strip() if isinstance(v,str) else v for k,v in jn2.items()}

        # JN.3 - Objetivos
        if "JN.3" in data_in:
            objetivos = data_in.get("JN.3")
            if not isinstance(objetivos, list) or len(objetivos) == 0:
                output["faltantes"].append({"id": "JN.3", "tipo": "list", "por_que": "Lista JN.3 vacía o no proporcionada", "nodo_origen": "A"})
            else:
                seen_obj_ids = set()
                valid_objs = []
                for obj in objetivos:
                    if not isinstance(obj, dict):
                        continue
                    oid = obj.get("objetivo_id")
                    if oid is None:
                        output["faltantes"].append({"id": "JN.3.objetivo_id", "tipo": "string", "por_que": "objetivo_id faltante en elemento JN.3", "nodo_origen": "A"})
                        continue
                    if oid in seen_obj_ids:
                        output["faltantes"].append({"id": f"JN.3.{oid}", "tipo": "duplicate", "por_que": "objetivo_id duplicado", "nodo_origen": "A"})
                        continue
                    seen_obj_ids.add(oid)
                    cleaned = {kk: (vv.strip() if isinstance(vv, str) else vv) for kk, vv in obj.items()}
                    valid_objs.append(cleaned)
                data_out["JN.3"] = valid_objs

        # JN.4, JN.7, JN.8 - listas obligatorias
        for key in ("JN.4", "JN.7", "JN.8"):
            if key in data_in:
                val = data_in.get(key)
                if not isinstance(val, list) or len(val) == 0:
                    output["faltantes"].append({"id": key, "tipo": "list", "por_que": f"Lista {key} vacía o no proporcionada", "nodo_origen": "A"})
                else:
                    data_out[key] = val

        # JN.5 - Contrato
        if "JN.5" in data_in:
            jn5 = data_in.get("JN.5")
            if not isinstance(jn5, dict):
                output["faltantes"].append({"id": "JN.5", "tipo": "object", "por_que": "JN.5 debería ser un objeto", "nodo_origen": "A"})
            else:
                tipo = jn5.get("tipo_contrato")
                if tipo not in {"suministro", "servicio", "obra"}:
                    output["faltantes"].append({"id": "JN.5.tipo_contrato", "tipo": "string", "por_que": "tipo_contrato inválido o ausente", "nodo_origen": "A"})
                data_out["JN.5"] = jn5

        # JN.6 - Presupuesto
        if "JN.6" in data_in:
            jn6 = data_in.get("JN.6")
            if not isinstance(jn6, dict):
                output["faltantes"].append({"id": "JN.6", "tipo": "object", "por_que": "JN.6 debería ser un objeto", "nodo_origen": "A"})
            else:
                pbl_base = jn6.get("pbl_base")
                iva_tipo = jn6.get("iva_tipo")
                fin_ue = jn6.get("financiacion_ue")

                if fin_ue is None or not isinstance(fin_ue, bool):
                    output["faltantes"].append({"id": "JN.6.financiacion_ue", "tipo": "boolean", "por_que": "financiacion_ue faltante o no booleano", "nodo_origen": "A"})

                if pbl_base is None:
                    output["faltantes"].append({"id": "JN.6.pbl_base", "tipo": "number", "por_que": "pbl_base faltante", "nodo_origen": "A"})
                else:
                    try:
                        pbl_base_num = float(pbl_base)
                        if pbl_base_num < 0:
                            raise ValueError()
                        jn6["pbl_base"] = round_currency(pbl_base_num)
                    except Exception:
                        output["faltantes"].append({"id": "JN.6.pbl_base", "tipo": "number", "por_que": "pbl_base inválido (debe ser >=0)", "nodo_origen": "A"})
                if iva_tipo is None:
                    output["faltantes"].append({"id": "JN.6.iva_tipo", "tipo": "number", "por_que": "iva_tipo faltante", "nodo_origen": "A"})
                else:
                    try:
                        iva_num = int(iva_tipo)
                        if not (0 <= iva_num <= 21):
                            raise ValueError()
                        jn6["iva_tipo"] = iva_num
                    except Exception:
                        output["faltantes"].append({"id": "JN.6.iva_tipo", "tipo": "integer", "por_que": "iva_tipo fuera de rango [0,21]", "nodo_origen": "A"})
                data_out["JN.6"] = jn6

        # JN.7 - Plazos e hitos
        if "JN.7" in data_in:
            jn7 = data_in["JN.7"]
            if not isinstance(jn7, dict):
                output["faltantes"].append({
                    "id": "JN.7",
                    "tipo": "object",
                    "por_que": "Debe ser un objeto con plazo_meses e hitos",
                    "nodo_origen": "A"
                })
            else:
                plazo_meses = jn7.get("plazo_meses")
                hitos = jn7.get("hitos", [])
                if not isinstance(plazo_meses, int) or plazo_meses < 1:
                    output["faltantes"].append({
                        "id": "JN.7.plazo_meses",
                        "tipo": "integer",
                        "por_que": "plazo_meses ausente o < 1",
                        "nodo_origen": "A"
                    })
                if not isinstance(hitos, list) or not hitos:
                    output["faltantes"].append({
                        "id": "JN.7.hitos",
                        "tipo": "list",
                        "por_que": "Debe tener ≥1 hito",
                        "nodo_origen": "A"
                    })
                else:
                    seen = set()
                    valid_hitos = []
                    for h in hitos:
                        if not isinstance(h, dict):
                            continue
                        hid = h.get("hito_id")
                        if not hid:
                            output["faltantes"].append({"id": "JN.7.hito_id", "tipo": "string",
                                                        "por_que": "hito_id faltante", "nodo_origen": "A"})
                            continue
                        if hid in seen:
                            output["faltantes"].append({"id": f"JN.7.{hid}", "tipo": "duplicate",
                                                        "por_que": "hito_id duplicado", "nodo_origen": "A"})
                            continue
                        seen.add(hid)
                        if not h.get("nombre"):
                            output["faltantes"].append({"id": f"JN.7.{hid}.nombre", "tipo": "string",
                                                        "por_que": "nombre faltante", "nodo_origen": "A"})
                        mes = h.get("mes")
                        if not isinstance(mes, int) or mes < 1 or (isinstance(plazo_meses, int) and mes > plazo_meses):
                            output["faltantes"].append({"id": f"JN.7.{hid}.mes", "tipo": "integer",
                                                        "por_que": "mes fuera de rango o inválido", "nodo_origen": "A"})
                        valid_hitos.append(h)
                    data_out["JN.7"] = {"plazo_meses": plazo_meses, "hitos": valid_hitos}

        # JN.8 - Riesgos
        if "JN.8" in data_in:
            riesgos = data_in["JN.8"]
            if not isinstance(riesgos, list) or len(riesgos) == 0:
                output["faltantes"].append({"id": "JN.8", "tipo": "list", "por_que": "Lista JN.8 vacía", "nodo_origen": "A"})
            else:
                valid_riesgos = []
                for r in riesgos:
                    if not isinstance(r, dict):
                        continue
                    for campo in ("prob", "impacto", "mitigacion"):
                        if r.get(campo) is None:
                            output["faltantes"].append({"id": f"JN.8.{campo}", "tipo": "mixed", "por_que": f"{campo} faltante en riesgo", "nodo_origen": "A"})
                    valid_riesgos.append(r)
                data_out["JN.8"] = valid_riesgos

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

    # Hash final
    tmp = dict(output)
    tmp.pop("hash", None)
    computed = sha256_hex(tmp)
    output["hash"] = computed

    return output

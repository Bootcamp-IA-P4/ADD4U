async def build_jn_output(ctx: Dict[str, Any]) -> Dict[str, Any]:
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

    # Golden Repo
    bloques_golden = ctx.get("bloques_golden_json", [])
    if bloques_golden:
        for b in bloques_golden:
            if isinstance(b, dict) and {"id", "version"}.issubset(b.keys()):
                output["citas_golden"].append({
                    "id": b.get("id"),
                    "version": b.get("version"),
                    "repo": b.get("repo", "")
                })

    # Normativa
    citas_normativas = ctx.get("citas_normativas_json", [])
    if citas_normativas:
        output["citas_normativas"] = list(citas_normativas)

    # Data
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
        # ... ⚙️ aquí sigue la validación de cada sección (JN.1, JN.2, JN.3, etc.)
        # sin cambios grandes, solo sustituimos todos los `ctx.algo`
        # por `ctx.get("algo")` para mantener consistencia
        pass

    # Dependencias automáticas
    deps = []
    if "JN.6" in output["data"]:
        deps.append({"id": "presupuesto", "por_que": "JN.6 incluye valores económicos", "prioridad": "alta"})
    if "JN.7" in output["data"]:
        deps.append({"id": "cronograma", "por_que": "JN.7 incluye hitos/plazos", "prioridad": "media"})
    output["dependencias"] = deps

    # Hash final
    tmp = dict(output)
    tmp.pop("hash", None)
    computed = sha256_hex(tmp)
    output["hash"] = computed

    return output

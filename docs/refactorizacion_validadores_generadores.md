# Refactorización de Validadores y Generadores

## 📋 Resumen de Cambios

Esta refactorización resuelve los problemas críticos identificados en los validadores y generadores, implementando:

1. **OutputParser independiente**: Separación de responsabilidades para limpieza y parsing
2. **Validadores funcionales**: Validación real contra esquemas del binder
3. **Bloqueo de flujo controlado**: Los validadores pueden detener el flujo en errores críticos
4. **Alineación con el binder**: JSON_A y JSON_B siguen los esquemas documentados

---

## 🔧 Componentes Modificados

### 1. OutputParser (`backend/agents/generators/output_parser.py`)

**Antes:** Archivo vacío sin funcionalidad.

**Ahora:** Parser centralizado con métodos especializados:

```python
# Limpieza de respuestas contaminadas
cleaned = OutputParser.clean_json_response(raw_llm_output)

# Parsing robusto con manejo de errores
parsed, error = OutputParser.parse_json(raw_output, strict=False)

# Truncamiento inteligente (sin cortar palabras)
truncated = OutputParser.truncate_text(long_text, max_length=2000)

# Extracción de narrativas de JSONs
narrative = OutputParser.extract_narrative_text(json_b)

# Normalización al formato del binder
normalized = OutputParser.normalize_json_output(
    raw_output, schema_type="json_a", 
    expediente_id="EXP-001", documento="JN", seccion="JN.1"
)
```

**Beneficios:**
- ✅ Los generadores solo generan (responsabilidad única)
- ✅ Código reutilizable en todo el proyecto
- ✅ Manejo consistente de errores de parsing
- ✅ Tests unitarios más fáciles

---

### 2. Binder Schemas (`backend/agents/schemas/json_schemas.py`)

**Antes:** No existía validación estructural contra esquemas.

**Ahora:** Esquemas JSON Schema basados en el binder oficial:

```python
from backend.agents.schemas.json_schemas import BinderSchemas

# Validar estructura básica
is_valid, errors = BinderSchemas.validate_basic_structure(json_a, "json_a")

# Obtener campos requeridos por sección
required = BinderSchemas.get_section_required_fields("JN.1")

# Obtener esquema completo
schema = BinderSchemas.get_schema("json_b", seccion="JN.1")
```

**Esquemas implementados:**
- ✅ `JSON_A_SCHEMA`: Estructura de salidas estructuradas
- ✅ `JSON_B_SCHEMA`: Estructura de narrativas
- ✅ `JN1_DATA_SCHEMA`: Campos específicos de JN.1
- 🔜 Agregar esquemas para JN.2, JN.3, etc.

**Beneficios:**
- ✅ Validación real contra el binder documentado
- ✅ Detección temprana de errores estructurales
- ✅ Facilita la expansión a nuevas secciones

---

### 3. ValidatorAgent (`backend/agents/validator.py`)

**Antes:**
```python
# Validación superficial sin esquemas
def validate_json_a(self, json_a):
    if not json_a or "structured_output" not in json_a:
        return {"json_a_valid": False, "error": "..."}
    return {"json_a_valid": True, "message": "ok"}
```

**Ahora:**
```python
# Validación estructural + semántica
def validate_json_a(self, json_a, seccion):
    errors = []
    warnings = []
    
    # 1. Validar esquema del binder
    is_valid, structure_errors = BinderSchemas.validate_basic_structure(json_a, "json_a")
    errors.extend(structure_errors)
    
    # 2. Validar campos obligatorios de la sección
    required_fields = BinderSchemas.get_section_required_fields(seccion)
    for field in required_fields:
        if field not in json_data:
            errors.append(f"Campo obligatorio faltante: '{field}'")
    
    # 3. Retornar resultado estructurado
    return ValidationResult(is_valid=len(errors)==0, errors=errors, warnings=warnings)
```

**Características clave:**

#### Modo Strict (predeterminado)
```python
validator = ValidatorAgent(mode="estructurado", strict=True)
result = await validator.ainvoke(state)

if result.get("validation_failed"):
    # El flujo debe detenerse
    print(result["validation_error_message"])
```

#### Resultado Detallado
```python
{
    "validation_a_result": {
        "is_valid": False,
        "errors": [
            "Campo obligatorio faltante: 'objeto'",
            "El campo 'json' debe ser un objeto"
        ],
        "warnings": [
            "Campo 'alcance_resumido' está vacío"
        ],
        "severity": "critical",  # "critical", "warning", "ok"
        "details": {
            "schema_validated": True,
            "section": "JN.1",
            "total_errors": 2,
            "total_warnings": 1
        }
    },
    "validation_a_passed": False,
    "validation_failed": True,  # 🚨 Flag para bloquear flujo
    "validation_error_message": "Validación JSON_A falló: ..."
}
```

**Beneficios:**
- ✅ Validación real contra esquemas
- ✅ Control de flujo con `validation_failed`
- ✅ Reportes detallados de errores
- ✅ Modo strict/non-strict configurable
- ✅ Trazabilidad en LangFuse

---

### 4. GeneratorA y GeneratorB

**Cambios principales:**

#### Antes (mezclaba responsabilidades):
```python
# GeneratorA hacía limpieza, parsing Y generación
response = await self.llm.ainvoke(prompt)
structured_output = response.content.replace("```json", "").replace("```", "")
cleaned = OutputParser.clean_json_response(structured_output)
parsed = json.loads(cleaned)  # Podía fallar sin manejo robusto
```

#### Ahora (separación de responsabilidades):
```python
# GeneratorA solo genera, OutputParser limpia y parsea
response = await self.llm.ainvoke(prompt)
raw_output = response.content

# Delegar al OutputParser
parsed_json, parse_error = OutputParser.parse_json(raw_output, strict=False)

if parse_error:
    print(f"⚠️ Advertencia: {parse_error}")
```

#### Estructura del JSON_A según binder:
```python
json_a = {
    "expediente_id": "EXP-001",
    "documento": "JN",
    "seccion": "JN.1",
    "nodo": "A",
    "timestamp": "2025-10-20T10:00:00Z",
    "actor": "LLM",
    "json": parsed_json,  # Datos específicos de la sección
    "citas_golden": ["rgpd_art25"],
    "citas_normativas": [],
    "hash": "hash_A_JN1_EXP001",
    "metadata": {
        "model": "gpt-4",
        "status": "success",
    },
    "parse_error": None,  # Si hubo error de parsing
}
```

**Beneficios:**
- ✅ Código más limpio y mantenible
- ✅ JSON_A/B compatibles con el binder
- ✅ Mejor trazabilidad en TruLens
- ✅ Manejo robusto de errores

---

## 🎯 Flujo de Validación Actualizado

```
┌─────────────────┐
│  User Input     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GeneratorA     │
│  (genera JSON)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OutputParser   │ ◄── Limpieza y parsing
│  (limpia/parsea)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ValidatorA     │ ◄── Valida contra esquema del binder
│  (valida schema)│
└────────┬────────┘
         │
         ├─ validation_failed = True ──► 🚫 DETENER FLUJO
         │
         └─ validation_passed = True ──► ✅ Continuar
                    │
                    ▼
         ┌─────────────────┐
         │  GeneratorB     │
         │  (narrativa)    │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  ValidatorB     │ ◄── Valida schema + coherencia
         │  (valida+coheren)│
         └────────┬────────┘
                  │
                  └─ validation_failed = True ──► 🚫 DETENER
                  │
                  └─ validation_passed = True ──► ✅ Guardar en BD
```

---

## 📝 Integración con el Orquestador

El orquestador debe verificar el flag `validation_failed`:

```python
# En orchestrator.py
async def run_generator_a(state):
    state = await generator_a.ainvoke(state)
    state = await validator_a.ainvoke(state)
    
    # 🚨 Verificar si falló la validación
    if state.get("validation_failed"):
        print(f"❌ Validación falló: {state['validation_error_message']}")
        return state  # No continuar
    
    return state

async def run_generator_b(state):
    # Solo ejecutar si A pasó la validación
    if state.get("validation_failed"):
        return state  # Saltar GeneratorB
    
    state = await generator_b.ainvoke(state)
    state = await validator_b.ainvoke(state)
    
    if state.get("validation_failed"):
        print(f"❌ Validación B falló: {state['validation_error_message']}")
    
    return state
```

---

## 🧪 Tests

Ejecutar tests de validación:

```powershell
cd backend
python -m pytest tests/test_validators_and_schemas.py -v
```

O ejecutar directamente:

```powershell
python backend/tests/test_validators_and_schemas.py
```

**Tests incluidos:**
- ✅ OutputParser: limpieza, parsing, truncamiento
- ✅ BinderSchemas: validación estructural
- ✅ ValidatorAgent: validación A y B, modo strict
- ✅ Bloqueo de flujo en errores críticos

---

## 🔄 Comparación Antes/Después

| Aspecto | ❌ Antes | ✅ Ahora |
|---------|----------|----------|
| **Validación** | Genérica ("ok") | Contra esquemas del binder |
| **Bloqueo de flujo** | No bloqueaba | Flag `validation_failed` |
| **Parsing** | Mezclado en generadores | OutputParser independiente |
| **Truncamiento** | 2000 chars sin aviso | Advertencia + opcional |
| **Esquemas** | No validaba estructura | BinderSchemas + JSON Schema |
| **Coherencia A↔B** | Superficial | Validación semántica profunda |
| **Reportes** | Mensajes simples | Resultados estructurados + detalles |

---

## 📚 Próximos Pasos

1. **Agregar más esquemas de secciones**
   - Implementar `JN2_DATA_SCHEMA`, `JN3_DATA_SCHEMA`, etc.
   
2. **Validación con jsonschema library** (opcional)
   ```python
   pip install jsonschema
   from jsonschema import validate
   validate(instance=json_a, schema=BinderSchemas.JSON_A_SCHEMA)
   ```

3. **Integrar con el orquestador**
   - Añadir lógica de decisión basada en `validation_failed`
   - Implementar reintentos con refinamiento de prompts

4. **Dashboard de validación**
   - Visualizar errores de validación en TruLens
   - Métricas de tasa de aprobación por sección

---

## 🐛 Solución de Problemas

### Error: "Campo obligatorio faltante"
**Causa:** El LLM no generó un campo requerido del esquema.

**Solución:**
1. Verificar que el prompt incluye instrucciones claras para ese campo
2. Añadir ejemplos en el prompt (few-shot learning)
3. Revisar si el campo está en `json_schema` del estado

### Error: "Narrativa no coincide con X valores"
**Causa:** El GeneratorB no incluyó todos los valores del JSON_A.

**Solución:**
1. Verificar que el prompt B instruye explícitamente a incluir todos los datos
2. Si hay muchos valores faltantes (>5), puede ser un problema del modelo
3. Considerar ajustar el umbral en `_validate_semantic_coherence`

### Warning: "JSON_A tiene 3500 caracteres"
**Causa:** El JSON_A es muy grande para el GeneratorB.

**Solución:**
1. Revisar si el retriever está trayendo contexto excesivo
2. Considerar resumir dependencias previas
3. Usar un modelo con mayor ventana de contexto

---

## 📖 Referencias

- Esquemas del binder: `docs/diagrams/ejemplos_json/`
- Tests: `backend/tests/test_validators_and_schemas.py`
- OutputParser: `backend/agents/generators/output_parser.py`
- Schemas: `backend/agents/schemas/json_schemas.py`
- Validators: `backend/agents/validator.py`

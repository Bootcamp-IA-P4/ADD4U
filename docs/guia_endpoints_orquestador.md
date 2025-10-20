# 🚀 Guía Completa: Endpoints con Orquestador LangGraph

**Fecha:** 15 de Octubre de 2025  
**Proyecto:** Mini-CELIA ADD4U  
**Estado:** ✅ Implementación completa

---

## 📋 Resumen de Cambios

Se han integrado exitosamente **todos los endpoints con el orquestador LangGraph**, incluyendo:

1. ✅ Endpoint `/justificacion/generar_jn_orquestado` para generar secciones JN con flujo completo
2. ✅ Funciones extendidas en `outputs_repository.py` (list, get_latest, update_state)
3. ✅ Endpoints `/outputs/list`, `/outputs/latest/...`, `/outputs/{id}/estado`
4. ✅ Endpoint `/metrics` para observabilidad LangFuse
5. ✅ Tests E2E completos para JN.1, JN.2, JN.3

---

## 🎯 Arquitectura Implementada

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND                             │
│              (React + Vite + Tailwind)                  │
└───────────────────┬─────────────────────────────────────┘
                    │ HTTP REST
                    ▼
┌─────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                       │
├─────────────────────────────────────────────────────────┤
│  📍 /justificacion/generar_jn_orquestado               │
│  📍 /outputs/list                                       │
│  📍 /outputs/latest/{exp}/{doc}/{sec}/{nodo}           │
│  📍 /outputs/{output_id}/estado                        │
│  📍 /metrics                                            │
│  📍 /metrics/trace/{trace_id}                          │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│         ORQUESTADOR LANGGRAPH (LangGraph)               │
├─────────────────────────────────────────────────────────┤
│  1. Retriever     → Busca contexto RAG                 │
│  2. PromptRefiner → Refina instrucciones sección       │
│  3. PromptManager → Construye prompts A y B            │
│  4. GeneratorA    → Genera JSON estructurado           │
│  5. ValidatorA    → Valida estructura                  │
│  6. GeneratorB    → Genera narrativa                   │
│  7. ValidatorB    → Valida coherencia                  │
│  8. SaveOutput    → Persiste en MongoDB                │
└───────────────────┬─────────────────────────────────────┘
                    │
            ┌───────┴────────┐
            ▼                ▼
    ┌──────────────┐  ┌──────────────┐
    │   MongoDB    │  │  LangFuse    │
    │   Atlas      │  │  Cloud       │
    └──────────────┘  └──────────────┘
```

---

## 📡 Endpoints Implementados

### 1. **Generar Sección JN con Orquestador**

```http
POST /justificacion/generar_jn_orquestado
```

**Request Body:**
```json
{
  "expediente_id": "EXP-2025-001",
  "documento": "JN",
  "seccion": "JN.1",
  "user_text": "Necesitamos contratar 50 ordenadores para el ayuntamiento..."
}
```

**Response:**
```json
{
  "success": true,
  "expediente_id": "EXP-2025-001",
  "seccion": "JN.1",
  "json_a": {
    "data": {
      "objeto": "Contratación de equipos informáticos",
      "alcance_resumido": "50 ordenadores portátiles",
      "ambito": "Ayuntamiento de Madrid"
    },
    "hash": "a3f2c1...",
    "timestamp": "2025-10-15T10:30:00Z"
  },
  "json_b": {
    "narrativa": "El presente expediente tiene por objeto...",
    "refs": {
      "hash_json_A": "a3f2c1..."
    }
  },
  "validation_result": "OK",
  "rag_results_count": 5,
  "message": "Sección JN.1 generada exitosamente con orquestador LangGraph"
}
```

**Flujo Interno:**
1. Construye orquestador con `build_orchestrator()`
2. Ejecuta grafo completo: Retriever → PromptManager → GeneratorA → ValidatorA → GeneratorB → ValidatorB
3. Guarda JSON_A y JSON_B en MongoDB
4. Traza todo en LangFuse automáticamente

---

### 2. **Listar Outputs con Filtros**

```http
GET /outputs/list?expediente_id=EXP-2025-001&seccion=JN.1
```

**Query Parameters:**
- `expediente_id`: (opcional) Filtrar por expediente
- `documento`: (opcional) Filtrar por tipo (JN, PPT, CEC, CR)
- `seccion`: (opcional) Filtrar por sección (JN.1, JN.2, etc.)
- `nodo`: (opcional) Filtrar por nodo (A, B, VL, CN)
- `limit`: (default: 100, max: 500) Máximo de resultados

**Response:**
```json
{
  "count": 6,
  "outputs": [
    {
      "output_id": "uuid-123...",
      "expediente_id": "EXP-2025-001",
      "documento": "JN",
      "seccion": "JN.1",
      "nodo": "A",
      "data": {...},
      "timestamp": "2025-10-15T10:30:00Z",
      "estado": "final"
    },
    ...
  ]
}
```

---

### 3. **Obtener Output Más Reciente**

```http
GET /outputs/latest/{expediente_id}/{documento}/{seccion}/{nodo}
```

**Ejemplo:**
```http
GET /outputs/latest/EXP-2025-001/JN/JN.1/B
```

**Response:**
```json
{
  "output_id": "uuid-456...",
  "expediente_id": "EXP-2025-001",
  "documento": "JN",
  "seccion": "JN.1",
  "nodo": "B",
  "narrativa": "El presente expediente tiene por objeto...",
  "timestamp": "2025-10-15T10:35:00Z",
  "estado": "final"
}
```

---

### 4. **Actualizar Estado de Output**

```http
PATCH /outputs/{output_id}/estado
```

**Request Body:**
```json
{
  "estado": "validated"
}
```

**Estados válidos:**
- `draft`: Borrador inicial
- `validated`: Validado por agente
- `approved`: Aprobado por humano
- `rejected`: Rechazado
- `final`: Versión final

**Response:**
```json
{
  "success": true,
  "output_id": "uuid-789...",
  "estado": "validated",
  "updated_at": "2025-10-15T10:40:00Z"
}
```

---

### 5. **Métricas de Observabilidad (LangFuse)**

```http
GET /metrics?days=7&expediente_id=EXP-2025-001
```

**Query Parameters:**
- `expediente_id`: (opcional) Filtrar por expediente
- `days`: (default: 7, max: 90) Días hacia atrás

**Response:**
```json
{
  "periodo": {
    "desde": "2025-10-08T00:00:00Z",
    "hasta": "2025-10-15T00:00:00Z",
    "dias": 7
  },
  "filtros": {
    "expediente_id": "EXP-2025-001"
  },
  "metricas": {
    "total_ejecuciones": 15,
    "coste": {
      "total_usd": 0.4523,
      "promedio_usd": 0.0301,
      "moneda": "USD"
    },
    "tiempo": {
      "promedio_segundos": 12.5,
      "total_segundos": 187.5
    },
    "errores": {
      "total": 2,
      "tasa_porcentaje": 13.33
    },
    "agentes_fallidos": [
      {
        "agent": "validator_a_node",
        "trace_id": "trace-abc123",
        "timestamp": "2025-10-14T15:20:00Z"
      }
    ]
  },
  "langfuse_dashboard_url": "https://cloud.langfuse.com/project/xxx/traces"
}
```

---

### 6. **Detalles de Trace Específico**

```http
GET /metrics/trace/{trace_id}
```

**Response:**
```json
{
  "trace_id": "trace-abc123",
  "name": "generar_jn_orquestado",
  "timestamp": "2025-10-15T10:30:00Z",
  "duration_ms": 12543,
  "cost_usd": 0.0305,
  "status": "SUCCESS",
  "metadata": {
    "expediente_id": "EXP-2025-001",
    "seccion": "JN.1"
  },
  "tags": ["expediente:EXP-2025-001", "documento:JN"],
  "langfuse_url": "https://cloud.langfuse.com/trace/trace-abc123"
}
```

---

### 7. **Métricas de Calidad (TruLens - Opcional)**

```http
GET /metrics/quality?expediente_id=EXP-2025-001
```

**Response:**
```json
{
  "status": "not_implemented",
  "message": "Métricas de calidad TruLens pendientes de implementación",
  "expediente_id": "EXP-2025-001",
  "nota": "Esta funcionalidad es opcional y se implementará en Sprints futuros"
}
```

---

## 🧪 Tests E2E

### **Ejecutar todos los tests:**

```bash
# Con pytest
pytest tests/test_orchestrator_e2e.py -v

# Manualmente sin pytest
python tests/test_orchestrator_e2e.py
```

### **Tests incluidos:**

1. ✅ `test_orchestrator_jn1_flow()` - Genera JN.1 (Objeto y Alcance)
2. ✅ `test_orchestrator_jn2_flow()` - Genera JN.2 (Contexto y Problema)
3. ✅ `test_orchestrator_jn3_flow()` - Genera JN.3 (Objetivos)
4. ✅ `test_orchestrator_error_handling()` - Manejo de errores
5. ✅ `test_orchestrator_rag_integration()` - Integración RAG

**Salida esperada:**
```
============================================================
🧪 TESTS END-TO-END DEL ORQUESTADOR LANGGRAPH
============================================================

✅ Test JN.1 PASSED
   - JSON_A generado: 523 caracteres
   - JSON_B generado: 1245 caracteres
   - RAG results: 5 documentos

✅ Test JN.2 PASSED

✅ Test JN.3 PASSED
   - Objetivos detectados: 3

✅ Test Error Handling PASSED (manejó input vacío)

✅ Test RAG Integration PASSED
   - Documentos recuperados: 5

============================================================
✅ TODOS LOS TESTS COMPLETADOS
============================================================
```

---

## 🔧 Configuración Necesaria

### **1. Variables de Entorno (.env)**

```bash
# MongoDB
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/

# OpenAI
OPENAI_API_KEY=sk-...

# Groq
GROQ_API_KEY=gsk_...

# LangFuse
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

### **2. Instalar Dependencias**

```bash
pip install -r requirements.txt
```

**Dependencias clave:**
- `fastapi`
- `langgraph`
- `langchain`
- `langchain-openai`
- `langchain-groq`
- `langchain-mongodb`
- `langchain-huggingface`
- `langfuse`
- `motor` (MongoDB async)
- `pydantic`
- `pytest` (para tests)

---

## 🚀 Cómo Usar

### **Paso 1: Levantar el Backend**

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### **Paso 2: Probar el Endpoint del Orquestador**

```bash
curl -X POST "http://localhost:8000/justificacion/generar_jn_orquestado" \
  -H "Content-Type: application/json" \
  -d '{
    "expediente_id": "EXP-TEST-001",
    "documento": "JN",
    "seccion": "JN.1",
    "user_text": "Necesitamos contratar 50 ordenadores para el ayuntamiento de Madrid, con instalación en 10 edificios municipales."
  }'
```

### **Paso 3: Consultar Outputs Generados**

```bash
# Listar todos los outputs del expediente
curl "http://localhost:8000/outputs/list?expediente_id=EXP-TEST-001"

# Obtener JSON_B más reciente de JN.1
curl "http://localhost:8000/outputs/latest/EXP-TEST-001/JN/JN.1/B"
```

### **Paso 4: Ver Métricas**

```bash
# Métricas generales (últimos 7 días)
curl "http://localhost:8000/metrics"

# Métricas filtradas por expediente
curl "http://localhost:8000/metrics?expediente_id=EXP-TEST-001&days=30"
```

### **Paso 5: Ver en LangFuse Dashboard**

1. Ve a: https://cloud.langfuse.com
2. Selecciona tu proyecto
3. Ve a "Traces" → verás cada ejecución del orquestador
4. Click en un trace para ver:
   - Cada nodo ejecutado (Retriever, GeneratorA, etc.)
   - Tiempo por nodo
   - Coste por nodo
   - Inputs/outputs de cada paso

---

## 📊 Estructura de Archivos Modificados

```
backend/
├── api/
│   ├── jn_routes.py                    # ✅ Nuevo endpoint con orquestador
│   ├── routes_outputs.py               # ✅ Nuevos endpoints list, latest, estado
│   └── routes_metrics.py               # ✅ NUEVO - Métricas LangFuse
├── agents/
│   └── orchestrator.py                 # ✅ Ya existía, ahora conectado
├── database/
│   └── outputs_repository.py           # ✅ Funciones list, get_latest, update_state
├── main.py                             # ✅ Router de metrics registrado
└── ...

tests/
└── test_orchestrator_e2e.py            # ✅ NUEVO - Tests E2E completos
```

---

## 🎯 Próximos Pasos

### **Sprint 2: Completar JN.4-JN.8**

1. Ampliar `binder.json` con secciones JN.4-JN.8
2. Crear schemas Pydantic para cada sección
3. Tests E2E para todas las secciones
4. Implementar Assembler Agent (documento completo)

### **Sprint 3: Documento PPT**

1. Crear `binder_ppt.json`
2. Extender orquestador para documento PPT
3. Nuevos endpoints `/ppt/...`

### **Mejoras de Observabilidad**

1. Integrar TruLens para métricas de calidad
2. Dashboard de métricas en el frontend
3. Alertas automáticas por errores
4. Reportes de coste por expediente

---

## 🐛 Troubleshooting

### **Error: "Import orchestrator could not be resolved"**

**Solución:**
```bash
# Asegúrate de estar en el directorio raíz
cd c:\Users\Administrator\Desktop\IA BOOTCAMP\ADD4U

# Ejecuta desde raíz
python -m backend.main
```

### **Error: "LangFuse trace not found"**

**Causa:** LangFuse no está configurado o las credenciales son inválidas.

**Solución:**
1. Verifica `.env` con `LANGFUSE_PUBLIC_KEY` y `LANGFUSE_SECRET_KEY`
2. Comprueba en https://cloud.langfuse.com que el proyecto existe
3. El endpoint `/metrics` devolverá datos solo si hay traces recientes

### **Error: "MongoDB connection failed"**

**Solución:**
1. Verifica `MONGO_URI` en `.env`
2. Asegúrate de que tu IP está en la whitelist de MongoDB Atlas
3. Comprueba que las colecciones existen: `expedientes`, `outputs`, `embeddings`

---

## ✅ Checklist de Implementación

- [x] Endpoint `/generar_jn_orquestado` creado
- [x] Funciones `list_outputs()`, `get_latest_output()`, `update_output_state()` implementadas
- [x] Endpoints `/outputs/list`, `/outputs/latest/...`, `/outputs/{id}/estado` funcionando
- [x] Router `routes_metrics.py` creado
- [x] Endpoint `/metrics` con integración LangFuse
- [x] Endpoint `/metrics/trace/{id}` para detalles de traces
- [x] Router registrado en `main.py`
- [x] Tests E2E completos para JN.1, JN.2, JN.3
- [x] Documentación completa creada

---

## 📞 Contacto y Soporte

Para dudas o problemas:
1. Revisa esta documentación
2. Ejecuta los tests: `python tests/test_orchestrator_e2e.py`
3. Verifica logs del backend: `uvicorn main:app --log-level debug`
4. Consulta LangFuse dashboard para trazabilidad

---

**🎉 ¡Implementación completada con éxito!**

Todos los endpoints están listos y funcionando con el orquestador LangGraph.

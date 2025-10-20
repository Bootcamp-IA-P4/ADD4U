# 🤖 Mini-CELIA - Documento Informativo Final

**Copilot Inteligente de Licitaciones para la Administración Pública**

---

## 📑 Índice

1. [Introducción al Proyecto](#1-introducción-al-proyecto)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Estructura de Carpetas Completa](#3-estructura-de-carpetas-completa)
4. [Pipeline Completo del Sistema](#4-pipeline-completo-del-sistema)
5. [Diagrama de Flujo Operativo](#5-diagrama-de-flujo-operativo)
6. [Componentes Principales](#6-componentes-principales)
7. [Ejemplos de Código](#7-ejemplos-de-código)
8. [Flujo de Datos Detallado](#8-flujo-de-datos-detallado)
9. [Casos de Uso Prácticos](#9-casos-de-uso-prácticos)
10. [Guía de Desarrollo](#10-guía-de-desarrollo)

---

## 1. Introducción al Proyecto

### 🎯 ¿Qué es Mini-CELIA?

**Mini-CELIA** (Copilot Inteligente de Licitaciones para la Administración) es un **sistema de IA especializado** que automatiza la generación de documentación para procesos de licitación pública en España.

### 🚨 Problema que Resuelve

En la administración pública española, preparar documentación de licitación es:
- ⏱️ **Lento**: 2-4 semanas por expediente
- 📚 **Complejo**: Requiere conocimiento profundo de normativa (LCSP, RGPD, DNSH)
- ❌ **Propenso a errores**: Riesgo de incumplimiento normativo
- 🔄 **Repetitivo**: Mismos patrones en documentos similares

### ✅ Solución: Mini-CELIA

Mini-CELIA automatiza el proceso mediante:

```
Usuario describe necesidad
        ↓
    IA procesa
        ↓
 Valida contra normativa
        ↓
Genera documento completo
        ↓
   Exporta (PDF/Word)
```

**Resultado**: De semanas a **minutos**, con cumplimiento normativo garantizado.

---

## 2. Arquitectura del Sistema

### 🏗️ Vista de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                    MINI-CELIA ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │   FRONTEND   │         │   BACKEND    │                     │
│  │              │         │              │                     │
│  │  React 18    │◄──HTTP─►│  FastAPI     │                     │
│  │  Vite        │         │  Python 3.11 │                     │
│  │  Tailwind    │         │  Async/Await │                     │
│  │  Port 5173   │         │  Port 8000   │                     │
│  └──────────────┘         └──────┬───────┘                     │
│                                   │                             │
│                    ┌──────────────┼──────────────┐             │
│                    │              │              │             │
│             ┌──────▼─────┐ ┌─────▼──────┐ ┌────▼─────┐       │
│             │  LANGCHAIN │ │  MONGODB   │ │  OPENAI  │       │
│             │ Orchestrator│ │  Database  │ │  GPT-4o  │       │
│             │  LangGraph │ │  Atlas     │ │          │       │
│             └──────┬─────┘ └────────────┘ └──────────┘       │
│                    │                                           │
│         ┌──────────┼───────────┐                              │
│         │          │           │                              │
│   ┌─────▼────┐ ┌──▼──────┐ ┌─▼──────────┐                   │
│   │ RETRIEVER│ │GENERATOR│ │ VALIDATOR  │                   │
│   │  Agent   │ │ Agents  │ │   Agent    │                   │
│   │ (RAG)    │ │  A & B  │ │ (Schemas)  │                   │
│   └──────────┘ └─────────┘ └────────────┘                   │
│                                                               │
│   ┌──────────────────────────────────────────────┐           │
│   │        OBSERVABILITY & MONITORING            │           │
│   │  ┌──────────┐  ┌──────────┐  ┌───────────┐  │           │
│   │  │ LangFuse │  │ TruLens  │  │  Logging  │  │           │
│   │  │ Tracing  │  │ Metrics  │  │  System   │  │           │
│   │  └──────────┘  └──────────┘  └───────────┘  │           │
│   └──────────────────────────────────────────────┘           │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 🔑 Componentes Clave

| Componente | Tecnología | Función |
|-----------|-----------|---------|
| **Frontend** | React + Vite + Tailwind | Interfaz de usuario conversacional |
| **Backend** | FastAPI + Python | API REST y lógica de negocio |
| **Orchestrator** | LangGraph + LangChain | Coordina flujo de agentes IA |
| **Agents** | OpenAI GPT-4o | Generación y validación de contenido |
| **Database** | MongoDB Atlas | Persistencia de expedientes y outputs |
| **Retrieval** | SentenceTransformers | RAG para contexto normativo |
| **Observability** | LangFuse + TruLens | Trazabilidad y métricas |

---

## 3. Estructura de Carpetas Completa

```
ADD4U/
│
├── 📁 backend/                              # 🔧 API y Lógica del Sistema
│   │
│   ├── 📁 agents/                           # 🤖 Agentes de IA (LangGraph)
│   │   ├── orchestrator.py                  # Orquestador principal (LangGraph)
│   │   ├── retriever_agent.py               # RAG: Recuperación de contexto normativo
│   │   ├── prompt_manager.py                # Gestor de prompts dinámicos
│   │   ├── prompt_refiner.py                # Refinador de prompts por sección
│   │   ├── validator.py                     # Validador con auto-retry
│   │   │
│   │   ├── 📁 generators/                   # Generadores de contenido
│   │   │   ├── generator_a.py               # Genera JSON estructurado (JSON_A)
│   │   │   ├── generator_b.py               # Genera narrativa legal (JSON_B)
│   │   │   └── output_parser.py             # Parser centralizado de outputs
│   │   │
│   │   ├── 📁 schemas/                      # Esquemas de validación
│   │   │   └── json_schemas.py              # BinderSchemas (JSON_A, JSON_B)
│   │   │
│   │   └── 📁 nodes/                        # Nodos del grafo LangGraph
│   │       └── (nodos individuales)
│   │
│   ├── 📁 api/                              # 🛣️ Endpoints REST
│   │   ├── __init__.py
│   │   ├── jn_routes.py                     # POST /jn/generate, GET /jn/status
│   │   ├── routes_expedientes.py            # CRUD expedientes
│   │   ├── routes_normativa.py              # Gestión normativa Golden
│   │   └── routes_outputs.py                # Historial de outputs generados
│   │
│   ├── 📁 core/                             # ⚡ Lógica Central
│   │   ├── config.py                        # Configuración global (Settings)
│   │   ├── llm_client.py                    # Cliente OpenAI/Groq
│   │   ├── logic_jn.py                      # Lógica de negocio JN
│   │   ├── langfuse_client.py               # Cliente trazabilidad LangFuse
│   │   ├── trulens_client.py                # Cliente métricas TruLens
│   │   └── trulens_metrics.py               # Definición de métricas
│   │
│   ├── 📁 database/                         # 🗄️ Persistencia MongoDB
│   │   ├── mongo.py                         # Configuración cliente AsyncMongo
│   │   ├── init_expedientes.py              # Inicialización BD expedientes
│   │   ├── init_normativa.py                # Inicialización BD normativa
│   │   ├── init_outputs.py                  # Inicialización BD outputs
│   │   ├── outputs_repository.py            # Repositorio de outputs
│   │   └── process_normativa_global.py      # Procesamiento embeddings
│   │
│   ├── 📁 models/                           # 📋 Esquemas Pydantic
│   │   ├── __init__.py
│   │   └── schemas_jn.py                    # Modelos de datos JN
│   │
│   ├── 📁 prompts/                          # 💭 Prompts Optimizados
│   │   ├── jn_prompts.py                    # Prompts específicos JN
│   │   └── 📁 templates/                    # Plantillas de prompts
│   │       └── (plantillas por sección)
│   │
│   ├── 📁 tests/                            # 🧪 Tests Unitarios
│   │   ├── test_orchestrator_e2e.py         # Test end-to-end
│   │   ├── test_validator_improvements.py   # Tests validador
│   │   ├── test_retriever.py                # Tests RAG
│   │   └── test_jn_validator.py             # Tests validación JN
│   │
│   ├── 📁 utils/                            # 🛠️ Utilidades
│   │   └── dict_utils.py                    # Helpers manipulación diccionarios
│   │
│   ├── 📁 trulens_data/                     # 📊 Base de datos TruLens
│   │   └── trulens.db                       # SQLite DB para métricas
│   │
│   └── main.py                              # 🚀 Punto de entrada FastAPI
│
├── 📁 frontend/                             # 🎨 Aplicación React
│   │
│   ├── 📁 src/
│   │   │
│   │   ├── 📁 components/                   # 🧩 Componentes React
│   │   │   ├── ChatSection.jsx              # Chat principal con IA
│   │   │   ├── ClarificationPrompts.jsx     # Prompts de clarificación
│   │   │   ├── DraftModal.jsx               # Modal de borradores
│   │   │   ├── ExportMenu.jsx               # Menú exportación (PDF/Word)
│   │   │   ├── LicitacionExamples.jsx       # Ejemplos de licitaciones
│   │   │   └── Toast.jsx                    # Sistema de notificaciones
│   │   │
│   │   ├── 📁 contexts/                     # 🔄 Context API
│   │   │   └── AppStateContext.jsx          # Estado global aplicación
│   │   │
│   │   ├── 📁 pages/                        # 📄 Páginas
│   │   │   └── MainApp.jsx                  # Página principal
│   │   │
│   │   ├── 📁 services/                     # 🌐 Servicios API
│   │   │   └── apiService.js                # Cliente HTTP (Axios)
│   │   │
│   │   ├── 📁 utils/                        # 🛠️ Utilidades
│   │   │   └── pdfGenerator.js              # Generador PDF (jsPDF)
│   │   │
│   │   ├── App.jsx                          # Componente raíz
│   │   ├── index.css                        # Estilos globales
│   │   └── main.jsx                         # Entrada React
│   │
│   ├── 📁 public/                           # 📂 Recursos estáticos
│   │   └── 📁 images/                       # Imágenes
│   │
│   ├── index.html                           # HTML principal
│   ├── package.json                         # Dependencias NPM
│   ├── postcss.config.js                    # Configuración PostCSS
│   ├── tailwind.config.js                   # Configuración Tailwind
│   └── vite.config.js                       # Configuración Vite
│
├── 📁 docs/                                 # 📚 Documentación
│   ├── 📁 diagrams/                         # Diagramas del sistema
│   │   ├── 📁 flujos/                       # Diagramas de flujo
│   │   │   ├── jn_operativo.md              # Flujo operativo JN
│   │   │   ├── flujo_operativo.md           # Flujo general
│   │   │   └── bbdd_flujo.md                # Flujo base de datos
│   │   │
│   │   ├── 📁 ejemplos_json/                # Ejemplos de estructuras
│   │   │   ├── output_jsonA.json            # Ejemplo JSON_A
│   │   │   ├── output_jsonB.json            # Ejemplo JSON_B
│   │   │   ├── expediente.json              # Ejemplo expediente
│   │   │   └── normativa_global.json        # Ejemplo normativa
│   │   │
│   │   └── 📁 sections/                     # Documentación secciones
│   │       └── 📁 jn/                       # Específico JN
│   │           ├── JN.1_objeto_promptA.txt
│   │           ├── JN.1_objeto_promptB.txt
│   │           └── (más prompts...)
│   │
│   ├── guia_endpoints_orquestador.md        # Guía API
│   ├── server_setup.md                      # Setup servidor
│   ├── mejoras_sistema_validacion.md        # Doc mejoras validación
│   └── Mini-CELIA-Final-Documento-Informativo.md  # Este documento
│
├── 📁 outputs/                              # 📤 Archivos generados
│   └── (PDFs y Word generados)
│
├── 📁 tests/                                # 🧪 Tests de integración
│   └── test_orchestrator_e2e.py
│
├── 📄 .env                                  # 🔐 Variables de entorno (local)
├── 📄 .env.example                          # 📄 Plantilla variables entorno
├── 📄 .gitignore                            # 🚫 Archivos ignorados Git
├── 📄 README.md                             # 📖 Documentación principal
├── 📄 requirements.txt                      # 📦 Dependencias Python
└── 📄 package.json                          # 📦 Metadatos proyecto
```

### 📌 Convenciones de Nomenclatura

- **`*_agent.py`**: Agentes individuales de LangChain
- **`*_routes.py`**: Endpoints FastAPI agrupados por dominio
- **`schemas_*.py`**: Modelos Pydantic de validación
- **`*.jsx`**: Componentes React
- **`*_prompts.py`**: Colecciones de prompts para IA

---

## 4. Pipeline Completo del Sistema

### 🔄 Flujo End-to-End: Generación de JN.1

```
┌─────────────────────────────────────────────────────────────────┐
│                   PIPELINE COMPLETO MINI-CELIA                  │
└─────────────────────────────────────────────────────────────────┘

[1] USUARIO                     [2] FRONTEND                [3] BACKEND
     │                               │                           │
     │ "Generar JN.1                 │                           │
     │  para limpieza"               │                           │
     └──────────────────────────────►│                           │
                                     │ POST /jn/generate         │
                                     │ {expediente_id,           │
                                     │  user_text,               │
                                     │  seccion: "JN.1"}         │
                                     └──────────────────────────►│
                                                                 │
                                     ┌───────────────────────────┘
                                     │
                        [4] ORCHESTRATOR (LangGraph)
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            [5] RETRIEVER      [6] PROMPT      [7] GENERATOR A
             (RAG Agent)        MANAGER         (Estructurado)
                    │                │                │
                    │ Vector Search  │ Build Prompt   │ LLM GPT-4o
                    │ MongoDB Atlas  │ A + context    │ → JSON_A
                    │ Embeddings     │                │
                    │                │                │
                    └────────────────┴────────────────┘
                                     │
                            [8] VALIDATOR A
                            (Schema Check)
                                     │
                              ┌──────┴──────┐
                              │ ❌ Error?   │
                              └──────┬──────┘
                                     │ Sí
                          [9] AUTO-REPAIR (max 2 retries)
                                     │
                              Regenera JSON_A
                                     │
                                     │ No (✅)
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
           [10] GENERATOR B   [11] VALIDATOR B  [12] SAVE TO DB
            (Narrativa)        (Coherence)       (MongoDB)
                    │                │                │
            LLM GPT-4o         JSON_A vs JSON_B       │
            → JSON_B           Semantic check         │
                    │                │                │
                    └────────────────┴────────────────┘
                                     │
                          [13] RETURN TO FRONTEND
                                     │
                              JSON_A + JSON_B
                                     │
         ┌───────────────────────────┘
         │
[14] FRONTEND RENDER
         │
    ┌────┴─────┐
    │ Display  │
    │ Chat     │
    │ Response │
    └────┬─────┘
         │
[15] USER ACTIONS
    │
    ├─► 💾 Guardar
    ├─► 📄 Exportar PDF
    ├─► 📝 Exportar Word
    └─► 🔄 Regenerar
```

### 📊 Detalle de Cada Paso

#### **[1] Usuario Input**
```javascript
// Usuario en frontend escribe:
"Necesito una JN para servicios de limpieza urbana"
```

#### **[2] Frontend → Backend Request**
```javascript
// ChatSection.jsx
const response = await apiService.post('/jn/generate', {
  expediente_id: 'EXP-2025-001',
  user_text: 'Servicios de limpieza urbana...',
  seccion: 'JN.1',
  documento: 'JN'
});
```

#### **[3] Backend Receive**
```python
# backend/api/jn_routes.py
@router.post("/jn/generate")
async def generate_jn(request: GenerateJNRequest):
    # Envia al orchestrator
    result = await orchestrator.ainvoke({
        "expediente_id": request.expediente_id,
        "user_text": request.user_text,
        "seccion": request.seccion,
        "documento": request.documento
    })
    return result
```

#### **[4] Orchestrator (LangGraph)**
```python
# backend/agents/orchestrator.py
graph = StateGraph(OrchestratorState)

# Añadir nodos
graph.add_node("retriever", retriever_node)
graph.add_node("prompt_manager", prompt_manager_node)
graph.add_node("generator_a", generator_a_node)
graph.add_node("validator_a", validator_a_node)
graph.add_node("generator_b", generator_b_node)
graph.add_node("validator_b", validator_b_node)

# Definir flujo
graph.add_edge(START, "retriever")
graph.add_edge("retriever", "prompt_manager")
graph.add_edge("prompt_manager", "generator_a")
graph.add_edge("generator_a", "validator_a")
graph.add_edge("validator_a", "generator_b")
graph.add_edge("generator_b", "validator_b")
graph.add_edge("validator_b", END)
```

#### **[5] Retriever Agent (RAG)**
```python
# backend/agents/retriever_agent.py
class RetrieverAgent:
    async def ainvoke(self, inputs):
        query_embedding = self.model.encode(inputs["user_text"])
        
        # Vector search en MongoDB
        results = await self.collection.aggregate([
            {"$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 150,
                "limit": 5,
                "index": "vector_index"
            }}
        ]).to_list(5)
        
        # Construir contexto
        context = "\n\n".join([r["text"] for r in results])
        
        return {
            "context": context,
            "matches": results
        }
```

#### **[6] Prompt Manager**
```python
# backend/agents/prompt_manager.py
async def ainvoke(self, inputs):
    prompt_a = f"""
    Eres un experto en licitaciones públicas españolas.
    
    USUARIO: {inputs['user_text']}
    
    CONTEXTO NORMATIVO:
    {inputs['context']}
    
    Genera un JSON estructurado con:
    {{
      "secciones_JN": {{
        "objeto": "...",
        "alcance": "...",
        "ambito": "..."
      }}
    }}
    """
    return {"prompt_a": prompt_a}
```

#### **[7] Generator A (Estructurado)**
```python
# backend/agents/generators/generator_a.py
class GeneratorA:
    async def ainvoke(self, state):
        response = await self.llm.ainvoke(state["prompt_a"])
        
        # Parsear JSON
        json_data, error = OutputParser.parse_json(response.content)
        
        # Construir JSON_A
        json_a = {
            "expediente_id": state["expediente_id"],
            "documento": "JN",
            "seccion": "JN.1",
            "nodo": "A",
            "timestamp": datetime.utcnow().isoformat(),
            "actor": "LLM",
            "json": json_data,
            "citas_golden": state.get("citas_golden", []),
            "metadata": {"model": "gpt-4o"}
        }
        
        state["json_a"] = json_a
        return state
```

#### **[8] Validator A**
```python
# backend/agents/validator.py
class ValidatorAgent:
    def validate_json_a(self, json_a, seccion):
        errors = []
        
        # Validar estructura básica
        if "json" not in json_a:
            errors.append("Falta campo 'json'")
        
        # Validar campos requeridos de la sección
        json_data = json_a["json"]
        required = BinderSchemas.get_section_required_fields(seccion)
        
        for field in required:
            if field not in json_data:
                errors.append(f"Campo faltante: {field}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )
```

#### **[9] Auto-Repair (si falla validación)**
```python
# backend/agents/validator.py
async def auto_repair_json_a(self, json_a, errors, seccion):
    repair_prompt = f"""
    JSON CON ERRORES:
    {json.dumps(json_a['json'], indent=2)}
    
    ERRORES:
    {errors}
    
    CAMPOS REQUERIDOS:
    {BinderSchemas.get_section_required_fields(seccion)}
    
    Repara el JSON añadiendo campos faltantes.
    """
    
    response = await llm.ainvoke(repair_prompt)
    repaired_json = OutputParser.parse_json(response.content)
    
    json_a["json"] = repaired_json
    json_a["metadata"]["repaired"] = True
    
    return json_a
```

#### **[10-13] Generator B, Validator B, Save**
Similar al flujo A pero para narrativa legal.

#### **[14] Frontend Render**
```javascript
// ChatSection.jsx
const botMessage = {
  role: 'bot',
  content: `
    <h3>JN.1 - Justificación de la Necesidad</h3>
    <p>${json_b.narrativa}</p>
    
    <div class="metadata">
      <span>Expediente: ${json_a.expediente_id}</span>
      <span>Generado: ${json_a.timestamp}</span>
    </div>
  `
};
```

#### **[15] User Actions**
```javascript
// Export PDF
const handleDownloadPDF = () => {
  const sections = extractAllJNSections(chat);
  generateJNPDF(expedienteId, sections);
};
```

---

## 5. Diagrama de Flujo Operativo

### 📈 Flujo Detallado JN.1 con Validaciones

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryColor':'#38b6ff','primaryTextColor':'#000','primaryBorderColor':'#38b6ff','lineColor':'#38b6ff','secondaryColor':'#32a842','tertiaryColor':'#ffcf00'}}}%%
flowchart TD
    Start([👤 Usuario inicia generación JN.1]) --> Input[📝 Input: expediente_id + user_text]
    
    Input --> Orchestrator{⚙️ Orchestrator<br/>LangGraph}
    
    Orchestrator --> Retriever[🔍 Retriever Agent<br/>Vector Search MongoDB]
    Retriever --> Context[📚 Contexto normativo<br/>LCSP + RGPD + DNSH]
    
    Context --> PromptMgr[💭 Prompt Manager<br/>Build Prompt A]
    PromptMgr --> GenA[🤖 Generator A<br/>GPT-4o → JSON_A]
    
    GenA --> Parser[🔧 Output Parser<br/>Clean HTML + Parse JSON]
    Parser --> ValidA{✅ Validator A<br/>Schema Check}
    
    ValidA -->|❌ Errores| AutoRepair[🔄 Auto-Repair<br/>Generate repair prompt<br/>Retry max 2 times]
    AutoRepair --> ValidA
    
    ValidA -->|✅ OK| Sanitize[🧹 Sanitize 'faltantes'<br/>Convert to empty strings]
    Sanitize --> GenB[📝 Generator B<br/>GPT-4o → JSON_B]
    
    GenB --> ValidB{✅ Validator B<br/>Coherence Check}
    ValidB -->|❌ Errores| Error[⚠️ Error response]
    ValidB -->|✅ OK| SaveDB[(💾 Save to MongoDB<br/>JSON_A + JSON_B)]
    
    SaveDB --> Langfuse[📊 Log to LangFuse<br/>Tracing]
    Langfuse --> TruLens[📈 Log to TruLens<br/>Metrics]
    
    TruLens --> Response[📤 Return to Frontend<br/>JSON_A + JSON_B]
    Response --> Display[🖥️ Display in Chat<br/>Formatted narrative]
    
    Display --> Actions{🎬 User Actions}
    Actions -->|💾| Save[Save draft]
    Actions -->|📄| PDF[Export PDF]
    Actions -->|📝| Word[Export Word]
    Actions -->|🔄| Regenerate[Regenerate]
    
    Save --> End([✅ End])
    PDF --> End
    Word --> End
    Regenerate --> Input
    Error --> End
    
    style Start fill:#32a842,stroke:#2a8f38,stroke-width:3px,color:#fff
    style End fill:#32a842,stroke:#2a8f38,stroke-width:3px,color:#fff
    style Orchestrator fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style Retriever fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style Context fill:#f8f4eb,stroke:#38b6ff,stroke-width:2px,color:#000
    style PromptMgr fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style GenA fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style Parser fill:#f8f4eb,stroke:#38b6ff,stroke-width:2px,color:#000
    style ValidA fill:#ffcf00,stroke:#e6ba00,stroke-width:2px,color:#000
    style AutoRepair fill:#ff6b6b,stroke:#e65555,stroke-width:2px,color:#fff
    style Sanitize fill:#f8f4eb,stroke:#38b6ff,stroke-width:2px,color:#000
    style GenB fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style ValidB fill:#ffcf00,stroke:#e6ba00,stroke-width:2px,color:#000
    style Error fill:#ff6b6b,stroke:#e65555,stroke-width:2px,color:#fff
    style SaveDB fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style Langfuse fill:#f8f4eb,stroke:#38b6ff,stroke-width:2px,color:#000
    style TruLens fill:#f8f4eb,stroke:#38b6ff,stroke-width:2px,color:#000
    style Response fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style Display fill:#f8f4eb,stroke:#38b6ff,stroke-width:2px,color:#000
    style Actions fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
    style Save fill:#32a842,stroke:#2a8f38,stroke-width:2px,color:#fff
    style PDF fill:#32a842,stroke:#2a8f38,stroke-width:2px,color:#fff
    style Word fill:#32a842,stroke:#2a8f38,stroke-width:2px,color:#fff
    style Regenerate fill:#38b6ff,stroke:#2a9de6,stroke-width:2px,color:#000
```

### 🔄 Estados del Sistema

```
Estado Inicial → Esperando input usuario
    ↓
Estado Procesando → Retriever + Prompt Manager
    ↓
Estado Generando A → Generator A + Validator A
    ↓
    ├─► [Validación OK] → Siguiente fase
    └─► [Validación FAIL] → Auto-Repair → Retry
            ↓
            └─► [Max retries] → Error final
    ↓
Estado Generando B → Generator B + Validator B
    ↓
Estado Guardando → MongoDB + LangFuse + TruLens
    ↓
Estado Completado → Response al frontend
```

---

## 6. Componentes Principales

### 🤖 Agentes del Sistema

#### **1. Orchestrator (Cerebro del Sistema)**

**Archivo**: `backend/agents/orchestrator.py`

**Función**: Coordina todos los agentes usando LangGraph

```python
class OrchestratorState(TypedDict):
    expediente_id: str          # ID del expediente
    documento: str              # "JN", "PPT", "PCAP"
    seccion: str                # "JN.1", "JN.2", etc.
    user_text: str              # Input del usuario
    context: str                # Contexto normativo (RAG)
    prompt_a: str               # Prompt para Generator A
    prompt_b: str               # Prompt para Generator B
    json_a: dict                # Output estructurado
    json_b: dict                # Output narrativo
    validation_a_result: dict   # Resultado validación A
    validation_b_result: dict   # Resultado validación B
    validation_failed: bool     # Flag de fallo crítico
```

**Ejemplo de uso**:
```python
orchestrator = build_orchestrator(debug_mode=False)

result = await orchestrator.ainvoke({
    "expediente_id": "EXP-2025-001",
    "documento": "JN",
    "seccion": "JN.1",
    "user_text": "Necesitamos servicios de limpieza..."
})

# result contiene json_a y json_b
print(result["json_a"])
print(result["json_b"])
```

#### **2. Retriever Agent (RAG)**

**Archivo**: `backend/agents/retriever_agent.py`

**Función**: Recupera contexto normativo usando embeddings vectoriales

**Tecnología**: 
- `sentence-transformers/all-MiniLM-L6-v2`
- MongoDB Atlas Vector Search

**Flujo**:
```python
User Query: "servicios de limpieza"
    ↓
Encode to vector (384 dimensions)
    ↓
Vector Search in MongoDB
    ↓
Top 5 matches (LCSP, RGPD, DNSH)
    ↓
Concatenate context
    ↓
Return to Orchestrator
```

**Ejemplo**:
```python
retriever = RetrieverAgent()

result = await retriever.ainvoke({
    "user_text": "Contratar servicios de limpieza urbana",
    "documento": "JN",
    "seccion": "JN.1"
})

print(result["context"])  # Artículos LCSP relevantes
print(result["matches"])  # List[{text, score, title}]
```

#### **3. Generator A (Estructurado)**

**Archivo**: `backend/agents/generators/generator_a.py`

**Función**: Genera JSON estructurado (JSON_A) con datos canónicos

**Output esperado**:
```json
{
  "expediente_id": "EXP-2025-001",
  "documento": "JN",
  "seccion": "JN.1",
  "nodo": "A",
  "timestamp": "2025-10-20T15:30:00Z",
  "actor": "LLM",
  "json": {
    "secciones_JN": {
      "objeto": "Servicios de limpieza urbana",
      "alcance": "Limpieza de calles, parques y plazas",
      "ambito": "Ámbito municipal - Todas las zonas urbanas"
    }
  },
  "citas_golden": ["LCSP_Art_99", "RGPD_Art_5"],
  "citas_normativas": [],
  "metadata": {
    "model": "gpt-4o",
    "status": "success"
  }
}
```

#### **4. Generator B (Narrativa)**

**Archivo**: `backend/agents/generators/generator_b.py`

**Función**: Genera narrativa legal legible (JSON_B)

**Output esperado**:
```json
{
  "expediente_id": "EXP-2025-001",
  "documento": "JN",
  "seccion": "JN.1",
  "nodo": "B",
  "timestamp": "2025-10-20T15:31:00Z",
  "actor": "LLM",
  "narrativa": "El objeto del presente contrato consiste en la prestación de servicios de limpieza urbana...",
  "refs": {
    "hash_json_A": "abc123...",
    "citas_golden": ["LCSP_Art_99"],
    "citas_normativas": []
  },
  "metadata": {
    "model": "gpt-4o",
    "narrative_length": 1250
  }
}
```

#### **5. Validator Agent**

**Archivo**: `backend/agents/validator.py`

**Función**: Valida outputs contra esquemas del binder

**Características**:
- ✅ Validación de estructura JSON
- ✅ Validación de campos requeridos
- ✅ Sanitización de valores "faltantes"
- ✅ Auto-repair con retry (max 2 intentos)
- ✅ Validación de coherencia semántica (JSON_A vs JSON_B)

**Ejemplo**:
```python
validator = ValidatorAgent(mode="estructurado", max_retries=2)

result = validator.validate_json_a(json_a, seccion="JN.1")

if not result.is_valid:
    print(f"Errores: {result.errors}")
    # Auto-repair se activa automáticamente
```

---

## 7. Ejemplos de Código

### 📝 Ejemplo Completo: Generar JN.1 desde Cero

#### **Backend**: Endpoint `/jn/generate`

```python
# backend/api/jn_routes.py
from fastapi import APIRouter, HTTPException
from backend.agents.orchestrator import build_orchestrator
from backend.models.schemas_jn import GenerateJNRequest

router = APIRouter(prefix="/jn", tags=["JN"])

@router.post("/generate")
async def generate_jn(request: GenerateJNRequest):
    """
    Genera una sección de Justificación de la Necesidad (JN)
    
    Args:
        request: {
            expediente_id: str
            user_text: str
            seccion: str (ej: "JN.1")
            documento: str (ej: "JN")
        }
    
    Returns:
        {
            json_a: dict (datos estructurados)
            json_b: dict (narrativa)
            status: str
        }
    """
    try:
        # Construir orchestrator
        orchestrator = build_orchestrator(debug_mode=False)
        
        # Ejecutar flujo completo
        result = await orchestrator.ainvoke({
            "expediente_id": request.expediente_id,
            "documento": request.documento,
            "seccion": request.seccion,
            "user_text": request.user_text
        })
        
        # Verificar si hubo fallo en validación
        if result.get("validation_failed"):
            raise HTTPException(
                status_code=422,
                detail=result.get("validation_error_message")
            )
        
        return {
            "status": "success",
            "json_a": result["json_a"],
            "json_b": result["json_b"],
            "expediente_id": request.expediente_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### **Frontend**: Llamada desde React

```javascript
// frontend/src/services/apiService.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiService = {
  async generateJN(data) {
    try {
      const response = await axios.post(`${API_BASE_URL}/jn/generate`, {
        expediente_id: data.expediente_id,
        user_text: data.user_text,
        seccion: data.seccion || 'JN.1',
        documento: 'JN'
      });
      
      return response.data;
    } catch (error) {
      console.error('Error generating JN:', error);
      throw error;
    }
  }
};
```

```javascript
// frontend/src/components/ChatSection.jsx
import { apiService } from '../services/apiService';

function ChatSection() {
  const handleGenerateJN = async () => {
    try {
      const result = await apiService.generateJN({
        expediente_id: 'EXP-2025-001',
        user_text: userInput,
        seccion: 'JN.1'
      });
      
      // Mostrar resultado en el chat
      addMessage({
        role: 'bot',
        content: result.json_b.narrativa
      });
      
    } catch (error) {
      showToast('Error al generar JN', 'error');
    }
  };
  
  return (
    <div className="chat-section">
      {/* Chat UI */}
    </div>
  );
}
```

### 🔧 Ejemplo: Crear un Nuevo Agente

```python
# backend/agents/mi_nuevo_agente.py
from typing import Dict, Any
from langfuse import observe

class MiNuevoAgente:
    """
    Agente personalizado para [describir función]
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        # Inicializar recursos necesarios
    
    @observe(name="mi_nuevo_agente")
    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método principal del agente (asíncrono)
        
        Args:
            state: Estado actual del flujo
        
        Returns:
            state: Estado actualizado
        """
        # 1. Extraer inputs del state
        input_data = state.get("campo_input")
        
        # 2. Procesamiento
        resultado = await self._procesar(input_data)
        
        # 3. Actualizar state
        state["campo_output"] = resultado
        
        # 4. Retornar state modificado
        return state
    
    async def _procesar(self, data):
        """Lógica de procesamiento"""
        # Implementar lógica aquí
        return data
```

**Integrar en el Orchestrator**:
```python
# backend/agents/orchestrator.py
from backend.agents.mi_nuevo_agente import MiNuevoAgente

def build_orchestrator():
    graph = StateGraph(OrchestratorState)
    
    # Instanciar el nuevo agente
    mi_agente = MiNuevoAgente()
    
    # Crear nodo
    async def mi_agente_node(state):
        return await mi_agente.ainvoke(state)
    
    # Añadir al grafo
    graph.add_node("mi_agente", mi_agente_node)
    
    # Conectar en el flujo
    graph.add_edge("prompt_manager", "mi_agente")
    graph.add_edge("mi_agente", "generator_a")
    
    return graph.compile()
```

---

## 8. Flujo de Datos Detallado

### 📊 Transformaciones de Datos

```
[PASO 1: Input Usuario]
{
  "text": "Necesito servicios de limpieza"
}
    ↓
[PASO 2: Enriched Input]
{
  "expediente_id": "EXP-2025-001",
  "user_text": "Necesito servicios de limpieza",
  "seccion": "JN.1",
  "documento": "JN"
}
    ↓
[PASO 3: After Retriever]
{
  ...anterior,
  "context": "Art. 99 LCSP: ...\nArt. 5 RGPD: ...",
  "matches": [
    {"text": "...", "score": 0.89, "title": "LCSP Art 99"},
    {"text": "...", "score": 0.85, "title": "RGPD Art 5"}
  ]
}
    ↓
[PASO 4: After Prompt Manager]
{
  ...anterior,
  "prompt_a": "Eres un experto...\n\nUSUARIO: Necesito...\n\nCONTEXTO: Art. 99...",
  "prompt_b": "Genera narrativa legal..."
}
    ↓
[PASO 5: After Generator A]
{
  ...anterior,
  "json_a": {
    "expediente_id": "EXP-2025-001",
    "documento": "JN",
    "seccion": "JN.1",
    "nodo": "A",
    "timestamp": "2025-10-20T15:30:00Z",
    "json": {
      "secciones_JN": {
        "objeto": "Servicios de limpieza urbana",
        "alcance": "Calles, parques y plazas",
        "ambito": "Municipal"
      }
    }
  }
}
    ↓
[PASO 6: After Validator A]
{
  ...anterior,
  "validation_a_result": {
    "is_valid": true,
    "errors": [],
    "warnings": []
  },
  "validation_a_passed": true
}
    ↓
[PASO 7: After Generator B]
{
  ...anterior,
  "json_b": {
    "expediente_id": "EXP-2025-001",
    "documento": "JN",
    "seccion": "JN.1",
    "nodo": "B",
    "timestamp": "2025-10-20T15:31:00Z",
    "narrativa": "El objeto del presente contrato...",
    "refs": {
      "hash_json_A": "abc123..."
    }
  }
}
    ↓
[PASO 8: After Validator B & Save]
{
  ...anterior,
  "validation_b_result": {
    "is_valid": true,
    "coherence_score": 0.95
  },
  "_id": ObjectId("507f1f77bcf86cd799439011")
}
    ↓
[PASO 9: Response to Frontend]
{
  "status": "success",
  "json_a": {...},
  "json_b": {...},
  "expediente_id": "EXP-2025-001"
}
```

---

## 9. Casos de Uso Prácticos

### 🏗️ Caso 1: Licitación de Obras

**Escenario**: Ayuntamiento necesita licitar obras de mejora en un colegio

```javascript
// Frontend Input
{
  expediente_id: "OBR-2025-042",
  user_text: `
    Necesitamos realizar obras de mejora de accesibilidad 
    en el CEIP San Juan. Incluye:
    - Instalación de rampas
    - Ascensor
    - Baños adaptados
    Presupuesto estimado: 180.000€
    Plazo: 6 meses
  `,
  seccion: "JN.1"
}
```

**Output JSON_A**:
```json
{
  "json": {
    "secciones_JN": {
      "objeto": "Obras de mejora de accesibilidad en CEIP San Juan",
      "alcance": "Instalación de rampas, ascensor y baños adaptados conforme a normativa de accesibilidad universal",
      "ambito": "Centro educativo CEIP San Juan, ámbito municipal"
    },
    "presupuesto": {
      "valor": 180000,
      "moneda": "EUR"
    },
    "plazo_ejecucion": {
      "valor": 6,
      "unidad": "meses"
    }
  }
}
```

**Output JSON_B (narrativa)**:
```
El objeto del presente contrato consiste en la ejecución de 
obras de mejora de accesibilidad en el Centro de Educación 
Infantil y Primaria (CEIP) San Juan, con el fin de garantizar 
el acceso universal a todas las instalaciones educativas...

El alcance de las obras comprende:
1. Instalación de rampas de acceso conforme al CTE DB-SUA
2. Ascensor accesible según norma UNE-EN 81-70
3. Adaptación de servicios higiénicos...

Este contrato se enmarca en el cumplimiento del artículo 9.2 
de la Constitución Española y la Ley General de derechos de 
las personas con discapacidad...
```

### 🛠️ Caso 2: Servicios de Mantenimiento

**Escenario**: Diputación necesita contratar mantenimiento de edificios

```javascript
{
  expediente_id: "SER-2025-108",
  user_text: `
    Mantenimiento preventivo y correctivo de:
    - 5 edificios administrativos
    - Instalaciones eléctricas
    - Climatización
    - Fontanería
    Duración: 2 años
    Valor estimado: 250.000€/año
  `,
  seccion: "JN.1"
}
```

**Output incluye**:
- ✅ Validación DNSH (no causar daño significativo al medioambiente)
- ✅ Validación RGPD (si hay acceso a oficinas con datos)
- ✅ Cláusulas de igualdad de género
- ✅ Criterios de sostenibilidad

---

## 10. Guía de Desarrollo

### 🚀 Setup Inicial

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-org/ADD4U.git
cd ADD4U

# 2. Crear entorno virtual Python
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows

# 3. Instalar dependencias backend
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 5. Instalar dependencias frontend
cd frontend
npm install

# 6. Iniciar backend
cd ..
uvicorn backend.main:app --reload

# 7. Iniciar frontend (en otra terminal)
cd frontend
npm run dev
```

### 🔧 Configuración Avanzada

#### **Variables de Entorno Críticas**

```env
# .env
# ======================================
# APIS DE IA
# ======================================
OPENAI_API_KEY=sk-proj-xxxxx
GROQ_API_KEY=gsk-xxxxx

# ======================================
# BASE DE DATOS
# ======================================
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGO_DB=Golden
EMBEDDINGS_COLLECTION=embeddings
VECTOR_INDEX_NAME=vector_index

# ======================================
# EMBEDDINGS
# ======================================
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
SENTENCE_TRANSFORMERS_HOME=./models_cache

# ======================================
# OBSERVABILITY
# ======================================
LANGFUSE_PUBLIC_KEY=pk-xxxxx
LANGFUSE_SECRET_KEY=sk-xxxxx
LANGFUSE_HOST=https://cloud.langfuse.com

# ======================================
# RETRIEVER TUNING
# ======================================
VSEARCH_NUM_CANDIDATES=150
VSEARCH_LIMIT=5
MAX_CONTEXT_CHARS=4000
```

### 🧪 Testing

```bash
# Tests backend
pytest backend/tests/ -v

# Test específico
pytest backend/tests/test_validator_improvements.py -v

# Test con coverage
pytest backend/tests/ --cov=backend --cov-report=html

# Tests frontend
cd frontend
npm test

# E2E tests
npm run test:e2e
```

### 📝 Añadir Nueva Sección (ej: JN.2)

1. **Definir esquema**:
```python
# backend/agents/schemas/json_schemas.py
JN2_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "justificacion": {
            "type": "object",
            "required": ["necesidad", "adecuacion", "eficiencia"],
            "properties": {
                "necesidad": {"type": "string"},
                "adecuacion": {"type": "string"},
                "eficiencia": {"type": "string"}
            }
        }
    },
    "required": ["justificacion"]
}

SECTION_SCHEMAS = {
    "JN.1": JN1_DATA_SCHEMA,
    "JN.2": JN2_DATA_SCHEMA,  # ← Añadir aquí
}
```

2. **Crear prompts**:
```python
# backend/prompts/jn_prompts.py
PROMPT_JN2_A = """
Genera la justificación de la necesidad siguiendo:
1. Necesidad: ¿Por qué es necesario este contrato?
2. Adecuación: ¿Por qué esta solución?
3. Eficiencia: ¿Por qué esta forma de contratación?

Devuelve JSON:
{{
  "justificacion": {{
    "necesidad": "...",
    "adecuacion": "...",
    "eficiencia": "..."
  }}
}}
"""
```

3. **Tests**:
```python
# backend/tests/test_jn2.py
def test_jn2_validation():
    validator = ValidatorAgent(mode="estructurado")
    
    json_a = {
        "expediente_id": "TEST-001",
        "seccion": "JN.2",
        "json": {
            "justificacion": {
                "necesidad": "Test",
                "adecuacion": "Test",
                "eficiencia": "Test"
            }
        }
    }
    
    result = validator.validate_json_a(json_a, "JN.2")
    assert result.is_valid
```

### 🐛 Debugging

```python
# Activar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Usar debugger
import pdb; pdb.set_trace()

# O ipdb (mejor)
import ipdb; ipdb.set_trace()

# En orchestrator
async def debug_node(state):
    print(f"State actual: {state.keys()}")
    print(f"JSON_A: {state.get('json_a')}")
    import ipdb; ipdb.set_trace()
    return state
```

### 📊 Monitoreo en Producción

```python
# LangFuse: Ver en https://cloud.langfuse.com
# TruLens: Dashboard local
python backend/core/run_trulens_dashboard.py
# Abrir http://localhost:8501
```

---

## 📚 Recursos Adicionales

### 🔗 Enlaces Útiles

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LangChain Docs**: https://python.langchain.com/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **React Docs**: https://react.dev/
- **MongoDB Atlas**: https://www.mongodb.com/docs/atlas/
- **OpenAI API**: https://platform.openai.com/docs/

### 📖 Normativa Relevante

- **LCSP**: Ley 9/2017 de Contratos del Sector Público
- **RGPD**: Reglamento (UE) 2016/679
- **DNSH**: Do No Significant Harm (EU Green Deal)
- **Directiva 2014/24/UE**: Contratación pública

### 🎓 Conceptos Clave

**LangGraph**: Framework para construir aplicaciones multi-agente con grafos de estado.

**RAG (Retrieval Augmented Generation)**: Técnica que combina búsqueda de información con generación de texto.

**Vector Embeddings**: Representaciones numéricas de texto que permiten búsqueda semántica.

**JSON_A vs JSON_B**: 
- **JSON_A**: Datos estructurados canónicos (para procesamiento)
- **JSON_B**: Narrativa legal legible (para humanos)

**Binder Schemas**: Esquemas de validación que definen la estructura esperada de los outputs.

---

## ✅ Checklist de Entendimiento

Si has leído este documento completo, deberías poder responder:

- [ ] ¿Qué problema resuelve Mini-CELIA?
- [ ] ¿Cuáles son los componentes principales de la arquitectura?
- [ ] ¿Qué es el Orchestrator y qué hace?
- [ ] ¿Cuál es la diferencia entre Generator A y Generator B?
- [ ] ¿Qué hace el Retriever Agent?
- [ ] ¿Cómo funciona la validación con auto-retry?
- [ ] ¿Qué es JSON_A y JSON_B?
- [ ] ¿Cómo se añade una nueva sección (ej: JN.3)?
- [ ] ¿Qué herramientas de observability se usan?
- [ ] ¿Cómo exportar un PDF desde el frontend?

---

## 🎯 Próximos Pasos

### Para Desarrolladores Nuevos:

1. **Día 1**: Setup local + explorar frontend
2. **Día 2**: Entender orchestrator + ejecutar test JN.1
3. **Día 3**: Crear nuevo agente simple
4. **Día 4**: Añadir nueva sección JN.2
5. **Día 5**: Implementar mejora en validador

### Para Product Owners:

1. Entender capacidades actuales (JN.1 completo)
2. Priorizar nuevas secciones (JN.2, JN.3, JN.4, JN.5)
3. Definir roadmap de documentos (PPT, PCAP, CEC)
4. Evaluar integraciones con otros sistemas

### Para Administradores:

1. Configurar entorno de producción
2. Setup MongoDB Atlas
3. Configurar observability (LangFuse + TruLens)
4. Implementar backup y disaster recovery
5. Monitorear costos de APIs (OpenAI)

---

## 📞 Soporte

**Documentación técnica**: `/docs`
**Issues**: GitHub Issues
**Preguntas**: GitHub Discussions

---

<div align="center">

**🚀 Mini-CELIA - Transformando la Administración Pública con IA**

*Desarrollado con ❤️ por el equipo de ADD4U*

**Versión**: 3.0  
**Fecha**: 20 de Octubre de 2025  
**Licencia**: MIT

</div>

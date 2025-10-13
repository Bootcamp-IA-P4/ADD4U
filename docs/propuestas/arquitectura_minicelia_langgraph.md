# 🧠 Mini-CELIA – Arquitectura Unificada con LangGraph y Prompts Dinámicos

Copiloto asistido por IA para la preparación de expedientes de licitación pública.  
Este documento describe la **arquitectura completa actualizada** del proyecto Mini-CELIA, integrando las aportaciones del stakeholder (binder de prompts dinámicos) con la nueva **orquestación de agentes LangGraph**.

Su propósito es que cualquier miembro del equipo pueda entender el funcionamiento global del sistema, cómo se conectan las piezas y cómo avanzar paso a paso en la implementación.

---

## 🎯 Objetivo General

Mini-CELIA asiste en la **preparación de expedientes de licitación pública**, automatizando la generación de documentos mediante agentes de IA especializados.

Documentos gestionados:
- **JN** – Justificación de la Necesidad  
- **PPT** – Pliego Técnico  
- **CEC** – Cuadro Económico  
- **CR** – Cuadro Resumen  

Cada documento se genera **por secciones**, aplicando un flujo orquestado de agentes que:
1. Recuperan contexto normativo y de expedientes (RAG).
2. Generan contenido estructurado (Prompt A).
3. Validan el resultado contra normativa y esquema.
4. Generan la narrativa (Prompt B).
5. Validan coherencia narrativa y estilo.
6. Guardan todos los resultados con trazabilidad.
7. Ensamblan y validan el documento completo.

---

## 🧩 Estructura del Proyecto

```
backend/
 ├── api/
 │   ├── jn_routes.py
 │   ├── routes_outputs.py
 │   └── ...
 │
 ├── agents/
 │   ├── jn_agent.py                # Generador de secciones JN (Prompt A y B)
 │   ├── validator_agent.py         # Agente validador (estructurado, narrativa, global)
 │   ├── retriever_agent.py         # Recupera normativa y expedientes (RAG)
 │   ├── prompt_manager.py          # Nuevo: genera prompts dinámicos desde el binder
 │   ├── assembler_agent.py         # Ensambla narrativas
 │   └── orchestrator.py            # Nuevo: flujo LangGraph orquestado
 │
 ├── database/
 │   ├── mongo.py
 │   ├── outputs_repository.py      # Guarda outputs con trazabilidad
 │   └── ...
 │
 ├── prompts/
 │   ├── binder.json                # Binder dinámico: configuración de cada sección
 │   ├── prompt_a_template.txt      # Plantilla base Prompt A
 │   ├── prompt_b_template.txt      # Plantilla base Prompt B
 │   ├── prompt_validator.txt
 │   └── ...
 │
 ├── models/
 │   ├── schemas_jn.py
 │   └── ...
 │
 └── core/
     ├── logic_jn.py
     └── ...
```

---

## 🧠 Arquitectura de Agentes

### 1. **Prompt Manager Agent**
Construye los prompts de forma dinámica a partir del **binder**, una librería JSON que define:
- Qué plantilla usar para cada sección.
- Qué variables deben inyectarse.
- Qué versión del prompt se está utilizando.

```python
from pathlib import Path
import json

class PromptManager:
    def __init__(self, binder_path="backend/prompts/binder.json"):
        with open(binder_path, "r", encoding="utf-8") as f:
            self.binder = json.load(f)

    def build_prompt(self, documento: str, seccion: str, tipo: str):
        config = self.binder[documento][seccion]
        template_path = Path(config[f"prompt_{tipo}_template"])
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        prompt = template.format(**config["variables"])
        return {"prompt": prompt, "version": config["version"]}
```

**Ejemplo de binder.json:**
```json
{
  "JN": {
    "JN.1": {
      "version": "1.0.0",
      "prompt_A_template": "backend/prompts/prompt_a_template.txt",
      "prompt_B_template": "backend/prompts/prompt_b_template.txt",
      "variables": {
        "objetivo": "Justificar la necesidad del contrato",
        "referencia_normativa": "Ley 9/2017 de Contratos del Sector Público"
      }
    }
  }
}
```

---

### 2. **Retriever Agent (RAG)**
Busca contexto relevante desde Mongo (embeddings, normativa y expedientes).  
Integra tanto búsqueda vectorial como consultas directas para trazabilidad.

```python
from backend.database.mongo import get_collection
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
import os

class RetrieverAgent:
    def __init__(self):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
            connection_string=os.getenv("MONGO_URI"),
            namespace="Golden.embeddings",
            embedding=embeddings,
            index_name="default"
        )

    async def retrieve(self, query: str, expediente_id: str):
        results = self.vectorstore.similarity_search(query, k=3)
        context_text = "\n\n".join([r.page_content for r in results])
        expedientes = get_collection("expedientes")
        expediente_doc = await expedientes.find_one({"expediente_id": expediente_id})
        return {
            "contexto": context_text,
            "expediente": expediente_doc,
            "citas_normativas": [r.metadata for r in results]
        }
```

---

### 3. **Validator Agent**
Valida los resultados en tres modos distintos.

```python
class ValidatorAgent:
    def __init__(self, mode: str):
        self.mode = mode

    async def validate_document(self, content: dict):
        if self.mode == "estructurado":
            prompt = "Valida el JSON estructurado..."
        elif self.mode == "narrativa":
            prompt = "Valida la narrativa comparándola con JSON_A..."
        elif self.mode == "global":
            prompt = "Revisa coherencia, estilo y cumplimiento general..."
        return {"validado": True, "modo": self.mode}
```

---

### 4. **Orchestrator (LangGraph)**

El orquestador coordina todos los agentes.  
Cada agente es un nodo del grafo.

```python
from langgraph.graph import StateGraph, END
from backend.agents.retriever_agent import RetrieverAgent
from backend.agents.prompt_manager import PromptManager
from backend.agents.jn_agent import GeneratorA, GeneratorB
from backend.agents.validator_agent import ValidatorAgent
from backend.database.outputs_repository import save_output

graph = StateGraph()

retriever = RetrieverAgent().as_node("retriever")
prompt_manager = PromptManager().as_node("prompt_manager")
generator_a = GeneratorA().as_node("generator_a")
validator_a = ValidatorAgent("estructurado").as_node("validator_a")
generator_b = GeneratorB().as_node("generator_b")
validator_b = ValidatorAgent("narrativa").as_node("validator_b")
save_node = save_output.as_node("save_output")

graph.add_edge("retriever", "prompt_manager")
graph.add_edge("prompt_manager", "generator_a")
graph.add_edge("generator_a", "validator_a")
graph.add_edge("validator_a", "generator_b")
graph.add_edge("generator_b", "validator_b")
graph.add_edge("validator_b", "save_output")
graph.add_edge("save_output", END)

workflow = graph.compile()
```

Ejecución:
```python
result = await workflow.ainvoke({
    "expediente_id": "EXP-001",
    "documento": "JN",
    "seccion": "JN.1",
    "user_text": "Queremos montar un mercadillo con 15 puestos."
})
```

---

### 5. **Persistencia y Trazabilidad**

```python
async def save_output(expediente_id, documento, seccion, nodo, content, prompt_version="", prompt_used=""):
    collection = get_collection("outputs")
    doc = {
        "expediente_id": expediente_id,
        "documento": documento,
        "seccion": seccion,
        "nodo": nodo,
        "prompt_version": prompt_version,
        "prompt_used": prompt_used,
        "data": content.get("data", {}),
        "narrativa": content.get("narrativa", {}),
        "citas_normativas": content.get("citas_normativas", []),
        "dependencias": content.get("dependencias", []),
        "estado": "draft",
        "timestamp": datetime.utcnow().isoformat(),
        "raw": content
    }
    await collection.insert_one(doc)
```

---

## 🔄 Flujo General (Resumen Visual)

### Por Sección
```mermaid
graph TD
    A[Retriever (RAG)] --> B[Prompt Manager]
    B --> C[Generator A]
    C --> D[Validator (estructurado)]
    D --> E[Generator B]
    E --> F[Validator (narrativa)]
    F --> G[Save Output A+B]
```

### Global
```mermaid
graph TD
    H[Assembler (concatena narrativas)] --> I[Validator (global)]
    I --> J[Save Output VALIDATED]
```

---

## ⚙️ Configuración paso a paso

1. **Configurar .env:**
   ```bash
   MONGO_URI=mongodb+srv://user:pass@cluster
   INDEX_NAME=default
   ```

2. **Binder JSON** define las reglas de cada documento/sección.

3. **Prompt Manager** genera el texto del prompt dinámicamente.

4. **Retriever** trae contexto (embeddings + expediente).

5. **Generators A/B** generan JSON_A y JSON_B respectivamente.

6. **Validators** revisan estructura, narrativa y documento global.

7. **Outputs Repository** guarda todo con metadatos y hashes.

8. **LangGraph Orchestrator** define el flujo y ejecuta los agentes.

---

## 🚀 Próximos pasos

1. Implementar prompt_manager.py y probar la carga del binder.  
2. Integrar el Prompt Manager en jn_agent.  
3. Añadir consultas directas a expedientes en el RetrieverAgent.  
4. Crear el flujo en orchestrator.py (LangGraph).  
5. Verificar la trazabilidad completa en la colección outputs.  
6. Ampliar el sistema para PPT, CEC y CR.  
7. Añadir validación global y revisión humana en la UI.

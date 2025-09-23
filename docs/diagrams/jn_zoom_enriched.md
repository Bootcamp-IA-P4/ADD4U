# 🔍 Zoom Enriquecido – Generación de la Justificación de la Necesidad (JN)

```mermaid
%%{init: {'theme':'redux'}}%%
flowchart TD
    U[👤 Usuario] --> S{¿Slots JN completos?}
    S -->|No| R1[Repreguntar al usuario]
    S -->|Sí| O[⚙️ Orquestador]

    O --> G[📚 Golden Repo normativa: LCSP, RGPD, DNSH]
    O --> M[🤖 Modelo GPT-5 / Claude – narrativa legal]
    G --> M

    M --> V1{¿Plazo > 0 y objeto no vacío?}
    V1 -->|No| R2[Error: repreguntar datos básicos]
    V1 -->|Sí| V2

    V2{¿Presupuesto coherente con slots?}
    V2 -->|No| R3[Error: revisar presupuesto]
    V2 -->|Sí| V[🔒 Validador JN]

    V --> N{¿Normativa completa?}
    N -->|No| A[Auto-inyección de cláusulas faltantes]
    N -->|Sí| DB[(🗄️ MongoDB)]

    DB --> OUT[📤 Documento JN en JSON / PDF / DOCX]

```
## 📖 Glosario de bloques

- **Usuario 👤** → Introduce los datos de la JN (objeto, contexto, presupuesto, plazo).  
- **Slots JN completos ✅** → Revisión de que los campos mínimos estén rellenos.  
  - ❌ Si falta → repregunta al usuario.  
- **Orquestador ⚙️** → Coordina el flujo hacia modelo y normativa.  
- **Golden Repo 📚** → Repositorio normativo (LCSP, RGPD, DNSH, igualdad, accesibilidad).  
- **Modelo 🤖** → Genera la narrativa legal de la JN en base a slots + normativa.  
- **Validación plazo/objeto** → Revisa que `plazo > 0` y `objeto` no esté vacío.  
- **Validación presupuesto** → Comprueba coherencia entre presupuesto y slots.  
- **Validador JN 🔒** → Chequea normativa y coherencia antes de guardar.  
- **Auto-inyección 🔄** → Si falta normativa, el sistema la añade automáticamente.  
- **MongoDB 🗄️** → Guarda el documento en JSON estructurado.  
- **Exportación 📤** → Genera los documentos finales (JSON, PDF, DOCX).  

# 🌍 Esquema Global – Mini-CELIA

```mermaid
flowchart LR
    U[Usuario] --> F[Frontend React - wizard/chat]
    F --> O[Orquestador - FastAPI + LangGraph]
    O --> JN[Agente JN – Justificación de la Necesidad]
    O --> PPT[Agente PPT – Pliego Técnico]
    O --> CEC[Agente CEC – Cuadro Económico]
    O --> CR[Agente CR – Cuadro Resumen]
    JN --> V[Validador Normativo + Coherencia]
    PPT --> V
    CEC --> V
    CR --> V
    V --> DB[(MongoDB + Golden Repo)]
    V --> OUT[Exportación DOCX/PDF/JSON]

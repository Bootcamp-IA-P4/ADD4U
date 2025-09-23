
# 🔍 Zoom – Generación de la Justificación de la Necesidad (JN)

```mermaid

---
config:
      theme: redux
---
flowchart TD
    U[Usuario] --> S[Slots JN: objeto, contexto, presupuesto, plazo]
    S --> O[Orquestador]
    O --> G[Golden Repo normativa LCSP RGPD DNSH]
    O --> M[Modelo GPT-5 Claude narrativa legal]
    G --> M
    M --> V[Validador JN reglas modelo ligero]
    V --> DB[(MongoDB)]
    V --> OUT[Documento JN en JSON PDF DOCX]

# 📑 Guía Operativa y Técnica – Flujo Enriquecido de la Justificación de la Necesidad (JN)

Este documento actúa como **guía de referencia específica** para la generación de la **Justificación de la Necesidad (JN)** dentro de Mini-CELIA.  
Conecta el flujo operativo con el **JSON canónico, validaciones, outputs, dependencias y errores comunes**, de forma que cualquier miembro pueda consultar el proceso en detalle.

---

## 1. Tabla de agentes y validaciones

| Agente        | Rol                                      | JSON campos principales                          | Validaciones                                       | Output              | Posibles errores                          |
|---------------|------------------------------------------|-------------------------------------------------|---------------------------------------------------|---------------------|-------------------------------------------|
| **Usuario**   | Proporciona la información inicial       | `objeto`, `contexto`, `plazo`, `presupuesto`    | Todos los campos obligatorios deben estar presentes | Slots validados     | Slots incompletos → repregunta en frontend |
| **Orquestador** | Coordina flujo entre modelo y normativa | –                                               | –                                                 | Slots procesados    | Falla conexión con modelo → reintento      |
| **Golden Repo** | Fuente normativa base                  | `normativa`                                     | Debe incluir RGPD, DNSH, igualdad, accesibilidad  | Normativa inyectada | Falta normativa → auto-inyección           |
| **Modelo**    | Genera narrativa legal                  | Slots + normativa                               | –                                                 | Narrativa JN        | Narrativa incompleta → reintento           |
| **Validador JN** | Comprueba coherencia y normativa      | `objeto`, `plazo`, `presupuesto`, `normativa`   | `plazo > 0`, `objeto != vacío`, `presupuesto > 0` | JN validado         | Incoherencias detectadas → corrección      |
| **MongoDB**   | Almacena el documento                   | Todos                                           | –                                                 | JSON JN persistente | Error de guardado → rollback               |
| **Exportador**| Genera salidas editables                | Todos                                           | –                                                 | JSON / DOCX / PDF   | Error exportación → reintento              |

---

## 2. Dependencias con otros documentos

- **JN → CEC**: el presupuesto definido en la JN debe coincidir con el que se use en el Cuadro Económico.  
- **JN → CR**: los plazos de ejecución definidos en la JN deben heredarse en el CR.  
- **JN → PPT**: el objeto y contexto de la JN sirven de base para definir fases y entregables en el PPT.  

---

## 3. Errores comunes y resolución

- ❌ **Slots incompletos** → el frontend repregunta al usuario antes de continuar.  
- ❌ **Objeto vacío o plazo ≤ 0** → error de validación, no se genera narrativa hasta corregir.  
- ❌ **Presupuesto incoherente** → bloquea exportación y repregunta valores.  
- ❌ **Normativa faltante** → el Validador inyecta automáticamente las cláusulas.  
- ❌ **Fallo de exportación** → se reintenta generar PDF/DOCX/JSON.  

---

## 4. Estrategia de escalado

- Este flujo detallado de JN sirve como **plantilla** para el resto de documentos.  
- En cada caso se añaden validaciones específicas:  
  - **PPT** → fases, entregables y metodología.  
  - **CEC** → cálculos económicos y coherencia presupuestaria.  
  - **CR** → coherencia administrativa y criterios de adjudicación.  

---

## 0. Diagrama de Flujo Enriquecido JN

```mermaid
%%{init: {'theme':'redux'}}%%
flowchart TD
    U[👤 Usuario] --> S{¿Slots JN completos?}
    S -->|No| R1[Repregunta en frontend]
    S -->|Sí| O[⚙️ Orquestador]

    O --> G[📚 Golden Repo normativa: LCSP, RGPD, DNSH]
    O --> M[🤖 Modelo GPT-5 / Claude – narrativa legal]
    G --> M

    M --> V1{¿Plazo > 0 y objeto no vacío?}
    V1 -->|No| R2[Error: repreguntar datos básicos]
    V1 -->|Sí| V2

    V2{¿Presupuesto coherente?}
    V2 -->|No| R3[Error: revisar presupuesto]
    V2 -->|Sí| V[🔒 Validador JN]

    V --> N{¿Normativa completa?}
    N -->|No| A[Auto-inyección de cláusulas faltantes]
    N -->|Sí| DB[(🗄️ MongoDB)]

    DB --> OUT[📤 Documento JN en JSON / PDF / DOCX]

# 📑 Guía Operativa y Técnica – Flujo Enriquecido de Mini-CELIA

Este documento actúa como **guía central de referencia** para el equipo.  
Conecta la arquitectura multiagente con el **JSON canónico, validaciones, outputs, dependencias y errores comunes**, de forma que cualquier miembro pueda consultar el flujo en detalle y entender qué hace cada bloque.

---

## 1. Tabla de agentes y validaciones

| Agente        | Rol                                         | JSON campos principales                          | Validaciones                                       | Output                        | Posibles errores                          |
|---------------|---------------------------------------------|-------------------------------------------------|---------------------------------------------------|--------------------------------|-------------------------------------------|
| **JN**        | Redacta la Justificación de la Necesidad    | `objeto`, `contexto`, `plazo`, `presupuesto`    | `plazo > 0`, `objeto != vacío`                    | JSON JN + narrativa            | Slots incompletos → repregunta al usuario |
| **PPT**       | Define requisitos técnicos                  | `fases`, `metodología`, `entregables`           | –                                                 | JSON PPT                       | Entregables vacíos → warning              |
| **CEC**       | Calcula presupuesto                         | `pbl_base`, `iva_tipo`, `pbl_total`, `lotes`    | `pbl_total = pbl_base * (1+IVA)`                  | JSON CEC                       | Incoherencia presupuestaria → error       |
| **CR**        | Cuadro resumen administrativo               | Todos los anteriores                            | `criterios_adjudicacion = 100%`                   | JSON CR                        | Criterios ≠ 100% → repregunta             |
| **Validador** | Coherencia + normativa transversal          | Todos                                           | Inclusión de RGPD, DNSH, igualdad, accesibilidad  | Expediente validado y completo | Normativa faltante → auto-inyección       |

---

## 2. Dependencias entre documentos

- **JN → CEC**: el presupuesto indicado en la Justificación de la Necesidad debe coincidir con el del Cuadro Económico.  
- **JN → CR**: los plazos de ejecución definidos en la JN deben heredarse en el CR.  
- **PPT → CR**: las fases y entregables resumidos deben aparecer en el CR.  
- **CEC → CR**: los importes del CEC deben trasladarse íntegramente al CR.  

---

## 3. Errores comunes y resolución

- ❌ **Slots incompletos** → el frontend repregunta al usuario antes de continuar.  
- ❌ **Presupuesto incoherente** → el agente CEC devuelve error y bloquea la exportación hasta corregir.  
- ❌ **Criterios adjudicación ≠ 100%** → repregunta automática al usuario.  
- ❌ **Normativa faltante** → el Validador la inyecta automáticamente antes de guardar/exportar.  

---

## 4. Estrategia de escalado

- Este flujo detallado se ha trabajado sobre **JN** como ejemplo.  
- La misma lógica se aplicará de forma específica a:  
  - **PPT** → validaciones de fases/entregables.  
  - **CEC** → validaciones económicas.  
  - **CR** → coherencia administrativa.  
- La arquitectura multiagente permite añadir más documentos (ej. contratos de obras) sin romper la estructura.  

---

✅ Con esta guía, cualquier miembro del equipo puede:  
- Ver qué **campos JSON** corresponden a cada agente.  
- Entender qué **validaciones** se aplican y cómo se resuelven los errores.  
- Identificar las **dependencias entre documentos**.  
- Consultar qué hace el **Validador** para asegurar normativa y coherencia.  

---

# 📑 Guía Operativa y Técnica – Flujo Enriquecido de Mini-CELIA

Este documento actúa como **guía central de referencia** para el equipo.  
Conecta la arquitectura multiagente con el **JSON canónico, validaciones, outputs, dependencias y errores comunes**, de forma que cualquier miembro pueda consultar el flujo en detalle y entender qué hace cada bloque.

---

## 0. Diagrama de Flujo Enriquecido

```mermaid
%%{init: {'theme':'redux'}}%%
flowchart TD
    U[👤 Usuario] --> S{¿Slots completos?}
    S -->|No| R1[Repregunta en frontend]
    S -->|Sí| O[⚙️ Orquestador]

    O --> JN[📄 Agente JN]
    O --> PPT[📑 Agente PPT]
    O --> CEC[💰 Agente CEC]
    O --> CR[📋 Agente CR]

    CEC --> V1{¿Presupuesto coherente?}
    V1 -->|No| R2[Error: incoherencia presupuestaria]
    V1 -->|Sí| V

    CR --> V2{¿Criterios = 100%?}
    V2 -->|No| R3[Repregunta usuario]
    V2 -->|Sí| V

    JN --> V
    PPT --> V
    V1 --> V
    V2 --> V

    V[🔒 Validador Normativo y Coherencia]
    V --> N{¿Normativa completa?}
    N -->|No| A[Auto-inyección de cláusulas RGPD/DNSH/Igualdad/Accesibilidad]
    N -->|Sí| DB[(🗄️ MongoDB + 📚 Golden Repo)]

    DB --> OUT[📤 Exportación final: JSON / DOCX / PDF]

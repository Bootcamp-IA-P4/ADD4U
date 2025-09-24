# 📑 Guía Operativa – JN.1 Objeto y Alcance

Este documento describe la primera sección de la **Justificación de la Necesidad (JN)**: el **Objeto y Alcance del contrato**.  
El objetivo es definir de forma estructurada qué se contrata, para qué sirve y a qué áreas o servicios afecta.

---

## 1. Campos JSON y validaciones

| Campo JSON    | Descripción                               | Validación                         | Error posible          | Acción del sistema   |
|---------------|-------------------------------------------|------------------------------------|------------------------|----------------------|
| `objeto`      | Objeto del contrato                       | No vacío, longitud > 10 caracteres | Campo vacío o muy corto | Repreguntar usuario |
| `alcance`     | Áreas o servicios cubiertos               | Lista no vacía                     | Lista vacía            | Repreguntar usuario |
| `categoria`   | Tipo de contrato (`suministro/servicio`)  | Valor permitido (enum)             | Valor no válido        | Repreguntar usuario |

---

## 2. Dependencias con otros documentos

- **JN.1 → PPT**: el objeto alimenta la definición de entregables y requisitos técnicos.  
- **JN.1 → CR**: el objeto se incluye en el resumen administrativo.  

---

## 3. Errores comunes y resolución

- ❌ **Objeto vacío** → repreguntar usuario antes de avanzar.  
- ❌ **Categoría no válida** → mostrar opciones válidas (`suministro`, `servicio`, `obra`).  
- ❌ **Alcance no definido** → repreguntar usuario o marcar en `faltantes[]`.  

---

## 4. Diagrama de flujo – JN.1

```mermaid
%%{init: {'theme':'redux'}}%%
flowchart TD
    U[👤 Usuario] --> S{¿Objeto definido?}
    S -->|No| R1[Repreguntar usuario]
    S -->|Sí| C1{¿Categoría válida?}
    C1 -->|No| R2[Mostrar opciones válidas]
    C1 -->|Sí| C2{¿Alcance definido?}
    C2 -->|No| R3[Repreguntar usuario o marcar faltantes]
    C2 -->|Sí| OUT[📤 JSON estructurado JN.1]

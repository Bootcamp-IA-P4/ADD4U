# 📑 Guía Operativa – JN.1 Objeto y Alcance

Esta sección define de forma clara el **Objeto y Alcance del contrato**, estableciendo:
- Qué se contrata (objeto).
- Qué actividades o servicios cubre (alcance resumido).
- Dónde aplica (ámbito).

---

## 1. Campos JSON y validaciones

| Campo JSON          | Descripción                                      | Validación                       | Error posible       | Acción del sistema   |
|---------------------|--------------------------------------------------|----------------------------------|---------------------|----------------------|
| `objeto`            | Descripción del objeto de la licitación           | No vacío, longitud > 10 caracteres | Campo vacío/corto   | Repreguntar usuario |
| `alcance_resumido`  | Resumen de actividades o servicios incluidos      | No vacío                         | Campo vacío         | Repreguntar usuario |
| `ambito`            | Ámbito geográfico o institucional de aplicación   | No vacío                         | Campo vacío         | Repreguntar usuario |

---

## 2. Dependencias con otros documentos

- **JN.1 → PPT**: el objeto alimenta la definición de fases y entregables.  
- **JN.1 → CR**: el objeto y ámbito se incluyen en el resumen administrativo.  

---

## 3. Errores comunes y resolución

- ❌ **Objeto vacío o muy genérico** → repreguntar antes de avanzar.  
- ❌ **Alcance resumido ausente** → marcar en `faltantes[]`.  
- ❌ **Ámbito no definido** → repreguntar usuario.  

---

## 4. Diagrama de flujo – JN.1

```mermaid
%%{init: {'theme':'default'}}%%
flowchart TD
    U[👤 Usuario] --> S{¿Objeto definido?}
    S -->|No| R1[Repreguntar usuario]
    S -->|Sí| C1{¿Alcance resumido definido?}
    C1 -->|No| R2[Repreguntar o marcar faltantes]
    C1 -->|Sí| C2{¿Ámbito definido?}
    C2 -->|No| R3[Repreguntar usuario]
    C2 -->|Sí| OUT[📤 JSON estructurado JN.1]

# 🤖 Mini-CELIA — Copilot Inteligente de Licitaciones para la Administración
<div align="center">
  <img src="https://github.com/user-attachments/assets/bcc32bb3-f826-44a9-955c-4f369ae98a77" alt="Imagen 1" width="600" style="margin-right: 20px;" />
  <img src="https://github.com/user-attachments/assets/af42f077-9189-456c-b93b-4b0c81d09278" alt="Imagen 2" width="220" />
</div>
<div align="center">

**Sistema de IA especializado que automatiza la generación de documentación para licitaciones públicas en España, reduciendo tiempos de semanas a minutos con cumplimiento normativo garantizado**

![Status](https://img.shields.io/badge/Status-Activo-brightgreen)
![Version](https://img.shields.io/badge/Version-3.0-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

### 🛠️ Tecnologías

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq&logoColor=white" alt="Groq">
</p>

</div>

---

## 📋 **¿Qué es Mini-CELIA?**

**Mini-CELIA** (Copilot Inteligente de Licitaciones para la Administración) es un **sistema de IA multi-agente** que automatiza la generación de documentación para procesos de licitación pública en España. Utilizando **arquitectura LangGraph**, coordina múltiples agentes especializados (Retriever RAG, Generadores, Validadores) para producir documentos completos con **validación automática** y **cumplimiento normativo garantizado**.

### 🎯 **Problema que Resuelve**

En la administración pública española, preparar documentación de licitación es:
- ⏱️ **Lento**: 2-4 semanas por expediente
- 📚 **Complejo**: Requiere conocimiento profundo de normativa (LCSP, RGPD, DNSH)
- ❌ **Propenso a errores**: Riesgo de incumplimiento normativo
- 🔄 **Repetitivo**: Mismos patrones en documentos similares

### ✅ **Solución: Mini-CELIA**

Mini-CELIA automatiza el proceso completo:
- ⚡ **Rápido**: De semanas a **menos de 10 segundos**
- 🤖 **Inteligente**: Sistema multi-agente con **auto-validación y auto-reparación**
- ✅ **Compliant**: Cumplimiento normativo automático (LCSP + RGPD + DNSH)
- 📊 **Trazable**: Observabilidad completa con LangFuse y TruLens
- 📄 **Exportable**: PDF multi-sección con narrativas legales completas

---

## 🚀 **Instalación Completa desde Cero**

### 📋 **Prerequisitos**
- 🐍 **Python 3.11+** ([Descargar](https://www.python.org/downloads/))
- 📦 **Node.js 18+** ([Descargar](https://nodejs.org/))
- 🔑 **OpenAI API Key** ([Obtener](https://platform.openai.com/api-keys)) (opcional)
- 🔑 **Groq API Key** ([Obtener](https://console.groq.com/keys)) (opcional)
- 🍃 **MongoDB** ([Atlas Cloud](https://mongodb.com/atlas) o local)

---

## ⚙️ **Paso 1: Configuración del Entorno**

### **1.1 Clonar el Repositorio**
```bash
git clone https://github.com/Bootcamp-IA-P4/ADD4U.git
cd ADD4U
```

### **1.2 Crear y Activar Entorno Virtual**

#### **🪟 Windows (PowerShell)**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Si tienes problemas de permisos, ejecuta primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **🪟 Windows (CMD)**
```cmd
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate.bat
```

#### **🐧 Linux / 🍎 macOS (Bash/Zsh)**
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate
```

#### **🪟 Windows (Git Bash)**
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/Scripts/activate
```

> **💡 Verificación**: Deberías ver `(.venv)` al inicio de tu línea de comandos

### **1.3 Configurar Variables de Entorno**

**Crear archivo `.env` desde la plantilla:**
```bash
# Copiar plantilla de variables de entorno
cp .env.example .env
```

**Editar el archivo `.env`** con tus credenciales reales (OpenAI API Key, MongoDB URI, etc.). 
El archivo `.env.example` contiene todas las variables necesarias con valores de ejemplo.

> **💡 Nota:** Para desarrollo local, el sistema puede funcionar sin MongoDB ni APIs externas usando datos mock.

> **📄 Variables de Entorno:** Revisa el archivo `.env.example` para ver todas las variables disponibles y su descripción.

---

## ⚙️ **Paso 2: Configuración del Backend (FastAPI)**

### **2.1 Instalar Dependencias de Python**
```powershell
# Asegúrate de que el entorno virtual esté activado
# Deberías ver (.venv) en tu prompt

# Instalar todas las dependencias
pip install -r requirements.txt
```

### **2.2 Ejecutar el Servidor Backend**

#### **🪟 Windows (PowerShell/CMD)**
```powershell
# Asegúrate de tener el entorno virtual activado
# Deberías ver (.venv) en tu prompt

# Ejecutar con uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### **🐧 Linux / 🍎 macOS**
```bash
# Asegúrate de tener el entorno virtual activado
source .venv/bin/activate

# Ejecutar con uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**El backend estará disponible en:** `http://localhost:8000`  
**Documentación Swagger:** `http://localhost:8000/docs`  
**Health Check:** `http://localhost:8000/health`

> **✅ Verificación**: Deberías ver `Application startup complete` en la consola

---

## 🎨 **Paso 3: Configuración del Frontend (React + Vite)**

### **3.1 Instalar Dependencias de Node.js**
```powershell
# Ir al directorio del frontend
cd frontend

# Instalar dependencias
npm install
```

### **3.2 Ejecutar el Frontend**

#### **Todos los Sistemas Operativos**
```bash
# Dentro del directorio frontend/

# Modo desarrollo (con hot reload)
npm run dev

# Build para producción
npm run build

# Preview del build de producción
npm run preview
```

**El frontend estará disponible en:** `http://localhost:5173`

> **✅ Verificación**: Deberías ver el mensaje `Local: http://localhost:5173/` en la consola

---

## 🚦 **Paso 4: Verificación Completa**

### **4.1 Verificar que Todo Funciona**

#### **1. Backend funcionando:**

**🪟 Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
# Debería responder: {"status":"ok","service":"mini-celia-backend","timestamp":"..."}
```

**🐧 Linux / 🍎 macOS:**
```bash
curl http://localhost:8000/health
# Debería responder: {"status":"ok","service":"mini-celia-backend","timestamp":"..."}
```

**🌐 Navegador:**
- Abrir `http://localhost:8000/docs` (Swagger UI)
- Verificar que se muestra la documentación de la API

#### **2. Frontend funcionando:**
- Abrir navegador en `http://localhost:5173`
- Verificar que la interfaz carga correctamente
- Verificar que el chat muestra el mensaje de bienvenida

#### **3. Integración backend-frontend:**
- Escribir en el chat: "Hola"
- Verificar respuesta del bot
- Probar generación: "Generar JN.1 para servicios de limpieza"
- Verificar que se genera la narrativa completa

### **4.2 Solución de Problemas Comunes**

#### **❌ Error: "Backend not available" o "Connection refused"**

**🪟 Windows:**
```powershell
# Verificar que el backend esté corriendo en puerto 8000
netstat -an | findstr :8000

# Verificar proceso Python
Get-Process python
```

**🐧 Linux / 🍎 macOS:**
```bash
# Verificar que el backend esté corriendo en puerto 8000
lsof -i :8000

# O alternativa:
netstat -tuln | grep :8000
```

**Solución**: Asegúrate de que el backend esté ejecutándose y el firewall no bloquee el puerto 8000

---

#### **❌ Error: "Module not found" o "ImportError"**

**Todos los sistemas:**
```bash
# 1. Activar entorno virtual primero
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# 2. Reinstalar dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt

# 3. Verificar instalación
pip list | grep fastapi
```

---

#### **❌ Error: "Cannot activate venv" (Windows)**

**Windows PowerShell:**
```powershell
# Habilitar ejecución de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar cambio:
Get-ExecutionPolicy

# Luego activar:
.\.venv\Scripts\Activate.ps1
```

**Windows CMD (alternativa):**
```cmd
# Usar script .bat en lugar de .ps1
.venv\Scripts\activate.bat
```

---

#### **❌ Error: "Port 8000 already in use"**

**🪟 Windows:**
```powershell
# Encontrar proceso usando puerto 8000
netstat -ano | findstr :8000

# Matar proceso (reemplaza PID con el número encontrado)
taskkill /PID <PID> /F
```

**🐧 Linux / 🍎 macOS:**
```bash
# Encontrar proceso
lsof -ti:8000

# Matar proceso
kill -9 $(lsof -ti:8000)
```

---

#### **❌ Error: Frontend no conecta con Backend**

**Verificar VITE_API_URL:**
```bash
# En frontend/.env
VITE_API_URL=http://localhost:8000

# NO usar https, NO añadir /api al final
```

**Verificar CORS:**
El backend debe permitir peticiones desde `http://localhost:5173`. Esto ya está configurado en `backend/main.py`

---

## 📚 **Comandos de Desarrollo Rápido**

### **Iniciar todo el stack de desarrollo:**

#### **🪟 Windows PowerShell (2 terminales)**
```powershell
# ===== TERMINAL 1 - Backend =====
cd "C:\ruta\a\tu\ADD4U"
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# ===== TERMINAL 2 - Frontend =====
cd "C:\ruta\a\tu\ADD4U\frontend"
npm run dev
```

#### **🪟 Windows CMD (2 terminales)**
```cmd
REM ===== TERMINAL 1 - Backend =====
cd C:\ruta\a\tu\ADD4U
.venv\Scripts\activate.bat
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

REM ===== TERMINAL 2 - Frontend =====
cd C:\ruta\a\tu\ADD4U\frontend
npm run dev
```

#### **🐧 Linux / 🍎 macOS (Bash/Zsh - 2 terminales)**
```bash
# ===== TERMINAL 1 - Backend =====
cd ~/ruta/a/tu/ADD4U
source .venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# ===== TERMINAL 2 - Frontend =====
cd ~/ruta/a/tu/ADD4U/frontend
npm run dev
```

#### **🪟 Windows Git Bash (2 terminales)**
```bash
# ===== TERMINAL 1 - Backend =====
cd /c/ruta/a/tu/ADD4U
source .venv/Scripts/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# ===== TERMINAL 2 - Frontend =====
cd /c/ruta/a/tu/ADD4U/frontend
npm run dev
```

### **Script de inicio rápido (opcional):**

**Crear `start-dev.ps1` (Windows):**
```powershell
# Archivo: start-dev.ps1
Write-Host "🚀 Iniciando Mini-CELIA..." -ForegroundColor Green
.\.venv\Scripts\Activate.ps1
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
uvicorn backend.main:app --reload
```

**Crear `start-dev.sh` (Linux/macOS):**
```bash
#!/bin/bash
echo "🚀 Iniciando Mini-CELIA..."
source .venv/bin/activate
gnome-terminal -- bash -c "cd frontend && npm run dev; exec bash" &
uvicorn backend.main:app --reload
```

---

## 🎯 **Uso del Sistema**

### **Funcionalidades Principales:**

1. **💬 Chat Inteligente**
   - Interfaz conversacional tipo ChatGPT
   - Respuestas contextuales sobre licitaciones
   - Modo offline (sin APIs) y online (con IA)

2. **📋 Generación de Justificación de la Necesidad (JN)**
   - Click en "Generar JN"
   - Introduce ID del expediente
   - Describe la necesidad
   - IA genera la documentación completa

3. **🔍 Validación Normativa**
   - Cumplimiento DNSH
   - Protección de datos RGPD
   - Prevención de fraccionamiento

4. **📊 Exportación**
   - Formatos Word, PDF
   - Plantillas oficiales
   - Metadatos incluidos

### **Flujo de Trabajo Típico:**

```mermaid
flowchart TD

    A[Usuario abre Mini-CELIA] --> B[Chat de bienvenida]
    B --> C["Click \"Generar JN\""]
    C --> D[Introduce ID expediente]
    D --> E[Describe la necesidad]
    E --> F[IA procesa con GPT-4]
    F --> G[Documento JN generado]
    G --> H[Revisar y exportar]

```

---

## 🏗️ **Arquitectura del Sistema**

### **Vista de Alto Nivel**

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

### **🔄 Pipeline Completo: Generación de JN.1**

```
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

### **⏱️ Tiempos de Ejecución**

| Fase | Tiempo Promedio | Descripción |
|------|----------------|-------------|
| Retriever (RAG) | ~1-2 seg | Búsqueda vectorial en MongoDB |
| Generator A | ~3-5 seg | Generación JSON estructurado |
| Validator A | ~100 ms | Validación + Auto-repair si es necesario |
| Generator B | ~3-4 seg | Generación narrativa legal |
| Validator B | ~100 ms | Validación de coherencia |
| **TOTAL** | **~8-12 seg** | **Pipeline completo end-to-end** |

### **🔑 Stack Tecnológico Detallado**

| Capa | Tecnología | Función | Versión |
|------|-----------|---------|---------|
| **🎨 Frontend** | React | Interfaz de usuario | 18.x |
| | Vite | Build tool + HMR | 5.x |
| | Tailwind CSS | Estilos utility-first | 3.x |
| | jsPDF | Generación PDF client-side | Latest |
| | Axios | Cliente HTTP | Latest |
| **🚀 Backend** | FastAPI | Framework web | 0.109+ |
| | Python | Lenguaje | 3.11+ |
| | Uvicorn | Servidor ASGI | Latest |
| | Pydantic | Validación de datos | 2.x |
| **🤖 IA Multi-Agente** | LangGraph | Orquestación de agentes | Latest |
| | LangChain | Framework LLM | Latest |
| | OpenAI GPT-4o | Generación estructurada | Latest |
| | Groq Llama 3.1 | Generación narrativa | 70B |
| **🔍 RAG** | SentenceTransformers | Embeddings vectoriales | all-MiniLM-L6-v2 |
| | MongoDB Atlas | Vector search | 7.0+ |
| **✅ Validación** | BinderSchemas | JSON Schema validation | Custom |
| | OutputParser | Limpieza y parsing | Custom |
| **📊 Observability** | LangFuse | Tracing distribuido | Cloud |
| | TruLens | Métricas y evaluación | Latest |
| **🗄️ Base de Datos** | MongoDB Atlas | Persistencia + Vector DB | 7.0+ |

---

## 🔧 **Configuración Avanzada**

### **Variables de Entorno Detalladas:**

| Variable | Descripción | Valor por Defecto | Requerido |
|----------|-------------|------------------|-----------|
| `OPENAI_API_KEY` | API Key de OpenAI | - | No* |
| `GROQ_API_KEY` | API Key de Groq | - | No* |
| `MONGODB_URI` | Conexión MongoDB | `mongodb://localhost:27017` | No* |
| `VITE_API_URL` | URL del backend | `http://localhost:8000` | Sí |
| `PORT` | Puerto del backend | `8000` | No |
| `DEBUG` | Logs detallados | `true` | No |

> **\*** El sistema funciona offline sin estas variables

### **Modelos de IA Configurables:**

```env
# Modelos OpenAI disponibles
DEFAULT_STRUCTURED_MODEL=gpt-4o-mini          # Más económico
# DEFAULT_STRUCTURED_MODEL=gpt-4o             # Más potente

# Modelos Groq disponibles  
DEFAULT_NARRATIVE_MODEL=llama-3.1-70b-versatile  # Recomendado
# DEFAULT_NARRATIVE_MODEL=llama-3.1-8b-instant   # Más rápido
# DEFAULT_NARRATIVE_MODEL=mixtral-8x7b-32768     # Alternativo
```

### **Configuración de MongoDB:**

**Opción 1 - MongoDB Local:**
```bash
# Instalar MongoDB Community
# Windows: https://www.mongodb.com/try/download/community
# Ubuntu: sudo apt-get install mongodb
# macOS: brew install mongodb/brew/mongodb-community

# Iniciar servicio
mongod --dbpath ./data/db
```

**Opción 2 - MongoDB Atlas (Cloud):**
```env
MONGODB_URI=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/mini_celia?retryWrites=true&w=majority
```

---



## 🧪 **Testing y Desarrollo**

### **Ejecutar Tests:**
```bash
# Tests del backend
pytest backend/tests/ -v

# Tests del frontend  
cd frontend && npm test
```

### **Desarrollo con Hot Reload:**
```bash
# Backend con auto-reload
uvicorn backend.main:app --reload

# Frontend con HMR (Hot Module Replacement)
cd frontend && npm run dev
```

### **Debugging:**
```bash
# Logs detallados del backend
DEBUG=true uvicorn backend.main:app --reload

# Inspeccionar base de datos
mongosh mini_celia --eval "db.expedientes.find().pretty()"
```

---

## 🚀 **Deployment en Producción**

### **Backend (FastAPI):**
```bash
# Build para producción
pip install -r requirements.txt

# Ejecutar con Gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Frontend (React):**
```bash
# Build estático
cd frontend && npm run build

# Servir con servidor web (nginx, apache, etc.)
# Los archivos están en frontend/dist/
```

### **Docker (Opcional):**
```dockerfile
# Dockerfile.backend
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend/
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dockerfile.frontend  
FROM node:18-alpine
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

---



## 👥 **Contribuidores**

<div align="center">

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/stephyangeles">
        <img src="https://github.com/stephyangeles.png" width="100px;" alt="stephyangeles"/>
        <br />
        <sub><b>stephyangeles</b></sub>
      </a>
      <br />
      <sub>Frontend & IA Developer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/abbyenredes">
        <img src="https://github.com/abbyenredes.png" width="100px;" alt="abbyenredes"/>
        <br />
        <sub><b>abbyenredes</b></sub>
      </a>
      <br />
      <sub>IA Developer & Base de Datos</sub>
    </td>
    <td align="center">
      <a href="https://github.com/Jorgeluuu">
        <img src="https://github.com/Jorgeluuu.png" width="100px;" alt="Jorgeluuu"/>
        <br />
        <sub><b>Jorgeluuu</b></sub>
      </a>
      <br />
      <sub>IA Developer & Backend</sub>
    </td>
    <td align="center">
      <a href="https://github.com/mikewig">
        <img src="https://github.com/mikewig.png" width="100px;" alt="mikewig"/>
        <br />
        <sub><b>mikewig</b></sub>
      </a>
      <br />
      <sub>IA Developer & Backend</sub>
    </td>
    <td align="center">
      <a href="https://github.com/merkandez">
        <img src="https://github.com/merkandez.png" width="100px;" alt="merkandez"/>
        <br />
        <sub><b>merkandez</b></sub>
      </a>
      <br />
      <sub>IA Developer & Backend</sub>
    </td>
  </tr>
</table>

</div>

---







## ✨ **Características Principales**

### 🎨 **Interfaz de Usuario**
- 💬 **Chat Conversacional**: Interfaz tipo ChatGPT optimizada para licitaciones
- 📱 **Diseño Responsivo**: Perfecto en móvil, tablet y desktop con Tailwind CSS
- 📄 **Exportación PDF Multi-Sección**: Detecta automáticamente todas las secciones JN generadas (JN.1 a JN.5)
- 💾 **Gestión de Borradores**: Sistema de guardado y carga de trabajos previos
- 🎯 **Ejemplos Integrados**: Panel lateral con casos de uso reales

### 🤖 **Sistema Multi-Agente (LangGraph)**
- 🧠 **Orchestrator**: Coordina flujo completo de 8 pasos con LangGraph
- 🔍 **Retriever Agent (RAG)**: Búsqueda vectorial en MongoDB con embeddings (score > 0.75)
- 📝 **Generator A**: JSON estructurado (JSON_A) con campos validados
- 📖 **Generator B**: Narrativa legal legible (JSON_B) con referencias normativas
- ✅ **Validator Agent**: Validación automática con **auto-retry** (max 2 intentos)
- 🔧 **Output Parser**: Limpieza HTML y parsing centralizado
- 🧹 **Sanitizer**: Conversión automática de valores "faltantes" a campos vacíos

### ⚡ **Validación Inteligente**
- 📋 **BinderSchemas**: Validación contra JSON Schema con estructura nested
- 🔄 **Auto-Repair**: Regeneración automática con prompts especializados si falla validación
- 🎯 **Nested Fields**: Validación recursiva con dot notation (ej: `secciones_JN.objeto`)
- ⚠️ **Warnings**: Sistema de alertas para campos incompletos sin bloquear flujo
- � **Tasa de Éxito**: Del 70% al **95%** con auto-retry implementado

### 📊 **Observabilidad y Monitoreo**
- 🔍 **LangFuse**: Tracing distribuido de todas las invocaciones LLM con contexto
- 📈 **TruLens**: Métricas de evaluación y dashboard local (puerto 8501)
- � **Health Endpoint**: `/health` con timestamp UTC y status del servicio
- 📝 **Logs Estructurados**: Sistema de logging con niveles configurables

### 🚀 **Optimizaciones de Rendimiento**
- ⚡ **Local Cache**: Modelos de embeddings en `./models_cache` (reduce startup de 30s a <3s)
- 🔄 **Async/Await**: Backend completamente asíncrono con FastAPI
- 📦 **HuggingFace Timeout Fix**: Sin dependencia de descarga en cada inicio
- 🎯 **Vector Search**: MongoDB Atlas con índices optimizados (150 candidates, top 5)

### 📄 **Cumplimiento Normativo**
- ✅ **LCSP**: Ley 9/2017 de Contratos del Sector Público
- ✅ **RGPD**: Reglamento (UE) 2016/679 de Protección de Datos
- ✅ **DNSH**: Do No Significant Harm (EU Green Deal)
- ✅ **Directiva 2014/24/UE**: Contratación pública europea

---

## 📂 **Estructura del Proyecto**

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
│   │
│   ├── 📁 api/                              # 🛣️ Endpoints REST
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
│   │   └── schemas_jn.py                    # Modelos de datos JN
│   │
│   ├── 📁 prompts/                          # 💭 Prompts Optimizados
│   │   ├── jn_prompts.py                    # Prompts específicos JN
│   │   └── 📁 templates/                    # Plantillas de prompts
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
│   ├── index.html                           # HTML principal
│   ├── package.json                         # Dependencias NPM
│   ├── postcss.config.js                    # Configuración PostCSS
│   ├── tailwind.config.js                   # Configuración Tailwind
│   └── vite.config.js                       # Configuración Vite
│
├── 📁 docs/                                 # 📚 Documentación
│   ├── 📁 diagrams/flujos/                  # Diagramas de flujo
│   │   ├── jn_operativo.md                  # Flujo operativo JN
│   │   ├── flujo_operativo.md               # Flujo general
│   │   └── bbdd_flujo.md                    # Flujo base de datos
│   │
│   ├── 📁 diagrams/ejemplos_json/           # Ejemplos de estructuras
│   │   ├── output_jsonA.json                # Ejemplo JSON_A
│   │   ├── output_jsonB.json                # Ejemplo JSON_B
│   │   ├── expediente.json                  # Ejemplo expediente
│   │   └── normativa_global.json            # Ejemplo normativa
│   │
│   ├── guia_endpoints_orquestador.md        # Guía API
│   ├── server_setup.md                      # Setup servidor
│   ├── mejoras_sistema_validacion.md        # Doc mejoras validación
│   └── Mini-CELIA-Final-Documento-Informativo.md  # 📖 Doc completo para entender proyecto
│
├── 📁 outputs/                              # 📤 Archivos generados
├── 📁 tests/                                # 🧪 Tests de integración
│
├── 📄 .env                                  # 🔐 Variables de entorno (local)
├── 📄 .env.example                          # 📄 Plantilla variables entorno
├── 📄 .gitignore                            # 🚫 Archivos ignorados Git
├── 📄 README.md                             # 📖 Este documento
├── 📄 requirements.txt                      # 📦 Dependencias Python
└── 📄 package.json                          # 📦 Metadatos proyecto
```

### 📌 **Convenciones de Nomenclatura**

- **`*_agent.py`**: Agentes individuales de LangChain/LangGraph
- **`*_routes.py`**: Endpoints FastAPI agrupados por dominio
- **`schemas_*.py`**: Modelos Pydantic de validación
- **`*.jsx`**: Componentes React
- **`*_prompts.py`**: Colecciones de prompts para IA

---

## 💡 **Cómo Usar Mini-CELIA**

### 🎯 **Ejemplos por Categoría**
Al abrir la aplicación, encontrarás ejemplos organizados en 4 categorías:

#### **📦 Servicios**
- **Servicios de Limpieza**: Ejemplo para limpieza de edificios municipales
- **Mantenimiento Informático**: Soporte técnico para equipos IT

#### **🏗️ Obras**
- **Rehabilitación de Edificio**: Restauración de edificios históricos
- **Pavimentación Urbana**: Obras de mejora de calles y aceras

#### **📋 Suministros**
- **Equipos Informáticos**: Renovación de parque informático
- **Mobiliario de Oficina**: Adquisición de mesas, sillas y archivadores

#### **💼 Consultoría**
- **Auditoría Energética**: Análisis y mejora de eficiencia energética
- **Asesoría Legal**: Servicios jurídicos especializados

> **💡 Consejo**: Haz clic en cualquier ejemplo para prellenarlo en el chat, luego personalízalo con tus datos específicos.

### 💬 **Chat Conversacional**
Escribe directamente en el chat para obtener ayuda personalizada:
```
"Necesito una justificación para contratar servicios de limpieza de 5 edificios"
"Genera documentación para rehabilitar un edificio histórico de 1500m²"
"Ayúdame con la contratación de 50 ordenadores portátiles"
"Quiero hacer una auditoría energética de 10 edificios"
```

### 📋 **Flujo de Trabajo**
1. 🚀 **Iniciar**: Abre la aplicación en `http://localhost:5173`
2. 🎯 **Seleccionar**: Haz clic en un ejemplo o escribe tu consulta
3. 📝 **Personalizar**: Ajusta cantidades, ubicaciones y requisitos específicos
4. ⚡ **Generar**: La IA procesa tu solicitud y genera la documentación completa
5. 📄 **Revisar**: Verifica el contenido generado en formato JSON estructurado
6. 💾 **Exportar**: Descarga en PDF o Word con un clic



---

## 🌟 **Características Avanzadas**

### 🔄 **Modos de Operación**

#### **Modo Online** (Con OpenAI)
- 🧠 Respuestas inteligentes y contextuales
- 📚 Acceso a conocimiento actualizado
- 🎯 Personalización por tipo de licitación
- ✅ Cumplimiento normativo automático

### 📊 **Indicadores de Estado**
- 🟢 **Verde**: Conectado a OpenAI
- 🔴 **Rojo**: Modo offline/simulado
- ⏳ **Amarillo**: Cargando respuesta

### 🎨 **Diseño y UX**
- 🌈 **Tema Corporativo**: Amarillo y blanco elegante
- ✨ **Efectos Glass**: Interfaces modernas y atractivas
- 🎭 **Iconos SVG**: Profesionales 
- 📱 **Mobile First**: Optimizado para dispositivos móviles

---

## 🔒 **Seguridad y Privacidad**

### 🛡️ **Características de Seguridad**
- 🚫 **Sin Autenticación**: No hay datos personales almacenados
- 🔐 **API Keys Locales**: Las claves solo se almacenan localmente
- 🏠 **Procesamiento Local**: Datos no enviados a servidores externos
- 🔄 **Sesiones Temporales**: No hay persistencia de conversaciones

### 📋 **Cumplimiento Normativo**
- ✅ **LCSP**: Ley de Contratos del Sector Público
- ✅ **RGPD**: Reglamento General de Protección de Datos
- ✅ **DNSH**: Do No Significant Harm (EU)
- ✅ **PRTR**: Plan de Recuperación, Transformación y Resiliencia

---

## 🚀 **Roadmap y Futuras Características**

### 🎯 **Próximas Versiones**
- 📄 **Generación PPT** (Pliego de Prescripciones Técnicas)
- 📋 **Generación CEC** (Cuadro de Características)
- ⚖️ **Criterios de Adjudicación** automáticos
- 📊 **Dashboard de Analytics**
- 🔄 **Integración con sistemas ERP**
- 📱 **Aplicación móvil nativa**

### 🎨 **Mejoras Planificadas**
- 🎯 **Plantillas por Organismos**: Adaptadas a diferentes administraciones
- 🤖 **Agentes Especializados**: Por tipos de licitación específicos
- 📚 **Base de Conocimiento**: Jurisprudencia y casos de éxito
- 🔄 **Workflow Completo**: Desde inicio hasta adjudicación

---

## 🤝 **Contribución y Desarrollo**

### 👥 **Equipo de Desarrollo**
Este proyecto ha sido desarrollado como **Proof of Concept (PoC)** para demostrar las capacidades de IA aplicadas al sector público español.

### 🔧 **Para Desarrolladores**

**Configuración inicial:**
```bash
# Fork y clonar repositorio
git clone [repository-url]
cd ADD4U

# Crear branch para tu feature
git checkout -b feature/nueva-funcionalidad
```

**Desarrollo:**
- Seguir **PEP 8** para Python
- Usar **ESLint** para JavaScript
- Documentar funciones nuevas
- Incluir tests unitarios
- Actualizar README si es necesario

**Enviar cambios:**
1. **Commit** tus cambios: `git commit -am 'Add nueva funcionalidad'`
2. **Push** al branch: `git push origin feature/nueva-funcionalidad`
3. **Crear Pull Request**

### 🐛 **Reportar Problemas**
Si encuentras algún problema o tienes sugerencias:
1. 📝 Describe el problema detalladamente
2. 🔄 Incluye pasos para reproducirlo
3. 📸 Adjunta capturas de pantalla si es posible
4. 💻 Especifica tu sistema operativo y navegador

---

## 📞 **Soporte y Documentación**

### **Enlaces Útiles:**
- 📖 **Documentación API:** `http://localhost:8000/docs`
- 🐛 **Reportar Bugs:** [GitHub Issues]
- 💬 **Discusiones:** [GitHub Discussions]

### 📧 **Contacto**
Para consultas técnicas avanzadas o implementaciones empresariales, contacta con el equipo de desarrollo.

---

## 📄 **Licencia y Créditos**

### ⚖️ **Licencia MIT**
Este proyecto está bajo licencia MIT, lo que permite:
- ✅ Uso comercial y personal
- ✅ Modificación y distribución
- ✅ Uso en proyectos privados
- ❌ No incluye garantías

### 🙏 **Créditos**
- **OpenAI GPT-4** para generación de contenido
- **Groq** para modelos open-source
- **FastAPI** por el excelente framework
- **React** y **Vite** por la experiencia de desarrollo
- **MongoDB** para la persistencia de datos

### 🏛️ **Uso en Administración Pública**
Mini-CELIA está diseñado específicamente para:
- 🏢 **Ayuntamientos** de cualquier tamaño
- 🏛️ **Diputaciones** provinciales
- 🎓 **Universidades** públicas
- 🏥 **Organismos** autónomos
- 🚀 **Empresas** del sector público

---

<div align="center">

**🚀 ¡Transforma tu proceso de licitaciones con IA!**

*Desarrollado con ❤️ para modernizar la Administración Pública española*

</div>

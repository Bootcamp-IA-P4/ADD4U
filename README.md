# 🤖 Mini-CELIA — Chatbot Inteligente para Licitaciones Públicas

<div align="center">

**Un asistente de IA especializado en la generación automática de documentación para procesos de licitación pública en España**

![Status](https://img.shields.io/badge/Status-Activo-brightgreen)
![Version](https://img.shields.io/badge/Version-2.0-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## 📋 **¿Qué es Mini-CELIA?**

Mini-CELIA es un **chatbot inteligente** que revoluciona la forma de crear documentación para licitaciones públicas. Utiliza **Inteligencia Artificial** (OpenAI GPT-4) para generar automáticamente las secciones más complejas de los expedientes de licitación, como la **Justificación de la Necesidad (JN)**, siguiendo la normativa española vigente.

### 🎯 **Problema que Resuelve**
- ❌ **Antes**: Redactar documentación de licitaciones tomaba semanas
- ❌ **Antes**: Alto riesgo de errores normativos y de cumplimiento
- ❌ **Antes**: Procesos manuales repetitivos y poco eficientes
- ✅ **Ahora**: Generación automática en minutos con IA
- ✅ **Ahora**: Cumplimiento normativo garantizado
- ✅ **Ahora**: Interfaz intuitiva tipo ChatGPT

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
git clone <tu-repositorio>
cd ADD4U
```

### **1.2 Crear y Activar Entorno Virtual**

**En Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1
# O si tienes problemas de permisos:
.\.venv\Scripts\activate.bat
```

**En Linux/macOS (Bash):**
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate
```

**En Git Bash en Windows:**
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/Scripts/activate
```

### **1.3 Configurar Variables de Entorno**

**Crear archivo `.env` desde la plantilla:**
```bash
# Copiar plantilla de variables de entorno
cp .env.example .env
```

**Editar el archivo `.env` con tus credenciales:**
```env
# APIs de IA (OPCIONALES - funciona sin ellas)
OPENAI_API_KEY=sk-proj-tu-api-key-aqui
GROQ_API_KEY=gsk-tu-groq-key-aqui

# Base de datos (OPCIONAL)
MONGODB_URI=mongodb://localhost:27017/mini_celia

# Frontend
VITE_API_URL=http://localhost:8000
```

> **💡 Nota:** Las API Keys son opcionales. El sistema funciona offline sin ellas usando contenido mock.

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
```powershell
# Opción 1: Ejecutar desde la raíz del proyecto
python -m backend.main

# Opción 2: Usar uvicorn directamente
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Opción 3: Desde el directorio backend
cd backend
uvicorn main:app --reload
```

**El backend estará disponible en:** `http://localhost:8000`
**Documentación Swagger:** `http://localhost:8000/docs`

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
```powershell
# Modo desarrollo (con hot reload)
npm run dev

# Build para producción
npm run build

# Preview del build de producción
npm run preview
```

**El frontend estará disponible en:** `http://localhost:5173`

---

## 🚦 **Paso 4: Verificación Completa**

### **4.1 Verificar que Todo Funciona**

**1. Backend funcionando:**
```bash
curl http://localhost:8000/health
# Debería responder: {"status":"healthy"}
```

**2. Frontend funcionando:**
- Abrir navegador en `http://localhost:5173`
- Verificar que la interfaz carga correctamente
- Probar el chat escribiendo "Hola"

**3. Integración backend-frontend:**
- Hacer clic en "Generar JN" en el chat
- Seguir el flujo conversacional
- Verificar que se conecta con el backend

### **4.2 Solución de Problemas Comunes**

**❌ Error: "Backend not available"**
```bash
# Verificar que el backend esté corriendo en puerto 8000
netstat -an | findstr :8000
# O en Linux/macOS:
lsof -i :8000
```

**❌ Error: "Module not found"**
```bash
# Reinstalar dependencias de Python
pip install -r requirements.txt

# Reinstalar dependencias de Node
cd frontend && npm install
```

**❌ Error: "Cannot activate venv"**
```powershell
# En PowerShell, habilitar ejecución de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego activar:
.\.venv\Scripts\Activate.ps1
```

---

## 📚 **Comandos de Desarrollo Rápido**

### **Iniciar todo el stack de desarrollo:**

**En Windows PowerShell (2 terminales):**
```powershell
# Terminal 1 - Backend
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**En Linux/macOS/Git Bash (2 terminales):**
```bash
# Terminal 1 - Backend
source .venv/bin/activate
uvicorn backend.main:app --reload

# Terminal 2 - Frontend
cd frontend
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
graph TD
    A[Usuario abre Mini-CELIA] --> B[Chat de bienvenida]
    B --> C[Click "Generar JN"]
    C --> D[Introduce ID expediente]
    D --> E[Describe la necesidad]
    E --> F[IA procesa con GPT-4]
    F --> G[Documento JN generado]
    G --> H[Revisar y exportar]
```

---

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────────────────────────────────────────────────────┐
│                     MINI-CELIA ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   REACT     │    │   FASTAPI   │    │  OPENAI     │        │
│  │  Frontend   │◄──►│   Backend   │◄──►│   GPT-4     │        │
│  │ (Port 5173) │    │ (Port 8000) │    │             │        │
│  └─────────────┘    └─────────────┘    └─────────────┘        │
│        │                   │                   │              │
│        │                   │            ┌─────────────┐        │
│        │                   └───────────►│    GROQ     │        │
│        │                                │ Llama 3.1   │        │
│        │                                └─────────────┘        │
│        │                                                       │
│        │            ┌─────────────┐    ┌─────────────┐        │
│        └───────────►│  MONGODB    │    │   VECTOR    │        │
│                     │  Database   │    │  Embeddings │        │
│                     └─────────────┘    └─────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### **Stack Tecnológico:**

**🎨 Frontend:**
- **React 18** con hooks modernos
- **Vite** para desarrollo rápido
- **Tailwind CSS** para estilos
- **Axios** para comunicación HTTP

**🚀 Backend:**
- **FastAPI** con Python 3.11+
- **Pydantic** para validación de datos
- **Uvicorn** como servidor ASGI
- **MongoDB** para persistencia

**🤖 IA & LLM:**
- **OpenAI GPT-4** para generación estructurada
- **Groq (Llama 3.1)** para narrativa
- **LangChain** para orquestación
- **Vector embeddings** para contexto

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

## 📂 **Estructura del Proyecto**

```
ADD4U/
├── 📁 backend/                 # Backend FastAPI
│   ├── 📁 agents/             # Agentes de IA
│   │   └── jn_agent.py        # Agente para JN
│   ├── 📁 api/                # Rutas de la API
│   │   └── jn_routes.py       # Endpoints de JN
│   ├── 📁 core/               # Lógica de negocio
│   │   └── logic_jn.py        # Lógica de JN
│   ├── 📁 models/             # Schemas Pydantic
│   │   └── schemas_jn.py      # Modelos de JN
│   └── main.py                # Entrada principal
├── 📁 frontend/               # Frontend React
│   ├── 📁 src/
│   │   ├── 📁 components/     # Componentes React
│   │   │   └── ChatSection.jsx # Chat principal
│   │   ├── 📁 services/       # Servicios HTTP
│   │   │   └── apiService.js  # Cliente API
│   │   └── App.jsx            # Componente raíz
│   └── package.json           # Dependencias Node
├── 📁 data/                   # Datos de entrenamiento
├── 📁 docs/                   # Documentación
├── .env.example               # Variables de entorno
├── requirements.txt           # Dependencias Python
└── README.md                  # Este archivo
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

## 🤝 **Contribución y Desarrollo**

### **Para Desarrolladores:**

1. **Fork** del repositorio
2. **Crear branch** para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** tus cambios: `git commit -am 'Add nueva funcionalidad'`
4. **Push** al branch: `git push origin feature/nueva-funcionalidad`
5. **Crear Pull Request**

### **Guidelines:**
- Seguir **PEP 8** para Python
- Usar **ESLint** para JavaScript
- Documentar funciones nuevas
- Incluir tests unitarios
- Actualizar README si es necesario

---

## 📄 **Licencia y Créditos**

### **Licencia:**
MIT License - Ver archivo `LICENSE` para detalles

### **Créditos:**
- **OpenAI GPT-4** para generación de contenido
- **Groq** para modelos open-source
- **FastAPI** por el excelente framework
- **React** y **Vite** por la experiencia de desarrollo
- **MongoDB** para la persistencia de datos

### **Autor:**
Desarrollado con ❤️ para modernizar la administración pública española

---

## 🆘 **Soporte y Documentación**

### **Enlaces Útiles:**
- 📖 **Documentación API:** `http://localhost:8000/docs`
- 🐛 **Reportar Bugs:** [GitHub Issues]
- 💬 **Discusiones:** [GitHub Discussions]
- 📧 **Contacto:** [tu-email@ejemplo.com]

### **FAQ:**

**❓ ¿Funciona sin internet?**
✅ Sí, tiene modo offline con contenido mock

**❓ ¿Es gratuito?**
✅ El software es open-source. Solo pagas las APIs de IA que uses

**❓ ¿Cumple la normativa española?**
✅ Sí, está diseñado específicamente para LCSP española

**❓ ¿Puedo personalizarlo para mi organización?**
✅ Completamente personalizable y open-source

---

<div align="center">

**🤖 Mini-CELIA - Revolucionando las Licitaciones Públicas con IA**

*Hecho con ❤️ para la modernización de la administración pública*

</div>

### 🔧 **Configuración de Variables de Entorno**
```powershell
# 1. Copiar plantilla de variables de entorno
copy .env.example .env

# 2. Editar el archivo .env con tus API keys
notepad .env
```

**Contenido del archivo .env:**
```bash
# Configuración OpenAI (REQUERIDO para IA)
OPENAI_API_KEY=sk-proj-tu-openai-api-key-aqui

# Configuración LangChain (opcional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=lsv2_pt_tu-langchain-key-aqui
LANGCHAIN_PROJECT="Mini-CELIA-JN-Prototype"

# Configuración Groq (opcional)
GROQ_API_KEY=gsk_tu-groq-key-aqui

# Configuración MongoDB (para persistencia)
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
```

### 📱 **URLs del Sistema**
- 🌐 **Aplicación Principal**: http://localhost:5173
- 🔧 **API Documentation**: http://localhost:8000/docs
- 📊 **Health Check**: http://localhost:8000/health

---

## ✨ **Características Principales**

### 🎨 **Interfaz de Usuario**
- 💬 **Chat Inteligente**: Interfaz tipo ChatGPT optimizada para licitaciones
- 📱 **Diseño Responsivo**: Perfecto en móvil, tablet y desktop
- 🎯 **Acciones Rápidas**: 6 botones para tareas comunes integrados en el chat
- 🔄 **Tiempo Real**: Respuestas instantáneas con indicador de estado
- 🎭 **Sin Autenticación**: Acceso directo sin registros ni logins

### 🤖 **Inteligencia Artificial**
- 🧠 **OpenAI GPT-4**: Generación de texto de alta calidad
- 📚 **Especializado**: Entrenado específicamente en normativa española
- 🔄 **Modo Offline**: Funciona con respuestas simuladas sin internet
- 🎯 **Contexto Inteligente**: Entiende el contexto de licitaciones públicas

### ⚡ **Generación Automática**
- 📄 **Justificación de la Necesidad (JN)**: Sección completa en segundos
- 🎯 **Acciones Específicas**: "Generar JN para [tipo de servicio]"
- 📋 **Plantillas Inteligentes**: Adaptadas a diferentes tipos de licitación
- ✅ **Cumplimiento Normativo**: Siguiendo LCSP y normativas EU

---

## 🏗️ **Arquitectura del Sistema**

### 🔧 **Stack Tecnológico**

#### **Frontend** (Interfaz de Usuario)
```
React 18 + Vite + Tailwind CSS
├── Componentes Modulares
├── Hooks Personalizados  
├── Estados Globales con Context
├── Diseño Mobile-First
└── Iconos SVG Profesionales
```

#### **Backend** (API + IA)
```
FastAPI + Python 3.11+
├── OpenAI GPT-4 Integration
├── MongoDB Database
├── LangChain Framework
├── Async/Await Architecture
└── RESTful API Design
```

### 📂 **Estructura del Proyecto**
```
ADD4U/
├── 📁 backend/                          # 🔧 API FastAPI + IA
│   ├── agents/                          # 🤖 Agentes de IA especializados
│   │   ├── jn_agent.py                  # Agente para Justificación de Necesidad
│   │   └── __pycache__/                 # Cache de Python
│   ├── api/                             # 🛣️ Rutas y endpoints
│   │   ├── __init__.py
│   │   ├── jn_routes.py                 # Endpoints de JN
│   │   ├── routes_expedientes.py        # Rutas de expedientes
│   │   └── __pycache__/
│   ├── core/                            # ⚡ Lógica central del sistema
│   │   ├── __init__.py
│   │   ├── config.py                    # Configuración global
│   │   ├── logic_jn.py                  # Lógica de negocio JN
│   │   └── __pycache__/
│   ├── database/                        # 🗄️ Conexiones y esquemas DB
│   │   ├── init_expedientes.py          # Inicialización de expedientes
│   │   ├── mongo.py                     # Configuración MongoDB
│   │   └── __pycache__/
│   ├── models/                          # 📋 Esquemas de datos
│   │   ├── __init__.py
│   │   ├── schemas_jn.py                # Schemas para JN
│   │   └── __pycache__/
│   ├── prompts/                         # 💭 Prompts optimizados para IA
│   │   ├── jn_prompts.py                # Prompts específicos de JN
│   │   └── __pycache__/
│   ├── main.py                          # 🚀 Punto de entrada FastAPI
│   └── __init__.py
├── 📁 frontend/                         # 🎨 Aplicación React
│   ├── src/                             # Código fuente
│   │   ├── components/                  # 🧩 Componentes reutilizables
│   │   │   ├── ChatSection.jsx          # Chat principal con IA
│   │   │   ├── DraftModal.jsx           # Modal de borradores
│   │   │   ├── ExportMenu.jsx           # Menú de exportación
│   │   │   ├── Header.jsx               # Header de la app
│   │   │   └── Toast.jsx                # Notificaciones
│   │   ├── contexts/                    # 🔄 Gestores de estado global
│   │   │   └── AppStateContext.jsx      # Context principal
│   │   ├── hooks/                       # 🪝 Hooks personalizados
│   │   ├── pages/                       # 📄 Páginas principales
│   │   │   └── MainApp.jsx              # Aplicación principal
│   │   ├── services/                    # 🌐 Conexión con APIs
│   │   │   └── apiService.js            # Servicio API principal
│   │   ├── utils/                       # 🛠️ Utilidades
│   │   ├── App.jsx                      # Componente raíz
│   │   ├── index.css                    # Estilos globales
│   │   └── main.jsx                     # Punto de entrada React
│   ├── index.html                       # HTML principal
│   ├── package.json                     # Dependencias npm
│   ├── postcss.config.js               # Config PostCSS
│   ├── tailwind.config.js              # Config Tailwind CSS
│   ├── vite.config.js                  # Config Vite
│   └── __init__.py
├── 📁 docs/                            # 📚 Documentación técnica
│   ├── diagrams/                        # Diagramas del sistema
│   │   ├── bbdd_flujo.md
│   │   ├── flujo_operativo.md
│   │   ├── global_scheme.png
│   │   ├── jn_operativo.md
│   │   ├── jn_zoom.png
│   │   ├── ejemplos_json/               # Ejemplos de estructuras JSON
│   │   └── sections/                    # Documentación por secciones
│   │       └── jn/                      # Específico de JN
├── 📁 data/                            # 📊 Datos de entrenamiento y ejemplos
├── 📁 outputs/                         # 📤 Archivos generados por el sistema
├── 📁 tests/                           # 🧪 Tests automatizados
├── 📁 .venv/                           # 🐍 Entorno virtual de Python
├── 📄 .env                             # 🔐 Variables de entorno (local)
├── 📄 .env.example                     # 📄 Plantilla de variables de entorno
├── 📄 .gitignore                       # 🚫 Archivos ignorados por Git
├── 📄 README.md                        # 📖 Este archivo
└── 📄 requirements.txt                 # 📦 Dependencias Python
```

---

## 💡 **Cómo Usar Mini-CELIA**

### 🎯 **Acciones Rápidas Integradas**
Al abrir la aplicación, verás 6 botones de acciones rápidas:

1. 🏗️ **"Generar JN Obras"** - Para licitaciones de construcción
2. 🛠️ **"Generar JN Servicios"** - Para servicios generales
3. 📦 **"Generar JN Suministros"** - Para compra de materiales
4. 🔧 **"Generar JN Mantenimiento"** - Para servicios de mantenimiento
5. 💻 **"Generar JN Tecnología"** - Para soluciones IT
6. 🎓 **"Generar JN Formación"** - Para servicios educativos

### 💬 **Chat Natural**
También puedes escribir directamente en el chat:
```
"Necesito una justificación para contratar servicios de limpieza"
"Genera una JN para obras de mejora en un colegio"
"Ayúdame con la documentación para comprar mobiliario de oficina"
```

### 📋 **Flujo Típico de Uso**
1. 🚀 **Abrir**: Ejecutar backend y frontend por separado
2. 🎯 **Seleccionar**: Hacer clic en una acción rápida o escribir en el chat
3. 📝 **Especificar**: Proporcionar detalles del proyecto/servicio
4. ⚡ **Generar**: La IA crea la documentación automáticamente
5. 📄 **Revisar**: Revisar y ajustar el contenido generado
6. 💾 **Exportar**: Guardar en el formato deseado



---

## 🌟 **Características Avanzadas**

### 🔄 **Modos de Operación**

#### **Modo Online** (Con OpenAI)
- 🧠 Respuestas inteligentes y contextuales
- 📚 Acceso a conocimiento actualizado
- 🎯 Personalización por tipo de licitación
- ✅ Cumplimiento normativo automático

#### **Modo Offline** (Sin Internet)
- 🔄 Respuestas simuladas profesionales
- 📄 Plantillas predefinidas
- ⚡ Funcionamiento sin dependencias externas
- 💼 Perfecto para demostraciones

### 📊 **Indicadores de Estado**
- 🟢 **Verde**: Conectado a OpenAI
- 🔴 **Rojo**: Modo offline/simulado
- ⏳ **Amarillo**: Cargando respuesta

### 🎨 **Diseño y UX**
- 🌈 **Tema Corporativo**: Rojo y blanco elegante
- ✨ **Efectos Glass**: Interfaces modernas y atractivas
- 🎭 **Iconos SVG**: Profesionales sin emojis
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
```powershell
# Clonar repositorio
git clone [repository-url]
cd ADD4U

# Instalar todo (requiere Node.js + Python)
npm run install:all

# Desarrollo con hot-reload
npm run dev:all
```

### 🐛 **Reportar Problemas**
Si encuentras algún problema o tienes sugerencias:
1. 📝 Describe el problema detalladamente
2. 🔄 Incluye pasos para reproducirlo
3. 📸 Adjunta capturas de pantalla si es posible
4. 💻 Especifica tu sistema operativo y navegador

---

## 📞 **Soporte y Contacto**

### 🆘 **Resolución de Problemas Comunes**

#### ❌ **"El backend no se conecta"**
```powershell
# Verificar Python instalado
python --version

# Verificar puerto 8000 libre
netstat -an | findstr 8000
```

#### ❌ **"El frontend no carga"**
```powershell
# Verificar Node.js instalado
node --version

# Limpiar caché y reinstalar
npm cache clean --force
npm install
```

#### ❌ **"OpenAI no responde"**
- 🔑 Verificar API Key en archivo `.env`
- 💳 Comprobar créditos disponibles en OpenAI
- 🌐 Verificar conexión a internet

### 📧 **Contacto Técnico**
Para consultas técnicas avanzadas o implementaciones empresariales, contacta con el equipo de desarrollo.

---

## 📄 **Licencia y Términos**

### ⚖️ **Licencia MIT**
Este proyecto está bajo licencia MIT, lo que permite:
- ✅ Uso comercial y personal
- ✅ Modificación y distribución
- ✅ Uso en proyectos privados
- ❌ No incluye garantías

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
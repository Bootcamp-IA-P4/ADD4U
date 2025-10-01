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

## 🚀 **Instalación y Ejecución**

### 📋 **Prerequisitos**
- 🐍 **Python 3.11+** 
- 📦 **Node.js 18+**
- 🔑 **OpenAI API Key** (opcional, funciona offline)
- 🍃 **MongoDB** (para persistencia)

### ⚙️ **Configuración del Backend**
```powershell
# 1. Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno (.env)
copy .env.example .env
# Editar .env con tus API keys

# 4. Ejecutar servidor
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
uvicorn backend.main:app --reload
```

### 🎨 **Configuración del Frontend**
```powershell
# 1. Instalar dependencias
cd frontend
npm install

# 2. Ejecutar en desarrollo
npm run dev

# 3. Build para producción
npm run build
```

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
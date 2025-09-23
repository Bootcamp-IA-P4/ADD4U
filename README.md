# Mini-CELIA — Chatbot de Licitaciones (PoC)

Sistema de generación y validación de expedientes de licitación con enfoque de cumplimiento normativo.

## 🚀 Frontend (React + Vite)

### Características
- ✅ **Sistema de usuarios** con roles (Admin/Usuario)
- ✅ **Interfaz moderna** con Tailwind CSS
- ✅ **Chat interactivo** con respuestas automáticas
- ✅ **Generación de secciones** (JN, PPT, CEC, CR)
- ✅ **Panel de administrador** con orquestador de secciones
- ✅ **Sistema de borrador** editable
- ✅ **Validación de cumplimiento** normativo (DNSH/PRTR, RGPD)
- ✅ **Exportación** múltiples formatos (.md, .doc, .json, .txt)
- ✅ **Persistencia** en localStorage

### Instalación y ejecución

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

El servidor se iniciará en `http://localhost:3000`

### Credenciales de prueba

**Administrador:**
- Email: `admin@minicelia.es`
- Password: `admin123`

**Usuario:**
- Email: `user@minicelia.es`
- Password: `user123`

### Tecnologías
- **React 18** - Interfaz de usuario
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Framework de CSS
- **React Router** - Enrutamiento
- **Context API** - Gestión de estado

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   ├── contexts/           # Context providers (Auth, AppState)
│   ├── pages/              # Páginas principales
│   ├── services/           # Servicios API y autenticación
│   └── utils/              # Utilidades
├── public/                 # Archivos estáticos
└── package.json           # Dependencias y scripts
```

## 🔧 Scripts Disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Build para producción
- `npm run preview` - Preview del build de producción
- `npm run lint` - Linting del código
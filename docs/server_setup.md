# 🚀 Guía de Configuración y Uso del Servidor – Proyecto Mini-CELIA

Esta guía explica **todo el proceso** para que cualquier miembro del equipo pueda conectarse al servidor remoto de Mini-CELIA, configurar el entorno y trabajar con backend (FastAPI) y frontend (Vite), usando **Visual Studio Code** y su terminal integrada.

---

## 1️⃣ Obtener y preparar la clave `.pem`

1. Descarga el archivo `pre-andon-teydisa.pem` desde el enlace seguro compartido por el stakeholder (SharePoint).  
2. Mueve el archivo a tu carpeta de claves SSH:  

   En la terminal de VS Code:
   ```bash
   mkdir -p ~/.ssh
   mv ~/Desktop/pre-andon-teydisa.pem ~/.ssh/
   chmod 600 ~/.ssh/pre-andon-teydisa.pem
   ```

⚠️ Importante:  
- **Nunca** subas el `.pem` a GitHub ni lo compartas en repositorios públicos.  
- Solo debe estar en tu carpeta `~/.ssh/` local.

---

## 2️⃣ Configurar acceso SSH

Para no tener que escribir siempre el comando largo, vamos a crear un acceso rápido llamado **`minicelia`**.

### Opción A: Editar con VS Code
```bash
code ~/.ssh/config
```

### Opción B: Editar con `nano`
Si prefieres usar la terminal:
```bash
nano ~/.ssh/config
```

Esto abrirá un editor de texto en la consola.  
Pega lo siguiente dentro:

```
Host minicelia
    HostName 52.213.214.76
    User ubuntu
    IdentityFile ~/.ssh/pre-andon-teydisa.pem
    IdentitiesOnly yes
```

👉 En `nano`:
- Escribir/pegar el contenido.  
- Guardar con `CTRL + O` y después `Enter`.  
- Salir con `CTRL + X`.  

---

## 3️⃣ Probar la conexión

Ejecuta:
```bash
ssh minicelia
```

La primera vez te pedirá confirmar la huella digital → escribe `yes`.  
Si ves algo como:
```
ubuntu@ip-172-31-28-50:~$
```
👉 ya estás dentro del servidor.

---

## 4️⃣ Conexión desde VS Code (Remote - SSH)

1. Instala la extensión **Remote - SSH** en VS Code (icono verde `><`).  
2. Haz clic en el icono verde `><` abajo a la izquierda.  
3. Selecciona **Connect to Host…** → `minicelia`.  
4. Se abrirá una nueva ventana de VS Code conectada al servidor.  
5. Abre la carpeta de trabajo:
   ```
   /home/ubuntu/minicelia
   ```

👉 Ahora estás editando y ejecutando directamente en el servidor, con la comodidad de VS Code.

---

## 5️⃣ Backend (FastAPI con Python 3.11)

### Crear entorno virtual (solo la primera vez)
En la carpeta del backend:
```bash
cd /home/ubuntu/minicelia/backend
python3.11 -m venv .venv
```

### Activar entorno virtual
Cada vez que empieces a trabajar:
```bash
source .venv/bin/activate
```

El prompt mostrará `(.venv)` al inicio.

### Instalar dependencias
Si existe `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Si no, instalar lo básico:
```bash
pip install fastapi uvicorn python-dotenv
```

### Ejecutar backend
Desde la **raíz del proyecto**:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 3002 --reload
```

Acceso:
- API → http://52.213.214.76:3002  
- Swagger UI → http://52.213.214.76:3002/docs  
- ReDoc → http://52.213.214.76:3002/redoc  

---

## 6️⃣ Frontend (Vite/React)

### Instalar dependencias
```bash
cd /home/ubuntu/minicelia/frontend
npm install
```

### Ejecutar frontend
```bash
npm run dev -- --host 0.0.0.0 --port 5174
```

Acceso en navegador:  
👉 http://52.213.214.76:5174

---

## 7️⃣ Variables de entorno (`.env`)

### Crear archivo `.env` en backend
En `/home/ubuntu/minicelia/backend/.env`:
```env
ENV=development
APP_NAME=MiniCELIA
APP_PORT=3002

DB_URI=mongodb://usuario:password@localhost:27017/minicelia
OPENAI_API_KEY=tu_api_key
```

⚠️ Este archivo **no debe subirse a GitHub**. Añádelo al `.gitignore`.  
En el repo se puede incluir un `.env.example` con las claves vacías para guiar a los devs.

### Usar `.env` en FastAPI
Ejemplo `main.py`:
```python
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

@app.get("/config")
def get_config():
    return {
        "app_name": os.getenv("APP_NAME"),
        "env": os.getenv("ENV")
    }
```

---

## 8️⃣ Flujo de trabajo en equipo

1. Conectarse con VS Code Remote - SSH al host `minicelia`.  
2. Abrir `/home/ubuntu/minicelia`.  
3. Cambiar a tu rama:
   ```bash
   git checkout feature/backend-json-flow
   git pull
   ```
4. Activar el entorno virtual:
   ```bash
   source backend/.venv/bin/activate
   ```
5. Instalar dependencias si cambió `requirements.txt`.  
6. Levantar backend y frontend.  
7. Probar en navegador y en Swagger.  

---

## 9️⃣ Cerrar sesión y reconectar

### Cerrar sesión SSH
Cuando termines de trabajar en el servidor:
```bash
exit
```
o simplemente:
```
CTRL + D
```

### Reconectar después
En la terminal de VS Code:
```bash
ssh minicelia
```

En VS Code Remote - SSH:  
- Clic en el icono verde `><`  
- Seleccionar **Connect to Host… → minicelia**

---

## ✅ Resumen

- El `.pem` es tu llave de acceso (no se comparte en repos públicos).  
- El archivo `~/.ssh/config` simplifica la conexión (puedes crearlo con `nano` o con VS Code).  
- **VS Code Remote - SSH** permite trabajar directamente en el servidor.  
- Se usa **un único venv compartido** en `/backend/.venv`.  
- Variables sensibles se gestionan en `.env` (no en GitHub).  
- Backend → puerto **3002** con Swagger en `/docs`.  
- Frontend → puerto **5174**.  
- Para cerrar: `exit`. Para volver: `ssh minicelia`. 
# API de Usuarios con SQLite

Esta es una API REST para gestión de usuarios implementada con FastAPI y SQLite.

## Características

- ✅ Autenticación JWT
- ✅ Base de datos SQLite con SQLAlchemy
- ✅ Operaciones CRUD completas para usuarios
- ✅ Hash seguro de contraseñas con bcrypt
- ✅ Migraciones de base de datos con Alembic
- ✅ Validación de datos con Pydantic

## Instalación

1. **Clonar el repositorio:**

```bash
git clone <tu-repositorio>
cd poc_simple_api_users
```

2. **Crear entorno virtual:**

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

## Configuración

1. **Variables de entorno (opcional):**
   Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./users.db
```

## Base de Datos

### Crear la base de datos inicial:

```bash
# Ejecutar la aplicación (crea automáticamente las tablas)
python main.py
```

### Usar Alembic para migraciones:

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones pendientes
alembic upgrade head

# Revertir a una versión anterior
alembic downgrade -1
```

## Ejecutar la aplicación

```bash
python main.py
```

La API estará disponible en: http://localhost:8000

## Documentación de la API

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Endpoints disponibles

### Autenticación

- `POST /auth/token` - Obtener token JWT

### Usuarios

- `POST /users/` - Crear nuevo usuario
- `GET /users/` - Listar usuarios (requiere autenticación)
- `PUT /users/{user_id}` - Actualizar usuario (requiere autenticación)
- `DELETE /users/{user_id}` - Eliminar usuario (requiere autenticación)

## Ejemplo de uso

### 1. Crear un usuario:

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "username": "usuario1",
    "full_name": "Usuario Ejemplo",
    "password": "contraseña123"
  }'
```

### 2. Obtener token de autenticación:

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario1&password=contraseña123"
```

### 3. Usar el token para acceder a endpoints protegidos:

```bash
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

## Estructura del proyecto

```
poc_simple_api_users/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py      # Rutas de autenticación
│   │       └── users.py     # Rutas de usuarios
│   ├── auth/
│   │   └── jwt.py          # Lógica de JWT
│   ├── core/
│   │   └── config.py       # Configuración
│   ├── database/
│   │   ├── database.py     # Configuración de SQLAlchemy
│   │   └── crud.py         # Operaciones de base de datos
│   └── models/
│       ├── user.py         # Modelos de usuario
│       └── token.py        # Modelos de token
├── alembic/                 # Migraciones de base de datos
├── main.py                  # Punto de entrada
└── requirements.txt         # Dependencias
```

## Notas importantes

- La base de datos SQLite se crea automáticamente en `./users.db`
- Las contraseñas se hashean con bcrypt antes de almacenarse
- Los tokens JWT expiran según la configuración en `ACCESS_TOKEN_EXPIRE_MINUTES`
- La aplicación incluye validación de datos y manejo de errores
- Solo los usuarios autenticados pueden acceder a la mayoría de endpoints
- Los usuarios solo pueden modificar/eliminar su propio perfil

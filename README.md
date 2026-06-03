# Fantasy Sticker Album

Aplicacion web hecha con FastAPI para el test tecnico de Codigo Libre Coop.

La idea es simple: un album de figuritas personalizadas donde una persona puede
iniciar sesion, ver su home y consumir una API REST para listar y crear
figuritas propias.

Tambien agregue una regla de visibilidad para albumes: pueden ser publicos o
privados. Los publicos se pueden consultar sin login; los privados solo los ve su
dueno.

El home tiene una capa simple de HTML, CSS y JavaScript para mostrar los datos de
forma mas clara, sin convertir el desafio en una app frontend grande. La
prioridad fue que el flujo completo se pueda correr, probar y entender sin
demasiada configuracion.

## Que incluye

- FastAPI como framework web.
- SQLAlchemy 2 para modelar y persistir datos.
- SQLite como base relacional local.
- Jinja2 para las vistas HTML.
- Sesiones firmadas para mantener al usuario logueado.
- Hash de passwords con `pwdlib[argon2]`.
- API REST con endpoint de lectura y endpoint de escritura.
- Albumes publicos y privados con una regla simple de permisos.
- Home con HTML/CSS propio y un filtro simple hecho con JavaScript.
- Tests de API con base de datos aislada en memoria.
- Ruff para chequeos de calidad de codigo.

## Requisitos

- Python 3.12 o superior.
- PowerShell, Bash o terminal equivalente.

## Instalacion

Desde la raiz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

En Linux/macOS, la activacion del entorno cambia a:

```bash
source venv/bin/activate
```

## Como levantar la aplicacion

```powershell
python -m fastapi dev app/main.py
```

La aplicacion queda disponible en:

- Home: http://127.0.0.1:8000
- Login: http://127.0.0.1:8000/login
- Documentacion interactiva: http://127.0.0.1:8000/docs

Al arrancar, la app inicializa la base desde el lifecycle de FastAPI: crea las
tablas necesarias y carga un usuario con datos demo si todavia no existen.

## Como levantar con Docker

Tambien se puede levantar la aplicacion en un contenedor:

```powershell
docker build -t fantasy-sticker-album .
docker run --rm -p 8000:8000 -e SESSION_SECRET_KEY="dev-secret-local" fantasy-sticker-album
```

Dentro del contenedor la app corre con Uvicorn, sin reload de desarrollo. La
base SQLite se crea dentro del contenedor; si se recrea el contenedor, esos datos
locales se pierden.

## Usuario demo

```text
usuario: demouser
password: demouser123
```

Con ese usuario se puede iniciar sesion desde `/login` y acceder al home.
El seed inicial tambien crea albumes y figuritas de ejemplo para que la pantalla
principal tenga datos visibles desde el primer arranque.

## API REST

Los endpoints principales de la API son:

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/api/albums/public` | Lista albumes publicos, sin login |
| `GET` | `/api/albums/me` | Lista los albumes del usuario logueado |
| `GET` | `/api/albums/{id}` | Muestra un album si es publico o si el usuario es su dueno |
| `POST` | `/api/albums/` | Crea un album para el usuario logueado |
| `GET` | `/api/stickers/` | Lista las figuritas del usuario logueado |
| `POST` | `/api/stickers/` | Crea una nueva figurita para el usuario logueado |
| `GET` | `/health` | Healthcheck simple de la aplicacion |

Los endpoints de escritura requieren sesion activa. Los albumes privados
devuelven `403 Forbidden` cuando el usuario no tiene permiso para verlos.

Para probarlos manualmente, FastAPI expone la documentacion interactiva en
`/docs`.

## Tests

Para correr la suite:

```powershell
python -m pytest -q
```

Los tests usan `TestClient`, una base SQLite en memoria y `dependency_overrides`
de FastAPI para no depender de `app.db` ni de datos locales. Esto permite que la
suite sea rapida, repetible y aislada.

## Calidad de codigo

```powershell
python -m ruff check .
```

Ruff ayuda a mantener imports ordenados, detectar codigo sin uso y evitar
patrones problematicos.

## Estructura del proyecto

```text
app/
  auth.py              # Hash y verificacion de passwords
  crud.py              # Operaciones de lectura/escritura sobre la DB
  database.py          # Engine, sesiones y dependencia get_db
  dependencies.py      # Dependencias compartidas de FastAPI
  main.py              # App, middlewares y registro de routers
  models.py            # Modelos SQLAlchemy
  permissions.py       # Reglas simples de acceso
  seed.py              # Datos demo iniciales
  schemas.py           # Schemas Pydantic para entrada/salida
  startup.py           # Inicializacion de DB en el lifecycle de FastAPI
  routers/
    albums.py          # API REST de albumes publicos/privados
    pages.py           # Login, logout y home HTML
    stickers.py        # API REST de figuritas
  templates/pages/     # Vistas Jinja2
  static/              # CSS y JS
tests/
  conftest.py          # Fixtures de DB, cliente y usuario autenticado
  test_albums_api.py   # Tests de visibilidad y permisos de albumes
  test_stickers_api.py # Tests de contrato HTTP de la API
```

## Decisiones tecnicas

Intente mantener el alcance acotado. Para este desafio, SQLite me parecio
suficiente para mostrar persistencia relacional sin sumar infraestructura extra.
La autenticacion esta resuelta con sesiones firmadas porque el flujo principal es
web y local; si fuera una API publica o una app con otros clientes, revisaria esa
decision segun el caso.

Separe la API en routers, schemas, modelos y funciones CRUD para que cada parte
tenga una responsabilidad clara. Los tests estan escritos desde el borde HTTP:
me interesaba cubrir lo que ve un cliente de la API, como la autenticacion
requerida, el listado, la creacion y la validacion de payloads.

La regla de visibilidad de albumes esta separada en una funcion chica para no
mezclar permisos con detalles del router: un album publico se puede ver sin
login, y un album privado solo se puede ver si el usuario logueado es el dueno.

La inicializacion de la base y el seed demo viven fuera de `main.py`. La app los
ejecuta al arrancar, no al importar el modulo, para evitar efectos secundarios y
para que los tests puedan crear una app con base aislada en memoria.

## Que mejoraria con mas tiempo

- Migraciones con Alembic.
- Configuracion tipada por ambiente y `SESSION_SECRET_KEY` obligatorio fuera de
  desarrollo.
- Docker Compose si quisiera separar servicios o montar volumenes de forma mas
  comoda.
- Mas reglas de negocio, por ejemplo evitar figuritas duplicadas dentro de un
  mismo album.
- Formularios en el home para crear albumes y figuritas sin pasar por `/docs`.
- CI en GitHub Actions para correr tests y lint en cada push.

## Nota personal

Encare este proyecto priorizando una entrega chica, completa y facil de revisar.
El ejercicio tambien me sirvio para trabajar sobre un stack que no es
necesariamente mi principal sin perder foco en las bases que intento sostener en
cualquier backend: entender el flujo principal, separar responsabilidades,
validar entradas, cubrir comportamiento importante con tests y dejar
instrucciones claras para que otra persona pueda levantar, leer y discutir el
proyecto sin friccion.

Tambien intente cuidar el alcance. Sume los extras que aportaban valor para la
consigna, como Docker, un home con HTML/CSS, una interaccion simple con
JavaScript y una regla de permisos, pero evite agregar piezas que no hacian falta
para resolver el problema. Si siguiera iterando, priorizaria mejoras concretas
como migraciones, configuracion por ambiente, CI y formularios para operar la API
desde el home.

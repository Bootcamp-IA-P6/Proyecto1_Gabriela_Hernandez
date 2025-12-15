# 🚕 Taxímetro Digital en Python

## Descripción del proyecto

Este proyecto consiste en el desarrollo de un taxímetro digital que simula el funcionamiento real de un taxi, permitiendo calcular el coste de un trayecto en función del tiempo que el vehículo está parado o en movimiento.

La aplicación ha sido diseñada de forma progresiva, pasando de un CLI básico a una arquitectura modular, incorporando:

persistencia en base de datos,

configuración dinámica,

y una interfaz gráfica web con Streamlit.

El objetivo principal es aprender buenas prácticas de desarrollo mientras se construye un sistema funcional y extensible.

## Funcionalidades principales
🟢 Funcionalidades básicas

Iniciar un trayecto.

Cambiar entre estado parado y en marcha.

Calcular el coste del trayecto en tiempo real.

Finalizar el trayecto y mostrar un resumen.

Reiniciar nuevos trayectos sin cerrar la aplicación.

🟡 Funcionalidades intermedias

Sistema de logging para trazabilidad.

Configuración de tarifas mediante archivo config.json.

Registro histórico de trayectos en archivo plano.

Tests unitarios básicos.

Refactorización a programación orientada a objetos (OOP).

🔴 Funcionalidades avanzadas 

Persistencia de trayectos en base de datos MySQL.

Gestión de credenciales mediante variables de entorno (.env).

Interfaz gráfica web con Streamlit.

Separación clara entre dominio, infraestructura y presentación.

## Arquitectura del proyecto
```
taximetro/
│
├── core/                # Lógica de dominio
│   └── trip.py
│
├── infra/               # Infraestructura (DB, repositorios)
│   ├── db.py
│   └── trip_repository_db.py
│
├── utils/               # Utilidades transversales
│   ├── logger.py
│   ├── config.py
│   └── history.py
│
├── data/                # Datos locales
│   └── config.json
│
├── logs/                # Logs de la aplicación
│
├── tests/               # Tests unitarios
│
├── app.py               # Interfaz gráfica (Streamlit)
├── main.py              # CLI
├── .env.example         # Variables de entorno de ejemplo
├── requirements.txt
└── README.md
```

## Cómo ejecutar el proyecto
1️⃣ Clonar el repositorio
git clone <https://github.com/Bootcamp-IA-P6/Proyecto1_Gabriela_Hernandez/tree/feat%2Fintegrate-database>
cd taximetro

2️⃣ Crear entorno virtual e instalar dependencias
```
python -m venv venv
source venv/Script/activate  o: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ Configurar variables de entorno

Crear un archivo .env en la raíz:

DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=taximeter


## Ejecutar el taxímetro en modo CLI
```
python main.py
``` 


Comandos disponibles:

start   → iniciar trayecto
move    → taxi en marcha
stop    → taxi detenido
finish  → finalizar trayecto
exit    → salir

🌐 Ejecutar la interfaz gráfica (GUI)
```
streamlit run app.py
```


Desde la interfaz podrás:

controlar el trayecto paso a paso,

ver el total acumulado en tiempo real,

y guardar automáticamente el viaje en la base de datos.

## Ejecutar tests
```
python -m unittest
```

## Base de datos

Motor: MySQL

ORM: SQLAlchemy

Persistencia desacoplada mediante repositorio (TripRepositoryDB).

Ejemplo de verificación:

SELECT * FROM trips ORDER BY id DESC;

## Decisiones técnicas relevantes

Separación de responsabilidades:
dominio, infraestructura y presentación están desacoplados.

Uso de OOP para encapsular el estado del trayecto.

Repositorio para aislar el acceso a datos.

Streamlit para una GUI rápida, clara y funcional.

Variables de entorno para seguridad y portabilidad.

## Posibles mejoras futuras

Autenticación de usuarios.

Dockerización de la aplicación.

Dashboard de trayectos históricos.

API REST para consumo externo.

Despliegue en la nube.

## Autora: Gabriela Hernández 

Proyecto desarrollado como ejercicio de aprendizaje y práctica de:

Python

Arquitectura de software

Control de versiones con Git

Buenas prácticas de desarrollo
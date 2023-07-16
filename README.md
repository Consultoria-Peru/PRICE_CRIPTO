# Sistema Airflow con Docker y Docker Compose

Este proyecto establece un sistema Airflow en Docker utilizando Docker Compose. El sistema consta de un servidor web de Airflow, un programador (scheduler) de Airflow y una base de datos PostgreSQL.

## Prerrequisitos

- Docker
- Docker Compose

## Estructura del Proyecto

textCopy code

`. ├── Dockerfile ├── README.md ├── docker-compose.yml ├── dags/ ├── config/ │   └── airflow.cfg └── requirements.txt`

- `Dockerfile`: Define la construcción de la imagen de Airflow.
- `README.md`: Este archivo.
- `docker-compose.yml`: Configura los servicios de Docker para el servidor web de Airflow, el scheduler de Airflow y la base de datos PostgreSQL.
- `dags/`: Directorio que contiene tus Directed Acyclic Graphs (DAGs) de Airflow.
- `config/`: Directorio que contiene la configuración de Airflow.
    - `airflow.cfg`: Configuración de Airflow.
- `requirements.txt`: Listado de dependencias de Python que serán instaladas.

## Uso

1. Primero, construye la imagen de Airflow con Docker:
    
    bashCopy code
    
    `docker build -t sistema_airflow .`
    
2. Inicia los servicios con Docker Compose:
    
    bashCopy code
    
    `docker-compose up -d`
    
3. Abre tu navegador y visita `http://localhost:8080` para acceder a la interfaz de usuario web de Airflow.
    

## Detener los servicios

Para detener los servicios, ejecuta:

bashCopy code

`docker-compose down`

---
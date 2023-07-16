# Usar una imagen de python como base
FROM python:3.8-slim-buster

# Variables de entorno para las versiones de Airflow y Python
ARG AIRFLOW_VERSION=2.6.3
ARG PYTHON_VERSION=3.8

# Actualizar e instalar dependencias del sistema
RUN apt-get update -y \
  && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends \
    ufw net-tools bleachbit wget python3-pip python3-venv git gdebi curl \
    build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
    libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev \
    libpq-dev lsof unrar \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Direcciones para el usuario y base de Airflow
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Instalar Apache Airflow con constraints
RUN CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" \
    && pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Crear el directorio y usuario de Airflow
RUN useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow
WORKDIR ${AIRFLOW_USER_HOME}
USER airflow

# Inicializar la base de datos de Airflow
RUN airflow db init

# Copiar la configuración y DAGs existentes
COPY --chown=airflow:airflow dags/ ${AIRFLOW_USER_HOME}/dags/
COPY --chown=airflow:airflow config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

# Configurar el servidor web de Airflow para escuchar en todas las direcciones
ENV AIRFLOW__WEBSERVER__BASE_URL=http://0.0.0.0:8080
ENV AIRFLOW__WEBSERVER__WEBSERVER_HOST=0.0.0.0

# Exponer el puerto de Airflow
EXPOSE 8080

# Punto de entrada
CMD ["airflow", "webserver"]

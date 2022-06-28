FROM apache/airflow:2.2.3

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get upgrade -y && \
    apt-get install -y git
# git gcc g++ -qqq

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

ARG CLOUD_SDK_VERSION=322.0.0
ENV GCLOUD_HOME=/home/google-cloud-sdk

ENV PATH="${GCLOUD_HOME}/bin/:${PATH}"

RUN DOWNLOAD_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fL "${DOWNLOAD_URL}" --output "${TMP_DIR}/google-cloud-sdk.tar.gz" \
    && mkdir -p "${GCLOUD_HOME}" \
    && tar xzf "${TMP_DIR}/google-cloud-sdk.tar.gz" -C "${GCLOUD_HOME}" --strip-components=1 \
    && "${GCLOUD_HOME}/install.sh" \
    --bash-completion=false \
    --path-update=false \
    --usage-reporting=false \
    --quiet \
    && rm -rf "${TMP_DIR}" \
    && gcloud --version

RUN  apt-get update \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

RUN  apt-get update \
    && apt-get install -y unzip \
    && rm -rf /var/lib/apt/lists/*

# # Install OpenJDK-11
# RUN apt update && \
#     apt-get install -y openjdk-11-jdk && \
#     apt-get install -y ant && \
#     apt-get clean;

# # Set JAVA_HOME
# RUN export JAVA_HOME='/usr/lib/jvm/java-8-openjdk-amd64'
# RUN PATH=$PATH:$JAVA_HOME/bin

# RUN source ~/.bashrc

# # Download and install spark
# RUN cd /opt \ 
#     && mkdir spark \
#     && cd spark 
# RUN wget https://dlcdn.apache.org/spark/spark-3.0.3/spark-3.0.3-bin-hadoop3.2.tgz 
# RUN tar xzfv spark-3.0.3-bin-hadoop3.2.tgz \
#     && rm spark-3.0.3-bin-hadoop3.2.tgz 

# ENV SPARK_HOME /opt/spark/spark-3.0.3-bin-hadoop3.2/
# RUN export SPARK_HOME
# # RUN export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin


WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID
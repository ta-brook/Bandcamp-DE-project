# Bandcamp-DE-project

A ELT Data Engineer project with various of tools: Airflow, Terraform, Docker, Spark, GCP and more

## Table of contents

- [Description](#description)
    - [Overview](#overview)
    - [Architect](#architect)
    - [Dasboard](#dashboard)
    - [Goal](#goal)
    - [Dataset](#dataset)
    - [Tool&Techs](#tools--techs)
    - [Scalability](#scalability)
    - [Insight from the dataset](#insight-from-the-dataset)
- [Reproduce this project](#reproduce-this-project)
- [Acknowledgement](#acknowledgement)


## Description


### Overview

This project is ingest data from [Bandcamp sale data](https://components.one/datasets/bandcamp-sales) and create an end-to-end data pipeline. The data would be transformed into daily parquet file and stored in data lake. Next, the daily batch jobs will consume these data, load to data warehouse, applies transformations, and displays to the dashboard.

### Architect

![Architecture](assets/Architect.png)

### Dashboard

You can access [Dashboard](https://datastudio.google.com/reporting/d145a14a-b4da-4c9b-973b-723fbea5bffb) here.
![Bandcamp-dashboard](assets/bandcamp-dashboard.JPG)

### DAGS

Some dag are depend on another dag [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/1.10.3/_api/airflow/sensors/external_task_sensor/index.html)

![dags](assets/dags.JPG)

### Goal

My mainly goal is to learn more about data engineer work flow/tools. But that not how we describe the problem right? So, the final goal of this project is to create data pipeline based on GCP and analyze the data by create dashboard to describe the following business question below:

- Which Artist has highest purchase and how much is it?

- Which hour of the day has highest and lowest purchases?

- Which type of product has highest purchases and at what time of the day?

- Ranking of Region/Country purchases and amount of it in USD

### Dataset

The main dataset is [Bandcamp sale data](https://components.one/datasets/bandcamp-sales) which contain 1,000,000 items from Bandcamp's sales feed between 9/9/2020 and 10/2/2020 and is a slice of the whole dataset of 6.7 million sales. Other dataset: [Country regional code](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes) and [Currency](https://github.com/datasets/currency-codes/blob/master/data/codes-all.csv) is used for cleansing and transformation.

### Tools & Techs

- Cloud - Google Cloud Platform
- Infrastructure as Code software - Terraform
- Containerization - Docker, Docker Compose
- Orchestration - Airflow
- Transformation - dbt, Spark
- Cluster management - Dataproc
- Data Lake - Google Cloud Storage
- Data Warehouse - BigQuery
- Data Visualization - Data Studio
- Language - Python, Bash

### Scalability

If the data is increased in a significant number let's say 1000x then, scale up dataproc cluster in horizontally (add more worker/node) or both vertically and horizontally (add more worker and improve performance) is a good idea too.

### Insight from the dataset

#### Most purchases country by region
- American: United States, 397666
- Europe: United Kingdom, 148551
- Oceania: Australia, 55637
- Asia: Japan, 32496
- Africa: South Africa, 2155


#### What time has the highest Purchases in a day
- 1 PM : 59903 


#### What time has the lowest Purchases in a day
- 5 AM : 24007


## Reproduce this project

will be added soon..

### Prerequisites

The following requirements are needed to reproduce the project:

### GCP setup

- Download and install Google [SDK](https://cloud.google.com/sdk/docs/install-sdk) for local setup

### Create account

1. create account with your google email.
2. Create new project or using 'My first project' that auto created
3. Go to `service account`
    - create service account
    - download `credential.json`
4. Set env for `credential.json`
```
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/google_credentials.json>"

# Refresh token/session, and verify authentication
gcloud auth application-default login
```

### IAM configuration

not done yet will continue tomorrow

1. go to `IAM & Admin`
2. grant principal these roles
    - Bigquery Admin
    - Compute Admin
    - Dataproc Admin
    - Storage Admin
    - Storage Object Admin
3. Enable API
    - 

### Terraform

more detail [here](https://github.com/ta-brook/terraform)

### Airflow

waiting for dbt to attached with airflow

### dbt

trying to put it in airflow docker

## Are there any ways to improves this project?

- Build based on VM 
- add test
- add CI/CD
- add docs for dbt 
- create more dimensional model for other used? (maybe we can get more insight from our data)


## Acknowledgement

This project cannot be completed without this amazing [course](https://github.com/DataTalksClub/data-engineering-zoomcamp) from [DataTalks.Club](https://datatalks.club/).

Also [Dockerfile](https://github.com/ankurchavda/streamify/blob/main/airflow/Dockerfile) from [streamify](https://github.com/ankurchavda/streamify) that can run dbt with airflow.

## ref

- [Data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [streamify](https://github.com/ankurchavda/streamify)
- [dphi](https://dphi.tech/community/)
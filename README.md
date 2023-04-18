# Final Project for the Data Engineering Zoomcamp hosted by DataTalksClub.
## Dataset
First at all, I'll work with a batch pipeline (the data will be updated day by day). I was looking for some climate data and I've chosen this [one](https://www.kaggle.com/datasets/mnassrib/jena-climate?resource=download).
## Pipeline diagram
## Technologies
- Python
- GCP (Google Cloud Plattform)
- Prefect
- DBT
- Google Data Studio or Looker
- Terraform
### What is Terraform?
- Terraform is an open-source infrastructure as code software tool created by HashiCorp. Users define and provide data center infrastructure using a declarative configuration language known as HashiCorp Configuration Language, or optionally JSON.
### Create a project in GCP
- Create a project in GCP
- I will called it `dtc-de`
- Go to IAM and create a service account (assign the viewer role)
- Create a key for the account service

### Install Google Cloud SDK
Follow the instructions from [here](https://cloud.google.com/sdk/docs/install?hl=en-419)
### Make sure that all is working well using the command 
```sh
gcloud -v
```
### Add Rol to your service account
- Storage Admin
- Storage Object Admin
- Big Query Admin

### Look for API's and enable `IAM Service Account Credentials API`

### Refresh service-account's auth-token for this season
```sh
gcloud auth application-default login
```
### Creating GCP Infrastucture with Terraform
Watch more [here](https://www.youtube.com/watch?v=dNkEgO-CExg&t=5s)
### Initialize state file (.tfstate)
terraform init

### Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"

## Terraform files
### main.tf
```terraform
  terraform {
    required_version = ">= 1.0"
    backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
    required_providers {
      google = {
        source  = "hashicorp/google"
      }
    }
  }
```
We have to specified the required_version. Backend "local" means that we'll save our configuration in a tf-state file in our local computer.

We define a provider here:
```terraform
  provider "google" {
    project = var.project
    region  = var.region
    zone    = var.zone
  }
```
And then a resource, in this case we'll use a storage bucket
```terraform
  resource "google_storage_bucket" "bucket" {
    name          = "dtc-de-bucket"
    location      = var.region
    storage_class = "REGIONAL"
    force_destroy = true
  }
```
### variables.tf
This file contains all the variables that we'll use in our main.tf file
```terraform
  variable "project" {
    type        = string
    description = "The GCP project to use for integration tests"
  }
  variable "region" {
    type        = string
    description = "The GCP region to use for integration tests"
    default     = "us-central1"
  }
  variable "zone" {
    type        = string
    description = "The GCP zone to use for integration tests"
    default     = "us-central1-a"
  }
```
## Overview of terraform commands
- terraform init
- terraform plan
- terraform apply
- terraform destroy

## Terraform commands
### Initialize state file (.tfstate)
```sh
terraform init
```
### Check changes to new infra plan
```sh
terraform plan -var="project=<your-gcp-project-id>"
```
### Apply changes to new infra
```sh
terraform apply -var="project=<your-gcp-project-id>"
```
### Destroy changes to new infra
```sh
terraform destroy -var="project=<your-gcp-project-id>"
```

## Local
### Docker-compose
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.

[More info](https://docs.docker.com/compose/)

### Docker-compose file
[path](src/docker-compose.yaml)

In this docker-compose file we have two images, one of them is for postgres and the other is for pgadmin.

In order to have these images, you need to install them.

### Install postgres
```sh
docker pull postgres
```
### Install pgadmin
```sh
docker pull dpage/pgadmin4
```
### Make sure that you have both of them
```sh
docker images
```

### Run docker-compose
```sh
docker-compose up -d
```
### Check if the containers are running
```sh
docker ps
```
### Stop docker-compose
```sh
docker-compose down
```

## Dockerfile
This dockerfile will upload the data directly from url to postgres (using docker-compose file to create postgres db)
### Build image
```sh
docker build -t climate_ingest:v001 .
```
### Run the image
```sh
docker run climate_ingest:v001 `
      --user=root `
      --password=root `
      --host=pgdatabase `
      --port=5432 `
      --db=climate_data `
      --table_name=jena_climate `
      --url='https://test-esteban-270101.s3.us-east-1.amazonaws.com/jena_climate_2009_2016.csv'
```
Directly using python

```python 
python src/upload-data.py `
      --user=root `
      --password=root `
      --host=localhost `
      --port=5432 `
      --db=climate_data `
      --table_name=jena_climate `
      --url='https://test-esteban-270101.s3.us-east-1.amazonaws.com/jena_climate_2009_2016.csv' 
```

Now we have the data inside the db.


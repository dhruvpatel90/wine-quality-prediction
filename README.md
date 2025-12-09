# CS 643 Cloud Computing - Programming Project 2: Wine Quality Prediction

This repository contains the PySpark application for training a parallel Machine Learning model on AWS EC2 instances and the containerized application for running predictions using Docker.

## Project Overview

The goal is to predict wine quality (score 1-10) using physical parameters.

* **Model:** PySpark MLlib Logistic Regression Classifier.
* **Training:** Executed in parallel across **4 EC2 instances**.
* **Prediction:** Deployed via **Docker container** for portability.
* **Metric:** F1 Score (Validation: 0.5673).

## Repository Contents

* `train_model.py`: PySpark script used for parallel model training on the 4-node cluster. Saves the model to the `wine_quality_model/` directory.
* `prediction_app.py`: PySpark script used to load the saved model, perform feature engineering (`VectorAssembler`), and calculate the F1 score on input data.
* `Dockerfile`: Defines the environment to containerize `prediction_app.py`, ensuring all PySpark dependencies are met.
* `entrypoint.sh`: A wrapper script to execute `spark-submit` correctly within the Docker container and pass the necessary command-line arguments.
* `wine_quality_model/`: Directory containing the saved Logistic Regression Model files (not the full Pipeline, due to deployment constraints).

## Deployment and Testing

The Docker image must be run with a volume mount (`-v`) to allow the container to read the input CSV file from the host machine.

### 1. Build the Docker Image

```bash
sudo docker build -t wine-predictor:latest .

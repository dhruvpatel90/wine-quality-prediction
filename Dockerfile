FROM ubuntu:22.04

# Spark Configuration
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark

# Install Java, Python, pip, and wget
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    python3 \
    python3-pip \
    wget && \
    rm -rf /var/lib/apt/lists/*

# Download and Extract Spark
RUN mkdir -p ${SPARK_HOME} && \
    wget -qO - https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | \
    tar -xzf - -C ${SPARK_HOME} --strip-components=1

# Install Python dependencies
RUN pip3 install numpy pandas

# Set environment variables for Spark and Python
ENV PATH=${SPARK_HOME}/bin:${PATH}
ENV PYTHONPATH=${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.7.zip:${PYTHONPATH}

# Set working directory inside the container
WORKDIR /app

# Copy the corrected Python script
COPY prediction_app.py /app/prediction_app.py

# Copy the trained ML model directory
COPY wine_quality_model /app/wine_quality_model

# 🎯 CRITICAL FIX: Use a shell script wrapper to ensure argument passing works correctly with spark-submit.
# This requires creating the entrypoint.sh script on the host first (Step 1 in previous response).
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# FINAL ENTRYPOINT: Execute the wrapper script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

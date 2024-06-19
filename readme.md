# Apache Kafka Setup Guide

This guide provides step-by-step instructions to set up and run Apache Kafka on a Linux-based system, as well as to run a Kafka project using Python.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Java Development Kit (JDK)
- Python 3.x
- wget (for downloading Kafka)

## Step 1: Download and Extract Kafka

Download Kafka from the official website or using the following command:

```bash
wget https://downloads.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz -O ~/Downloads/kafka.tgz

Extract the downloaded archive:

bash

mkdir -p ~/kafka
tar -xvzf ~/Downloads/kafka.tgz -C ~/kafka --strip 1

Step 2: Start Zookeeper

Kafka uses Zookeeper for managing its cluster state. Start Zookeeper by running the following command:

bash

cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

Step 3: Start Kafka Server

Start the Kafka server by running the following command:

bash

bin/kafka-server-start.sh config/server.properties

Step 4: Create a Kafka Topic

Create a Kafka topic to use in your project. Replace <topic_name> with your desired topic name.

bash

bin/kafka-topics.sh --create --topic <topic_name> --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

Step 5: Install Kafka-Python Library

Install the Kafka-Python library using pip:

bash

pip install kafka-python

Step 6: Run Kafka Project

Run your Kafka project. Ensure that you have the necessary producer and consumer scripts set up to interact with Kafka.
Step 7: Test Kafka Project

Run your unit tests to ensure that your Kafka project is functioning as expected:

bash

python -m unittest discover -s test -p "test_*.py"
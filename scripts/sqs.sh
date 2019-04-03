#!/usr/bin/env bash
python3 src/SQS/main.py
pytest --junitxml=pytest/sqs.xml test/SQS/test.py
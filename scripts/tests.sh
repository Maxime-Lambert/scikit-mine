#!/usr/bin/env bash
python3 test/testAssert.py
pytest --junitxml=pytest/test.xml test/testAssert.py



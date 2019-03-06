#!/usr/bin/env bash
python3 src/DiffNorm/Main.py
pytest --junitxml=pytest/diffnorm.xml test/Diffnorm/test_DiffNorm.py
flake8 src/DiffNorm/*.py > flake8/diffnorm.xml
#!/bin/bash

# Install spaCy desired model
python -m spacy download en_core_web_trf

# Run the Python application
python web.py
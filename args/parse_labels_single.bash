#!/bin/bash

./labels/parse_labels.py \
  --text-dir=./data/dl_random_2023-09-14/dl_random_2023-09-14_typewritten_ocr \
  --image-dir=./data/dl_random_2023-09-14/dl_random_2023-09-14_typewritten_labels \
  --html-file=./data/dl_random_2023-09-14/dl_random_2023-09-14_typewritten.html \
  --json-output=./data/dl_random_2023-09-14/dl_random_2023-09-14_typewritten.json

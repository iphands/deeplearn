#!/bin/bash

mkdir -p output

virtualenv-3 deeplearnvenv
source deeplearnvenv/bin/activate

pip install tensorflow Pillow pynput keras

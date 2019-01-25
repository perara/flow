#!/usr/bin/env bash

source ~/virtual_environments/flow/bin/activate
git clone https://github.com/google/flatbuffers.git
cd flatbuffers/python
pip install . --upgrade
cd ../../
rm -rf flatbuffers
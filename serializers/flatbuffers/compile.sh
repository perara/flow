#!/usr/bin/env bash
source ~/virtual_environments/flow/bin/activate

for entry in schemas/*
do
    flatc ${entry} --python
done
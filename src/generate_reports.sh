#!/bin/bash

set -x

FORMATTED_DIR=$1
EXP_NAME=$2
REPORT_DIR=reports/$EXP_NAME
mkdir -p $REPORT_DIR

for f in data/wmt21/formatted/*;
    do
        report_name=$(basename $f .tsv)
        explainaboard --task machine-translation --system_outputs $f > $REPORT_DIR/$report_name.json
    done
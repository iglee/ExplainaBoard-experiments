#!/bin/bash

short_date=$(/bin/date +%m%d%y)
exec 2>>reports/"$2".log

set -x

FORMATTED_DIR=$1
EXP_NAME=$2
REPORT_DIR=reports/$EXP_NAME
mkdir -p $REPORT_DIR

for f in $FORMATTED_DIR/data/*;
    do
        report_name=$(basename $f .data)
        explainaboard --task machine-translation --custom_dataset_paths $f --system_outputs $FORMATTED_DIR/sysout/$report_name.sysout --metrics chrf  > $REPORT_DIR/$report_name.json
    done
# BLEU, chrf, and COMET

#!/bin/bash

DIR=`dirname $0`
# echo $DIR

#(cd $DIR && exec python my_exam.py $1)
python $DIR/my_exam.py $1

#!/bin/bash
for file in ../*.yaml; do
    output=`basename $file | sed -e 's/yaml/rst/'`
    python yaml2rst.py $file > "./source/advisories/$output"
done
make html

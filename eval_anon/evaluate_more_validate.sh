#!/bin/bash

cat more_validate.txt | python3 reformat_for_tok.py |
    docker run -i mtaril/emtsv tok | python3 label_to_column.py |
    docker run -i mtaril/emtsv morph,pos | python3 ../emPreverb > more_validate_output.tsv
    
cat more_validate_output.tsv | python3 evaluate.py > more_validate_results.txt
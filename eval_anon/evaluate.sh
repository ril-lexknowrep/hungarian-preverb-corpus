#!/bin/bash

for filename in difficult_test general_test;
do
    echo Evaluating ${filename}
    echo This will take a few minutes...
    cat ${filename}.txt | python3 reformat_for_tok.py |
        docker run -i mtaril/emtsv tok | python3 label_to_column.py |
        docker run -i mtaril/emtsv morph,pos | python3 ../emPreverb |
        python3 baselines.py > ${filename}_baseline_output.tsv

    echo A few more minutes...
    cat ${filename}.txt | python3 reformat_for_tok.py |
        docker run -i mtaril/emtsv emstanza-tok | python3 label_to_column.py |
        docker run -i mtaril/emtsv emstanza-lem |
        docker run -i mtaril/emtsv emstanza-parse |
        python3 add_stanzaid.py > ${filename}_stanzaids.tsv

    cat ${filename}_baseline_output.tsv | python3 evaluate.py > ${filename}_results.txt
    cat ${filename}_stanzaids.tsv | python3 evaluate.py >> ${filename}_results.txt

    echo -e "\nResults for ${filename}\n--------------------------"
    cat ${filename}_results.txt;
    echo -e "***********************\n"
done;

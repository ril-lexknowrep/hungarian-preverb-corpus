# Hungarian Preverb Corpus
A gold standard corpus manually annotated with __verb-preverb__ connections for Hungarian.


## corpus

The [corpus](corpus) consist of the following 4 files:

|filename|# sentences|# preverbs|
|:--|--:|--:|
|difficult_validate1.txt|310|357|
|difficult_validate2.txt|840|935|
|difficult_test.txt|327|376|
|general_test.txt|503|500|
<!-- for F in *.txt ; do echo $F ; cat $F | wc -l ; cat $F | sed "s/\([\|][0-9]\)/\n\1\n/g" | grep "^[\\\]" | wc -l ; done -->

Preverbs in the `general` dataset are in the distribution as they appear in normal Hungarian text. The `difficult` dataset is specially crafted: the most common and most-easy-to-handle pattern, i.e. when the preverb follows the verb immediately (e.g. _megy ki_ 'go out'), is omitted. `validate` is for development/validation, `test` is for testing. Note that a `general_validate` dataset would not be useful, because the trivial pattern would be in vast majority overwhelming the more interesting less frequent patterns. 

Accordingly, the [`emPreverb`](https://github.com/ril-lexknowrep/emPreverb) tool which connects preverbs to their corresponding verb, was developed based only on interesting `difficult` examples, and tested both on `difficult` and `general` data. 

(Remark. The `difficult_validate` dataset is divided into two parts for historical reasons, but you can simply use them together: they consist a total of 1150 sentences and 1292 preverbs.)


## evaluation

TODO

See also: https://github.com/ril-lexknowrep/emPreverb


## development

TODO

See also: https://github.com/ril-lexknowrep/emPreverb


## citation

If you use the corpus, please cite the following paper.

Pethő, Gergely and Sass, Bálint and Kalivoda, Ágnes and Simon, László and Lipp, Veronika: Igekötő-kapcsolás. In: MSZNY 2022.


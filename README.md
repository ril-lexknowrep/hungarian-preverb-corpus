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

Preverbs in the `general` dataset are in the distribution as they appear in normal Hungarian text. The `difficult` dataset is specially crafted: the most common and most-easy-to-handle pattern, i.e. when a verb is directly followed by its preverb (e.g. _megy ki_ 'go out'), is omitted. `validate` is for development/validation, `test` is for testing. Note that a `general_validate` dataset would not be useful, because the trivial pattern would be in vast majority overwhelming the more interesting less frequent patterns. 

Accordingly, the [`emPreverb`](https://github.com/ril-lexknowrep/emPreverb) tool which connects preverbs to their corresponding verb, was developed based only on interesting `difficult` examples, and tested both on `difficult` and `general` data. 

(Remark. The `difficult_validate` dataset is divided into two parts for historical reasons, but you can simply use them together: they consist a total of 1150 sentences and 1292 preverbs.)


## corpus annotation guidelines

- Preverb marked by a suffixed backslash followed by a (single digit!) ID number: `meg\1`.
- Word from which the preverb was separated marked by a pipe followed by the same ID number: `főzve|1`.
- Within the same line, different verb-prefix pairs must (obviously) receive different ID numbers.
- A preverb that does not belong to any word in the sentence (ellipsis etc.) is marked with a zero ID: `"Hazakísérhetlek?" "Meg\0 hát."` Any number of preverbs can have the `0` ID within the same line.
- In the `difficult` dataset, a verb directly followed by its preverb is <!-- only annotated if the preverb is not separated from the preceding verb: --> not annotated: `főzte meg`, but: `főzte|1 volna meg\1`.
- In the `general` dataset, the first pattern is annotated as well: `főzte|1 meg\1`.
- Normally there is a 1:1 correspondence between preverbs and verbs. However, there are exceptions, and these are annotated accordingly, e.g. `Se ki\1, se be\1 nem lehetett menni|1 Budakesziről`; `át-\1 meg átjárták|1`.

Check (see Step 1 to 4 in [`evaluate.ipynb`](development/evaluate.ipynb)) whether tokens annotated as separated preverbs are also analysed by [`e-magyar`](https://github.com/nytud/emtsv) `morph,pos` as preverbs. If not (e.g. if the preverb _meg_ is tagged by emtsv as a `[/Conj]`), _remove this annotation_ (or the whole item if no annotation left) from the dataset because `preverb` will necessarily fail due to incorrect emtsv annotation, which is extraneous to its performance evaluation. _Exception:_ person-inflected preverb-like postpositions such as in `utánam\1 dobják|1`, which are tagged by emtsv as `[/Post]`, and case-inflected personal pronouns such as in `hozzá\1 voltam szokva|1`, which are tagged as `[/N|Pro]`, _should not be removed from the dataset_ since `preverb` should be able to handle these.

If a token is annotated as the verb stem counterpart of a separated preverb, but is not tagged by emtsv as a verb, check whether the preverb annotation is correct, but if so, _do not remove this annotation_ from the dataset. `preverb` is supposed to be able to handle the connection of such separated preverbs.


## evaluation

An environment for _reproducing_ evaluation of [`emPreverb`](https://github.com/ril-lexknowrep/emPreverb) as published in the paper below.

```bash
git clone https://github.com/ril-lexknowrep/emPreverb
cd emPreverb
git clone https://github.com/ril-lexknowrep/hungarian-preverb-corpus
make evaluate
```
(Remark. Yes, please clone this repo _inside_ `emPreverb`.)

The results are obtained in [`general_test_results.txt`](evaluation/general_test_results.txt) and [`difficult_test_results.txt`](evaluation/difficult_test_results.txt).
This should be exactly the same which can be found in Table 3 of the paper below.


## development

An environment used for developing [`emPreverb`](https://github.com/ril-lexknowrep/emPreverb).
It is "for us" but if you insist to use it:
```bash
git clone https://github.com/ril-lexknowrep/emPreverb
cd emPreverb
git clone https://github.com/ril-lexknowrep/hungarian-preverb-corpus
cd hungarian-preverb-corpus/development
jupyter notebook evaluate.ipynb
```
(Remark. Yes, please clone this repo _inside_ `emPreverb`.)


## citation

If you use the corpus, please cite the following paper.

Pethő, Gergely and Sass, Bálint and Kalivoda, Ágnes and Simon, László and Lipp, Veronika: Igekötő-kapcsolás. In: MSZNY 2022.


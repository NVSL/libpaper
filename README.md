# Common Resources for NVSL Papers

You should only make changes to the contents of this repo if they useful across other, future papers we will write.

If you need to modify something for your specific paper, you could create a branch or, perferably,  modify `libpaper` to allow an graceful override in your paper.

##  What Gets Built

By default, `Make.rules` builds `paper.pdf` but you can have it build anything else by setting `PDF_TARGETS` in your paper's make file.

## Submitting to ArXiv

To build a version to submit to Arxiv, you need to change the top line of `paper.tex` to 

```tex
\documentclass[manuscript]{acmart}
```

and then do 

```sh
make arxiv
```

This will create a `*-arxiv.tgz` which should upload and build fine on Arxiv.  Please try it and make sure it works, but *do not* post the document.  Steve will do that.


## Grammar Checking

Grammerly (https://app.grammarly.com/) is a free and useful grammar checker.  It can't understand tex, but you can still use it to check the grammar in your papers by exporting the paper as text and uploading.  Create an Grammarly account and then do 

```sh
$ make paper.grammarly.txt
```

The resulting `paper.grammarly.txt` is a text version of your paper formatted and filtered a little bit minimize the number of spurious warning in Grammarly.

Greate a Grammarly account, upload the text file, and go through its suggestions.

Like all grammar checkers, it is imperfect, so you must use your judgement and read the suggestions carefully.  It catches a bunch of stuff, though.

Please commit all the changes made in response to Grammarly suggestions as a single commit.  It's useful to be able to see what it's catching.



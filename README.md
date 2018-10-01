# Common Resources for NVSL Papers

You should only make changes to the contents of this repo if they useful across other, future papers we will write.

If you need to modify something for your specific paper, you could create a branch or, perferably,  modify `libpaper` to allow an graceful override in your paper.

##  What Gets Built

By default, `Make.rules` builds `paper.pdf` but you can have it build anything else by setting `PDF_TARGETS` in your paper's make file.

## Submitting to ArXiv

To prepare a paper for submission to the ArXiv (or for distribution to companies, etc.)

1. Make sure the paper builds properly using `libpaper`
2. Make sure the 'make arxiv' target works properly. It should give you a tar ball with everything you need to build the paper: `*-arxiv.tgz`. There are some variables you may need to set in your `Makefile`.  See `NVSL/paper-template` for an example.
3. Create a branch for the arxiv submission with the name `arxiv`
4. Change the first line of `paper.tex` to `\documentclass[twocolumn]{article}`.
5. Make any other changes necessary to make the paper build.
6. Check the paper output does not include any copyright information (e.g., for ACM or USENIX)
7. Remove all the comments and `\ignore{}`s -- Everything that does not appear in the paper output.
8. Remove any files that are not needed to build the paper.  In particular, check for .tex files that we don't include anywhere.
8. Make sure the paper looks good (E.g., all the figures and tables fit in their columns).
9. Add the authors and affiliations.  Arxiv is not blind.
11. Add an acknowledgemnts section in `acks.tex`  Acknowledge who you think should be acknowledged.  Send draft to Steve to verify.
10. Create an account on http://arxiv.org and an ORCiD https://orcid.org/, if you don't have one.
11. Test that it builds properly on arxiv. **__do not__** submit it (this is very important).  Select "non-exclusive and irrevocable license to distribute the article" as the license.
11. Commit the changes to the branch.
12. Let Steve know that it's ready for review, implement any changes.

Once it's approved, submit it to Arxiv:

1. Create a new tar ball, upload it and verify that it builds.
2. Make sure all changes are committed.
3. Enter paper metadata (abstract, etc.)
4. Submit the paper
6. Track it's progress. Once it has been "announced" retrieve the paper password and commit it to the repo as `arxiv_paper_password.txt`.  Not it's "official arXiv identifier"
5. Tag the repo as `axriv-<arxiv-identifier>`.  Don't forget to push the tag: `git push origin <tag_name>`.
7. Send email to authors with a pointer to the paper on `arxiv.org`, include the paper password.

## Submitting to SRC

For some of our work, we need to submit to SRC (https://www.src.org/app/publication/submit/step/1/).  You might need to register with SRC.  If so, ask Steve which task(s) you are working on.  The first step is to prepare a version of the paper according the guidelines for ArXiv (see above), but _do_not_ submit it to the arxiv.

You need to add this to acknowledgements section: "This work was supported in part by CRISP, one of six centers in JUMP, a Semiconductor Research Corporation (SRC) program sponsored by DARPA.”

Here’s a general set of answers to the questions on the submission form:

* Venue: **Conference**
* Is this publication related to an SRC event? **No**
* Earliest anticipated publication or release date: **60 days from from the date of submission or the conference date, whichever is sooner.**
* Destination details: **Conference name (e.g., FAST 2019)**
* Was this publication reviewed by a refereed selection committee? **For accepted papers, yes, otherwise no.**
* I agree to make this publication available to other university participants currently funded by SRC: **Yes**
* Is new, potentially patentable Intellectual Property (IP) disclosed in this publication? **Ask Steve**

Sync up with Steve if you have any questions about how to answer the questions the SRC site asks.

Record the date on which you submitted the paper to SRC in your paper's `README.md`.

## Grammar Checking

Grammerly (https://app.grammarly.com/) is a free and very good grammar checker.  It can't understand TeX, but you can still use it to check the grammar in your papers by exporting the paper as text and uploading.  Create an Grammarly account and then do 

```sh
$ make paper.grammarly.txt
```

To generate a text version of your paper, upload it, and go through its suggestions.

Like all grammar checkers, it is imperfect, so you must use your judgement and read the suggestions carefully.  It catches a bunch of stuff, though.

### Grammarly is not Magic

You still need to proofread your paper yourself and you cannot blindly accept Grammarly's suggestions.  Doing so will make your paper worse, not better.

### Interpretting Grammarly Errors

Grammarly is built for general writing, so some of it's errors/warnings don't apply directly to our papers (which are technical).  The most important thing about text in a paper is that be clear and easy to understand.  Here are some notes about how to respond to common warnings:

#### “Split Infinitive"
  Remove if it is easy.  This is not a big deal
  
  
#### "Repetitive Word"
Repitition can make text boring, but in technical writing referring to the same concept with the same word increases clarity.

So if it is being used a technical sense or to refer to a specific concept, do not change it.  For instance, grammarly flagged “commit” and “log” as  repetitive in a section and transaction processing.  These are technical terms, so you have to use them to be clear.   

If it’s not a technical term, minimize repetition.  For instance, grammarly flagged “traditional” as repetitive in a related work section, so I changed some of the “traditional”s to “previous” or "recent" or just deleted them.   

#### "Overused Word"

These are words that people use too much in general.  If it’s a technical term, keep it.    For instance, “strongest” has a technical meaning in terms of consistency, but in a non-technical context, you could replace with “most powerful”.   For non-techinical terms, you don’t always need to fix these.  Use the most clear, descriptive, and accurate word you can find.

#### TeX Artifacts
paper.grammarly.txt is not perfect, and some TeX artifacts end up in there.  Ignore any complaints from Grammarly about those.

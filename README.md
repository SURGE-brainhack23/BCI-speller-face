# BCI Speller with Emotional Faces

This repository contains a PsychoPy script and associated files for a BCI speller paradigm. A 6 x 6 grid of characters is shown on the screen. For each block of trials, a target letter (selected at random) is highlighted and then the rows/columns are highlighted in random order at a rate of 1 highlight per 500 ms. The experiment consists of 4 runs, each with a different type of row/column highlight. The four conditions are:
- greyscale, emotionally-neutral faces
- greyscale angry faces
- red emotionally-neutral faces
- red angry faces

The use of the term "BCI" here is more aspirational than real. An online speller is not implemented. This paradigm only serves to generate data that can be used to train an offline classifier. 

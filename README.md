# Model of Life take home test

## Prerequisites

To run the tests, please install pytest in a virtual environment and run the tests.

`` pip install pytest ``

`` python -m pytest tests ``


## General programming approach

To complete the task provided the following approach was taken.

The file provided was loaded into the programme as a JSON object and the sequences checked for length and composition. The DNA sequences were then analysed for:

1. Number of each nucleotide (adenine, thymine, guanine, cytosine).

2. Identification of the top 5 most common k-mers for k=2, 3, 4, and 5.

3. Longest palindromic sequence of 20 base pairs or over as defined by a forward strand sequence (5-3) equal to a reverse strand sequence (3-5) complement being a palindrome of equal of over 20 base pairs. 

4. Some analysis of the longest "GC" and "AT" continuous sequences was also carried out.

5. After DNA sequence analysis the results were aggregated to provide totals for steps 1, 2, 3.

6. The programme created a simple markdown report.

7. Tests were written for the functions used in the analysis.

### Programme feature

The best function I could come up with to determine the longest palindromic sequence of each DNA sequence had total time complexity of O(n^3).

To allow the programme to run most efficiently the following steps were taken:

1. The multiprocessing package was used to enable parallelization of the anlysis of the DNA sequences.

2. The 'find_longest_palindrome' function pre-computed the complement DNA sequence which reduced the overall time spent determining the longest palidromic sequence.

3. Code was optimized for speed while trying to maintain good readabilty.

To enable maintainabilty, type hinting was used throughout and the code heavily commented.

## DNA sequence analysis report.

The markdown report created by the programme is presented below:

Total number sequences = 200

Total number invalid sequences = 8

Total nucleotide counts:

Adenine = 38703

Thymine = 39460

Guanine = 58281

Cytosine = 55556

| k_mer (k2)| number
| ----------| ------
| gg| 21806
| cc| 19907
| gc| 14971
| cg| 9459
| ag| 7415

| k_mer (k3)| number
| ----------| ------
| ggg| 6961
| ccc| 5684
| ggc| 3450
| gcc| 3406
| gcg| 3157

| k_mer (k4)| number
| ----------| ------
| gggg| 1900
| cccc| 1660
| gggc| 1064
| ggcg| 876
| cggg| 870

| k_mer (k5)| number
| ----------| ------
| ccccc| 406
| ggggg| 400
| ggggc| 390
| ttttt| 314
| cgggg| 301

Total palindromes equal to or over 20 base pairs = 16

The longest palindrome was 34(bp) and had a sequence of TAAACGGGCCTTAATATATATTAAGGCCCGTTTA

| Palindrome sequence| length(bp)
| -------------------| ----------
| TAAACGGGCCTTAATATATATTAAGGCCCGTTTA| 34
| GGCCCGCAAATAATTATTTGCGGGCC| 26
| GCGCGGTAAAATATTTTACCGCGC| 24
| AAATTTAATATATATTAAATTT| 22
| CCGGCCGCCCCGGGGCGGCCGG| 22
| AAATTTAATATTTTTAAAAATATTAAATTT| 30
| GGGCCCGGGGCGCCCCGGGCCC| 22
| CGGGGCCCCCCGGGGGGCCCCG| 22
| CGCGCCGGGCCGGCCCGGCGCG| 22
| CGGGGGCCCGGCCGGGCCCCCG| 22
| GCCGCGGCGCCGGCGCCGCGGC| 22
| TTAAATATTTTAAAATATTTAA| 22
| GGCGGCCCCGCGCGCGGGGCCGCC| 24
| TTTATTATTAATTAATAATAAA| 22
| CGGCGCGCCCGCGGGCGCGCCG| 22
| CCCGGGCGGGCGCCCGCCCGGG| 22

## Analysis of the DNA sequence analysis report

### Overview of DNA sequences

Of the 200 DNA sequences provided, 8 were found to contain letters other than A,T,G or C. This indicates that in those cases sequencing errors, ambiguous identification or base modifications (e.g 5-methylcytosine (5mC)) may have occurred.

Overall the DNA sequences appear to be enriched in guanine (G) and cytosine (C) bases, having a GC content of 59.3%, ((58281 + 55556)/ 192000).

This could  occur for many reasons including:

1. Species specific composition of the DNA sequences originating from a particular species or genus. For example some microbial genomes tend to exhibit high GC contents,  but the causes of this variation have yet to be resolved ([ref 1]( https://www.sciencedirect.com/topics/)).

2. Enrichment of genomic regions in GC. Promoter regions for example have a tendency to high GC content ([ref-2](https://pmc.ncbi.nlm.nih.gov/articles/PMC3514669/)).

3. Sampling or sequencing bias. For example PCR based sequencing could exhibit GC bias due to the higher probability of primer annealing to those regions ([ref-3](https://pubmed.ncbi.nlm.nih.gov/28060945/)).

### K-mer analysis

The k-mer analysis results also show that the most common are  G, C or GC containing. 

### Palindrome analysis

The analysis found 16 DNA sequences where palindromes are of 20 base pairs or over. This finding could occur due to sequencing artifacts which have been found to occur in PCR based sequencing approaches ([ref-4](https://bmcgenomics.biomedcentral.com/articles/10.1186/)). 

However, if these palindromic sequences are real they could be involved in a diverse range of processes, from bacterial immune responses to the regulation of gene expression in eukaryotes ([ref-5](https://www.sciencedirect.com/science/article/abs/pii/B9780128225639000652)). 

Palindromic sequences are also often associated with amplified genes in both prokaryotes and eukaryotes ([ref-6](https://academic.oup.com/genetics/article-abstract/161/3/1065/6052570?redirectedFrom=fulltext)). 

Without further information on the composition and preparation of the DNA sequence dataset and further analysis, it is difficult to expand more on this finding.

A short analysis running some of the longest palindromic sequences through the BLAST sequence alignment tool ([ref-7](https://blast.ncbi.nlm.nih.gov/Blast.cgi)), using default settings,  indicated many originated from bacteria as shown below:

| Sequence | Species | 
| -------- | ------- | 
| GGCCCGCAAATAATTATTTGCGGGCC | Pantoea dispersa strain (gram negative bacterium) |
| GCGCGGTAAAATATTTTACCGCGC | Edwardsiella ictaluri (gram negative bacterium) |
| AAATTTAATATATATTAAATTT  | Medioppia subpectinata ( ciliate protozoan) |
| CCGGCCGCCCCGGGGCGGCCGG  | Micromonospora krabiensis (gram positive bacterium) |
|  CGGGGCCCCCCGGGGGGCCCCG  | Thermus thermophilus (gram negative bacterium) |
|  CGGGGCCCCCCGGGGGGCCCCG  | Pantoea dispersa (gram negative bacterium) |

Although the sequence alignment analysis is cursory, the results along with the enhanced GC content of the DNA sequences overall may indicate that many or all of the DNA sequences are of bacterial origin.  But more work would be required to establish this assertion.

### Program design and future opportunities

The programatic approach taken allows for a relatively rapid analysis of DNA sequences to be carried out. Since each DNA sequence is analysed independently, further interrogation of this dataset is avalable to drill down into the characteristics of each DNA sequence;  while the aggregated results provide an overview of all of the DNA seqeunces making up the dataset.



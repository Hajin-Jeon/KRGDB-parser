# KRGDB Parser
## 0. Purpose
This is a web scraper to obtain KRGDB allele frequency for target SNPs from dbSNP.

## 1. Motivation
Accessing the KRGDB database directly is currently not feasible. Therefore, it needs to be indirectly checked through dbSNP.

However, when using the Entrez Programming Utilities provided by NCBI, there is an issue where some allele frequencies are not available.

(Example: For https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&id=rs761437962&report=XML, only allele frequency for C in the KOREAN study is shown.)

To overcome this, I decided to directly read the dbSNP website and parse the html file.

## 2. Usage
### 2-1. Environment
- Python3
- Requires requests and beautifulsoup4 library
```bash
pip install requests
pip install beautifulsoup4
```
### 2-2. How to use
The basic usage is as follows:
```bash
python krgdb_parser.py [OPTION] (file or rs_id)
```
Options are as follows:
- `b, --batch`: Accepts a file containing multiple rs ids as input.

## 3. Sample input and output
### 3-1. Output format
- `rs_id`: name of the rs
- `population_size`: size of the population (of KRGDB)
- `REF`: reference allele
- `REF frequency`: allele frequency of the reference allele
- `ALT`: alternative allele
- `ALT frequency`: allele frequency of the alternative allele

ALT and ALT frequency can be shown multiple times.

### 3-2. Example case
Here's an example case:
- Input: `python krgdb_parser.py rs12732870`
- Output: `rs12732870	2920	T	0.8192	A 0.0301	G 0.1507`

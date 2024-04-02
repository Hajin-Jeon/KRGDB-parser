# KRGDB Parser
## 0. Purpose
This web scraper obtains KRGDB allele frequencies for target SNPs from dbSNP.

## 1. Motivation
Direct access to the KRGDB database is not feasible, necessitating indirect checks through dbSNP.

However, using NCBI's Entrez Programming Utilities sometimes results in missing allele frequencies.

(Example: For https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=snp&id=rs761437962&report=XML, only allele frequency for C in the KOREAN study is shown, not for A or T.)

## 2. Usage
### 2-1. Environment
- Python3
- Requires `requests` and `beautifulsoup4` libraries:
```bash
pip install requests
pip install beautifulsoup4
```
### 2-2. How to Use
Basic usage:
```bash
python krgdb_parser.py [-h] [-b] [-o OUTPUT] input_arg
```
Options:
- `-h, --help`: show the help message
- `-b, --batch`: process in batch mode
- `-o OUTPUT, --output OUTPUT`: output file to write results to.

## 3. Sample Input and Output
### 3-1. Output Format
- `rs_id`: name of the rs
- `population_size`: size of the population (of KRGDB)
- `REF`: reference allele
- `REF frequency`: allele frequency of the reference allele
- `ALT`: alternative allele
- `ALT frequency`: allele frequency of the alternative allele

ALT and ALT frequency can be shown multiple times.

### 3-2. Example Case
Example 1:
- Input: `python krgdb_parser.py rs12732870`
- Output: `rs12732870	2920	T	0.8192	A	0.0301	G	0.1507`


Example 2 (Using tags):
- Input: `python krgdb_parser.py -b -o result.txt file.txt`
- Input file `file.txt`:
```
rs200949691
rs141478865
rs141265262
rs72648929
rs34936017
```
- Output file `result.txt`:
```
rs200949691	2930	C	0.9799	G	0.0201

rs141265262	2922	C	0.9849	T	0.0151
rs72648929	2922	C	0.9610	T	0.0390
rs34936017	2922	A	0.9846	G	0.0154
```

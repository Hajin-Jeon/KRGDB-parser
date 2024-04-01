import argparse
import os
import re
import requests
import sys
import time
from bs4 import BeautifulSoup

def download_html(rs_id):
    url = f"https://www.ncbi.nlm.nih.gov/snp/{rs_id}"
    # sleep: NCBI allows 3 requests per second
    time.sleep(0.34)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching {url}")
        return None

# input: "A=0.0007, C=0.0164, T=0.1068"
# return: [('A', '0.0007'), ('C', '0.0164'), ('T', '0.1068')]
def extract_frequency_data(text):
    frequency_data = []
    parts = text.split(", ")
    for part in parts:
        allele, freq = part.split("=")
        frequency_data.append((allele, freq))
    return frequency_data

def parse_html(rs_id, html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    for tr in soup.find_all('tr'):
        a_tags = tr.find_all('a')
        for a in a_tags:
            if 'KRGDB' in a.text:
                tds = tr.find_all('td')
                sample_size = ""
                frequencies = []
                for td in tds:
                    text = td.text.strip()
                    if "samp_s" in td.get("class", []):
                        sample_size = text
                    elif "=" in text:
                        frequencies.extend(extract_frequency_data(text))
                if frequencies:
                    ref, ref_freq = frequencies[0]
                    alts = frequencies[1:]
                    alt_str = '\t'.join([f"{allele} {freq}" for allele, freq in alts])
                    print(f"{rs_id}\t{sample_size}\t{ref}\t{ref_freq}\t{alt_str}")

def process_single_rs(rs_id):
    if not os.path.exists(rs_id):
        html_content = download_html(rs_id)
    else:
        with open(rs_id, 'r', encoding='utf-8') as file:
            html_content = file.read()
    if html_content:
        parse_html(rs_id, html_content)

def process_rs_file(input_arg):
    with open(input_arg, 'r', encoding='utf-8') as file:
        for rs_id in file:
            rs_id = rs_id.strip()
            if rs_id:
                process_single_rs(rs_id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_arg", help="Input file name or option")
    parser.add_argument("-b", "--batch", action="store_true", help="Process in batch mode")

    args = parser.parse_args()

    if re.match(r'^rs\d+$', args.input_arg) and not args.batch:
        process_single_rs(args.input_arg)
    elif os.path.exists(args.input_arg):
        process_rs_file(args.input_arg)
    else:
        print(f"File {args.input_arg} not found.")

if __name__ == "__main__":
    main()


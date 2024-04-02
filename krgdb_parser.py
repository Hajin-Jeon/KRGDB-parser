import argparse
import os
import re
import requests
import sys
import time
from bs4 import BeautifulSoup

def download_html(rs_id):
    url = f"https://www.ncbi.nlm.nih.gov/snp/{rs_id}"
    time.sleep(0.2)  # NCBI allows 3 requests per second
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
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

def parse_html(rs_id, html_doc, output_file=None):
    soup = BeautifulSoup(html_doc, 'html.parser')
    results = []

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
                    result_line = f"{rs_id}\t{sample_size}\t{ref}\t{ref_freq}\t{alt_str}"
                    results.append(result_line)
    
    if output_file:
        with open(output_file, 'a') as file:
            file.writelines('\n'.join(results) + '\n')
    else:
        print('\n'.join(results))

def process_single_rs(rs_id, output_file=None):
    if not os.path.exists(rs_id):
        html_content = download_html(rs_id)
    else:
        with open(rs_id, 'r', encoding='utf-8') as file:
            html_content = file.read()
    if html_content:
        parse_html(rs_id, html_content, output_file)

def process_rs_file(input_arg, output_file=None):
    with open(input_arg, 'r', encoding='utf-8') as file:
        for rs_id in file:
            rs_id = rs_id.strip()
            if rs_id:
                process_single_rs(rs_id, output_file)

def check_output_file_writable(output_file):
    if output_file:
        try:
            with open(output_file, 'a') as file:
                pass  # Successfully opened for appending, file is writable
        except IOError as e:
            print(f"Unable to write to output file {output_file}: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_arg", help="input file name or rs ID")
    parser.add_argument("-b", "--batch", action="store_true", help="process in batch mode")
    parser.add_argument("-o", "--output", help="output file to write results to.", default=None)

    args = parser.parse_args()

    check_output_file_writable(args.output)

    if args.batch and os.path.exists(args.input_arg):
        process_rs_file(args.input_arg, args.output)
    elif re.match(r'^rs\d+$', args.input_arg):
        process_single_rs(args.input_arg, args.output)
    else:
        print(f"Invalid input or file not found: {args.input_arg}")

if __name__ == "__main__":
    main()




import os
import time
import json

import pandas as pd

from utils import fetch_publication_details, save_to_csv, arg_parser, get_all_pubmed_ids

def execute_main():

    args = arg_parser()
    args_dict = vars(args)

    search_term = args_dict['search_terms']
    ouput_folder = args_dict['output_folder']

    pubmed_ids = get_all_pubmed_ids(search_term)

    print(f"Total PubMed IDs retrieved: {len(pubmed_ids)}")
    
    publications = fetch_publication_details(pubmed_ids)

    save_to_csv(publications, output_folder=ouput_folder)

if __name__ == "__main__":
    execute_main()

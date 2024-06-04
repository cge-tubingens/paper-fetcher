

import os
import time
import json

import pandas as pd

from helpers import arg_parser, get_all_pubmed_ids, get_pub_details

def execute_main():

    args = arg_parser()
    args_dict = vars(args)

    search_term = args_dict['search_terms']
    ouput_folder = args_dict['output_folder']

    pubmed_ids = get_all_pubmed_ids(search_term)

    print(f"{len(pubmed_ids)} PubMed IDs has been fetched")

    lst = []

    for id in pubmed_ids:

        time.sleep(0.5)

        path_web = f"https://pubmed.ncbi.nlm.nih.gov/{id}"

        info = get_pub_details(path_web)

        info['pubmed_id'] = id

        lst.append(info)

    df_pubs = pd.DataFrame(columns=['PubMed ID', 'Journal', 'Year', 'Title'])

    count=0
    for pub_dict in lst:
        df_pubs.loc[count, 'PubMed_ID'] = pub_dict['pubmed_id']
        df_pubs.loc[count, 'Journal'] = pub_dict['journal']
        df_pubs.loc[count, 'Year'] = pub_dict['year']
        df_pubs.loc[count, 'Title'] = pub_dict['title']

    path_to_file = os.path.join(ouput_folder, 'publications_info.txt')
    path_to_pubs = os.path.join(ouput_folder, 'publications.csv')

    df_pubs.to_csv(path_to_pubs, index=False)

    with open(path_to_file, 'w') as file:
        file.write(json.dumps(lst))

if __name__ == "__main__":
    execute_main()



import os
import time
import json

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

    path_to_file = os.path.join(ouput_folder, 'publications_info.txt')

    with open(path_to_file, 'w') as file:
        file.write(json.dumps(lst))

if __name__ == "__main__":
    execute_main()


import argparse
import requests
from xml.etree import ElementTree

from bs4.element import Tag
from bs4 import BeautifulSoup

# Function to get all PubMed IDs related to a search term, excluding preprints
def get_all_pubmed_ids(search_term, batch_size=100):
    pubmed_ids = []
    retstart = 0
    while True:
        # Exclude preprints by adding "-medrxiv[All Fields] -biorxiv[All Fields]" to the search term
        esearch_url = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
            f"db=pubmed&term={search_term} NOT medrxiv[All Fields] NOT biorxiv[All Fields] NOT ArXiv[All Fields]" 
            f"&retmax={batch_size}&retstart={retstart}&retmode=xml"
        )
        esearch_response = requests.get(esearch_url)
        esearch_response.raise_for_status()

        esearch_tree = ElementTree.fromstring(esearch_response.content)
        id_list = [id_elem.text for id_elem in esearch_tree.findall(".//Id")]
        pubmed_ids.extend(id_list)
        
        if len(id_list) < batch_size:
            break
        
        retstart += batch_size
    
    return pubmed_ids


def get_pub_details(web_address:str)->dict:

    # Create a handle, page, to handle the contents of the website
    data = requests.get(web_address).text

    # Creating BeautifulSoup object
    soup = BeautifulSoup(data, 'html.parser')

    result_dict = {}

    result_dict['title'] = soup.find_all('meta', {"name":"citation_title"})[0]['content']
    result_dict['journal'] = soup.find_all('meta', {"name":"citation_journal_title"})[0]['content']

    if soup.find('time', {"class":"citation-year"}) is not None:
        result_dict['year'] = soup.find('time', {"class":"citation-year"}).text
    else:
        None
    result_dict['authors'] = []

    if len(soup.find_all('div', {"class":"authors-list"}))>0:
 
        auth_list = soup.find_all('div', {"class":"authors-list"})[0]
    
        info = []
        for th in auth_list.children:
            if isinstance(th, Tag):
                info.append(th)
    
        for elem in info:

            auth_name = elem.find('a', {"class":"full-name"}).text
            if elem.find('a', {"class":"affiliation-link"}) is not None:
                auth_aff = elem.find('a', {"class":"affiliation-link"})['title']
            else:
                auth_aff = None
            result_dict["authors"].append(
                (auth_name, auth_aff)
            )

        return result_dict
    
    else: return result_dict

def arg_parser()->dict:

    # define parser
    parser = argparse.ArgumentParser(description='Adresses to configuration files')

    # parameters of quality control
    parser.add_argument('--search-terms', type=str, nargs='?', default=None, const=None, help='Keyword to search in PubMed')

    # path to data and names of files
    parser.add_argument('--output-folder', type=str, nargs='?', default=None, const=None, help='Folder where the data will be stored')

    # parse args and turn into dict
    args = parser.parse_args()

    return args

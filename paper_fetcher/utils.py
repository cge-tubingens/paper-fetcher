import requests
from xml.etree import ElementTree
import os
import csv
import argparse

# Function to get all PubMed IDs related to a search term, excluding preprints
def get_all_pubmed_ids(search_term:str, batch_size:int=100)->list:

    pubmed_ids= []
    retstart  = 0

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

# Function to extract the country from an affiliation string
def extract_country(affiliation:str)->str:

    # This regex looks for the last word in the affiliation string, assuming it is the country
    parts = affiliation.split(';')
    last_parts = [part.split(',')[-1].strip() for part in parts]

    return ';'.join(last_parts) if last_parts else "Unknown"

# Function to fetch publication details for a list of PubMed IDs
def fetch_publication_details(pubmed_ids:list)->list:

    publications = []
    batch_size = 100
    
    for start in range(0, len(pubmed_ids), batch_size):

        batch_ids = pubmed_ids[start:start + batch_size]
        efetch_url = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
            f"db=pubmed&id={','.join(batch_ids)}&retmode=xml"
        )
        efetch_response = requests.get(efetch_url)
        efetch_response.raise_for_status()
        
        efetch_tree = ElementTree.fromstring(efetch_response.content)
        
        for article in efetch_tree.findall(".//PubmedArticle"):
            pubmed_id_elem = article.find(".//MedlineCitation/PMID")
            pubmed_id = pubmed_id_elem.text if pubmed_id_elem is not None else "Unknown"

            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No title available"

            # Extract publication year
            pubdate_elem = article.find(".//PubDate/Year")
            if pubdate_elem is None:  # if <Year> is not found, look for <MedlineDate>
                pubdate_elem = article.find(".//PubDate/MedlineDate")
            pubyear = pubdate_elem.text[:4] if pubdate_elem is not None else "Unknown"

            authors_with_affiliations = []

            for author in article.findall(".//Author"):
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                affiliation_infos = author.findall(".//AffiliationInfo/Affiliation")
                
                name = f"{fore_name.text if fore_name is not None else ''} {last_name.text if last_name is not None else ''}".strip()
                affiliations = [affiliation.text for affiliation in affiliation_infos if affiliation is not None]
                
                if name:
                    authors_with_affiliations.append((name, affiliations))
            
            publications.append({
                "pubmed_id": pubmed_id,
                "title": title,
                "pubyear": pubyear,
                "authors_with_affiliations": authors_with_affiliations
            })
    
    return publications

# Function to save publication details to a CSV file
def save_to_csv(publications, output_folder:str, filename:str="publications_filtered.csv")->None:

    path_to_csv = os.path.join(output_folder, filename)

    with open(path_to_csv, mode='w', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)
        writer.writerow(["PubMed ID","Title", "Publication Year", "Author", "Affiliations", "Country"])

        for pub in publications:
            for author, affiliations in pub['authors_with_affiliations']:
                for affiliation in affiliations:

                    country = extract_country(affiliation)
                    writer.writerow([pub['pubmed_id'],pub['title'], pub['pubyear'], author, affiliation, country])

    pass

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

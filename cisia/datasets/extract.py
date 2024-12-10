import requests
from requests.exceptions import ChunkedEncodingError
from http.client import IncompleteRead
import time
import os
from .auxiliary_functions import *
from bs4 import BeautifulSoup

def url_exists(url, save_path):
    """
    Attempts to download a file from the given URL and save it to the specified path.
    Returns True if the file was downloaded successfully, indicating the URL exists.

    Parameters:
    - url: The URL of the file to download.
    - save_path: The full path (including filename) where the file should be saved.

    Returns:
    - True if the file is downloaded successfully, False otherwise.
    """
    try:
        ensure_folder_exists('temp')
        with requests.get(url, stream=True) as r:
            # Check if the request was successful
            if r.status_code == 200:
                # Check for non-empty content
                if int(r.headers.get('Content-Length', 0)) > 0:
                    with open(save_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return True
            # If the status code is not 200 or content length is 0, treat as failure
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def scrapping_venda_url(soup, fuel_type, location_type):
    h3_tags = soup.find_all('h3')
    list_urls = []    
    # Loop through each <h3> tag found
    padrao_data = r'\d{2}/\d{2}/\d{4}'
    file_name = ""

    if location_type == "estado":
        for li_tag in soup.find_all('li'):
            a_tag = li_tag.find('a')
            if a_tag and "Vendas de derivados petróleo e etanol" in a_tag.get_text():
                if a_tag['href'].endswith('.csv'):
                    link = a_tag['href']
                    
                    span_tag = li_tag.find('span')
                    updated_at = span_tag.get_text() if span_tag else None
                    list_urls.append(link)
                    file_name = f'{unidecode(location_type)}_{updated_at}' 
                    
        return list_urls, file_name
    for h3 in h3_tags:
        if location_type in h3.text:
            # Find all <ul> tags that are after the <h3> tag
            ul_tags = h3.find_all_next('ul')
            for ul_tag in ul_tags:
                if ul_tag:
                    # Loop through all <li> tags in the <ul>
                    for li in ul_tag.find_all('li'):
                        # Look for <b> tags inside each <li>
                        b_tag = li.find('b')
                        if b_tag and fuel_type in b_tag.text:
                            # Now, find the next <ul> tag after the current <ul> and search for <a> with .csv link
                            next_ul = ul_tag.find_next('ul')
                            # print(next_ul)
                            if next_ul:
                                # Look for all <a> tags in the next <ul> with .csv in the href
                                a_tags = next_ul.find_all('a', href=True)
                                li_tags = next_ul.find_all('li')
                                # print(li_tags[1].text)
                                for index, a_tag in enumerate(a_tags):
                                    # print(a_tag)
                                    if a_tag and a_tag['href'].endswith('.csv'):
                                        link_csv = a_tag['href']
                                        
                                        # se for municipio pega correto o anual
                                        if unidecode(location_type) == "municipio":
                                            csv_file = link_csv.split("/")[-1]
                                            if unidecode(location_type) in csv_file:
                                                updated_at = re.findall(padrao_data, li_tags[index].text)[0]
                                                file_name = f'{unidecode(location_type)}_{fuel_type}_{updated_at}' 
                                                list_urls.append(a_tag['href']) 
                                            

    return list_urls, file_name
def scrape_for_file_links(url, transaction_type, fuel_type, location_type):
    """
    Scrape a given URL for links to files with specific extensions (.csv, .zip) and return a list of these file URLs.

    Args:
    url (str): The URL of the website to scrape.

    Returns:
    list: A list of URLs (str) pointing to files ending with .csv or .zip. The list will be empty if no such links are found or if the page fails to load.

    The function makes an HTTP GET request to the provided URL. If the request is successful, it parses the HTML content to find all anchor tags with an 'href' attribute that ends with '.csv' or '.zip'. It adds these URLs to a list which is then returned. If the request is unsuccessful, it prints an error message with the failed status code.
    """
    list_urls = []
    # Make a GET request to fetch the raw HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if transaction_type == "venda":
            return scrapping_venda_url(soup, fuel_type, location_type) 
        else:
            return "not exists"
        
        # Loop through all found <a> tags
        # for link in links:
        #     # Extract the URL from the 'href' attribute
        #     href = link['href']
            
        #     # Extract the text of the <a> tag
        #     text = link.get_text()

        #     if href.endswith('.csv') or href.endswith('.zip') :
        #         if type == "state":
        #             if href.contains("estado"):
        #                 list_urls.append(href)
        #         elif type == "city":
        #             if href.contains("municipio"):
        #                 list_urls.append(href)
    else:
        print(f"Failed to retrieve the website: status code {response.status_code}")
    return list_urls

def download_file_directly(url, folder, filename=None, max_retries=10):
    """
    Download a file from a specified URL directly to a given folder with optional retry logic.

    Args:
    url (str): The URL from which to download the file.
    folder (str): The local directory path where the file will be saved.
    filename (str, optional): The name to save the file as. If not provided, the name is taken from the last segment of the URL.
    max_retries (int, optional): The maximum number of retries if the download fails. Defaults to 20.

    Returns:
    str: A message indicating the success or failure of the download. Success messages include the path where the file was saved, and failure messages include an error code or description.

    This function attempts to download a file by making a GET request to the provided URL. If the request is successful and the server responds with a 200 status code, the file is written to the specified location in chunks. If the server response indicates a failure (any status code other than 200), or if an exception occurs during download, the function will retry the download up to `max_retries` times before giving up. The wait time between retries is 10 seconds.
    """
    attempts = 0
    
    while attempts < max_retries:
        try:
            print("Checking download...")
            if not filename:
                filename = url.split('/')[-1]
            file_path = os.path.join(folder, filename)
            # print(f"Downloading {url} to {file_path}...")
            needDownload = os.path.isfile(file_path)
            if not needDownload:
                with requests.get(url, stream=True) as response:
                    # print(f"Response Status Code: {response.status_code}")

                    if response.status_code == 200:
                        # print("Saving file...")
                        with open(file_path, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    file.write(chunk)
                        # print(f"\033[32mFile saved successfully at {file_path}\033[0m")
                        return f"File downloaded successfully"
                    else:
                        return "\033[31mError: The download request failed with status code: " + str(response.status_code) + "\033[0m"
                    
            return f"Dataset already updated"
        except (ChunkedEncodingError, IncompleteRead) as e:
            print(f"\033[31mAn error occurred: {e}\033[0m. Retrying in 5 seconds...")
            time.sleep(10)  # Corrected to show 10 seconds as per your retry sleep
            attempts += 1
        except Exception as e:
            print(f"\033[31mAn error occurred: {e}\033[0m")
            return "An error occurred: " + str(e)

    return "\033[31mError: Max retries reached. Failed to download the file.\033[0m"

def download_anp_data(transaction_type="sales", location_type="state", fuel_type="gasolinec"):
    """
    Download data from various ANP URLs and organize it into specified folders.

    Args:
    folder_paths (list of str, optional): A base path list that determines where to create folders for each data category. Defaults to ['dados', 'raw_data'].

    This function iterates over a predefined dictionary of data categories and their corresponding URLs. For each category, it:
    1. Constructs a path by joining the base folder paths with the category name.
    2. Ensures the folder exists (using the `ensure_folder_exists` function).
    3. Scrapes the page at the category's URL for file links (using the `scrape_for_file_links` function).
    4. Downloads each file found to the constructed folder path (using the `download_file_directly` function).
    5. If the file is a zip file, it is extracted and the zip file is deleted (using the `unzip_and_delete` function).

    The function organizes downloaded files by their data categories into subdirectories within the specified base directory path. Each category has its own folder.
    """
    folder_paths=['dados', 'raw_data']
    dic = {
        'venda': 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/vendas-de-derivados-de-petroleo-e-biocombustiveis',
        'producao_historica': 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/producao-de-petroleo-e-gas-natural-nacional',
        'producao_estados': 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/producao-de-petroleo-e-gas-natural-por-estado-e-localizacao',
        'importacao_exportacao': 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/importacoes-e-exportacoes',
        'preco_historico': 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis'
    }
    # for element in dic:
    categoria = translate_transaction_type_name(transaction_type)
    derivado = "" if fuel_type is None else translate_fuel_name(fuel_type)
    localidade = translate_location_type_name(location_type)
    
    folder_path = os.path.join(*folder_paths, categoria)
    # folder_path = os.path.join(file_path, folder_path)
    folder_path = ensure_folder_exists([folder_path])
    url = dic[categoria]
    links, file_name = scrape_for_file_links(url, transaction_type=categoria, fuel_type=derivado, location_type=localidade)
    file_name=file_name.replace("/", "-")+".csv"
    for link in links:
        # print(file_name)
        msg = download_file_directly(url=link, filename=file_name, folder=folder_path)
        print(msg)
        if '.zip' in link:
            file_name = link.split('/')[-1]
            unzip_and_delete(os.path.join(folder_path, file_name))
    return file_name
# download_anp_data()
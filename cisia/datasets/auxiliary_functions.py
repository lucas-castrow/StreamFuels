
import os
import zipfile
from unidecode import unidecode
import re

def translate_fuel_name(fuel_name):
    fuel_mapping = {
        'ethanol': 'Etanol hidratado',
        'gasoline-r': 'Gasolina C',
        'gasoline-a': 'Gasolina de aviação',
        'fuel oil': 'Óleo combustível',
        'LPG': 'GLP',
        'diesel': 'Óleo diesel',
        'kerosene-i': 'Querosene iluminante',
        'kerosene-a': 'Querosene de aviação'
    }
    return fuel_mapping.get(fuel_name.lower(), "Invalid")


def translate_location_type_name(name):
    mapping = {
        'city': 'município',
        'state': 'estado',
    }
    return mapping.get(name.lower(), "Invalid")

def translate_transaction_type_name(name):
    mapping = {
        'sales': 'venda',
        'import': 'importacao',
        'export': 'exportacao',
    }
    return mapping.get(name.lower(), "Invalid")
def get_default_download_dir():
    """Return the default directory for downloads."""
    default_dir = os.path.join(os.path.expanduser("~"), ".cisia")
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
    return default_dir
def unzip_and_delete(zip_file_path):
    """
    Unzips a ZIP file and deletes the original ZIP file after extraction.
    
    Parameters:
    - zip_file_path: Path to the ZIP file.
    """
    # Check if the file exists and is a zip file
    if not zipfile.is_zipfile(zip_file_path):
        print(f"The file at {zip_file_path} is not a valid zip file.")
        return

    try:
        # Create a ZipFile object in read mode
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract all the contents into the directory of the zip file
            extract_path = os.path.dirname(zip_file_path)
            zip_ref.extractall(extract_path)
            print(f"Extracted all contents to {extract_path}")

        # Remove the original ZIP file
        os.remove(zip_file_path)
        print(f"Deleted original zip file: {zip_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_string(string):
    return re.sub(r'[^a-zA-Z0-9]', '', unidecode(str(string).lower()))

def mes_para_numero(mes):
    meses = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
        'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
        'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
    }
    return meses.get(mes.upper(), '00')

def ensure_folder_exists(parts):
    """
    Checks if a folder exists, and creates it (including any necessary parent directories)
    if it doesn't.

    Parameters:
    - folder_path: The path to the folder to check and create.
    """
    file_path = get_default_download_dir()
    p = os.path.join(file_path, *parts)
    
    if not os.path.exists(p):
        os.makedirs(p)
    return p

def estado_para_sigla(estado):
    # Mapeamento dos nomes dos estados para suas siglas
    estados = {
        'acre': 'ac',
        'alagoas': 'al',
        'amapa': 'ap',
        'amazonas': 'am',
        'bahia': 'ba',
        'ceara': 'ce',
        'distritofederal': 'df',
        'espiritosanto': 'es',
        'goias': 'go',
        'maranhao': 'ma',
        'matogrosso': 'mt',
        'matogrossodosul': 'ms',
        'minasgerais': 'mg',
        'para': 'pa',
        'paraiba': 'pb',
        'parana': 'pr',
        'pernambuco': 'pe',
        'piaui': 'pi',
        'riodejaneiro': 'rj',
        'riograndedonorte': 'rn',
        'riograndedosul': 'rs',
        'rondonia': 'ro',
        'roraima': 'rr',
        'santacatarina': 'sc',
        'saopaulo': 'sp',
        'sergipe': 'se',
        'tocantins': 'to'
    }
    # Retorna a sigla do estado, ou "Estado inválido" se não encontrado
    return estados.get(estado, 'Estado inválido')

def obter_max_min_datas(df, col_data, mes_ou_ano):
    max,min = (None, None)
    if mes_ou_ano == 'ano':
        max =  df[col_data].astype(int).max()
        min =  df[col_data].astype(int).min()
    else:
        max =  df[col_data].astype(str).str.replace("-", "").astype(int).max()
        min =  df[col_data].astype(str).str.replace("-", "").astype(int).min()
    return max,min

def kg_to_m3(material, kg):
    #https://www.gov.br/anp/pt-br/centrais-de-conteudo/publicacoes/anuario-estatistico/arquivos-anuario-estatistico-2022/outras-pecas-documentais/fatores-conversao-2022.pdf
    densidades = { #em TERA / M3
        'etanolanidro': 0.79100,
        'etanolhidratado': 0.80900,
        'asfalto': 1025.00,
        'biodieselb100': 880.00,
        'gasolinac': 754.25,
        'gasolinadeaviacao': 726.00,
        'glp': 552.00,
        'lgn': 580.00,
        'oleodiesel': 840.00,
        'oleocombustivel': 1013.00,
        'petroleo': 849.76,
        'querosenedeaviacao': 799.00,
        'queroseneiluminante': 799.00,
        'solventes': 741.00
    }
    
    if material in densidades:
        densidade = densidades[material] / 1e3  # Convertendo para kg/m³
        m3 = kg / densidade
        return m3
    else:
        return "Material não encontrado na lista."

def registrar_meses_duplicados(df, produto, local, tempo):
    #os.remove(f'timestamps_duplicadas_{tempo}.csv') if os.path.exists(f'timestamps_duplicadas_{tempo}.csv') else None
    df_c = df.copy()
    df_c['duplicatas'] = df_c.groupby('timestamp')['timestamp'].transform('count') - 1
    df_c = df_c[df_c['duplicatas']>=1]
    df_c['derivado'] = produto
    df_c['local'] = local
    df_c.to_csv(f'timestamps_duplicadas_{tempo}.csv', mode='a', header=False, index=False)
    
def combinar_valores_unicos_colunas(df, colunas):
    # Agrupar pelo conjunto de colunas e resetar o índice para transformar em DataFrame
    df_unicos = df[colunas].drop_duplicates().reset_index(drop=True)
    
    # Converter o DataFrame resultante em uma lista de tuplas
    combinacoes_existentes = [tuple(x) for x in df_unicos.values]
    
    return combinacoes_existentes

def first_non_nan_value(df, column_name):
    """
    Find the first non-NaN value in the specified column of a DataFrame.

    Args:
    df (DataFrame): The pandas DataFrame.
    column_name (str): The name of the column to search for non-NaN values.

    Returns:
    The first non-NaN value in the specified column, or None if no non-NaN values are found.
    """
    first_non_nan_index = df[column_name].first_valid_index()
    if first_non_nan_index is not None:
        return df[column_name].iloc[first_non_nan_index]
    else:
        return None
    
def last_non_nan_value(df, column_name):
    """
    Find the last non-NaN value in the specified column of a DataFrame.

    Args:
    df (DataFrame): The pandas DataFrame.
    column_name (str): The name of the column to search for non-NaN values.

    Returns:
    The last non-NaN value in the specified column, or None if no non-NaN values are found.
    """
    last_non_nan_index = df[column_name].last_valid_index()
    if last_non_nan_index is not None:
        return df[column_name].iloc[last_non_nan_index]
    else:
        return None

def find_first_sequence(arr):
    """
    Find the first sequence of consecutive elements in the given array.

    Args:
        arr (list): The input list of integers.

    Returns:
        list: The list containing the first sequence of consecutive elements.
    """
    if not arr:
        return []  # Return an empty list if the input array is empty
    
    sequence = [arr[0]]  # Start with the first element
    for i in range(1, len(arr)):
        # If the current element is consecutive with the previous one, add it to the sequence
        if arr[i] == sequence[-1] + 1:
            sequence.append(arr[i])
        else:
            break  # Break the loop when the sequence breaks
    return sequence

def find_last_sequence(arr):
    """
    Find the last sequence of consecutive elements in the given array.

    Args:
        arr (list): The input list of integers.

    Returns:
        list: The list containing the last sequence of consecutive elements.
    """
    if not arr:
        return []  # Return an empty list if the input array is empty
    
    sequence = [arr[-1]]  # Start with the last element
    for i in range(len(arr) - 2, -1, -1):
        # If the current element is consecutive with the next one, add it to the sequence
        if arr[i] == sequence[-1] - 1:
            sequence.append(arr[i])
        else:
            break  # Break the loop when the sequence breaks
    sequence.reverse()  # Reverse the sequence to have it in ascending order
    return sequence
    
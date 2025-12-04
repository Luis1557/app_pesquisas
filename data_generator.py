# data_generator.py

import random
from faker import Faker

NUM_REGISTROS = 10000
# Inicializa a biblioteca Faker para gerar dados realistas (nomes, cidades, etc.)
fake = Faker('pt_BR') 

def gerar_e_preparar_dados():
    """
    Gera a lista principal com 10.000 registros e prepara as três estruturas de dados.
    """
    lista_principal = []
    
    for i in range(1, NUM_REGISTROS + 1):
        # Gera um ID único e sequencial para a chave de busca
        registro = {
            'id': i, 
            'nome': fake.name(),
            'cidade': fake.city(),
            'valor': round(random.uniform(10.0, 1000.0), 2)
        }
        lista_principal.append(registro)

    # 1. Estrutura para Pesquisa Sequencial:
    # A lista_principal, sem ordenação.

    # 2. Estrutura para Pesquisa Indexada (Binária):
    # Cópia da lista ordenada pelo 'id' (requisito para a busca binária).
    lista_ordenada = sorted(lista_principal, key=lambda x: x['id'])
    
    # 3. Estrutura para Pesquisa por HashMap:
    # Dicionário Python, onde a chave é o 'id' e o valor é o registro (Complexidade O(1)).
    hash_map = {registro['id']: registro for registro in lista_principal}
    
    return lista_principal, lista_ordenada, hash_map

# Variáveis globais que serão importadas e usadas pelo Flask (backend)
LISTA_SEQUENCIAL, LISTA_BINARIA, HASH_MAP = gerar_e_preparar_dados()
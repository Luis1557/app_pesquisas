# app.py

from flask import Flask, jsonify, request, render_template
from data_generator import LISTA_SEQUENCIAL, LISTA_BINARIA, HASH_MAP, NUM_REGISTROS
import time

app = Flask(__name__)

# --- Funções de Pesquisa (Algoritmos) ---

def pesquisa_sequencial(lista, chave):
    """ Pesquisa Linear Simples (O(n)). """
    for registro in lista:
        if registro['id'] == chave:
            return registro
    return None

def pesquisa_binaria(lista, chave):
    """ Pesquisa Indexada/Binária (O(log n)). Requer lista ordenada. """
    baixo = 0
    alto = len(lista) - 1
    
    while baixo <= alto:
        meio = (baixo + alto) // 2
        registro_meio = lista[meio]
        
        if registro_meio['id'] == chave:
            return registro_meio
        elif registro_meio['id'] < chave:
            baixo = meio + 1
        else:
            alto = meio - 1
            
    return None

def pesquisa_hashmap(hash_map, chave):
    """ Pesquisa em Tabela Hash/Dicionário (O(1)). """
    return hash_map.get(chave)

# --- Rotas do Servidor (API) ---

@app.route('/')
def home():
    # Rota principal que carrega a interface (index.html)
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_all():
    """ Rota que executa as 3 pesquisas e mede o tempo. """
    try:
        data = request.get_json()
        chave_str = data.get('chave')
        
        try:
            chave_busca = int(chave_str)
        except ValueError:
            return jsonify({'error': 'A chave de busca deve ser um número inteiro.'}), 400
        
        if not (1 <= chave_busca <= NUM_REGISTROS):
            return jsonify({'error': f'ID fora do intervalo válido (1 a {NUM_REGISTROS}).'}), 400

        resultados = {}
        
        # Medição 1: Pesquisa Sequencial
        start = time.perf_counter()
        resultado_seq = pesquisa_sequencial(LISTA_SEQUENCIAL, chave_busca)
        tempo_seq = (time.perf_counter() - start) * 1000 # Tempo em ms
        resultados['sequencial'] = {'tempo': f'{tempo_seq:.6f} ms', 'registro': resultado_seq}

        # Medição 2: Pesquisa Indexada (Binária)
        start = time.perf_counter()
        resultado_bin = pesquisa_binaria(LISTA_BINARIA, chave_busca)
        tempo_bin = (time.perf_counter() - start) * 1000 
        resultados['indexada'] = {'tempo': f'{tempo_bin:.6f} ms', 'registro': resultado_bin}

        # Medição 3: Pesquisa por HashMap
        start = time.perf_counter()
        resultado_hash = pesquisa_hashmap(HASH_MAP, chave_busca)
        tempo_hash = (time.perf_counter() - start) * 1000
        resultados['hashmap'] = {'tempo': f'{tempo_hash:.6f} ms', 'registro': resultado_hash}
        
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    print(f"Dados gerados com sucesso: {NUM_REGISTROS} registros.")
    # Executa o servidor Flask
    app.run(debug=True)
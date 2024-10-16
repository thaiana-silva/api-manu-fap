import os
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

API_URL = os.getenv('API_URL', 'https://facilit.plataformatarget.com.br/rest/api/target/v1')
CLIENT_ID = os.getenv('CLIENT_ID', '3101').strip()

# Mock Data para testes locais
MOCK_DATA = {
    "uuid": "5c46b2ec-5c6c-477f-abab-eb2579aaecb9",
    "objetivos": [
        {"id": "obj-01", "nome": "Objetivo 01", "statusId": 1, "diretoria": 100}
    ],
    "projetos": [
        {"id": "proj-01", "nome": "Projeto 01", "objetivoId": "obj-01", "statusId": 1, "diretoria": 100}
    ],
    "status": [{"id": 1, "nome": "Atrasado", "cor": "#e84c3d"}],
    "diretorias": [
        {"id": 100, "nome": "Diretoria de Produto", "sigla": "DPO"},
        {"id": 101, "nome": "Diretoria Administrativa", "sigla": "DADM"}
    ]
}

app = Flask(__name__)

def is_authorized():
    """Verifica se o clientID está presente e é válido."""
    client_id = request.headers.get('ClientID') or request.headers.get('clientid')
    client_id = client_id.strip() if client_id else ""

    print(f"DEBUG: clientID recebido -> '{client_id}' (tipo: {type(client_id)})")
    print(f"DEBUG: clientID esperado -> '{CLIENT_ID}' (tipo: {type(CLIENT_ID)})")

    return client_id == CLIENT_ID

def get_mock_data(uuid):
    """Retorna o Mock Data se o UUID corresponder."""
    if uuid == MOCK_DATA["uuid"]:
        return MOCK_DATA
    return None

@app.route('/entity/<uuid>', methods=['GET', 'POST'])
def get_or_create_entity(uuid):
    """Endpoint que busca dados ou cria uma nova entidade."""
    if not is_authorized():
        return jsonify({"error": "Não autorizado. Verifique o clientID ou autenticação."}), 401

    if request.method == 'POST':
        data = request.get_json()
        print(f"DEBUG: Dados recebidos no POST -> {data}")
        return jsonify({"message": "Entidade criada com sucesso.", "data": data}), 201

    data = get_mock_data(uuid)
    if data:
        return jsonify(data), 200

    return jsonify({"error": "Entidade não encontrada."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    """Tratamento global para erro 405."""
    return jsonify({"error": "Método não permitido para esta URL. Use GET."}), 405

if __name__ == '__main__':
    app.run(debug=True)
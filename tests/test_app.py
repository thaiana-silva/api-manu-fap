import unittest
import json
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        """Configura o cliente de teste do Flask."""
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {
            'ClientID': '3101',
            'Content-Type': 'application/json'
        }

    def test_get_entity_valid_uuid(self):
        """Teste para GET com UUID válido."""
        response = self.app.get('/entity/5c46b2ec-5c6c-477f-abab-eb2579aaecb9', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("uuid", data)

    def test_get_entity_not_found(self):
        """Teste para GET com UUID inexistente."""
        response = self.app.get('/entity/00000000-0000-0000-0000-000000000000', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Entidade não encontrada.")

    def test_post_entity(self):
        """Teste para POST que cria uma nova entidade."""
        payload = {
            "nome": "Nova Entidade",
            "statusId": 1,
            "diretoria": 101
        }
        response = self.app.post(
            '/entity/5c46b2ec-5c6c-477f-abab-eb2579aaecb9',
            data=json.dumps(payload),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Entidade criada com sucesso.")
        self.assertEqual(data["data"]["nome"], "Nova Entidade")

    def test_method_not_allowed(self):
        """Teste para erro 405 Method Not Allowed."""
        response = self.app.put('/entity/5c46b2ec-5c6c-477f-abab-eb2579aaecb9', headers=self.headers)
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Método não permitido para esta URL. Use GET.")

if __name__ == '__main__':
    unittest.main()
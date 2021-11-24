from iserv_cli.auth import CliAuth
from iserv_cli.config import CliConfig
import requests
import json


class IdentityServerApi:
    def __init__(self):
        self.config = CliConfig()
        self.base_url = self.config.values.get('base_url')
        self.auth = CliAuth()

    def get_headers(self, form_encoded=False):
        content_type = 'x-www-form-urlencoded' if form_encoded else 'json'
        token = self.auth.get_token()
        headers = {
            'Content-Type': f'application/{content_type}',
            'Authorization': f'Bearer {token}'
        }

        return headers

    def get_clients(self):
        clients = requests.get(
            url=f'{self.base_url}/api/Client',
            headers=self.get_headers())
        return self.parse_response(clients)

    def get_roles(self):
        roles = requests.get(
            url=f'{self.base_url}/api/Role',
            headers=self.get_headers())
        return self.parse_response(roles)

    def get_scopes(self):
        scopes = requests.get(
            url=f'{self.base_url}/api/Scope',
            headers=self.get_headers())
        return self.parse_response(scopes)

    def post_clients(self, body: dict):
        clients = requests.post(
            url=f'{self.base_url}/api/Client',
            headers=self.get_headers(),
            json=body)
        return self.parse_response(clients)

    def post_roles(self, body: dict):
        roles = requests.post(
            url=f'{self.base_url}/api/Role',
            headers=self.get_headers(),
            json=body)
        return self.parse_response(roles)

    def post_scopes(self, body: dict):
        clients = requests.post(
            url=f'{self.base_url}/api/Scope',
            headers=self.get_headers(),
            json=body)
        return self.parse_response(clients)

    def put_clients(self, body: dict):
        clients = requests.put(
            f'{self.base_url}/api/Client',
            headers=self.get_headers(),
            json=body)
        return self.parse_response(clients)

    def put_roles(self, body: dict):
        roles = requests.put(
            url=f'{self.base_url}/api/Role',
            headers=self.get_headers(),
            json=body)
        return self.parse_response(roles)

    def put_scopes(self, body: dict):
        scopes = requests.put(
            url=f'{self.base_url}/api/Scope',
            headers=self.get_headers(),
            json=body)
        return self.parse_response(scopes)

    def get_client(self, name: str) -> dict:
        client = requests.get(
            url=f'{self.base_url}/api/Client/{name}',
            headers=self.get_headers())
        return self.parse_response(client)

    def get_role(self, name: str) -> dict:
        role = requests.get(
            url=f'{self.base_url}/api/Role/{name}',
            headers=self.get_headers())
        return self.parse_response(role)

    def get_scope(self, name: str) -> dict:
        scope = requests.get(
            url=f'{self.base_url}/api/Scope/{name}',
            headers=self.get_headers())
        return self.parse_response(scope)

    def delete_client(self, name: str) -> None:
        requests.delete(
            url=f'{self.base_url}/api/Client/{name}',
            headers=self.get_headers())

    def delete_role(self, name: str) -> None:
        requests.delete(
            url=f'{self.base_url}/api/Role/{name}',
            headers=self.get_headers())

    def delete_scope(self, name: str) -> None:
        requests.delete(
            url=f'{self.base_url}/api/Scope/{name}',
            headers=self.get_headers())

    def get_token(self, client: str, secret: str, scopes: list) -> dict:
        data = {
            'client_id': client,
            'client_secret': secret,
            'scope': ' '.join(scopes) if isinstance(scopes, list) else scopes,
            'grant_type': 'client_credentials'
        }

        response = requests.post(
            url=f'{self.base_url}/connect/token',
            headers=self.get_headers(form_encoded=True),
            data=data)
        print(response.status_code)

        return response.json()

    def parse_response(self, response) -> dict:
        try:
            content = json.loads(response.content)
            return content
        except:
            return response.content

from iserv_cli.api import IdentityServerApi
from iserv_cli.console import ConsoleDisplayCli
from iserv_cli.mapper import RequestMapper
from dotenv import load_dotenv
import json
import os
load_dotenv()

api_key = os.environ['ISERV_API_KEY']


class IdentityServerCli:
    def __init__(self, config_path):
        self.config_path = config_path
        config = self.load_config()
        self.api = IdentityServerApi(
            base_url=config.get('base_url'),
            api_key=api_key)
        self.mapper = RequestMapper()
        self.console = ConsoleDisplayCli()
        self.config = config

    def load_config(self):
        with open(f'{self.config_path}/iserv.json', 'r') as file:
            config = json.loads(file.read())
        return config

    def save_config(self, config):
        self.config = config
        with open(f'{self.config_path}/iserv.json', 'w') as file:
            file.write(json.dumps(config))

    def config_set_base_uri(self, uri):
        config = self.load_config()
        config['base_url'] = uri
        self.save_config(config=config)
        print('uri updated successfully')

    def config_get_base_uri(self):
        config = self.load_config()
        self.console.write(
            content=config.get('base_url'),
            output_type='text')

    def list_role(self, output):
        roles = self.api.get_roles()
        if len(roles) > 0:
            self.console.write(content=roles, output_type=output)
        else:
            self.console.write('No roles found', output_type='text')

    def list_client(self, output):
        clients = self.api.get_clients()
        if len(clients) > 0:
            self.console.write(content=clients, output_type=output)
        else:
            self.console.write('No clients found', output_type='text')

    def list_scope(self, output):
        scopes = self.api.get_scopes()
        if len(scopes) > 0:
            self.console.write(content=scopes, output_type=output)
        else:
            self.console.write('No scopes found', output_type='text')

    def get_client(self, name, output):
        client = self.api.get_client(name)
        if client is not None:
            self.console.write(content=[client], output_type=output)
        else:
            self.console.write(f'No client with the name {name} was found')

    def get_scope(self, name, output):
        scope = self.api.get_scope(name)
        if scope is not None:
            self.console.write(content=[scope], output_type=output)
        else:
            self.console.write(f'No scope with the name {name} was found')

    def get_role(self, name, output):
        role = self.api.get_role(name)
        if role is not None:
            self.console.write(content=[role], output_type=output)
        else:
            self.console.write(f'No role with the name {name} was found')

    def add_client(self, name, secret, grants, scopes, output):
        request = self.mapper.build_client(name, secret, scopes, grants)
        self.api.post_clients(request)
        client = self.api.get_client(name)

        if client is not None:
            self.console.write(content=[client], output_type=output)
        else:
            self.console.write(f'Failed to create client')

    def add_scope(self, name, claims, output):
        request = self.mapper.build_scope(name, claims)
        self.api.post_scopes(request)
        scope = self.api.get_scope(name)

        if scope is not None:
            self.console.write(content=[scope], output_type=output)
        else:
            self.console.write('Failed to create scope')

    def add_role(self, name, output):
        request = self.mapper.build_role(name)
        self.api.post_roles(request)
        role = self.api.get_role(name)

        if role is not None:
            self.console.write(content=[role], output_type=output)
        else:
            self.console.write('Failed to create role')

    def update_client(self, name, secret, grants, scopes, output):
        request = self.mapper.build_client(name, secret, scopes, grants)
        self.api.put_clients(request)
        client = self.api.get_client(name)

        if client is not None:
            self.console.write(content=[client], output_type=output)
        else:
            self.console.write(f'Failed to update client')

    def update_scope(self, name, claims, output):
        request = self.mapper.build_scope(name, claims)
        self.api.put_scopes(request)
        scope = self.api.get_scope(name)

        if scope is not None:
            self.console.write(content=[scope], output_type=output)
        else:
            self.console.write('Failed to update scope')

    def update_role(self, name, output):
        request = self.mapper.build_role(name)
        self.api.put_roles(request)
        role = self.api.get_role(name)

        if role is not None:
            self.console.write(content=[role], output_type=output)
        else:
            self.console.write('Failed to update role')

    def delete_client(self, name, output):
        self.api.delete_client(name)

    def delete_scope(self, name, output):
        self.api.delete_scope(name)

    def delete_role(self, name, output):
        self.api.delete_role(name)

    def token_client(self, client, secret, scopes, output):
        token = self.api.get_token(client, secret, scopes)
        self.console.write(content=[token], output_type=output)

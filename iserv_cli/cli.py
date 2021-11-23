from iserv_cli.api import IdentityServerApi
from iserv_cli.config import CliConfig
from iserv_cli.console import ConsoleDisplayCli
from iserv_cli.mapper import RequestMapper
from dotenv import load_dotenv
load_dotenv()


class IdentityServerCli:
    def __init__(self):
        self.config = CliConfig()
        self.api = IdentityServerApi()
        self.mapper = RequestMapper()
        self.console = ConsoleDisplayCli()

    def config_set_base_uri(self, uri: str) -> None:
        self.config.values['base_uri'] = uri
        self.config.save_config()
        print('uri updated successfully')

    def config_get_base_uri(self) -> None:
        base_uri = self.config.values.get('base_uri')
        self.console.write(
            content=base_uri,
            output_type='text')

    def list_role(self, output: str) -> None:
        roles = self.api.get_roles()
        if len(roles) > 0:
            self.console.write(content=roles, output_type=output)
        else:
            self.console.write('No roles found', output_type='text')

    def list_client(self, output) -> None:
        clients = self.api.get_clients()
        if len(clients) > 0:
            self.console.write(content=clients, output_type=output)
        else:
            self.console.write('No clients found', output_type='text')

    def list_scope(self, output) -> None:
        scopes = self.api.get_scopes()
        if len(scopes) > 0:
            self.console.write(content=scopes, output_type=output)
        else:
            self.console.write('No scopes found', output_type='text')

    def get_client(self, name, output) -> None:
        client = self.api.get_client(name)
        if client is not None:
            self.console.write(content=[client], output_type=output)
        else:
            self.console.write(f'No client with the name {name} was found')

    def get_scope(self, name, output) -> None:
        scope = self.api.get_scope(name)
        if scope is not None:
            self.console.write(content=[scope], output_type=output)
        else:
            self.console.write(f'No scope with the name {name} was found')

    def get_role(self, name, output) -> None:
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

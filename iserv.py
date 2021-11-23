from iserv_cli.cli import IdentityServerCli
from dotenv import load_dotenv
import argparse
import os
load_dotenv()

command_key = 'com'


class ParserBuiler:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.main = self.parser.add_subparsers(dest='base')
        self.cli = IdentityServerCli()

    def add_key(self, root, key):
        _root = root.copy()
        _root.append(key)
        return _root

    def to_dict(self, args):
        return args.__dict__

    def bind_argument(self, parser, argument: list, description: str, keys: list, required=True, **kwargs):
        key = '_'.join(keys) + f'__{argument[1]}'
        parser.add_argument(f'-{argument[0]}', f'--{argument[1]}',
                            type=str, required=required, help=description, dest=key, metavar='', **kwargs)

    def bind_output_type(self, parser, keys):
        choices = ['json',
                   'table',
                   'file-json',
                   'file-table',
                   'file-csv']

        self.bind_argument(parser=parser, argument=['o', 'output'],
                           description='output type', keys=keys, choices=choices, required=False, default='json')

    def get_subparser(self, root_key):
        return self.main.add_parser(name=root_key).add_subparsers(
            dest='_'.join([command_key, root_key]))

    def config_set_base_uri(self, root_key, config_parser):
        arg_key = 'set-base-uri'
        config_base_url_parser = config_parser.add_parser(arg_key)

        self.bind_argument(parser=config_base_url_parser, argument=['u', 'uri'],
                           description=f'server base uri', keys=[root_key, arg_key])

    def config_get_base_uri(self, config_parser):
        arg_key = 'get-base-uri'
        config_parser.add_parser(arg_key)

    def config_args(self):
        root_key = 'config'
        config_parser = self.get_subparser(root_key=root_key)

        self.config_set_base_uri(
            root_key=root_key,
            config_parser=config_parser)

        self.config_get_base_uri(
            config_parser=config_parser)

    def token_args(self):
        root_key = 'token'
        token_parser = self.get_subparser(root_key=root_key)

        self.token_client(
            parser=token_parser,
            root_key=root_key)

    def token_client(self, parser, root_key):
        arg_key = 'client'

        token_parser = parser.add_parser(arg_key)

        self.bind_argument(parser=token_parser, argument=[
            'c', 'client'], description='client id', keys=[root_key, arg_key])

        self.bind_argument(parser=token_parser, argument=[
            's', 'secret'], description='client secret', keys=[root_key, arg_key], required=False)

        self.bind_argument(parser=token_parser, argument=[
            'p', 'scopes'], description='allowed grants', keys=[root_key, arg_key], action='append', required=False)

        self.bind_output_type(parser=token_parser,
                              keys=[root_key, arg_key])

    def get_args(self):
        root_key = 'get'
        arg_keys = ['scope', 'client', 'role']

        get_parser = self.main.add_parser(name=root_key).add_subparsers(
            dest='_'.join([command_key, root_key]))

        for arg_key in arg_keys:
            arg_key_parser = get_parser.add_parser(arg_key)

            self.bind_argument(parser=arg_key_parser, argument=['n', 'name'],
                               description=f'{arg_key} name', keys=[root_key, arg_key])
            self.bind_output_type(parser=arg_key_parser,
                                  keys=[root_key, arg_key])

    def delete_args(self):
        root_key = 'delete'
        arg_keys = ['scope', 'client', 'role']

        delete_parser = self.main.add_parser(name=root_key).add_subparsers(
            dest='_'.join([command_key, root_key]))

        for arg_key in arg_keys:
            arg_key_parser = delete_parser.add_parser(arg_key)

            self.bind_argument(parser=arg_key_parser, argument=['n', 'name'],
                               description=f'{arg_key} name', keys=[root_key, arg_key])
            self.bind_output_type(parser=arg_key_parser,
                                  keys=[root_key, arg_key])

    def list_args(self):
        root_key = 'list'
        arg_keys = ['scope', 'client', 'role']

        list_parser = self.main.add_parser(name=root_key).add_subparsers(
            dest='_'.join([command_key, root_key]))

        for arg_key in arg_keys:
            arg_key_parser = list_parser.add_parser(arg_key)

            self.bind_output_type(parser=arg_key_parser,
                                  keys=[root_key, arg_key])

    def add_args(self):
        root_key = 'add'
        add_parser = self.main.add_parser(name=root_key).add_subparsers(
            dest='_'.join([command_key, root_key]))

        self.client_args(
            add_parser=add_parser,
            root_key=root_key)

        self.scope_args(
            add_parser=add_parser,
            root_key=root_key)

        self.role_args(
            add_parser=add_parser,
            root_key=root_key)

    def update_args(self):
        root_key = 'update'
        update_parser = self.main.add_parser(name=root_key).add_subparsers(
            dest='_'.join([command_key, root_key]))

        self.client_args(
            add_parser=update_parser,
            root_key=root_key)

        self.scope_args(
            add_parser=update_parser,
            root_key=root_key)

        self.role_args(
            add_parser=update_parser,
            root_key=root_key)

    def client_args(self, add_parser, root_key):
        arg_key = 'client'
        client_parser = add_parser.add_parser(arg_key)

        self.bind_argument(parser=client_parser, argument=[
            'n', 'name'], description='client id', keys=[root_key, arg_key])

        self.bind_argument(parser=client_parser, argument=[
            's', 'secret'], description='client secret', keys=[root_key, arg_key], required=False)

        self.bind_argument(parser=client_parser, argument=[
            'g', 'grants'], description='allowed grants', keys=[root_key, arg_key], action='append', required=False)

        self.bind_argument(parser=client_parser, argument=[
            'p', 'scopes'], description='allowed scopes', keys=[root_key, arg_key], action='append', required=False)

        self.bind_output_type(parser=client_parser,
                              keys=[root_key, arg_key])

    def scope_args(self, add_parser, root_key):
        arg_key = 'scope'
        scope_parser = add_parser.add_parser(arg_key)

        self.bind_argument(parser=scope_parser, argument=[
            'n', 'name'], description='scope name', keys=[root_key, arg_key])

        self.bind_argument(parser=scope_parser, argument=[
            'c', 'claims'], description='user claims', keys=[root_key, arg_key], action='append', required=False)

        self.bind_output_type(parser=scope_parser,
                              keys=[root_key, arg_key])

    def role_args(self, add_parser, root_key):
        arg_key = 'role'
        scope_parser = add_parser.add_parser(arg_key)

        self.bind_argument(parser=scope_parser, argument=[
            'n', 'name'], description='scope name', keys=[root_key, arg_key])

        self.bind_output_type(parser=scope_parser,
                              keys=[root_key, arg_key])

    def get_command_method(self, args):
        base_command = args.base
        base_command_key = '_'.join([command_key, base_command])
        base_command_method = self.to_dict(args).get(base_command_key)
        parameter_prefix = '_'.join([base_command, base_command_method])

        method_name = parameter_prefix
        if '-' in method_name:
            method_name = method_name.replace('-', '_')

        parameters = {
            'method': method_name,
            'parameters': {}
        }

        for param in self.to_dict(args):
            if param.startswith(parameter_prefix):
                key = param.split('__')[1]
                value = self.to_dict(args).get(param)
                parameters['parameters'].update({key: value})

        return parameters

    def execute_command(self, args):
        parameters = self.get_command_method(args)
        func = getattr(self.cli, parameters.get('method'))
        func(**parameters.get('parameters'))

    def parse(self):
        self.get_args()
        self.list_args()
        self.add_args()
        self.update_args()
        self.delete_args()
        self.config_args()
        self.token_args()

        self.execute_command(
            args=self.parser.parse_args())


parser = ParserBuiler()
parser.parse()

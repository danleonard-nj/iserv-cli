class RequestMapper:
    def __init__(self):
        pass

    def build_scope(self, name, user_claims=[], **kwargs):
        request = {
            'name': name,
        }

        if user_claims is not None and len(user_claims) > 0:
            request['userClaims'] = user_claims

        return request

    def build_client(self, client_id, client_secret, allowed_scopes, allowed_grants, **kwargs):
        request = {}

        if client_id is not None:
            request['clientId'] = client_id
        if client_secret is not None:
            request['clientSecrets'] = [{
                'value': client_secret
            }]
        if allowed_grants is not None:
            request['allowedGrantTypes'] = allowed_grants
        if allowed_scopes is not None:
            request['allowedScopes'] = allowed_scopes

        return request

    def build_role(self, name, **kwargs):
        request = {
            'name': name
        }

        request.update(kwargs)
        return request

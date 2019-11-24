from requests import exceptions, request


class GraphQLQuery:
    BASE_URL = "https://api.github.com/graphql"

    def __init__(self, token=None, query=None, params=None, additional_headers=None):
        self.token = token
        self.query = query
        self.params = params
        self.additional_headers = additional_headers or dict()

    @property
    def headers(self):
        return {**dict(Authorization=f"token {self.token}",), **self.additional_headers}

    def generator(self):
        while True:
            try:
                yield request(
                    "POST",
                    self.BASE_URL,
                    headers=self.headers,
                    json=dict(query=self.query.format_map(self.params)),
                ).json()
            except exceptions.HTTPError as http_err:
                raise http_err
            except Exception as err:
                raise err

    def iterator(self):
        pass

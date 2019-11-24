from requests import exceptions, request


class Client:
    BASE_URL = "https://git.sr.ht"

    def __init__(self, token=None, additional_headers=None):
        self.token = token
        self.additional_headers = additional_headers or dict()

    @property
    def headers(self):
        return {**dict(Authorization=f"token {self.token}",), **self.additional_headers}

    def post(self, endpoint, params):
        try:
            res = request(
                "POST",
                f"{self.BASE_URL}/{endpoint}",
                headers=self.headers,
                json=dict(params),
            )
        except exceptions.HTTPError as http_err:
            raise http_err
        except Exception as err:
            raise err

        return res.json()

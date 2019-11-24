from .graphql_query import GraphQLQuery


class RepositoryQuery(GraphQLQuery):
    # TODO: Handle errors
    REPO_QUERY = """
        query($after: String) {{
            viewer {{
                repositories(
                    first: 100,
                    after: $after,
                    isFork: false,
                    ownerAffiliations: OWNER,
                ) {{
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                    totalCount
                    nodes {{
                        id
                        name
                        description
                        isArchived
                        isDisabled
                        isPrivate
                        viewerCanAdminister
                        sshUrl
                    }}
                }}
            }}
        }}
        """
    PARAMS = dict(after="")

    def __init__(self, token):
        super().__init__(
            token=token, query=self.REPO_QUERY, params=self.PARAMS,
        )

    def iterator(self):
        generator = self.generator()
        has_next_page = True
        repos = []

        while has_next_page:
            res = next(generator)

            edges = res["data"]["viewer"]["repositories"]

            page_info = edges["pageInfo"]
            end_cursor = page_info["endCursor"]
            has_next_page = page_info["hasNextPage"]

            nodes = edges["nodes"]
            repos.extend(nodes)

            self.params = dict(after=end_cursor)

        return repos

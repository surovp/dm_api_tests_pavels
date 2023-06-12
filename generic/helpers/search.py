from dm_api_search import DmApiSearch
from dm_api_search.search_pb2 import SearchRequest


class Search:
    def init(self, target):
        self.grpc_search = DmApiSearch(target=target)

    def search(self, query: str, size: int, skip: int, search_across: list):
        response = self.grpc_search.search(
            request=SearchRequest(
                query=query,
                size=size,
                skip=skip,
                searchAcross=search_across
            )
        )
        return response

    def close(self):
        self.grpc_search.close()

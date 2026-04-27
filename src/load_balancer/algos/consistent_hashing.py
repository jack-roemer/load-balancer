import hashlib
import bisect

from load_balancer.algos.routing_strategy import RoutingStrategy
from load_balancer.core.request import Request
from load_balancer.servers.server import Server


""" 
implements Consistent Hashing, a strategy used to ensure that the same client (or request) always goes to the same server, 
even if the pool of servers changes slightly. 
"""
class ConsistentHashingStrategy(RoutingStrategy):

    def __init__(self, replicas: int = 100) -> None:

        self._number_of_replicas = replicas
        self._ring: dict[int, Server] = {}
        self._locations: list[int] = []
        self._server_ids: set[str] = set()


    def _hash(self, key: str) -> int:

        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
    

    def _build_ring(self, servers: list[Server]) -> None:

        self._ring = {}
        self._locations = []
        self._server_ids = {server.id for server in servers}

        for server in servers:
            for index in range(self._number_of_replicas):
                key = f"{server.id}:{index}"
                hashed_key = self._hash(key)
                self._ring[hashed_key] = server
                self._locations.append(hashed_key)

        self._locations.sort()


    def select_server(self, request: Request, servers: list[Server]) -> Server:

        if not servers:
            raise ValueError("No servers in server pool.")

        server_ids = {server.id for server in servers}

        if not self._ring or server_ids != self._server_ids:
            self._build_ring(servers)

        request_key = request.client_id if request.client_id else request.path

        request_hash = self._hash(request_key)

        # uses binary search to find the index of first location hash that is greater than or equal to the request hash
        index = bisect.bisect_left(self._locations, request_hash)

        if index == len(self._locations):
            index = 0

        return self._ring[self._locations[index]]
from load_balancer.algos.routing_strategy import RoutingStrategy
from load_balancer.servers.server import Server
from load_balancer.core.request import Request


# uses circular indexing to select servers in a round robin fashion
class RoundRobinStrategy(RoutingStrategy):

    def __init__(self):

        self._index = 0 # index of next server to select


    def select_server(self, request: Request, servers: list[Server]) -> Server:

        if not servers:
            raise ValueError("No servers in server pool.")
        
        server = servers[self._index % len(servers)]
        self._index += 1

        return server
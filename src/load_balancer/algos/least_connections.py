from load_balancer.algos.routing_strategy import RoutingStrategy
from load_balancer.servers.server import Server
from load_balancer.core.request import Request


class LeastConnectionsStrategy(RoutingStrategy):

    def select_server(self, request: Request, servers: list[Server]) -> Server:

        if not servers:
            raise ValueError("No servers in server pool.")
        
        # since server is a dataclass, we use min with a key function to find server with the least active connections
        return min(servers, key=lambda s: s.active_connections) 
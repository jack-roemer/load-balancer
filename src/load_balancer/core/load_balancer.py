from load_balancer.algos.routing_strategy import RoutingStrategy
from load_balancer.servers.server_pool import ServerPool
from load_balancer.core.request import Request
from load_balancer.servers.server import Server


class NoHealthyServersAvailableError(Exception):
    """Raised when no servers are available to handle a request."""
    pass


class LoadBalancer:

    def __init__(self, server_pool: ServerPool, routing_strategy: RoutingStrategy):

        self._server_pool = server_pool
        self._routing_strategy = routing_strategy


    def handle_request(self, request: Request) -> Server:

        healthy_servers = self._server_pool.get_healthy_servers()

        if not healthy_servers:
            raise NoHealthyServersAvailableError("No healthy servers available to handle the request.")
        
        return self._routing_strategy.select_server(request, healthy_servers)
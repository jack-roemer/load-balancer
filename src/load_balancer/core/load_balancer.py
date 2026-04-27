from load_balancer.algos.routing_strategy import RoutingStrategy
from load_balancer.observability.metrics import Metrics
from load_balancer.servers.server_pool import ServerPool
from load_balancer.core.request import Request
from load_balancer.servers.server import Server


class NoHealthyServersAvailableError(Exception):
    """Raised when no servers are available to handle a request."""
    pass


class LoadBalancer:

    def __init__(self, server_pool: ServerPool, routing_strategy: RoutingStrategy, metrics: Metrics | None = None):

        self._server_pool = server_pool
        self._routing_strategy = routing_strategy
        self._metrics = metrics if metrics is not None else Metrics()


    def handle_request(self, request: Request) -> Server:

        healthy_servers = self._server_pool.get_healthy_servers()

        if not healthy_servers:
            self._metrics.log_failed_request()
            raise NoHealthyServersAvailableError("No healthy servers available to handle the request.")
        
        server = self._routing_strategy.select_server(request, healthy_servers)
        self._metrics.log_request(server.id)

        return server
    

    def get_metrics(self) -> dict:
        health_count = len(self._server_pool.get_healthy_servers())
        return self._metrics.get_metrics(health_count)
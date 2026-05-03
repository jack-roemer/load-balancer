from load_balancer.algos.routing_strategy import RoutingStrategy
from load_balancer.observability.metrics import Metrics
from load_balancer.servers.server_pool import ServerPool
from load_balancer.core.request import Request
from load_balancer.servers.server import Server


class NoHealthyServersAvailableError(Exception):
    """Raised when no servers are available to handle a request."""
    pass


class LoadBalancer:

    def __init__(self, server_pool: ServerPool, routing_strategy: RoutingStrategy, metrics: Metrics | None = None, faliure_threshold: int = 3):

        self._server_pool = server_pool
        self._routing_strategy = routing_strategy
        self._metrics = metrics if metrics is not None else Metrics()
        self._faliure_threshold = faliure_threshold


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
    
    def record_server_failure(self, server_id: str) -> None:

        server = self._server_pool.get_server(server_id)
        server.record_failure()

        if server.failure_count >= self._failure_threshold:
            server.set_unhealthy()

    def record_server_success(self, server_id: str) -> None:
        server = self._server_pool.get_server(server_id)
        server.reset_failures()
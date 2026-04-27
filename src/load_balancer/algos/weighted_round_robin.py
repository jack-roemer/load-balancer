from load_balancer.algos.routing_strategy import RoutingStrategy
from load_balancer.core.request import Request
from load_balancer.servers.server import Server


class WeightedRoundRobinStrategy(RoutingStrategy):

    def __init__(self):

        self._current_index = 0
        self._weighted_servers: list[Server] = []


    def select_server(self, request: Request, servers: list[Server]) -> Server:

        if not servers:
            raise ValueError("No servers in server pool.")
        
        # ids are used instead of set() for comparison to avoid hash issues e.g. if server is not hashable, mutability when server.weight changes, etc...
        weighted_server_ids = {server.id for server in self._weighted_servers}
        server_ids = {server.id for server in servers}

        if not self._weighted_servers or weighted_server_ids != server_ids:

            self._weighted_servers = []

            for server in servers:

                if server.weight < 1:
                    raise ValueError(f"Server {server.id} has invalid weight {server.weight}. Weight must be >= 1.")
                
                # flattens the server list based on weights, e.g. 3 servers with weights 1, 2, 3, creates[s1, s2, s2, s3, s3, s3]
                self._weighted_servers.extend([server] * server.weight)

            self._current_index = 0

        if not self._weighted_servers:
            raise ValueError("No valid weighted servers available.")

        self._current_index = (self._current_index + 1) % len(self._weighted_servers)

        return self._weighted_servers[self._current_index - 1]
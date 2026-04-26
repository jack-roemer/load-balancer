from __future__ import annotations
from abc import ABC, abstractmethod
from load_balancer.servers.server import Server
from load_balancer.core.request import Request


# An abstract base class for routing strategies
class RoutingStrategy(ABC):
    @abstractmethod
    def select_server(self, request: Request, servers: list[Server]) -> Server:
        """Select a server from the list of servers based on the routing strategy."""
        raise NotImplementedError("Subclasses of RoutingStrategy must implement this method")
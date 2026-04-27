from __future__ import annotations
from typing import Iterable
from load_balancer.servers.server import Server


# A wrapper class to manage servers for load balancing
class ServerPool:


    def __init__(self, servers: Iterable[Server] | None = None):

        self._servers: dict[str, Server] = {}

        if servers:
            for server in servers:
                self.add_server(server)


    def add_server(self, server: Server) -> None:

        if server.id in self._servers:
            raise KeyError(f"Server with id {server.id} already exists in server pool.")
        
        self._servers[server.id] = server

    
    def remove_server(self, server_id: str) -> None:

        if server_id not in self._servers:
            raise KeyError(f"Server with id {server_id} does not exist in server pool.")
        
        del self._servers[server_id]


    def get_server(self, server_id: str) -> Server:

        if server_id not in self._servers:
            raise KeyError(f"Server with id {server_id} does not exist in server pool.")
        
        return self._servers[server_id]
    

    def get_servers(self) -> Iterable[Server]:

        return self._servers.values()
    

    def get_healthy_servers(self) -> Iterable[Server]:

        return [server for server in self._servers.values() if server.healthy]
    

    def set_server_health(self, server_id: str, health: bool) -> None:

        if server_id not in self._servers:
            raise KeyError(f"Server with id {server_id} does not exist in server pool.")
        
        self._servers[server_id].set_health(health)
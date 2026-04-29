from typing import Iterable

from load_balancer.servers.server import Server, ServerState


"""
    A wrapper class to manage servers for load balancing
"""
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
    
    
    # returns a static list of servers
    def get_servers(self) -> list[Server]:
        return list(self._servers.values())

    def get_healthy_servers(self) -> list[Server]:
        return [server for server in self._servers.values() if server.state == ServerState.HEALTHY]
    

    def set_server_state(self, server_id:str, state: ServerState):
        self.get_server(server_id).set_state(state)

    def set_server_healthy(self, server_id: str):
        self.get_server(server_id).set_healthy()
        
    def set_server_draining(self, server_id: str):
        self.get_server(server_id).set_draining()

    def set_server_unhealthy(self, server_id: str):
        self.get_server(server_id).set_unhealthy()



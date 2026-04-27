from dataclasses import dataclass


# A class representing a backend server in the load balancer
@dataclass
class Server:

    id: str
    host: str
    port: int
    weight: int = 1
    healthy: bool = True
    active_connections: int = 0
    avg_response_time: float = 0.0

    @property
    def get_address(self) -> str:
        return f"{self.host}:{self.port}"
    
    def add_active_connection(self) -> None:
        self.active_connections += 1

    def remove_active_connection(self) -> None:
        if self.active_connections > 0:
            self.active_connections -= 1
    
    def set_health(self, healthy: bool):
        self.healthy = healthy

    
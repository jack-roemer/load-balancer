from dataclasses import dataclass
from enum import Enum


class ServerState(str, Enum):
    
    HEALTHY = "healthy"
    DRAINING = "draining"
    UNHEALTHY = "unhealthy"


# A class representing a backend server in the load balancer
@dataclass
class Server:

    id: str
    host: str
    port: int
    weight: int = 1
    state: ServerState = ServerState.HEALTHY
    active_connections: int = 0
    avg_response_time: float = 0.0
    faliure_count: int = 0

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"
    

    #TODO: remove this method
    # adds backward compatibility for healthy property, but moving to state property
    @property
    def healthy(self) -> bool:
        return self.state == ServerState.HEALTHY
    

    def add_active_connection(self):
        self.active_connections += 1

    def remove_active_connection(self):
        if self.active_connections > 0:
            self.active_connections -= 1

    
    def record_failure(self) -> None:
        self.failure_count += 1

    def reset_failures(self) -> None:
        self.failure_count = 0


    def set_state(self, state: ServerState):
        self.state = state

    def set_healthy(self):
        self.state = ServerState.HEALTHY
    
    def set_draining(self):
        self.state = ServerState.DRAINING

    def set_unhealthy(self):
        self.state = ServerState.UNHEALTHY

    
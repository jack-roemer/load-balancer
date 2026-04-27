from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Metrics:

    '''
    requests_per_second: float = 0.0
    throughput: float = 0.0
    active_connections: int = 0
    health_status: dict[str, bool] = {}
    connections_per_server: dict[str, int] = {}
    avg_response_time_per_server: dict[str, float] = {}
    '''

    # TODO: why not add more metrics
    total_requests: int = 0
    failed_requests: int = 0
    requests_per_server: dict[str, int] = field(default_factory=dict)

    def log_request(self, server_id: str):

        self.total_requests += 1
        
        self.requests_per_server[server_id] = self.requests_per_server.get(server_id, 0) + 1


    def log_failed_request(self):
        self.failed_requests += 1


    def get_metrics(self, health_count: int) -> dict:
        return {
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "requests_per_server": dict(self.requests_per_server),
            "health_count": health_count
        }

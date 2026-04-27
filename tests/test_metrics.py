from load_balancer import (
    LoadBalancer,
    Metrics,
    Request,
    RoundRobinStrategy,
    Server,
    ServerPool,
    NoHealthyServersAvailableError,
)


def test_metrics_record_requests():

    metrics = Metrics()

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
    ])

    lb = LoadBalancer(server_pool, RoundRobinStrategy(), metrics=metrics)

    lb.handle_request(Request())
    lb.handle_request(Request())
    lb.handle_request(Request())

    snapshot = lb.get_metrics()

    assert snapshot["total_requests"] == 3
    assert snapshot["failed_requests"] == 0
    assert snapshot["health_count"] == 2
    assert snapshot["requests_per_server"]["s1"] >= 1
    assert snapshot["requests_per_server"]["s2"] >= 1


def test_metrics_record_failed_requests():
    
    metrics = Metrics()

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, healthy=False),
        Server(id="s2", host="localhost", port=8002, healthy=False),
    ])

    lb = LoadBalancer(server_pool, RoundRobinStrategy(), metrics=metrics)

    try:
        lb.handle_request(Request())
    except NoHealthyServersAvailableError:
        pass

    snapshot = lb.get_metrics()

    assert snapshot["total_requests"] == 0
    assert snapshot["failed_requests"] == 1
    assert snapshot["health_count"] == 0
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from load_balancer import LoadBalancer, Request, RoundRobinStrategy, Server, ServerPool, ServerState, NoHealthyServersAvailableError


app = FastAPI(title="Adaptive Load Balancder API")

server_pool = ServerPool([
    Server(id="s1", host="localhost", port=8001),
    Server(id="s2", host="localhost", port=8002),
])

load_balancer = LoadBalancer(server_pool, RoundRobinStrategy())


class CreateServer(BaseModel):

    id: str
    host: str
    port: int
    weight: int = 1

class UpdateServer(BaseModel):

    state: ServerState

class HandleRequest(BaseModel):

    client_id: str | None = None
    path: str = "/"
    headers: dict[str, str] = Field(default_factory=dict)


@app.get("/servers")
def list_servers():

    servers = server_pool.get_servers()

    return [

        {
            "id": server.id,
            "host": server.host,
            "port": server.port,
            "weight": server.weight,
            "state": server.state.value,
            "active_connections": server.active_connections,
            "avg_response_time": server.avg_response_time,
        }

        for server in servers

    ]

@app.post("/servers")
def create_server(server_data: CreateServer):

    try: 

        server_pool.add_server(Server(**server_data.model_dump()))
        return {"message": f"Server {server_data.id} created successfully."}
    
    except KeyError as e:

        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete("/servers/{server_id}")
def delete_server(server_id: str):

    try:

        server_pool.remove_server(server_id)
        return {"message": f"Server {server_id} removed successfully."}
    
    except KeyError as e:

        raise HTTPException(status_code=404, detail=str(e))
    
@app.patch("/servers/{server_id}/state")
def update_server_state(server_id: str, server_data: UpdateServer):

    try: 

        server_pool.set_server_state(server_id, server_data.state)
        return {"message": f"Server {server_id} state updated to {server_data.state.value}."}
    
    except KeyError as e:

        raise HTTPException(status_code=404, detail=str(e))
    
@app.post("/handle_request")
def handle_request(request_data: HandleRequest):

    try:

        request = Request(client_id=request_data.client_id, path=request_data.path, headers=request_data.headers)
        server = load_balancer.handle_request(request)

        return {
            "message": "Request handled successfully.",
            "server_id": server.id,
            "address": server.address,
            "state": server.state,
        }
    
    except NoHealthyServersAvailableError as e:

        raise HTTPException(status_code=503, detail=str(e))
    
@app.get("/metrics")
def get_metrics():

    return load_balancer.get_metrics()
    

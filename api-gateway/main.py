from fastapi import FastAPI, Request, HTTPException
import httpx
import os

#teste
app = FastAPI()

#URLs de cada microservicio
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
INVESTMENT_SERVICE_URL = os.getenv("INVESTMENT_SERVICE_URL", "http://localhost:8002")

@app.get("/")
def read_root():
    return {"message": "API Gateway esta funcionando"}

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(full_path: str, request: Request):
    service_url = ""

    if full_path.startswith("users"):
        service_url = AUTH_SERVICE_URL
    elif full_path.startswith("investments"):
        service_url = INVESTMENT_SERVICE_URL
    else:
        raise HTTPException(status_code=404, detail="Rota nao encontrada")
    
    url = f"{service_url}/{full_path}"
    headers = dict(request.headers)
    method = request.method

    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "Post":
            response = await client.post(url, headers=headers, data=await request.body())
        elif method == "PUT":
            response = await client.put(url, headers=headers, data=await request.body())
        elif method == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise HTTPException(status_code=405, detail="Metodo nao permitido")
        
    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from agent import create_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LangChain Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

agent_app = None

@app.on_event("startup")
async def startup():
    global agent_app
    agent_app = await create_agent()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received message: {request.message}")
        result = await agent_app.ainvoke({"messages": [("user", request.message)]})
        # LangGraph 返回消息列表，获取最后一条消息
        messages = result.get("messages", [])
        if messages:
            response_text = str(messages[-1].content)
        else:
            response_text = "No response"
        logger.info(f"Response: {response_text}")
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from pydantic import BaseModel

from retriever import retrieve
from llm import answer_question,stream_answer
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
    
class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={}
    )

@app.post("/chat")
async def chat(req: QueryRequest):

    hits = retrieve(req.query, limit=10)

    context_parts = []
    citations = []

    for hit in hits:
        p = hit.payload

        context_parts.append(
            f"{p['reference']}\n{p['text']}"
        )

        citations.append(
            {
                "reference": p["reference"],
                # "score": hit.score,
            }
        )

    context = "\n\n".join(context_parts)

    answer = answer_question(
        req.query,
        context,
    )

    return {
        "question": req.query,
        "answer": answer,
        # "references": citations,
    }


@app.post("/chat/stream")
async def chat_stream(req: QueryRequest):

    hits = retrieve(req.query, limit=10)

    context = []

    for hit in hits:
        p = hit.payload

        context.append(
            f"{p['reference']}\n{p['text']}"
        )

    def generate():
        yield from stream_answer(
            req.query,
            "\n\n".join(context)
        )

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
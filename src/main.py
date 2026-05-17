import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from duckduckgo_search import DDGS

app = FastAPI(title="Methuselah - Sovereign Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== MODEL MAPPING ======================
MODEL_MAP = {
    "qwen2.5": "qwen2.5:latest",
    "llama": "llama3.1:8b",
    "mistral": "mistral-nemo:12b",
    "gemma": "gemma2:9b"
}

class State:
    current_model = "qwen2.5:latest"

state = State()

async def perform_web_search(query: str):
    try:
        print(f"🔍 Searching for: {query[:100]}...")
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=4)
            
            context = ""
            sources = []
            for r in results:
                title = r.get('title', 'No Title')
                body = r.get('body', '')[:350]
                href = r.get('href', '')
                
                context += f"Source: {title}\nSnippet: {body}\n\n"
                sources.append(f"• {title} — {href}")
            
            return context.strip(), sources
    except Exception as e:
        print(f"Search error: {e}")
        return "Web search temporarily unavailable.", []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Methuselah Connected")

    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            while True:
                payload = await websocket.receive_json()
                msg_type = payload.get("type")

                # ==================== MODEL CHANGE ====================
                if msg_type == "MODEL_CHANGE":
                    short = payload.get("model_id")
                    if short in MODEL_MAP:
                        state.current_model = MODEL_MAP[short]
                        print(f"🔄 Model switched to {state.current_model}")
                        await websocket.send_json({
                            "type": "STATUS", 
                            "message": f"Model: {short.upper()}", 
                            "color": "#00ffff"
                        })

                # ==================== MAIN PROMPT ====================
                elif msg_type == "PROMPT":
                    user_text = payload.get("text", "").strip()
                    category = payload.get("category", "gen-know")
                    tool_mode = payload.get("tool_id", "general")

                    print("="*60)
                    print(f"DEBUG: tool_mode received = '{tool_mode}'")
                    print(f"DEBUG: user_text = '{user_text[:150]}...'")
                    print("="*60)

                    if not user_text:
                        continue

                    await websocket.send_json({"light": "light-thinking", "state": "on"})
                    await websocket.send_json({"light": "light-ready", "state": "off"})

                    web_context = ""
                    sources = []

                    if tool_mode == "web":
                        print("✅ Web mode activated - Running search")
                        await websocket.send_json({"light": "light-searching", "state": "on"})
                        web_context, sources = await perform_web_search(user_text)
                    else:
                        print(f"Tool mode is '{tool_mode}' - No search performed")

                    try:
                        system_msg = f"You are operating in {category.upper()} mode. Be precise, truthful and helpful."

                        if web_context:
                            # We tell the LLM exactly how to handle the data we found
                            system_msg = (
                                f"You are operating in {category.upper()} mode. "
                                "Use the following WEB SEARCH RESULTS to provide a fresh, updated answer. "
                                "If you use information from a source, mention it. "
                                "Scrub away any irrelevant noise.\n\n"
                                f"=== RECENT WEB INFORMATION ===\n{web_context}"
                            )

                        resp = await client.post(
                            "http://127.0.0.1:11434/api/chat",
                            json={
                                "model": state.current_model,
                                "messages": [
                                    {"role": "system", "content": system_msg},
                                    {"role": "user", "content": user_text}
                                ],
                                "stream": False
                            }
                        )

                        reply = resp.json()['message']['content']

                        if sources:
                            reply += "\n\n<span style='color:#00ffff'>SOURCES:</span>\n" + "\n".join(sources)

                        await websocket.send_json({"type": "RESPONSE", "text": reply})

                        await websocket.send_json({"light": "light-searching", "state": "off"})
                        await websocket.send_json({"light": "light-commit", "state": "on"})
                        await asyncio.sleep(2)
                        await websocket.send_json({"light": "light-commit", "state": "off"})
                        await websocket.send_json({"light": "light-ready", "state": "on"})

                    except Exception as e:
                        print(f"Error: {e}")
                        await websocket.send_json({"type": "STATUS", "message": f"Error: {str(e)}", "color": "#ff4444"})
                        await websocket.send_json({"light": "light-ready", "state": "on"})

        except WebSocketDisconnect:
            print("Client disconnected")
        except Exception as e:
            print(f"WebSocket Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Methuselah Sovereign Dashboard...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
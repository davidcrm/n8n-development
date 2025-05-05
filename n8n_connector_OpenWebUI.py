# Librerías necesarias
from typing import Optional, Callable, Awaitable
from pydantic import BaseModel, Field
import os
import time
import requests

# Función que extrae información (chat_id, message_id) de un event emitter
def extract_event_info(event_emitter) -> tuple[Optional[str], Optional[str]]:
    if not event_emitter or not event_emitter.__closure__:
        return None, None
    for cell in event_emitter.__closure__:
        if isinstance(request_info := cell.cell_contents, dict):
            chat_id = request_info.get("chat_id")
            message_id = request_info.get("message_id")
            return chat_id, message_id
    return None, None

# Clase principal Pipe que conecta con un workflow de n8n
class Pipe:
    # Clase interna Valves: define configuración de conexión a n8n
    class Valves(BaseModel):
        n8n_url: str = Field(default="https://n8n.[your domain].com/webhook/[your webhook URL]")
        n8n_bearer_token: str = Field(default="...")  # Token de autorización para n8n
        input_field: str = Field(default="chatInput")  # Campo de entrada esperado por n8n
        response_field: str = Field(default="output")  # Campo donde se recibirá la respuesta
        emit_interval: float = Field(default=2.0, description="Intervalo en segundos entre emisiones de estado")
        enable_status_indicator: bool = Field(default=True, description="Habilitar o deshabilitar emisiones de estado")

    def __init__(self):
        # Inicializa la instancia de Pipe
        self.type = "pipe"
        self.id = "n8n_pipe"
        self.name = "N8N Pipe"
        self.valves = self.Valves()  # Configuración por defecto
        self.last_emit_time = 0  # Última vez que se envió un estado
        pass

    # Método para emitir estados (información o errores) al exterior
    async def emit_status(
        self,
        __event_emitter__: Callable[[dict], Awaitable[None]],
        level: str,
        message: str,
        done: bool,
    ):
        current_time = time.time()
        # Solo emite si ha pasado suficiente tiempo o si ya se ha terminado
        if (
            __event_emitter__
            and self.valves.enable_status_indicator
            and (current_time - self.last_emit_time >= self.valves.emit_interval or done)
        ):
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "status": "complete" if done else "in_progress",
                        "level": level,
                        "description": message,
                        "done": done,
                    },
                }
            )
            self.last_emit_time = current_time

    # Método principal: conecta el cuerpo del mensaje con un workflow de n8n
    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
        __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Optional[dict]:
        # Emite estado: llamando al workflow de n8n
        await self.emit_status(__event_emitter__, "info", "/Calling N8N Workflow...", False)
        
        chat_id, _ = extract_event_info(__event_emitter__)
        messages = body.get("messages", [])

        # Verifica que exista al menos un mensaje
        if messages:
            question = messages[-1]["content"]
            try:
                # Construye la petición POST a n8n
                headers = {
                    "Authorization": f"Bearer {self.valves.n8n_bearer_token}",
                    "Content-Type": "application/json",
                }
                payload = {"sessionId": f"{chat_id}"}
                payload[self.valves.input_field] = question
                response = requests.post(
                    self.valves.n8n_url, json=payload, headers=headers
                )
                # Si respuesta es exitosa, extrae la respuesta de n8n
                if response.status_code == 200:
                    n8n_response = response.json()[self.valves.response_field]
                else:
                    raise Exception(f"Error: {response.status_code} - {response.text}")

                # Agrega la respuesta de n8n al cuerpo de mensajes como asistente
                body["messages"].append({"role": "assistant", "content": n8n_response})
            except Exception as e:
                # Emite error si falla la comunicación
                await self.emit_status(
                    __event_emitter__,
                    "error",
                    f"Error during sequence execution: {str(e)}",
                    True,
                )
                return {"error": str(e)}
        else:
            # Si no hay mensajes en la solicitud, informa al usuario
            await self.emit_status(
                __event_emitter__,
                "error",
                "No messages found in the request body",
                True,
            )
            body["messages"].append(
                {
                    "role": "assistant",
                    "content": "No messages found in the request body",
                }
            )

        # Emite estado de completado
        await self.emit_status(__event_emitter__, "info", "Complete", True)
        return n8n_response

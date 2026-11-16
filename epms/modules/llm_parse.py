from llama_cpp import Llama
from flask import jsonify
from werkzeug.utils import secure_filename
import os


WEIGHTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weights")
WEIGHTS_FILE = "Qwen2.5-7B-Instruct-Q3_K_M.gguf"
weight_path = os.path.join(WEIGHTS_FOLDER, secure_filename(WEIGHTS_FILE))

llm = Llama(
    model_path=weight_path,
    n_ctx=8192,
    n_threads=8,
    n_gpu_layers=0
)

SYSTEM_PROMPT = """You are an expert in electronic components.
You are given a datasheet (1 page at a time) for an electronic part.
Datasheets are ad-hoc, so your job is to extract most valuable part data for stock tracking system.
This data may include:
- Metrics ranges (e.g. voltage/current)
- Key specification
- Temperature ranges
If the datasheet does not include this information - only return what you could find.
You must only retrieve essential information, text only (no diagrams/tables)
Return as JSON only."""

def parse_datasheet(datasheet):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": datasheet}
    ]
    output = llm.create_chat_completion(
        messages,
        max_tokens=2048,
        temperature=0.0,   # deterministic extraction
        stop=["</s>"]
    )
    print(output["choices"][0]["message"]["content"])
    return jsonify({"result": output["choices"][0]["message"]["content"]})
"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import re
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


def post_json(url: str, headers: dict, body: dict) -> dict:
    """Gửi một yêu cầu JSON; lỗi mạng/API được bộ chạy ghi vào cột error."""
    request = urllib.request.Request(
        url, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        message = error.read().decode("utf-8", "replace")[:300]
        raise RuntimeError("Model API HTTP %s: %s" % (error.code, message)) from error


def _require_config() -> None:
    if not MODEL_NAME or not API_KEY:
        raise RuntimeError("Cần MODEL_NAME và API_KEY trong .env để gọi model thật")


def _call_openai(system: str, user: str, url: str = "https://api.openai.com/v1/chat/completions",
                 extra: dict = None) -> dict:
    """Gọi API dạng OpenAI chat completions (OpenAI, OpenRouter)."""
    _require_config()
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages, **(extra or {})})
    if "error" in data:
        raise RuntimeError("Model API lỗi: %s" % str(data["error"])[:300])
    usage = data["usage"]
    content = data["choices"][0]["message"]["content"]
    if not isinstance(content, str):
        raise RuntimeError("Model không trả nội dung dạng chữ")
    return {"text": content, "model": data.get("model") or MODEL_NAME,
            "tokens_in": usage["prompt_tokens"], "tokens_out": usage["completion_tokens"]}


def _call_gemini(system: str, user: str) -> dict:
    _require_config()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", MODEL_NAME):
        raise ValueError("MODEL_NAME Gemini không hợp lệ")
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"responseMimeType": "application/json"}}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(
        "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL_NAME,
        {"x-goog-api-key": API_KEY}, body)
    candidate = data["candidates"][0]
    content = "".join(part.get("text", "") for part in candidate["content"]["parts"])
    if not content:
        raise RuntimeError("Gemini không trả nội dung dạng chữ")
    usage = data["usageMetadata"]
    tokens_in = usage["promptTokenCount"]
    tokens_out = (usage["totalTokenCount"] - tokens_in if "totalTokenCount" in usage
                  else usage["candidatesTokenCount"] + usage.get("thoughtsTokenCount", 0))
    return {"text": content, "model": data.get("modelVersion") or MODEL_NAME,
            "tokens_in": tokens_in, "tokens_out": tokens_out}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER == "openai":
        return _call_openai(system, user)
    if MODEL_PROVIDER == "openrouter":
        # OpenRouter dùng chung định dạng OpenAI; ép JSON vì agent.py đọc JSON decision/answer/citations.
        return _call_openai(system, user, "https://openrouter.ai/api/v1/chat/completions",
                            {"response_format": {"type": "json_object"}})
    if MODEL_PROVIDER == "gemini":
        return _call_gemini(system, user)
    raise NotImplementedError(
        "MODEL_PROVIDER=%s chưa được hỗ trợ; dùng openrouter, openai hoặc gemini — xem docs/connect-model.md"
        % MODEL_PROVIDER)

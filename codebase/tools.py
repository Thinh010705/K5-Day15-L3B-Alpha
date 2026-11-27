"""Công cụ chỉ đọc cho bản thử LessonLens CP2."""
import json
import os
import re
import unicodedata
from tracing import tool

LESSON_ID = "ai-co-ban-mau"
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "lesson_sample.json")
STOP = {"la", "gi", "the", "nao", "cho", "toi", "ve", "trong", "bai", "nay", "mot", "co", "khong", "duoc", "hay", "va", "cua", "nhung", "noi", "dung", "khai", "niem", "giai", "thich", "vi", "sao"}


def _terms(value: str) -> set:
    plain = unicodedata.normalize("NFD", value.lower())
    plain = "".join(c for c in plain if unicodedata.category(c) != "Mn").replace("đ", "d")
    return {x for x in re.findall(r"[a-z0-9]+", plain) if x not in STOP and len(x) > 1}


def _passages() -> list:
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    if data.get("lesson_id") != LESSON_ID:
        raise ValueError("Mã bài học trong dữ liệu không khớp")
    return data["passages"]


@tool
def search_lesson(query: str, lesson_id: str = LESSON_ID) -> list:
    """search_lesson · Input: câu hỏi và mã bài · Output: tối đa 3 đoạn {code,text,score}; không tác động ra ngoài."""
    if lesson_id != LESSON_ID:
        return []
    terms = _terms(query)
    if not terms:
        return []
    ranked = []
    for passage in _passages():
        score = len(terms & _terms(passage["title"] + " " + passage["text"] + " " + " ".join(passage["keywords"])))
        if score >= 2 or (len(terms) == 1 and score == 1 and len(next(iter(terms))) >= 5):
            ranked.append({"code": passage["code"], "text": passage["text"], "score": score})
    return sorted(ranked, key=lambda p: (-p["score"], p["code"]))[:3]


@tool
def get_passage(passage_id: str) -> dict:
    """get_passage · Input: mã đoạn · Output: đoạn {code,title,text} hoặc dict rỗng; không tác động ra ngoài."""
    return next(({"code": p["code"], "title": p["title"], "text": p["text"]}
                 for p in _passages() if p["code"] == passage_id), {})

from .chroma_db import build_retriever
from functools import partial

retriever_map = {
    "chroma_1": partial(build_retriever, k=1),
    "chroma_2": partial(build_retriever, k=2),
    "chroma_3": partial(build_retriever, k=3)
}
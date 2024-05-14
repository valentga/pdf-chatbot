from pathlib import Path
import sys
path_root = Path(__file__).parents[3]
sys.path.append(str(path_root))
import os 
from langchain.vectorstores.chroma import Chroma
#from app.chat.embeddings.openai import embeddings
from app.chat.embeddings.huggingface_embeddings import hf_embeddings
import time

vector_store = Chroma(
    persist_directory='/Users/gvalentino/embeddings',
    embedding_function=hf_embeddings
)

def build_retriever(chat_args, k):
    search_kwargs = {
        "filter": { "pdf_id": chat_args.pdf_id },
        "k": k
    }
    # MAGIC PRINT STATMENT: DELETE AT YOUR OWN RISK 
    print(chat_args)
    # time.sleep(20)
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
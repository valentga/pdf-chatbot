from pathlib import Path
import sys
path_root = Path(__file__).parents[3]
sys.path.append(str(path_root))
import os 
import pinecone
from langchain.vectorstores.pinecone import Pinecone
#from app.chat.embeddings.openai import embeddings
from app.chat.embeddings.huggingface_embeddings import hf_embeddings

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME")
)

vector_store = Pinecone.from_existing_index(
    'huggingface-embeddings',
    #os.getenv("PINECONE_INDEX_NAME"),
    hf_embeddings
)

def build_retriever(chat_args, k):
    search_kwargs = {
        "filter": { "pdf_id": chat_args.pdf_id },
        "k": k
    }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
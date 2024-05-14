from langchain.embeddings import HuggingFaceEmbeddings

model_path = '/Users/gvalentino/multilingual-e5-small'
#hf_embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-small')

hf_embeddings = HuggingFaceEmbeddings(model_name=model_path)
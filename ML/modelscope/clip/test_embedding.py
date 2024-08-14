# docs
import sys, os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

# Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")


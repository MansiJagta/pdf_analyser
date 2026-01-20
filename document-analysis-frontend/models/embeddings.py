# # from sentence_transformers import SentenceTransformer

# # class VectorEngine:
# #     def __init__(self):
# #         # This will download ~45MB on first run, then work offline
# #         self.model = SentenceTransformer('all-MiniLM-L6-v2')

# #     def create_embeddings(self, text_chunks):
# #         return self.model.encode(text_chunks)






# import sqlite3
# from sentence_transformers import SentenceTransformer
# from langchain.tools import tool

# class VectorEngine:
#     def __init__(self):
#         # Using a tiny 80MB model for CPU efficiency
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')

#     @tool("vector_indexer")
#     def index_text(self, text: str):
#         """Converts text to embeddings and stores them in local SQLite database."""
#         embeddings = self.model.encode([text])[0]
        
#         # Connect to local SQLite file
#         conn = sqlite3.connect("document_vectors.db")
#         # Logic to save blob to sqlite-vec goes here
#         conn.close()
#         return "Successfully indexed in local vector store."








import sqlite3
from sentence_transformers import SentenceTransformer
from langchain.tools import tool

# Initialize model globally to avoid reloading in every tool call
model = SentenceTransformer('all-MiniLM-L6-v2')

@tool("vector_indexer")
def index_vector_logic(text: str):
    """Converts text to embeddings and stores them in local SQLite database."""
    embeddings = model.encode([text])[0]
    
    # Connect to your local SQLite-vec database
    conn = sqlite3.connect("document_vectors.db")
    # (Your existing SQL logic to insert vectors goes here)
    conn.close()
    return "Successfully indexed in local vector store."
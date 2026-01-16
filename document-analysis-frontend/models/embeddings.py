from sentence_transformers import SentenceTransformer

class VectorEngine:
    def __init__(self):
        # This will download ~45MB on first run, then work offline
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def create_embeddings(self, text_chunks):
        return self.model.encode(text_chunks)
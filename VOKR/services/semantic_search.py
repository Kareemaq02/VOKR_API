import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticSearch:
    def __init__(self, manual_file):
        self.manual_file = manual_file
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self._load_manual()

    def _load_manual(self):
        with open(self.manual_file, 'r') as f:
            manual = json.load(f)
        self.documents = [item['content'] for item in manual['manual']]
        document_embeddings = self.model.encode(self.documents)
        dimension = document_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(document_embeddings))

    def search_manual(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), top_k)
        
        if distances[0][0] == float('inf') or distances[0][0] > 1.0:
            return "No relevant information found in the manual. Please check your query or contact support."
        
        combined_results = " ".join(self.documents[idx] for idx in indices[0])
        return combined_results

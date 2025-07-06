import json
import os
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEndpoint

class RAGPipeline:
    def __init__(self, qa_path: str, embedding_model: str = 'all-MiniLM-L6-v2'):
        self.qa_path = qa_path
        self.embedding_model = SentenceTransformer(embedding_model)
        self.questions, self.answers = self._load_qa()
        self.embeddings = self.embedding_model.encode(self.questions, show_progress_bar=False)
        self.index = self._build_faiss_index(self.embeddings)

    def _load_qa(self) -> Tuple[List[str], List[str]]:
        with open(self.qa_path, 'r') as f:
            data = json.load(f)
        questions = [item['question'] for item in data]
        answers = [item['answer'] for item in data]
        return questions, answers

    def _build_faiss_index(self, embeddings: np.ndarray):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings).astype('float32'))
        return index

    def retrieve(self, query: str, k: int = 3) -> List[Tuple[str, str, float]]:
        query_emb = self.embedding_model.encode([query])
        D, I = self.index.search(np.array(query_emb).astype('float32'), k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            results.append((self.questions[idx], self.answers[idx], dist))
        return results

# Example usage (for testing only):
if __name__ == "__main__":
    rag = RAGPipeline(qa_path=os.path.join(os.path.dirname(__file__), '../data/math_qa.json'))
    results = rag.retrieve("How do you add 7 and 5?", k=2)
    for q, a, d in results:
        print(f"Q: {q}\nA: {a}\nDist: {d}\n---") 
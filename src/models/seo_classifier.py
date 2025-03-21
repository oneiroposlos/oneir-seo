import logging.config
from dataclasses import dataclass

import torch
from transformers import AutoModel, AutoTokenizer

from src.config import *

logger = logging.getLogger(__name__)


@dataclass
class SeoClassifier:
    BASE_DIR = os.path.join(DATA_DIR, 'seo')
    BASE_MODEL_NAME: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    # EMBEDDING_DIMS depends on the model, change it accordingly
    NDIM: int = EMBEDDING_DIMS
    BASE_MODEL_PATH: str = os.path.join(DATA_DIR, 'models/mood_classifier')
    model = AutoModel.from_pretrained(BASE_MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)

    def __post_init__(self):
        pass

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def process(self):
        pass

    def train(self):
        pass

    def evaluate(self):
        pass

    def predict(self, sentences):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        return sentence_embeddings

    def load(self, model_path=BASE_MODEL_PATH):
        self.model = AutoModel.from_pretrained(model_path)
        logger.info(f"Loaded model from {model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        logger.info(f"Loaded tokenizer {model_path}")

    def save(self, model_path):
        self.model.save_pretrained(model_path)
        self.tokenizer.save_pretrained(model_path)


if __name__ == '__main__':
    embedder = SeoClassifier()
    # embedder.save(embedder.BASE_MODEL_PATH)
    sents = ['This is an example sentence', 'Each sentence is converted']
    embeddings = embedder.predict(sents)
    print("Sentence embeddings:")
    print(embeddings)

    sentence1 = 'This is an example sentence'
    sentence2 = 'Cách kiếm được tiền online'
    embeddings1 = embedder.predict([sentence1])
    embeddings2 = embedder.predict([sentence2])
    cosine_similarities = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
    cosine_similarities(embeddings1, embeddings2).item()
    print("Similarity score:", cosine_similarities(embeddings1, embeddings2).item())

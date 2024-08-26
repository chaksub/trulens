from openai import AzureOpenAI
from src.new_impl.embedding.embedding.config import api_version, endpoint
from src.new_impl.embedding.embedding.utils import create_embeddings
from opensearchpy import OpenSearch
import os

class AzureEmbeddingClient:
    def __init__(self, azure_token, opensearch_host, opensearch_port, opensearch_index):
        self.client = AzureOpenAI(
            azure_deployment='text-embedding-ada-002',
            api_version=api_version,
            azure_endpoint=endpoint,
            azure_ad_token=azure_token,
        )
        self.opensearch = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': opensearch_port}]
        )
        self.index = opensearch_index

    def create_embeddings(self, text):
        # Use the create_embeddings function from utils.py
        embeddings = create_embeddings(self, text)
        self.save_embeddings(text, embeddings)
        return embeddings

    def save_embeddings(self, text, embeddings):
        document = {
            'text': text,
            'embeddings': embeddings
        }
        response = self.opensearch.index(
            index=self.index,
            body=document
        )
        return response

    def check_index_exists(self):
        return self.opensearch.indices.exists(index=self.index)


def create_azure_client(token, opensearch_host, opensearch_port, opensearch_index):
    """
    Creates and returns an instance of AzureEmbeddingClient.

    Args:
        token (str): The Azure authentication token.
        opensearch_host (str): The OpenSearch host.
        opensearch_port (int): The OpenSearch port.
        opensearch_index (str): The OpenSearch index.

    Returns:
        AzureEmbeddingClient: An instance of AzureEmbeddingClient.
    """
    return AzureEmbeddingClient(token, opensearch_host, opensearch_port, opensearch_index)


# Example usage
if __name__ == "__main__":
    azure_token = os.getenv("AZURE_TOKEN")
    if not azure_token:
        raise ValueError("AZURE_TOKEN environment variable is not set")

    opensearch_host = "localhost"
    opensearch_port = 9200
    opensearch_index = "embeddings"

    client = create_azure_client(azure_token, opensearch_host, opensearch_port, opensearch_index)
    if client.check_index_exists():
        print(f"Index '{opensearch_index}' exists.")
    else:
        print(f"Index '{opensearch_index}' does not exist.")
from src.new_impl.embedding.embedding.client import AzureEmbeddingClient, create_azure_client
from src.new_impl.embedding.embedding.auth import get_azure_token


def main():
    azure_token = get_azure_token()
    opensearch_host = 'localhost'  # Replace with your OpenSearch host
    opensearch_port = 9200  # Replace with your OpenSearch port
    opensearch_index = 'embeddings'  # Replace with your OpenSearch index
    client = create_azure_client(azure_token, opensearch_host, opensearch_port, opensearch_index)
    text = input("Your text here")
    embedding = client.create_embeddings(text)
    print(embedding)

if __name__ == "__main__":
    main()
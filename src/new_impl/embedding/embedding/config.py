import os

# Configuration for Azure OpenAI
api_version = "2023-05-15"
endpoint = "https://beat-sandbox-openai-00001.openai.azure.com/"

# Load Azure token from environment variable
AZURE_TOKEN = os.getenv('AZURE_TOKEN', 'your_default_token_here')

# Sample texts for testing
TEXTS = [
    "Enter text for UW info",
    "Enter text for WSU info",
    "Enter text for Seattle info",
    "Enter text for Starbucks info"
]
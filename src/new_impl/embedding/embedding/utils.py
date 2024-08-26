def create_embeddings(self, text):
        try:
            response = self.client.embeddings.create(
                input=[text],
                model="text-embedding-ada-002"
            )
            embeddings = response.data[0].embedding 
            print(f"Created embedding for text: {text[:30]}...")  # Log the text and embedding creation
            return embeddings
        except Exception as e:
            print(f"Error creating embedding for text: {text[:30]}... Error: {e}")
            raise
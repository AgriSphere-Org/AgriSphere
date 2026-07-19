from services.rag_service import RAGService

rag = RAGService()

print("Loading PDFs...")
rag.create_vector_store()
print("Vector database created successfully!")
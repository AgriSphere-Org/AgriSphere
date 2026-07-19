import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


class RAGService:
    """
    Handles:
    - Loading PDFs
    - Splitting documents
    - Creating FAISS vector database
    - Loading FAISS database
    - Retrieving relevant chunks
    """

    def __init__(self):

        # backend/
        self.base_dir = Path(__file__).resolve().parent.parent

        # backend/rag/documents
        self.documents_path = self.base_dir / "rag" / "documents"

        # backend/rag/vector_store
        self.vector_db_path = self.base_dir / "rag" / "vector_store"

        # Create folders automatically if they don't exist
        self.documents_path.mkdir(parents=True, exist_ok=True)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)

        # Local embedding model (No API Required)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_db = None

    # -----------------------------------------------------

    def load_documents(self):

        documents = []

        pdf_files = list(self.documents_path.glob("*.pdf"))

        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF files found in:\n{self.documents_path}"
            )

        for pdf in pdf_files:
            print(f"Reading: {pdf.name}")
            loader = PyPDFLoader(str(pdf))
            documents.extend(loader.load())

        return documents

    # -----------------------------------------------------

    def split_documents(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

        return splitter.split_documents(documents)

    # -----------------------------------------------------

    def create_vector_store(self):

        print("Loading PDFs...")

        documents = self.load_documents()

        print(f"Loaded {len(documents)} pages.")

        print("Splitting documents...")

        chunks = self.split_documents(documents)

        print(f"Created {len(chunks)} chunks.")

        print("Generating embeddings...")
        print("The first run may take a few minutes because the model will be downloaded.")

        self.vector_db = FAISS.from_documents(
            chunks,
            self.embeddings
        )

        print("Saving vector database...")

        self.vector_db.save_local(str(self.vector_db_path))

        print("Vector database created successfully!")

    # -----------------------------------------------------

    def load_vector_store(self):

        self.vector_db = FAISS.load_local(
            str(self.vector_db_path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    # -----------------------------------------------------

    def retrieve(self, question, k=4):

        if self.vector_db is None:
            self.load_vector_store()

        return self.vector_db.similarity_search(
            question,
            k=k
        )
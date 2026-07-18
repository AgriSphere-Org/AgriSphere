import os

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv

load_dotenv()


class RAGService:

    """
    Handles document loading,
    embeddings,
    vector database creation
    and document retrieval.
    """

    def __init__(self):

        self.documents_path = "rag/documents"

        self.vector_db_path = "rag/vector_store"

        self.embeddings = GoogleGenerativeAIEmbeddings(

            model="models/embedding-001",

            google_api_key=os.getenv("GEMINI_API_KEY")

        )

        self.vector_db = None

    # -----------------------------------------------------

    def load_documents(self):

        documents = []

        for file in os.listdir(self.documents_path):

            if file.endswith(".pdf"):

                loader = PyPDFLoader(

                    os.path.join(

                        self.documents_path,

                        file

                    )

                )

                documents.extend(

                    loader.load()

                )

        return documents

    # -----------------------------------------------------

    def split_documents(

        self,

        documents

    ):

        splitter = RecursiveCharacterTextSplitter(

            chunk_size=800,

            chunk_overlap=150

        )

        return splitter.split_documents(

            documents

        )

    # -----------------------------------------------------

    def create_vector_store(self):

        documents = self.load_documents()

        chunks = self.split_documents(

            documents

        )

        self.vector_db = FAISS.from_documents(

            chunks,

            self.embeddings

        )

        self.vector_db.save_local(

            self.vector_db_path

        )

    # -----------------------------------------------------

    def load_vector_store(self):

        self.vector_db = FAISS.load_local(

            self.vector_db_path,

            self.embeddings,

            allow_dangerous_deserialization=True

        )

    # -----------------------------------------------------

    def retrieve(

        self,

        question,

        k=4

    ):

        if self.vector_db is None:

            self.load_vector_store()

        return self.vector_db.similarity_search(

            question,

            k=k

        )
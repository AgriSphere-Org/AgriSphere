import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


class RAGService:
    """
    Agricultural Retrieval-Augmented Generation Service.

    Responsibilities:
    - Load agricultural documents
    - Split documents into meaningful chunks
    - Preserve document and page metadata
    - Create and load FAISS vector database
    - Retrieve relevant agricultural evidence
    - Provide similarity information for evidence evaluation
    """

    def __init__(self):

        # =================================================
        # PATHS
        # =================================================

        self.base_dir = (
            Path(__file__).resolve().parent.parent
        )

        self.documents_path = (
            self.base_dir
            / "rag"
            / "documents"
        )

        self.vector_db_path = (
            self.base_dir
            / "rag"
            / "vector_store"
        )

        self.documents_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.vector_db_path.mkdir(
            parents=True,
            exist_ok=True
        )

        # =================================================
        # EMBEDDINGS
        # =================================================

        self.embeddings = HuggingFaceEmbeddings(
            model_name=(
                "sentence-transformers/"
                "all-MiniLM-L6-v2"
            )
        )

        self.vector_db = None

    # =====================================================
    # LOAD DOCUMENTS
    # =====================================================

    def load_documents(self):

        documents = []

        pdf_files = sorted(
            self.documents_path.glob("*.pdf")
        )

        if not pdf_files:

            raise FileNotFoundError(
                "No agricultural PDF documents were found in: "
                f"{self.documents_path}"
            )

        for pdf in pdf_files:

            print(
                f"Reading agricultural document: "
                f"{pdf.name}"
            )

            try:

                loader = PyPDFLoader(
                    str(pdf)
                )

                pdf_documents = (
                    loader.load()
                )

            except Exception as e:

                print(
                    f"Unable to read {pdf.name}: "
                    f"{e}"
                )

                continue

            # ---------------------------------------------
            # Document metadata
            # ---------------------------------------------

            for document in pdf_documents:

                document.metadata[
                    "document_name"
                ] = pdf.name

                document.metadata[
                    "source"
                ] = pdf.name

                document.metadata[
                    "domain"
                ] = "agriculture"

                document.metadata[
                    "file_type"
                ] = "pdf"

                # PyPDFLoader normally provides page.
                # Keep it if available.

                if "page" not in document.metadata:

                    document.metadata[
                        "page"
                    ] = None

            documents.extend(
                pdf_documents
            )

        if not documents:

            raise ValueError(
                "Agricultural documents were found, "
                "but no readable pages could be loaded."
            )

        return documents

    # =====================================================
    # SPLIT DOCUMENTS
    # =====================================================

    def split_documents(
        self,
        documents
    ):

        splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=1000,

                chunk_overlap=200,

                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    "? ",
                    "! ",
                    ", ",
                    " ",
                    ""
                ]
            )
        )

        chunks = (
            splitter.split_documents(
                documents
            )
        )

        # ---------------------------------------------
        # Add stable chunk metadata
        # ---------------------------------------------

        for index, chunk in enumerate(
            chunks
        ):

            chunk.metadata[
                "chunk_id"
            ] = index

            if not chunk.metadata.get(
                "domain"
            ):

                chunk.metadata[
                    "domain"
                ] = "agriculture"

        return chunks

    # =====================================================
    # CREATE VECTOR STORE
    # =====================================================

    def create_vector_store(self):

        print(
            "\nLoading agricultural PDFs..."
        )

        documents = (
            self.load_documents()
        )

        print(
            f"Loaded {len(documents)} pages."
        )

        print(
            "\nSplitting documents..."
        )

        chunks = (
            self.split_documents(
                documents
            )
        )

        print(
            f"Created {len(chunks)} chunks."
        )

        if not chunks:

            raise ValueError(
                "No document chunks were created."
            )

        print(
            "\nGenerating embeddings..."
        )

        self.vector_db = (
            FAISS.from_documents(
                chunks,
                self.embeddings
            )
        )

        print(
            "\nSaving FAISS vector database..."
        )

        self.vector_db.save_local(
            str(self.vector_db_path)
        )

        print(
            "\nAgricultural vector database "
            "created successfully."
        )

        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "vector_store": str(
                self.vector_db_path
            )
        }

    # =====================================================
    # LOAD VECTOR STORE
    # =====================================================

    def load_vector_store(self):

        index_file = (
            self.vector_db_path
            / "index.faiss"
        )

        metadata_file = (
            self.vector_db_path
            / "index.pkl"
        )

        if not index_file.exists() or not metadata_file.exists():

            raise FileNotFoundError(
                "Agricultural vector store does not exist. "
                "Create it using create_vector_store() "
                "before asking knowledge questions."
            )

        try:

            self.vector_db = (
                FAISS.load_local(

                    str(
                        self.vector_db_path
                    ),

                    self.embeddings,

                    allow_dangerous_deserialization=True
                )
            )

        except Exception as e:

            self.vector_db = None

            raise RuntimeError(
                "Unable to load the agricultural "
                f"vector database: {e}"
            )

        return self.vector_db

    # =====================================================
    # ENSURE VECTOR STORE
    # =====================================================

    def _ensure_vector_store(self):

        if self.vector_db is not None:

            return

        self.load_vector_store()

    # =====================================================
    # RETRIEVE
    # =====================================================

    def retrieve(
        self,
        question: str,
        k: int = 6
    ) -> List[Any]:
        """
        Retrieve relevant agricultural documents.

        Uses MMR so the returned evidence contains
        both relevance and diversity.
        """

        if not question or not question.strip():

            return []

        self._ensure_vector_store()

        k = max(
            1,
            min(k, 10)
        )

        fetch_k = max(
            20,
            k * 4
        )

        documents = (
            self.vector_db
            .max_marginal_relevance_search(

                question.strip(),

                k=k,

                fetch_k=fetch_k,

                lambda_mult=0.7
            )
        )

        return documents

    # =====================================================
    # RETRIEVE WITH SCORES
    # =====================================================

    def retrieve_with_scores(
        self,
        question: str,
        k: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Retrieve agricultural evidence together with
        similarity scores.

        Lower FAISS distance generally means a closer
        semantic match.

        This is useful for the Knowledge Agent when
        deciding whether retrieved evidence is actually
        relevant enough to support an answer.
        """

        if not question or not question.strip():

            return []

        self._ensure_vector_store()

        k = max(
            1,
            min(k, 10)
        )

        results = (
            self.vector_db
            .similarity_search_with_score(

                question.strip(),

                k=k
            )
        )

        evidence = []

        for document, score in results:

            evidence.append({

                "document": document,

                "score": float(score),

                "metadata":
                    dict(
                        document.metadata
                    )

            })

        return evidence

    # =====================================================
    # RETRIEVE RELEVANT EVIDENCE
    # =====================================================

    def retrieve_relevant_evidence(
        self,
        question: str,
        k: int = 6,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve evidence that can be evaluated by the
        Knowledge Agent.

        If score_threshold is provided, only results
        within that FAISS distance are retained.

        If no threshold is provided, all retrieved
        results are returned.
        """

        results = (
            self.retrieve_with_scores(
                question=question,
                k=k
            )
        )

        if score_threshold is None:

            return results

        return [

            result

            for result in results

            if result["score"]
            <= score_threshold

        ]

    # =====================================================
    # FORMAT EVIDENCE
    # =====================================================

    def format_evidence(
        self,
        documents: List[Any]
    ) -> List[Dict[str, Any]]:
        """
        Convert LangChain documents into a clean structure
        that the Knowledge Agent can use.
        """

        evidence = []

        for document in documents:

            metadata = (
                dict(
                    getattr(
                        document,
                        "metadata",
                        {}
                    )
                )
            )

            content = (
                getattr(
                    document,
                    "page_content",
                    ""
                )
                or ""
            ).strip()

            if not content:

                continue

            evidence.append({

                "content":
                    content,

                "source":
                    metadata.get(
                        "document_name",
                        metadata.get(
                            "source",
                            "Agricultural knowledge base"
                        )
                    ),

                "page":
                    metadata.get(
                        "page"
                    ),

                "chunk_id":
                    metadata.get(
                        "chunk_id"
                    ),

                "domain":
                    metadata.get(
                        "domain",
                        "agriculture"
                    )

            })

        return evidence

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        question: str,
        k: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Simple high-level search method.

        Returns formatted agricultural evidence.
        """

        documents = self.retrieve(
            question=question,
            k=k
        )

        return self.format_evidence(
            documents
        )
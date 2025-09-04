"""
RAG Vector Store Implementation
Handles vector database operations using FAISS and Pinecone
"""

import os
import json
import pickle
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.base import VectorStore
import pinecone
from pinecone import Pinecone, ServerlessSpec

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGVectorStore:
    """Vector store implementation for RAG system"""
    
    def __init__(self, 
                 embedding_model: str = "all-MiniLM-L6-v2",
                 vector_store_type: str = "faiss",
                 pinecone_api_key: Optional[str] = None,
                 pinecone_environment: Optional[str] = None):
        
        self.embedding_model = embedding_model
        self.vector_store_type = vector_store_type
        self.vector_store = None
        self.embeddings = None
        
        # Initialize embeddings
        self._initialize_embeddings()
        
        # Initialize vector store
        if vector_store_type == "faiss":
            self._initialize_faiss()
        elif vector_store_type == "pinecone":
            self._initialize_pinecone(pinecone_api_key, pinecone_environment)
        else:
            raise ValueError(f"Unsupported vector store type: {vector_store_type}")
    
    def _initialize_embeddings(self):
        """Initialize Hugging Face embeddings"""
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info(f"Initialized embeddings with model: {self.embedding_model}")
        except Exception as e:
            logger.error(f"Error initializing embeddings: {e}")
            raise
    
    def _initialize_faiss(self):
        """Initialize FAISS vector store"""
        try:
            # Create empty FAISS index
            self.vector_store = FAISS.from_texts(
                texts=["Initial document"],
                embedding=self.embeddings
            )
            # Remove the initial document
            self.vector_store.delete([0])
            logger.info("Initialized FAISS vector store")
        except Exception as e:
            logger.error(f"Error initializing FAISS: {e}")
            raise
    
    def _initialize_pinecone(self, api_key: Optional[str], environment: Optional[str]):
        """Initialize Pinecone vector store"""
        try:
            if not api_key:
                api_key = os.getenv("PINECONE_API_KEY")
            if not environment:
                environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
            
            if not api_key:
                raise ValueError("Pinecone API key not provided")
            
            # Initialize Pinecone
            pc = Pinecone(api_key=api_key)
            
            # Create or get index
            index_name = "techymart-rag"
            if index_name not in [index.name for index in pc.list_indexes()]:
                pc.create_index(
                    name=index_name,
                    dimension=384,  # all-MiniLM-L6-v2 dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=environment
                    )
                )
            
            self.pinecone_index = pc.Index(index_name)
            logger.info(f"Initialized Pinecone vector store with index: {index_name}")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vector store"""
        try:
            if not documents:
                logger.warning("No documents to add")
                return False
            
            if self.vector_store_type == "faiss":
                return self._add_documents_faiss(documents)
            elif self.vector_store_type == "pinecone":
                return self._add_documents_pinecone(documents)
            else:
                raise ValueError(f"Unsupported vector store type: {self.vector_store_type}")
                
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def _add_documents_faiss(self, documents: List[Document]) -> bool:
        """Add documents to FAISS vector store"""
        try:
            # Extract texts and metadata
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # Add to FAISS
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            
            logger.info(f"Added {len(documents)} documents to FAISS vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to FAISS: {e}")
            return False
    
    def _add_documents_pinecone(self, documents: List[Document]) -> bool:
        """Add documents to Pinecone vector store"""
        try:
            # Generate embeddings
            texts = [doc.page_content for doc in documents]
            embeddings = self.embeddings.embed_documents(texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                vector = {
                    'id': f"doc_{i}",
                    'values': embedding,
                    'metadata': {
                        **doc.metadata,
                        'text': doc.page_content[:1000]  # Truncate for metadata
                    }
                }
                vectors.append(vector)
            
            # Upsert to Pinecone
            self.pinecone_index.upsert(vectors=vectors)
            
            logger.info(f"Added {len(documents)} documents to Pinecone vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to Pinecone: {e}")
            return False
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 4, 
                         score_threshold: float = 0.0) -> List[Tuple[Document, float]]:
        """Perform similarity search"""
        try:
            if self.vector_store_type == "faiss":
                return self._similarity_search_faiss(query, k, score_threshold)
            elif self.vector_store_type == "pinecone":
                return self._similarity_search_pinecone(query, k, score_threshold)
            else:
                raise ValueError(f"Unsupported vector store type: {self.vector_store_type}")
                
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def _similarity_search_faiss(self, query: str, k: int, score_threshold: float) -> List[Tuple[Document, float]]:
        """Perform similarity search using FAISS"""
        try:
            # Search for similar documents
            docs_and_scores = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Filter by score threshold
            filtered_results = [
                (doc, score) for doc, score in docs_and_scores 
                if score >= score_threshold
            ]
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error in FAISS similarity search: {e}")
            return []
    
    def _similarity_search_pinecone(self, query: str, k: int, score_threshold: float) -> List[Tuple[Document, float]]:
        """Perform similarity search using Pinecone"""
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search Pinecone
            search_results = self.pinecone_index.query(
                vector=query_embedding,
                top_k=k,
                include_metadata=True
            )
            
            # Convert to Document objects
            results = []
            for match in search_results.matches:
                if match.score >= score_threshold:
                    doc = Document(
                        page_content=match.metadata.get('text', ''),
                        metadata={k: v for k, v in match.metadata.items() if k != 'text'}
                    )
                    results.append((doc, match.score))
            
            return results
            
        except Exception as e:
            logger.error(f"Error in Pinecone similarity search: {e}")
            return []
    
    def get_document_by_id(self, doc_id: str) -> Optional[Document]:
        """Get a specific document by ID"""
        try:
            if self.vector_store_type == "faiss":
                # FAISS doesn't support direct ID lookup, would need custom implementation
                logger.warning("Document ID lookup not supported in FAISS")
                return None
            elif self.vector_store_type == "pinecone":
                result = self.pinecone_index.fetch(ids=[doc_id])
                if doc_id in result.vectors:
                    vector_data = result.vectors[doc_id]
                    doc = Document(
                        page_content=vector_data.metadata.get('text', ''),
                        metadata={k: v for k, v in vector_data.metadata.items() if k != 'text'}
                    )
                    return doc
            return None
            
        except Exception as e:
            logger.error(f"Error getting document by ID: {e}")
            return None
    
    def save_vector_store(self, path: str) -> bool:
        """Save vector store to disk"""
        try:
            if self.vector_store_type == "faiss":
                self.vector_store.save_local(path)
                logger.info(f"Saved FAISS vector store to {path}")
                return True
            elif self.vector_store_type == "pinecone":
                # Pinecone is cloud-based, no local saving needed
                logger.info("Pinecone vector store is cloud-based, no local saving needed")
                return True
            else:
                logger.error(f"Unsupported vector store type for saving: {self.vector_store_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
            return False
    
    def load_vector_store(self, path: str) -> bool:
        """Load vector store from disk"""
        try:
            if self.vector_store_type == "faiss":
                self.vector_store = FAISS.load_local(path, self.embeddings)
                logger.info(f"Loaded FAISS vector store from {path}")
                return True
            elif self.vector_store_type == "pinecone":
                # Pinecone is cloud-based, no local loading needed
                logger.info("Pinecone vector store is cloud-based, no local loading needed")
                return True
            else:
                logger.error(f"Unsupported vector store type for loading: {self.vector_store_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            if self.vector_store_type == "faiss":
                return {
                    "type": "faiss",
                    "total_documents": self.vector_store.index.ntotal,
                    "embedding_dimension": self.vector_store.index.d,
                    "model": self.embedding_model
                }
            elif self.vector_store_type == "pinecone":
                stats = self.pinecone_index.describe_index_stats()
                return {
                    "type": "pinecone",
                    "total_documents": stats.total_vector_count,
                    "embedding_dimension": stats.dimension,
                    "model": self.embedding_model
                }
            else:
                return {"error": f"Unsupported vector store type: {self.vector_store_type}"}
                
        except Exception as e:
            logger.error(f"Error getting vector store stats: {e}")
            return {"error": str(e)}

# Global vector store instance
rag_vector_store = RAGVectorStore()

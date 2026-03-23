"""
RAG Pipeline Module

Implements Retrieval-Augmented Generation pipeline using embeddings and ChromaDB.
"""

import pandas as pd
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

try:
    from ai.vector_store import VectorStore, create_student_documents
except ImportError:
    from vector_store import VectorStore, create_student_documents


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for student data."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG pipeline.
        
        Args:
            model_name: Name of sentence transformer model
        """
        try:
            self.embedding_model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Warning: Could not load embedding model: {str(e)}")
            self.embedding_model = None
        
        self.vector_store = VectorStore()
        self.student_data = None
    
    def index_student_data(self, df: pd.DataFrame) -> bool:
        """
        Index student data for retrieval.
        
        Args:
            df: Student data DataFrame
            
        Returns:
            True if successful
        """
        try:
            self.student_data = df
            
            # Create collection
            if not self.vector_store.create_collection("student_records"):
                return False
            
            # Convert to documents
            documents, ids, metadatas = create_student_documents(df)
            
            # Add to vector store
            return self.vector_store.add_documents(documents, ids, metadatas)
        except Exception as e:
            print(f"Error indexing data: {str(e)}")
            return False
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User query
            top_k: Number of results to retrieve
            
        Returns:
            List of relevant documents
        """
        try:
            results = self.vector_store.search(query, n_results=top_k)
            return results['documents']
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def retrieve_context_with_metadata(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant context with metadata.
        
        Args:
            query: User query
            top_k: Number of results to retrieve
            
        Returns:
            List of documents with metadata
        """
        try:
            results = self.vector_store.search(query, n_results=top_k)
            
            combined = []
            for doc, meta in zip(results['documents'], results['metadatas']):
                combined.append({
                    'document': doc,
                    'metadata': meta
                })
            
            return combined
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def answer_query(self, query: str, llm_response: str) -> Dict:
        """
        Prepare context for LLM to answer query.
        
        Args:
            query: User query
            llm_response: Response from LLM
            
        Returns:
            Dictionary with query, context, and response
        """
        context = self.retrieve_context(query, top_k=5)
        context_str = "\n---\n".join(context)
        
        return {
            'query': query,
            'context': context_str,
            'response': llm_response,
            'context_count': len(context)
        }


def perform_rag_retrieval(student_df: pd.DataFrame, query: str, top_k: int = 5) -> Dict:
    """
    Perform RAG retrieval on student data.
    
    Args:
        student_df: Student data DataFrame
        query: User query
        top_k: Number of results
        
    Returns:
        Dictionary with retrieval results
    """
    pipeline = RAGPipeline()
    
    # Index data
    if not pipeline.index_student_data(student_df):
        return {'error': 'Failed to index data'}
    
    # Retrieve context
    results = pipeline.retrieve_context_with_metadata(query, top_k)
    
    return {
        'query': query,
        'results': results,
        'count': len(results)
    }

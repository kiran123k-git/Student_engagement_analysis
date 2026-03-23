"""
Vector Store Module

Manages ChromaDB vector database for storing and retrieving student records.
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
from typing import List, Dict


class VectorStore:
    """Manages ChromaDB vector storage for student data."""
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        """
        Initialize ChromaDB vector store.
        
        Args:
            persist_dir: Directory for persisting vector database
        """
        try:
            settings = Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=persist_dir,
                anonymized_telemetry=False
            )
            self.client = chromadb.Client(settings)
        except:
            # Fallback for newer chromadb versions
            self.client = chromadb.PersistentClient(path=persist_dir)
        
        self.collection = None
    
    def create_collection(self, name: str = "student_records") -> bool:
        """
        Create or get collection.
        
        Args:
            name: Collection name
            
        Returns:
            True if successful
        """
        try:
            # Delete existing collection if it exists
            try:
                self.client.delete_collection(name=name)
            except:
                pass
            
            self.collection = self.client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )
            return True
        except Exception as e:
            print(f"Error creating collection: {str(e)}")
            return False
    
    def add_documents(self, documents: List[str], ids: List[str], metadatas: List[Dict] = None) -> bool:
        """
        Add documents to vector store.
        
        Args:
            documents: List of text documents
            ids: List of unique document IDs
            metadatas: Optional metadata for each document
            
        Returns:
            True if successful
        """
        try:
            if metadatas is None:
                metadatas = [{}] * len(documents)
            
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            return True
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False
    
    def search(self, query: str, n_results: int = 5) -> Dict:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Dictionary with search results
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'ids': results['ids'][0] if results['ids'] else [],
                'distances': results['distances'][0] if results['distances'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else []
            }
        except Exception as e:
            print(f"Error searching: {str(e)}")
            return {'documents': [], 'ids': [], 'distances': [], 'metadatas': []}
    
    def clear(self) -> bool:
        """Clear all documents from collection."""
        try:
            if self.collection:
                # Reset collection
                self.client.delete_collection(name=self.collection.name)
                self.collection = self.client.create_collection(
                    name=self.collection.name,
                    metadata={"hnsw:space": "cosine"}
                )
            return True
        except Exception as e:
            print(f"Error clearing collection: {str(e)}")
            return False


def create_student_documents(df: pd.DataFrame) -> tuple:
    """
    Convert student records to text documents for embedding.
    
    Args:
        df: Student data DataFrame
        
    Returns:
        Tuple of (documents, ids, metadatas)
    """
    documents = []
    ids = []
    metadatas = []
    
    for idx, row in df.iterrows():
        # Create text representation of student
        doc = f"""
Student: {row.get('name', 'Unknown')}
Student ID: {row.get('student_id', 'N/A')}
Attendance: {row.get('attendance', 0):.1f}%
LMS Activity: {row.get('lms_logins', 0)} logins
Assignments: {row.get('assignments_submitted', 0)}/{row.get('total_assignments', 0)}
Engagement Score: {row.get('engagement_score', 0):.1f}/100
Engagement Level: {row.get('engagement_level', 'N/A')}
Risk Level: {row.get('risk_level', 'N/A')}
Wellbeing Status: {row.get('wellbeing_status', 'N/A')}
"""
        documents.append(doc.strip())
        ids.append(f"student_{row.get('student_id', idx)}")
        
        metadatas.append({
            'student_id': str(row.get('student_id', '')),
            'name': str(row.get('name', '')),
            'engagement_score': float(row.get('engagement_score', 0)),
            'risk_level': str(row.get('risk_level', ''))
        })
    
    return documents, ids, metadatas

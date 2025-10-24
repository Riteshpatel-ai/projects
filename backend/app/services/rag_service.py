"""
RAG (Retrieval-Augmented Generation) Query Service
Using FAISS for vector similarity search
"""
from openai import OpenAI
from app.core.config import settings
import faiss
import numpy as np
import json
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.db.models import EmailRecord
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class RAGQueryService:
    """RAG-based natural language query service for emails"""
    
    def __init__(self):
        self.index = None
        self.email_ids = []
        self.dimension = 1536  # OpenAI embedding dimension
        self.index_built = False
        self.last_rebuild = None
        self._embedding_cache = {}  # Cache embeddings to reduce API calls
    
    async def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for text using OpenAI with caching
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        # Check cache first
        cache_key = hash(text)
        if cache_key in self._embedding_cache:
            return self._embedding_cache[cache_key]
        
        try:
            response = client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=text
            )
            embedding = response.data[0].embedding
            
            # Cache the result
            self._embedding_cache[cache_key] = embedding
            return embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            return [0.0] * self.dimension
    
    async def build_index(self, db: Session, force_rebuild: bool = False):
        """
        Build FAISS index from email records with caching
        
        Args:
            db: Database session
            force_rebuild: Force rebuild even if index exists
        """
        # Skip if already built and not forcing rebuild
        if self.index_built and not force_rebuild:
            logger.info("Index already built, skipping rebuild")
            return
        
        try:
            emails = db.query(EmailRecord).filter(
                EmailRecord.is_deleted == False
            ).all()
            
            if not emails:
                logger.warning("No emails found to index")
                self.index_built = False
                return
            
            # Create embeddings for all emails
            embeddings = []
            self.email_ids = []
            
            logger.info(f"Building index for {len(emails)} emails...")
            
            for i, email in enumerate(emails):
                # Combine subject and summary for better context
                text = f"{email.subject} {email.summary or ''} {email.category or ''}"
                embedding = await self.create_embedding(text)
                embeddings.append(embedding)
                self.email_ids.append(email.id)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(emails)} emails")
            
            # Build FAISS index
            embeddings_array = np.array(embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(embeddings_array)
            
            self.index_built = True
            self.last_rebuild = datetime.now()
            
            logger.info(f"✅ Built FAISS index with {len(emails)} emails")
            
        except Exception as e:
            logger.error(f"Error building index: {str(e)}")
            self.index_built = False
    
    async def parse_natural_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into structured filters using GPT
        
        Args:
            query: Natural language query from user
            
        Returns:
            Dictionary with filters and search parameters
        """
        try:
            prompt = f"""
Parse this natural language query about hospital emails into structured filters.

Query: "{query}"

Extract the following information and return as JSON:
{{
    "categories": [list of relevant categories from: "Doctor / Patient Communication", "Diagnostic Results", "Insurance Claims", "Billing / Payment", "Appointment Confirmation", "Official Notice", "Medical Report"],
    "priority": "high" or "medium" or "low" or null,
    "time_range": {{
        "start_date": "YYYY-MM-DD" or null,
        "end_date": "YYYY-MM-DD" or null,
        "relative": "today" or "this week" or "last 3 days" or null
    }},
    "keywords": [list of important keywords to search],
    "entities": {{
        "patient_name": null or "<name>",
        "doctor_name": null or "<name>",
        "department": null or "<department>"
    }},
    "status": "unread" or "pending" or "processed" or null
}}

Today's date is {datetime.now().strftime('%Y-%m-%d')}.
"""
            
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a query parser. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Parsed query: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing query: {str(e)}")
            return {"keywords": [query]}
    
    async def semantic_search(self, query: str, k: int = 10) -> List[str]:
        """
        Perform semantic search using FAISS
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of email IDs
        """
        if not self.index:
            logger.warning("Index not built yet")
            return []
        
        try:
            # Create query embedding
            query_embedding = await self.create_embedding(query)
            query_vector = np.array([query_embedding]).astype('float32')
            
            # Search
            distances, indices = self.index.search(query_vector, k)
            
            # Return email IDs
            return [self.email_ids[idx] for idx in indices[0] if idx < len(self.email_ids)]
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []
    
    async def query_emails(self, query: str, db: Session) -> List[EmailRecord]:
        """
        Query emails using natural language
        
        Args:
            query: Natural language query
            db: Database session
            
        Returns:
            List of matching email records
        """
        try:
            # Build index if not already built
            if not self.index_built:
                await self.build_index(db)
            
            # Parse query into structured filters
            filters = await self.parse_natural_query(query)
            
            # Start with base query
            db_query = db.query(EmailRecord).filter(EmailRecord.is_deleted == False)
            
            # Apply category filter
            if filters.get('categories'):
                db_query = db_query.filter(EmailRecord.category.in_(filters['categories']))
            
            # Apply priority filter
            if filters.get('priority'):
                db_query = db_query.filter(EmailRecord.priority == filters['priority'])
            
            # Apply time range filter
            time_range = filters.get('time_range', {})
            if time_range.get('relative'):
                if time_range['relative'] == 'today':
                    start_date = datetime.now().replace(hour=0, minute=0, second=0)
                    db_query = db_query.filter(EmailRecord.timestamp >= start_date)
                elif 'week' in time_range['relative']:
                    start_date = datetime.now() - timedelta(days=7)
                    db_query = db_query.filter(EmailRecord.timestamp >= start_date)
                elif 'days' in time_range['relative']:
                    days = int(''.join(filter(str.isdigit, time_range['relative'])))
                    start_date = datetime.now() - timedelta(days=days)
                    db_query = db_query.filter(EmailRecord.timestamp >= start_date)
            
            # Apply status filter
            if filters.get('status'):
                db_query = db_query.filter(EmailRecord.status == filters['status'])
            
            # Apply entity filters
            entities = filters.get('entities', {})
            if entities.get('department'):
                db_query = db_query.filter(
                    EmailRecord.entities['department'].astext.contains(entities['department'])
                )
            
            # Perform semantic search if we have keywords
            if filters.get('keywords'):
                keyword_query = ' '.join(filters['keywords'])
                similar_ids = await self.semantic_search(keyword_query, k=50)
                if similar_ids:
                    db_query = db_query.filter(EmailRecord.id.in_(similar_ids))
            
            # Order by timestamp descending
            results = db_query.order_by(EmailRecord.timestamp.desc()).limit(100).all()
            
            logger.info(f"Query returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error querying emails: {str(e)}")
            return []


# Global RAG service instance
rag_service = RAGQueryService()

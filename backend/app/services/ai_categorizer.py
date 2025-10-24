"""
AI-powered Email Categorization Service
"""
from openai import OpenAI
from app.core.config import settings
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class EmailCategorizer:
    """AI-powered email categorization using GPT-4"""
    
    CATEGORIES = [
        "Doctor / Patient Communication",
        "Diagnostic Results",
        "Insurance Claims",
        "Billing / Payment",
        "Appointment Confirmation",
        "Official Notice",
        "Medical Report",
        "Prescription",
        "Lab Results",
        "Other"
    ]
    
    PRIORITY_LEVELS = ["high", "medium", "low"]
    
    @staticmethod
    def create_categorization_prompt(email_data: Dict[str, Any]) -> str:
        """
        Create prompt for email categorization
        
        Args:
            email_data: Dictionary containing email subject, sender, and content
            
        Returns:
            str: Formatted prompt for GPT-4
        """
        return f"""
You are an AI assistant specialized in categorizing hospital emails. Analyze the following email and provide a structured response.

Email Details:
- Sender: {email_data.get('sender', 'Unknown')}
- Subject: {email_data.get('subject', 'No Subject')}
- Content Preview: {email_data.get('content', '')[:1000]}

Your task:
1. Categorize this email into ONE of these categories: {', '.join(EmailCategorizer.CATEGORIES)}
2. Determine priority level: high, medium, or low
3. Extract a concise summary (2-3 sentences)
4. Identify key entities (patient names, doctor names, departments, amounts, dates, diagnosis, etc.)

Respond ONLY with valid JSON in this exact format:
{{
    "category": "<category name>",
    "priority": "<high/medium/low>",
    "summary": "<brief summary>",
    "entities": {{
        "patient_name": "<name or null>",
        "doctor_name": "<name or null>",
        "department": "<department or null>",
        "amount": "<monetary amount or null>",
        "date": "<important date or null>",
        "diagnosis": "<diagnosis or null>",
        "claim_id": "<claim/invoice ID or null>",
        "appointment_date": "<appointment date or null>"
    }},
    "confidence": <0.0-1.0>
}}
"""
    
    @staticmethod
    async def categorize_email(email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Categorize email using GPT-4
        
        Args:
            email_data: Email information dictionary
            
        Returns:
            Dict containing category, priority, summary, and entities
        """
        try:
            prompt = EmailCategorizer.create_categorization_prompt(email_data)
            
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a medical email classification expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate category
            if result.get('category') not in EmailCategorizer.CATEGORIES:
                result['category'] = 'Other'
            
            # Validate priority
            if result.get('priority') not in EmailCategorizer.PRIORITY_LEVELS:
                result['priority'] = 'medium'
            
            logger.info(f"Email categorized: {result.get('category')} with priority {result.get('priority')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error categorizing email: {str(e)}")
            return {
                "category": "Other",
                "priority": "medium",
                "summary": "Failed to categorize automatically",
                "entities": {},
                "confidence": 0.0
            }
    
    @staticmethod
    async def batch_categorize(emails: list) -> list:
        """
        Categorize multiple emails
        
        Args:
            emails: List of email dictionaries
            
        Returns:
            List of categorization results
        """
        results = []
        for email in emails:
            result = await EmailCategorizer.categorize_email(email)
            results.append(result)
        return results

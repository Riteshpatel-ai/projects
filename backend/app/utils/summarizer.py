"""
Text Summarization Utility
Summarize long email content using GPT
"""
from openai import OpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class TextSummarizer:
    """Summarize text content using AI"""
    
    @staticmethod
    async def summarize_text(
        text: str, 
        max_length: int = 200,
        style: str = "concise"
    ) -> str:
        """
        Summarize text using GPT
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary in words
            style: Summary style (concise, detailed, bullet-points)
            
        Returns:
            Summarized text
        """
        if len(text) < 100:
            return text
        
        try:
            style_prompts = {
                "concise": "in 2-3 sentences",
                "detailed": "in a detailed paragraph",
                "bullet-points": "in bullet points"
            }
            
            prompt = f"""
Summarize the following text {style_prompts.get(style, 'concisely')}:

{text[:3000]}

Summary:
"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical text summarization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=max_length
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Summarized {len(text)} chars to {len(summary)} chars")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return text[:200] + "..." if len(text) > 200 else text
    
    @staticmethod
    async def extract_key_points(text: str, num_points: int = 5) -> list:
        """
        Extract key points from text
        
        Args:
            text: Text to analyze
            num_points: Number of key points to extract
            
        Returns:
            List of key points
        """
        try:
            prompt = f"""
Extract the {num_points} most important points from the following text:

{text[:3000]}

Return as a JSON array of strings.
"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You extract key points from medical documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result.get('points', [])
            
        except Exception as e:
            logger.error(f"Error extracting key points: {str(e)}")
            return []

"""
PDF Parser Utility
Extract text and data from PDF attachments
"""
import PyPDF2
import pdfplumber
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """Parse PDF attachments for email processing"""
    
    @staticmethod
    def extract_text_pypdf2(pdf_path: str) -> str:
        """
        Extract text using PyPDF2
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with PyPDF2: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_pdfplumber(pdf_path: str) -> str:
        """
        Extract text using pdfplumber (better for tables)
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber: {str(e)}")
            return ""
    
    @staticmethod
    def extract_tables(pdf_path: str) -> list:
        """
        Extract tables from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of tables (each table is a list of rows)
        """
        try:
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables: {str(e)}")
            return []
    
    @staticmethod
    def parse_medical_report(pdf_path: str) -> Dict[str, Any]:
        """
        Parse medical report PDF and extract key information
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted information
        """
        try:
            text = PDFParser.extract_text_pdfplumber(pdf_path)
            tables = PDFParser.extract_tables(pdf_path)
            
            # Extract metadata
            result = {
                "text": text,
                "tables": tables,
                "page_count": 0,
                "has_tables": len(tables) > 0
            }
            
            with pdfplumber.open(pdf_path) as pdf:
                result["page_count"] = len(pdf.pages)
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing medical report: {str(e)}")
            return {
                "text": "",
                "tables": [],
                "page_count": 0,
                "has_tables": False,
                "error": str(e)
            }
    
    @staticmethod
    def summarize_pdf(pdf_path: str, max_chars: int = 1000) -> str:
        """
        Get a summary of PDF content
        
        Args:
            pdf_path: Path to PDF file
            max_chars: Maximum characters in summary
            
        Returns:
            Summary text
        """
        try:
            text = PDFParser.extract_text_pdfplumber(pdf_path)
            if len(text) > max_chars:
                return text[:max_chars] + "..."
            return text
        except Exception as e:
            logger.error(f"Error summarizing PDF: {str(e)}")
            return ""

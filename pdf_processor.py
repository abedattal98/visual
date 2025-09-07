import PyPDF2
import pdfplumber
import re
from typing import List, Dict, Optional
from pathlib import Path

class PDFProcessor:
    """Handles PDF text extraction and preprocessing"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        if not self.pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File must be a PDF: {pdf_path}")
    
    def extract_text_pypdf2(self) -> str:
        """Extract text using PyPDF2 (fallback method)"""
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {e}")
        return text
    
    def extract_text_pdfplumber(self) -> str:
        """Extract text using pdfplumber (primary method)"""
        text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
        return text
    
    def extract_text(self) -> str:
        """Extract text from PDF using the best available method"""
        # Try pdfplumber first (better text extraction)
        text = self.extract_text_pdfplumber()
        
        # Fallback to PyPDF2 if pdfplumber fails or returns empty
        if not text.strip():
            print("pdfplumber extraction failed or returned empty, trying PyPDF2...")
            text = self.extract_text_pypdf2()
        
        if not text.strip():
            raise ValueError("Could not extract any text from the PDF file")
        
        return self.clean_text(text)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers (basic patterns)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        text = re.sub(r'\n\s*Page \d+.*?\n', '\n', text, flags=re.IGNORECASE)
        
        # Fix common OCR errors
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def get_metadata(self) -> Dict:
        """Extract PDF metadata"""
        metadata = {}
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'producer': pdf_reader.metadata.get('/Producer', ''),
                        'creation_date': pdf_reader.metadata.get('/CreationDate', ''),
                        'modification_date': pdf_reader.metadata.get('/ModDate', '')
                    }
                metadata['num_pages'] = len(pdf_reader.pages)
        except Exception as e:
            print(f"Error extracting metadata: {e}")
        
        return metadata
    
    def extract_by_pages(self) -> List[str]:
        """Extract text page by page"""
        pages = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        pages.append(self.clean_text(page_text))
                    else:
                        pages.append("")
        except Exception as e:
            print(f"Error extracting pages: {e}")
            # Fallback to PyPDF2
            try:
                with open(self.pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        pages.append(self.clean_text(page_text) if page_text else "")
            except Exception as e2:
                print(f"Fallback extraction also failed: {e2}")
        
        return pages

def test_pdf_processor():
    """Test function for PDF processor"""
    # This would be used for testing with an actual PDF file
    pass

if __name__ == "__main__":
    test_pdf_processor()

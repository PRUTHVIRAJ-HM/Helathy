import os
import logging
import pytesseract
from PIL import Image
import PyPDF2
import io
import tempfile

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_text_from_image(image_path):
    """
    Extract text from an image file using pytesseract
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        
        logger.debug(f"Extracted text from image: {text[:100]}...")
        return text
    
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        return ""

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyPDF2
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from each page
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        logger.debug(f"Extracted text from PDF: {text[:100]}...")
        return text
    
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        
        # Try OCR as fallback for scanned PDFs
        try:
            logger.debug("Attempting OCR fallback for PDF...")
            return extract_text_from_pdf_using_ocr(pdf_path)
        except Exception as ocr_error:
            logger.error(f"OCR fallback failed: {str(ocr_error)}")
            return ""

def extract_text_from_pdf_using_ocr(pdf_path):
    """
    Extract text from a PDF using OCR (for scanned PDFs)
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF using OCR
    """
    try:
        from pdf2image import convert_from_path
        
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        
        # Extract text from each image
        text = ""
        for image in images:
            # Create a temporary file to save the image
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_filename = temp_file.name
                
            # Save the image
            image.save(temp_filename, 'JPEG')
            
            # Extract text from the image
            page_text = extract_text_from_image(temp_filename)
            text += page_text + "\n\n"
            
            # Remove the temporary file
            os.unlink(temp_filename)
        
        return text
    
    except Exception as e:
        logger.error(f"Error using OCR on PDF: {str(e)}")
        return ""

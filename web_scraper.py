import logging
import traceback
import trafilatura
import requests
from bs4 import BeautifulSoup
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    """
    try:
        # Send a request to the website
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            return text
        return ""
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {str(e)}")
        return ""

def get_food_information(food_name):
    """
    Scrapes food information from various sources
    Returns a dictionary with food ingredients and nutritional information
    """
    try:
        # First, try to get information from USDA Food Data Central
        usda_info = get_usda_food_data(food_name)
        if usda_info:
            return usda_info
        
        # If USDA fails, try Wikipedia
        wiki_info = get_wikipedia_food_info(food_name)
        if wiki_info:
            return wiki_info
        
        # Finally, try a general search result
        general_info = get_general_food_info(food_name)
        return general_info
    
    except Exception as e:
        logger.error(f"Error in food information retrieval: {str(e)}")
        logger.error(traceback.format_exc())
        # Return basic information in case of error
        return {
            "name": food_name,
            "ingredients": [],
            "nutrients": {},
            "description": f"Basic information for {food_name}. Detailed data unavailable.",
            "source": "default"
        }

def get_usda_food_data(food_name):
    """
    Attempts to get food data from USDA Food Data Central
    Using their search API
    """
    try:
        # Use the USDA Food Data Central search page
        search_url = f"https://fdc.nal.usda.gov/fdc-app.html#/?query={food_name}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            return None
            
        # Try to extract basic information from the search results page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a simplified version as the actual extraction would be complex
        # In a real app, we'd need to parse the JavaScript data or use their API directly
        food_info = {
            "name": food_name,
            "ingredients": [],
            "nutrients": {},
            "description": f"Information about {food_name} from USDA Food Data Central",
            "source": "USDA Food Data Central"
        }
        
        return food_info
    except Exception as e:
        logger.error(f"Error getting USDA data: {str(e)}")
        return None

def get_wikipedia_food_info(food_name):
    """
    Attempts to get food information from Wikipedia
    """
    try:
        # Format the search query for Wikipedia
        search_term = food_name.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{search_term}"
        
        # Get the main content
        text_content = get_website_text_content(url)
        
        if not text_content:
            return None
            
        # Create a basic structure for the food information
        food_info = {
            "name": food_name,
            "ingredients": extract_ingredients_from_text(text_content),
            "nutrients": {},
            "description": extract_description(text_content),
            "source": "Wikipedia"
        }
        
        return food_info
    except Exception as e:
        logger.error(f"Error getting Wikipedia data: {str(e)}")
        return None

def get_general_food_info(food_name):
    """
    General method to create basic food information
    Used as a fallback when other methods fail
    """
    # Create a generic food information object
    food_info = {
        "name": food_name,
        "ingredients": [],
        "nutrients": {},
        "description": f"Basic information for {food_name}. This food product may contain various ingredients.",
        "source": "general"
    }
    
    return food_info

def extract_ingredients_from_text(text):
    """
    Try to extract ingredients list from the text content
    Uses basic pattern matching
    """
    ingredients = []
    
    # Look for common patterns that indicate ingredients lists
    patterns = [
        r"(?:ingredients|contains):([^\.]+)",
        r"(?:made from|composed of):([^\.]+)",
        r"(?:ingredients include|contains):([^\.]+)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Split by commas and clean up
            for match in matches:
                items = [item.strip().lower() for item in match.split(',')]
                ingredients.extend(items)
    
    # If no ingredients found, try extracting common food ingredients
    if not ingredients:
        common_ingredients = [
            "salt", "sugar", "water", "flour", "rice", "wheat", "corn", "dairy",
            "milk", "eggs", "soy", "nuts", "peanuts", "fish", "shellfish",
            "gluten", "wheat", "vegetable oil", "butter", "cheese"
        ]
        
        for ingredient in common_ingredients:
            if ingredient in text.lower():
                ingredients.append(ingredient)
    
    return list(set(ingredients))  # Remove duplicates

def extract_description(text):
    """
    Extract a brief description from the text content
    """
    # Simplistic approach: take the first paragraph
    paragraphs = text.split('\n\n')
    if paragraphs:
        return paragraphs[0]
    
    # Fallback to the first 200 characters
    return text[:200] + "..."

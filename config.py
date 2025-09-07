import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the PDF to Manga converter"""
    
    # Gemini API Configuration for text generation
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-1.5-flash'
    GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta'
    
    # Vertex AI Configuration for image generation
    VERTEX_PROJECT_ID = os.getenv('VERTEX_PROJECT_ID', 'your-project-id')
    VERTEX_LOCATION = os.getenv('VERTEX_LOCATION', 'us-central1')
    IMAGEN_MODEL = 'imagegeneration@006'
    
    # Image Generation Settings
    IMAGE_WIDTH = 1024
    IMAGE_HEIGHT = 768
    GHIBLI_STYLE_PROMPT = "Studio Ghibli style, anime art, detailed background, soft colors, magical atmosphere"
    
    # Manga Layout Settings
    PANEL_MARGIN = 20
    DIALOGUE_BUBBLE_PADDING = 15
    FONT_SIZE_DIALOGUE = 16
    FONT_SIZE_NARRATION = 14
    
    # Text Processing Settings
    MAX_SCENE_LENGTH = 500  # Maximum characters per scene
    MIN_SCENE_LENGTH = 50   # Minimum characters per scene
    
    # Output Settings
    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"
    
    # Supported file formats
    SUPPORTED_PDF_EXTENSIONS = ['.pdf']
    OUTPUT_IMAGE_FORMAT = 'PNG'
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file.")
        
        # Create output directories if they don't exist
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        
        return True

# Default font paths (will be created/downloaded if needed)
FONT_PATHS = {
    'dialogue': 'assets/fonts/dialogue.ttf',
    'narration': 'assets/fonts/narration.ttf',
    'title': 'assets/fonts/title.ttf'
}

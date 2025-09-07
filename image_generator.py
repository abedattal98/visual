import requests
import json
import base64
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse
from config import Config
from story_analyzer import Scene, DialogueLine

class ImageGenerator:
    """Generates Ghibli-style images using Gemini API"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model = Config.GEMINI_MODEL
        self.api_url = Config.GEMINI_API_URL
        
        if not self.api_key:
            raise ValueError("Gemini API key is required")
    
    def create_scene_prompt(self, scene: Scene) -> str:
        """Create a detailed prompt for image generation based on scene analysis"""
        base_prompt = Config.GHIBLI_STYLE_PROMPT
        
        # Build scene description
        scene_elements = []
        
        # Add characters
        if scene.characters:
            char_desc = f"featuring {', '.join(scene.characters[:3])}"  # Limit to 3 characters
            scene_elements.append(char_desc)
        
        # Add setting
        if scene.setting:
            scene_elements.append(f"set in {scene.setting}")
        
        # Add mood/atmosphere
        if scene.mood:
            mood_descriptions = {
                'dark': 'dark and mysterious atmosphere',
                'bright': 'bright and cheerful atmosphere',
                'mysterious': 'mysterious and enchanting mood',
                'peaceful': 'peaceful and serene environment',
                'tense': 'tense and dramatic atmosphere',
                'romantic': 'romantic and dreamy setting',
                'neutral': 'calm and balanced atmosphere'
            }
            scene_elements.append(mood_descriptions.get(scene.mood, 'atmospheric setting'))
        
        # Extract key actions or descriptions from the scene text
        scene_summary = self.extract_scene_summary(scene.description)
        if scene_summary:
            scene_elements.append(scene_summary)
        
        # Combine all elements
        scene_description = ", ".join(scene_elements)
        
        # Create final prompt
        prompt = f"{base_prompt}, {scene_description}, high quality, detailed illustration, anime style, featuring characters, manga panel"
        
        return prompt
    
    def extract_scene_summary(self, scene_text: str, max_length: int = 100) -> str:
        """Extract a concise summary of the scene for image generation"""
        # Remove dialogue (we'll add it separately)
        import re
        text_without_dialogue = re.sub(r'["\'""]([^"\'""]*)["\'""]', '', scene_text)
        
        # Get first sentence or up to max_length characters
        sentences = text_without_dialogue.split('.')
        if sentences:
            summary = sentences[0].strip()
            if len(summary) > max_length:
                summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
            return summary
        
        return ""
    
    def generate_image_with_gemini(self, prompt: str) -> Optional[str]:
        """Generate actual AI images using Gemini API for prompts and Pollinations for image generation"""
        
        # Step 1: Use Gemini to create an optimized image prompt
        optimized_prompt = self.create_optimized_prompt_with_gemini(prompt)
        if not optimized_prompt:
            optimized_prompt = prompt
        
        # Step 2: Generate actual image using Pollinations AI
        return self.generate_image_with_pollinations(optimized_prompt)
    
    def create_optimized_prompt_with_gemini(self, prompt: str) -> Optional[str]:
        """Use Gemini to create an optimized prompt for image generation"""
        
        full_url = f"{self.api_url}/models/{self.model}:generateContent"
        
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Create a concise, detailed image generation prompt for this scene: {prompt}. Focus on Studio Ghibli anime style with specific visual details like character appearance, setting, colors, lighting, and atmosphere. Keep it under 200 words and optimized for AI image generation. Include: 'Studio Ghibli style, anime art, detailed, soft colors, magical atmosphere' and specific scene elements."
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 300
            }
        }
        
        try:
            response = requests.post(full_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0]['text'].strip()
            
        except Exception as e:
            print(f"Error creating optimized prompt with Gemini: {e}")
        
        return None
    
    def generate_image_with_pollinations(self, prompt: str) -> Optional[str]:
        """Generate actual AI image using Pollinations AI API"""
        
        try:
            # Clean and encode the prompt
            clean_prompt = prompt.replace('\n', ' ').strip()
            encoded_prompt = urllib.parse.quote(clean_prompt)
            
            # Pollinations AI API endpoint
            api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            
            # Add parameters for better quality
            params = {
                'width': Config.IMAGE_WIDTH,
                'height': Config.IMAGE_HEIGHT,
                'seed': int(time.time()),  # Random seed for variety
                'model': 'flux',  # Use Flux model for better quality
                'enhance': 'true'
            }
            
            # Build full URL with parameters
            param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{api_url}?{param_string}"
            
            print(f"Generating image with Pollinations AI...")
            print(f"Prompt: {clean_prompt[:100]}...")
            
            # Make request to generate image
            response = requests.get(full_url, timeout=120)
            response.raise_for_status()
            
            # Convert image to base64
            image_base64 = base64.b64encode(response.content).decode()
            
            print(f"✓ Successfully generated AI image")
            return image_base64
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Pollinations API: {e}")
            # Fallback to alternative image generation service
            return self.generate_image_with_alternative_service(prompt)
        except Exception as e:
            print(f"Unexpected error with Pollinations: {e}")
            return self.generate_image_with_alternative_service(prompt)
    
    def generate_image_with_alternative_service(self, prompt: str) -> Optional[str]:
        """Fallback: Generate image using alternative free AI image service"""
        
        try:
            # Try Hugging Face Inference API as fallback
            api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            
            headers = {
                "Content-Type": "application/json",
            }
            
            payload = {
                "inputs": f"{prompt}, Studio Ghibli style, anime art, high quality, detailed illustration",
                "parameters": {
                    "width": Config.IMAGE_WIDTH,
                    "height": Config.IMAGE_HEIGHT,
                    "num_inference_steps": 20
                }
            }
            
            print(f"Trying alternative image generation service...")
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                image_base64 = base64.b64encode(response.content).decode()
                print(f"✓ Successfully generated AI image with alternative service")
                return image_base64
            else:
                print(f"Alternative service returned status: {response.status_code}")
                
        except Exception as e:
            print(f"Alternative service error: {e}")
        
        # Final fallback: create enhanced placeholder with Gemini description
        print("Falling back to enhanced placeholder with Gemini description...")
        return self.create_enhanced_placeholder_with_gemini(prompt)
    
    def create_enhanced_placeholder_with_gemini(self, prompt: str) -> Optional[str]:
        """Create enhanced placeholder using Gemini description as final fallback"""
        
        # Get detailed description from Gemini
        full_url = f"{self.api_url}/models/{self.model}:generateContent"
        
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Describe this scene in vivid visual detail for a Studio Ghibli anime: {prompt}. Include character appearances, colors, lighting, and atmosphere."
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 500
            }
        }
        
        try:
            response = requests.post(full_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    description = candidate['content']['parts'][0]['text']
                    return self.create_gemini_based_image(prompt, description)
            
        except Exception as e:
            print(f"Error with Gemini fallback: {e}")
        
        return None
    
    def create_gemini_based_image(self, prompt: str, gemini_description: str) -> str:
        """Create a visual image based on Gemini's detailed description"""
        # Create a high-quality image with Ghibli-like colors
        width, height = Config.IMAGE_WIDTH, Config.IMAGE_HEIGHT
        
        # Enhanced Ghibli-inspired color palette based on description
        colors = self.extract_colors_from_description(gemini_description)
        
        # Create gradient background
        img = Image.new('RGB', (width, height), colors[0])
        draw = ImageDraw.Draw(img)
        
        # Create a more sophisticated gradient based on description
        self.create_enhanced_background(draw, width, height, colors, gemini_description)
        
        # Add character elements based on description
        self.add_character_elements(draw, width, height, gemini_description)
        
        # Add environmental elements
        self.add_enhanced_ghibli_elements(draw, width, height, gemini_description)
        
        # Add descriptive text overlay
        self.add_enhanced_scene_text(draw, gemini_description[:400], width, height)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return img_base64
    
    def extract_colors_from_description(self, description: str) -> List[Tuple[int, int, int]]:
        """Extract color palette from Gemini's description"""
        # Default Ghibli palette
        default_colors = [
            (135, 206, 235),  # Sky blue
            (144, 238, 144),  # Light green
            (255, 182, 193),  # Light pink
            (221, 160, 221),  # Plum
            (176, 196, 222),  # Light steel blue
            (255, 218, 185),  # Peach
        ]
        
        # Color mapping based on description keywords
        color_map = {
            'blue': (135, 206, 235),
            'green': (144, 238, 144),
            'pink': (255, 182, 193),
            'purple': (221, 160, 221),
            'yellow': (255, 255, 224),
            'orange': (255, 218, 185),
            'red': (255, 182, 193),
            'brown': (210, 180, 140),
            'gold': (255, 215, 0),
            'silver': (192, 192, 192)
        }
        
        description_lower = description.lower()
        extracted_colors = []
        
        for color_name, rgb in color_map.items():
            if color_name in description_lower:
                extracted_colors.append(rgb)
        
        # If no colors found, use default
        if not extracted_colors:
            extracted_colors = default_colors
        
        # Ensure we have at least 3 colors
        while len(extracted_colors) < 6:
            extracted_colors.extend(default_colors)
        
        return extracted_colors[:6]
    
    def create_enhanced_background(self, draw: ImageDraw.Draw, width: int, height: int, 
                                 colors: List[Tuple[int, int, int]], description: str):
        """Create enhanced background based on Gemini description"""
        # Create multi-layer gradient
        for i in range(height):
            ratio = i / height
            # Use different color combinations based on description
            if 'sky' in description.lower() or 'cloud' in description.lower():
                color1, color2 = colors[0], colors[4]  # Sky colors
            elif 'forest' in description.lower() or 'garden' in description.lower():
                color1, color2 = colors[1], colors[2]  # Nature colors
            else:
                color1, color2 = colors[0], colors[1]  # Default
            
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    def add_character_elements(self, draw: ImageDraw.Draw, width: int, height: int, description: str):
        """Add character representations based on description"""
        # Simple character representations
        if 'girl' in description.lower() or 'luna' in description.lower():
            # Draw a simple character silhouette
            char_x, char_y = width // 3, height // 2
            # Head
            draw.ellipse([char_x-15, char_y-30, char_x+15, char_y], fill=(255, 220, 177))
            # Body
            draw.rectangle([char_x-10, char_y, char_x+10, char_y+40], fill=(100, 149, 237))
            # Hair
            draw.ellipse([char_x-18, char_y-35, char_x+18, char_y-5], fill=(139, 69, 19))
        
        if 'creature' in description.lower() or 'animal' in description.lower():
            # Draw a small creature
            creature_x, creature_y = width // 2, height - 80
            draw.ellipse([creature_x-8, creature_y-8, creature_x+8, creature_y+8], fill=(255, 182, 193))
    
    def add_enhanced_ghibli_elements(self, draw: ImageDraw.Draw, width: int, height: int, description: str):
        """Add enhanced Ghibli-style elements based on description"""
        # Enhanced clouds
        if 'cloud' in description.lower() or 'sky' in description.lower():
            for i in range(4):
                x = (width // 5) * (i + 1)
                y = height // 6
                for j in range(6):
                    circle_x = x + j * 15 - 35
                    circle_y = y + (j % 3) * 8
                    draw.ellipse([circle_x, circle_y, circle_x + 30, circle_y + 20], 
                               fill=(255, 255, 255, 180))
        
        # Enhanced trees and nature
        if 'tree' in description.lower() or 'forest' in description.lower() or 'garden' in description.lower():
            for i in range(3):
                x = (width // 4) * (i + 1)
                y = height - 120
                # Tree trunk
                draw.rectangle([x - 8, y, x + 8, y + 60], fill=(101, 67, 33))
                # Tree crown - multiple layers
                for layer in range(3):
                    crown_y = y - 20 - (layer * 15)
                    crown_size = 35 - (layer * 5)
                    draw.ellipse([x - crown_size, crown_y, x + crown_size, crown_y + 40], 
                               fill=(34, 139, 34, 200 - layer * 30))
        
        # Magical elements
        if 'magic' in description.lower() or 'glow' in description.lower():
            # Add glowing particles
            import random
            for _ in range(20):
                px = random.randint(0, width)
                py = random.randint(0, height)
                draw.ellipse([px-2, py-2, px+2, py+2], fill=(255, 255, 0, 150))
    
    def add_enhanced_scene_text(self, draw: ImageDraw.Draw, text: str, width: int, height: int):
        """Add enhanced scene description text"""
        try:
            font = ImageFont.truetype("Arial.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        # Wrap text more intelligently
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < width - 60:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw text with enhanced styling
        y_start = height - len(lines) * 22 - 30
        for i, line in enumerate(lines[:6]):  # Limit to 6 lines
            y = y_start + i * 22
            # Enhanced text background with gradient
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            # Semi-transparent background
            draw.rectangle([15, y - 3, text_width + 35, y + 18], 
                         fill=(0, 0, 0, 160))
            # Text with slight shadow effect
            draw.text((21, y+1), line, fill=(100, 100, 100), font=font)  # Shadow
            draw.text((20, y), line, fill=(255, 255, 255), font=font)    # Main text
    
    def create_placeholder_image_with_description(self, prompt: str, description: str) -> str:
        """Create a placeholder image with Gemini-generated scene description"""
        # Create a placeholder image with Ghibli-like colors
        width, height = Config.IMAGE_WIDTH, Config.IMAGE_HEIGHT
        
        # Ghibli-inspired color palette
        colors = [
            (135, 206, 235),  # Sky blue
            (144, 238, 144),  # Light green
            (255, 182, 193),  # Light pink
            (221, 160, 221),  # Plum
            (176, 196, 222),  # Light steel blue
        ]
        
        # Create gradient background
        img = Image.new('RGB', (width, height), colors[0])
        draw = ImageDraw.Draw(img)
        
        # Create a simple gradient
        for i in range(height):
            ratio = i / height
            color1 = colors[0]
            color2 = colors[1]
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        # Add some decorative elements
        self.add_ghibli_elements(draw, width, height)
        
        # Add text description (first 300 characters)
        self.add_scene_text(draw, description[:300], width, height)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return img_base64
    
    def add_ghibli_elements(self, draw: ImageDraw.Draw, width: int, height: int):
        """Add Ghibli-style decorative elements to the image"""
        # Add some clouds
        cloud_color = (255, 255, 255, 180)
        
        # Simple cloud shapes
        for i in range(3):
            x = (width // 4) * (i + 1)
            y = height // 4
            # Draw cloud as overlapping circles
            for j in range(5):
                circle_x = x + j * 20 - 40
                circle_y = y + (j % 2) * 10
                draw.ellipse([circle_x, circle_y, circle_x + 40, circle_y + 30], 
                           fill=(255, 255, 255, 150))
        
        # Add some simple trees/nature elements
        tree_color = (34, 139, 34)
        for i in range(2):
            x = (width // 3) * (i + 1)
            y = height - 100
            # Simple tree trunk
            draw.rectangle([x - 5, y, x + 5, y + 50], fill=(139, 69, 19))
            # Tree crown
            draw.ellipse([x - 30, y - 40, x + 30, y + 20], fill=tree_color)
    
    def add_scene_text(self, draw: ImageDraw.Draw, text: str, width: int, height: int):
        """Add scene description text to the image"""
        try:
            # Try to use a nice font, fallback to default
            font = ImageFont.truetype("Arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw text with background
        y_start = height - len(lines) * 25 - 20
        for i, line in enumerate(lines[:5]):  # Limit to 5 lines
            y = y_start + i * 25
            # Text background
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            draw.rectangle([10, y - 2, text_width + 20, y + 20], 
                         fill=(0, 0, 0, 128))
            # Text
            draw.text((15, y), line, fill=(255, 255, 255), font=font)
    
    def generate_scene_image(self, scene: Scene) -> Optional[str]:
        """Generate an image for a specific scene"""
        prompt = self.create_scene_prompt(scene)
        print(f"Generating image for scene {scene.id} with prompt: {prompt[:100]}...")
        
        return self.generate_image_with_gemini(prompt)
    
    def save_image_from_base64(self, base64_data: str, filepath: str) -> bool:
        """Save base64 encoded image to file"""
        try:
            image_data = base64.b64decode(base64_data)
            with open(filepath, 'wb') as f:
                f.write(image_data)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def generate_images_for_scenes(self, scenes: List[Scene], output_dir: str) -> Dict[int, str]:
        """Generate images for all scenes and return mapping of scene_id to image_path"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        scene_images = {}
        
        for scene in scenes:
            print(f"Processing scene {scene.id}/{len(scenes)}...")
            
            # Generate image
            image_base64 = self.generate_scene_image(scene)
            
            if image_base64:
                # Save image
                image_filename = f"scene_{scene.id:03d}.png"
                image_path = output_path / image_filename
                
                if self.save_image_from_base64(image_base64, str(image_path)):
                    scene_images[scene.id] = str(image_path)
                    print(f"✓ Generated image for scene {scene.id}")
                else:
                    print(f"✗ Failed to save image for scene {scene.id}")
            else:
                print(f"✗ Failed to generate image for scene {scene.id}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
        
        return scene_images

def test_image_generator():
    """Test function for image generator"""
    from story_analyzer import Scene, DialogueLine
    
    # Create a test scene
    test_scene = Scene(
        id=1,
        description="A young girl walks through a magical forest filled with glowing flowers and friendly spirits.",
        dialogue=[
            DialogueLine(speaker="Girl", text="What a beautiful place!", emotion="excited")
        ],
        characters=["Girl"],
        setting="magical forest",
        mood="peaceful"
    )
    
    generator = ImageGenerator()
    prompt = generator.create_scene_prompt(test_scene)
    print(f"Generated prompt: {prompt}")

if __name__ == "__main__":
    test_image_generator()

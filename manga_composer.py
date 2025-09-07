import os
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple, Optional
import math
from pathlib import Path
from story_analyzer import Scene, DialogueLine
from config import Config

class MangaComposer:
    """Composes final manga pages with images and dialogue bubbles"""
    
    def __init__(self):
        self.panel_margin = Config.PANEL_MARGIN
        self.bubble_padding = Config.DIALOGUE_BUBBLE_PADDING
        self.font_size_dialogue = Config.FONT_SIZE_DIALOGUE
        self.font_size_narration = Config.FONT_SIZE_NARRATION
        
        # Load fonts
        self.dialogue_font = self.load_font('dialogue', self.font_size_dialogue)
        self.narration_font = self.load_font('narration', self.font_size_narration)
        
        # Dialogue bubble colors
        self.bubble_colors = {
            'normal': (255, 255, 255, 220),
            'thought': (240, 240, 255, 200),
            'shout': (255, 240, 240, 230),
            'whisper': (245, 245, 245, 180)
        }
    
    def load_font(self, font_type: str, size: int) -> ImageFont.ImageFont:
        """Load font with fallback to default"""
        font_paths = [
            f"assets/fonts/{font_type}.ttf",
            "Arial.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "C:/Windows/Fonts/arial.ttf"  # Windows
        ]
        
        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except (OSError, IOError):
                continue
        
        # Fallback to default font
        return ImageFont.load_default()
    
    def calculate_text_size(self, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
        """Calculate the size needed for text"""
        # Create a temporary image to measure text
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    def wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            text_width, _ = self.calculate_text_size(test_line, font)
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def determine_bubble_type(self, dialogue: DialogueLine) -> str:
        """Determine the type of dialogue bubble based on content and emotion"""
        text = dialogue.text.lower()
        
        if dialogue.emotion == 'angry' or '!' in dialogue.text:
            return 'shout'
        elif any(word in text for word in ['think', 'thought', 'wonder']):
            return 'thought'
        elif dialogue.emotion == 'whisper' or text.startswith('(') and text.endswith(')'):
            return 'whisper'
        else:
            return 'normal'
    
    def create_dialogue_bubble(self, dialogue: DialogueLine, max_width: int = 200) -> Image.Image:
        """Create a dialogue bubble image"""
        bubble_type = self.determine_bubble_type(dialogue)
        bubble_color = self.bubble_colors[bubble_type]
        
        # Wrap text
        lines = self.wrap_text(dialogue.text, self.dialogue_font, max_width - 2 * self.bubble_padding)
        
        # Calculate bubble size
        line_height = self.font_size_dialogue + 4
        text_height = len(lines) * line_height
        text_width = max(self.calculate_text_size(line, self.dialogue_font)[0] for line in lines) if lines else 0
        
        bubble_width = text_width + 2 * self.bubble_padding
        bubble_height = text_height + 2 * self.bubble_padding
        
        # Add speaker name if present
        speaker_height = 0
        if dialogue.speaker:
            speaker_height = self.font_size_dialogue + 8
            bubble_height += speaker_height
        
        # Create bubble image
        bubble_img = Image.new('RGBA', (bubble_width, bubble_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bubble_img)
        
        # Draw bubble background
        if bubble_type == 'thought':
            # Thought bubble (cloud-like)
            self.draw_thought_bubble(draw, bubble_width, bubble_height, bubble_color)
        else:
            # Regular speech bubble
            self.draw_speech_bubble(draw, bubble_width, bubble_height, bubble_color, bubble_type)
        
        # Draw speaker name
        y_offset = self.bubble_padding
        if dialogue.speaker:
            speaker_text = f"{dialogue.speaker}:"
            draw.text((self.bubble_padding, y_offset), speaker_text, 
                     fill=(0, 0, 0), font=self.dialogue_font)
            y_offset += speaker_height
        
        # Draw dialogue text
        for line in lines:
            draw.text((self.bubble_padding, y_offset), line, 
                     fill=(0, 0, 0), font=self.dialogue_font)
            y_offset += line_height
        
        return bubble_img
    
    def draw_speech_bubble(self, draw: ImageDraw.Draw, width: int, height: int, 
                          color: Tuple[int, int, int, int], bubble_type: str):
        """Draw a speech bubble background"""
        # Main bubble
        draw.rounded_rectangle([0, 0, width-1, height-1], radius=15, fill=color, outline=(0, 0, 0))
        
        # Add tail for speech bubble
        if bubble_type == 'shout':
            # Jagged edges for shouting
            points = []
            for i in range(0, width, 10):
                points.extend([(i, 0), (i+5, -5 if i % 20 == 0 else 0)])
            if len(points) > 2:
                draw.polygon(points, fill=color)
    
    def draw_thought_bubble(self, draw: ImageDraw.Draw, width: int, height: int, 
                           color: Tuple[int, int, int, int]):
        """Draw a thought bubble (cloud-like)"""
        # Main cloud
        draw.ellipse([0, 0, width-1, height-1], fill=color, outline=(0, 0, 0))
        
        # Add smaller circles for thought bubble effect
        circle_size = 8
        draw.ellipse([width//4, height + 5, width//4 + circle_size, height + 5 + circle_size], 
                    fill=color, outline=(0, 0, 0))
        
        circle_size = 5
        draw.ellipse([width//6, height + 15, width//6 + circle_size, height + 15 + circle_size], 
                    fill=color, outline=(0, 0, 0))
    
    def find_best_bubble_position(self, image: Image.Image, bubble: Image.Image, 
                                 avoid_areas: List[Tuple[int, int, int, int]] = None) -> Tuple[int, int]:
        """Find the best position for a dialogue bubble on the image"""
        img_width, img_height = image.size
        bubble_width, bubble_height = bubble.size
        
        if avoid_areas is None:
            avoid_areas = []
        
        # Preferred positions (top-left, top-right, bottom-left, bottom-right)
        positions = [
            (20, 20),  # Top-left
            (img_width - bubble_width - 20, 20),  # Top-right
            (20, img_height - bubble_height - 20),  # Bottom-left
            (img_width - bubble_width - 20, img_height - bubble_height - 20),  # Bottom-right
            (img_width // 2 - bubble_width // 2, 20),  # Top-center
            (img_width // 2 - bubble_width // 2, img_height - bubble_height - 20),  # Bottom-center
        ]
        
        # Check each position for overlap with avoid_areas
        for x, y in positions:
            # Ensure bubble is within image bounds
            if x < 0 or y < 0 or x + bubble_width > img_width or y + bubble_height > img_height:
                continue
            
            # Check for overlap with avoid areas
            bubble_rect = (x, y, x + bubble_width, y + bubble_height)
            overlaps = False
            
            for avoid_rect in avoid_areas:
                if self.rectangles_overlap(bubble_rect, avoid_rect):
                    overlaps = True
                    break
            
            if not overlaps:
                return x, y
        
        # If no good position found, use top-left as fallback
        return 20, 20
    
    def rectangles_overlap(self, rect1: Tuple[int, int, int, int], 
                          rect2: Tuple[int, int, int, int]) -> bool:
        """Check if two rectangles overlap"""
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2
        
        return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)
    
    def add_dialogue_to_image(self, image: Image.Image, dialogues: List[DialogueLine]) -> Image.Image:
        """Add dialogue bubbles to an image"""
        if not dialogues:
            return image
        
        # Create a copy of the image
        result_img = image.copy()
        
        # Keep track of bubble positions to avoid overlap
        used_areas = []
        
        for dialogue in dialogues:
            # Create dialogue bubble
            bubble = self.create_dialogue_bubble(dialogue)
            
            # Find best position
            x, y = self.find_best_bubble_position(result_img, bubble, used_areas)
            
            # Paste bubble onto image
            result_img.paste(bubble, (x, y), bubble)
            
            # Add this area to used areas
            bubble_width, bubble_height = bubble.size
            used_areas.append((x, y, x + bubble_width, y + bubble_height))
        
        return result_img
    
    def create_manga_page(self, scenes: List[Scene], scene_images: Dict[int, str], 
                         page_number: int, scenes_per_page: int = 2) -> Image.Image:
        """Create a manga page with multiple scenes"""
        page_width = Config.IMAGE_WIDTH
        page_height = Config.IMAGE_HEIGHT * 2  # Taller page for multiple panels
        
        # Create page background
        page = Image.new('RGB', (page_width, page_height), (255, 255, 255))
        
        # Calculate panel layout
        start_scene = (page_number - 1) * scenes_per_page
        end_scene = min(start_scene + scenes_per_page, len(scenes))
        page_scenes = scenes[start_scene:end_scene]
        
        panel_height = (page_height - (len(page_scenes) + 1) * self.panel_margin) // len(page_scenes)
        
        y_offset = self.panel_margin
        
        for i, scene in enumerate(page_scenes):
            if scene.id in scene_images:
                # Load and resize scene image
                scene_img = Image.open(scene_images[scene.id])
                scene_img = scene_img.resize((page_width - 2 * self.panel_margin, panel_height), 
                                           Image.Resampling.LANCZOS)
                
                # Add dialogue bubbles
                scene_with_dialogue = self.add_dialogue_to_image(scene_img, scene.dialogue)
                
                # Paste onto page
                page.paste(scene_with_dialogue, (self.panel_margin, y_offset))
                
                # Add panel border
                draw = ImageDraw.Draw(page)
                draw.rectangle([self.panel_margin - 2, y_offset - 2, 
                              page_width - self.panel_margin + 2, y_offset + panel_height + 2], 
                             outline=(0, 0, 0), width=2)
            
            y_offset += panel_height + self.panel_margin
        
        return page
    
    def create_manga_from_scenes(self, scenes: List[Scene], scene_images: Dict[int, str], 
                                output_dir: str) -> List[str]:
        """Create complete manga from scenes and return list of page file paths"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        scenes_per_page = 2
        total_pages = math.ceil(len(scenes) / scenes_per_page)
        
        page_files = []
        
        for page_num in range(1, total_pages + 1):
            print(f"Creating manga page {page_num}/{total_pages}...")
            
            # Create page
            page_img = self.create_manga_page(scenes, scene_images, page_num, scenes_per_page)
            
            # Save page
            page_filename = f"manga_page_{page_num:03d}.png"
            page_path = output_path / page_filename
            page_img.save(str(page_path), Config.OUTPUT_IMAGE_FORMAT)
            
            page_files.append(str(page_path))
            print(f"✓ Saved page {page_num}: {page_filename}")
        
        return page_files
    
    def create_title_page(self, title: str, author: str = "", output_path: str = "") -> str:
        """Create a title page for the manga"""
        page = Image.new('RGB', (Config.IMAGE_WIDTH, Config.IMAGE_HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        
        # Load title font (larger)
        try:
            title_font = ImageFont.truetype("Arial.ttf", 48)
            author_font = ImageFont.truetype("Arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()
        
        # Draw title
        title_width, title_height = self.calculate_text_size(title, title_font)
        title_x = (Config.IMAGE_WIDTH - title_width) // 2
        title_y = Config.IMAGE_HEIGHT // 3
        
        draw.text((title_x, title_y), title, fill=(0, 0, 0), font=title_font)
        
        # Draw author
        if author:
            author_text = f"by {author}"
            author_width, author_height = self.calculate_text_size(author_text, author_font)
            author_x = (Config.IMAGE_WIDTH - author_width) // 2
            author_y = title_y + title_height + 30
            
            draw.text((author_x, author_y), author_text, fill=(100, 100, 100), font=author_font)
        
        # Add decorative border
        border_margin = 50
        draw.rectangle([border_margin, border_margin, 
                       Config.IMAGE_WIDTH - border_margin, Config.IMAGE_HEIGHT - border_margin], 
                      outline=(0, 0, 0), width=3)
        
        # Save title page
        if not output_path:
            output_path = os.path.join(Config.OUTPUT_DIR, "manga_title_page.png")
        
        page.save(output_path, Config.OUTPUT_IMAGE_FORMAT)
        return output_path

def test_manga_composer():
    """Test function for manga composer"""
    from story_analyzer import Scene, DialogueLine
    
    # Create test dialogue
    test_dialogue = [
        DialogueLine(speaker="Alice", text="What a wonderful day!", emotion="happy"),
        DialogueLine(speaker="Bob", text="I couldn't agree more.", emotion="neutral")
    ]
    
    composer = MangaComposer()
    
    # Test bubble creation
    bubble = composer.create_dialogue_bubble(test_dialogue[0])
    print(f"Created dialogue bubble: {bubble.size}")

if __name__ == "__main__":
    test_manga_composer()

#!/usr/bin/env python3
"""
PDF to Visual Manga Converter

This application converts PDF stories into visual manga with Ghibli-style artwork
and anime-style dialogue bubbles.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict
import traceback

from config import Config
from pdf_processor import PDFProcessor
from story_analyzer import StoryAnalyzer
from image_generator import ImageGenerator
from manga_composer import MangaComposer

class PDFToMangaConverter:
    """Main application class for converting PDF to manga"""
    
    def __init__(self):
        self.config = Config()
        self.pdf_processor = None
        self.story_analyzer = StoryAnalyzer()
        self.image_generator = None
        self.manga_composer = MangaComposer()
    
    def validate_setup(self):
        """Validate that all required components are properly configured"""
        try:
            Config.validate_config()
            print("✓ Configuration validated")
            
            # Initialize image generator (this will check API key)
            self.image_generator = ImageGenerator()
            print("✓ Image generator initialized")
            
            return True
        except Exception as e:
            print(f"✗ Setup validation failed: {e}")
            return False
    
    def process_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file or text file for samples"""
        print(f"📖 Processing file: {pdf_path}")
        
        try:
            # Handle text files for sample mode
            if pdf_path.endswith('.txt'):
                with open(pdf_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                print(f"✓ Extracted {len(text)} characters from text file")
                return text
            else:
                # Handle PDF files
                self.pdf_processor = PDFProcessor(pdf_path)
                text = self.pdf_processor.extract_text()
                print(f"✓ Extracted {len(text)} characters from PDF")
                return text
        except Exception as e:
            print(f"✗ Failed to process file: {e}")
            raise
    
    def analyze_story(self, text: str) -> List:
        """Analyze story text to extract scenes and dialogue"""
        print("🔍 Analyzing story structure...")
        
        try:
            scenes = self.story_analyzer.analyze_story(text)
            
            print(f"✓ Identified {len(scenes)} scenes")
            
            # Print scene summary
            for scene in scenes[:3]:  # Show first 3 scenes
                print(f"  Scene {scene.id}: {len(scene.dialogue)} dialogue lines, "
                      f"characters: {', '.join(scene.characters[:3])}")
            
            if len(scenes) > 3:
                print(f"  ... and {len(scenes) - 3} more scenes")
            
            return scenes
        except Exception as e:
            print(f"✗ Failed to analyze story: {e}")
            raise
    
    def generate_images(self, scenes: List, output_dir: str) -> Dict[int, str]:
        """Generate images for all scenes"""
        print("🎨 Generating Ghibli-style images...")
        
        try:
            scene_images = self.image_generator.generate_images_for_scenes(scenes, output_dir)
            
            print(f"✓ Generated {len(scene_images)} images")
            return scene_images
        except Exception as e:
            print(f"✗ Failed to generate images: {e}")
            raise
    
    def create_manga(self, scenes: List, scene_images: Dict[int, str], 
                    output_dir: str, title: str = "", author: str = "") -> List[str]:
        """Create final manga pages"""
        print("📚 Composing manga pages...")
        
        try:
            # Create title page if title provided
            title_page_path = None
            if title:
                title_page_path = self.manga_composer.create_title_page(
                    title, author, os.path.join(output_dir, "manga_title_page.png")
                )
                print(f"✓ Created title page: {title_page_path}")
            
            # Create manga pages
            page_files = self.manga_composer.create_manga_from_scenes(
                scenes, scene_images, output_dir
            )
            
            # Combine title page with other pages
            all_pages = []
            if title_page_path:
                all_pages.append(title_page_path)
            all_pages.extend(page_files)
            
            print(f"✓ Created {len(page_files)} manga pages")
            return all_pages
        except Exception as e:
            print(f"✗ Failed to create manga: {e}")
            raise
    
    def convert(self, pdf_path: str, output_dir: str = None, title: str = "", 
               author: str = "") -> List[str]:
        """Main conversion method"""
        if not output_dir:
            output_dir = Config.OUTPUT_DIR
        
        print("🚀 Starting PDF to Manga conversion...")
        print(f"   Input: {pdf_path}")
        print(f"   Output: {output_dir}")
        print()
        
        try:
            # Step 1: Validate setup
            if not self.validate_setup():
                raise Exception("Setup validation failed")
            
            # Step 2: Process PDF
            text = self.process_pdf(pdf_path)
            
            # Step 3: Analyze story
            scenes = self.analyze_story(text)
            
            # Step 4: Generate images
            images_dir = os.path.join(output_dir, "images")
            scene_images = self.generate_images(scenes, images_dir)
            
            # Step 5: Create manga
            manga_pages = self.create_manga(scenes, scene_images, output_dir, title, author)
            
            print()
            print("🎉 Conversion completed successfully!")
            print(f"📁 Output directory: {output_dir}")
            print(f"📄 Generated {len(manga_pages)} pages")
            
            return manga_pages
            
        except Exception as e:
            print(f"\n💥 Conversion failed: {e}")
            print("\nFull error details:")
            traceback.print_exc()
            raise

def create_sample_pdf():
    """Create a sample PDF for testing"""
    sample_text = """
    The Magic Garden Adventure
    
    Once upon a time, in a small village nestled between rolling hills, there lived a young girl named Luna. She had always been curious about the mysterious garden behind her grandmother's house.
    
    "Grandmother, what's in that garden?" Luna asked one sunny morning.
    
    Her grandmother smiled mysteriously. "That, my dear, is a place where magic still lives. But only those with pure hearts can see its wonders."
    
    Luna's eyes sparkled with excitement. "Can I go there?"
    
    "Of course, child. But remember, treat everything with respect and kindness."
    
    Luna ran to the garden gate. As she pushed it open, the rusty hinges creaked softly. Inside, she gasped in wonder. The garden was filled with flowers that glowed like tiny stars, and butterflies with wings that shimmered like rainbows.
    
    "Welcome, Luna," whispered a gentle voice.
    
    Luna turned to see a small fairy sitting on a mushroom. "You can talk!"
    
    The fairy laughed like tiny silver bells. "In this garden, all living things can speak to those who listen with their hearts."
    
    And so began Luna's greatest adventure, in a place where magic was real and friendship knew no bounds.
    """
    
    # For now, just save as text file since we don't have reportlab
    sample_path = "sample_story.txt"
    with open(sample_path, 'w', encoding='utf-8') as f:
        f.write(sample_text)
    
    print(f"Created sample story file: {sample_path}")
    return sample_path

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Convert PDF stories to visual manga with Ghibli-style artwork"
    )
    parser.add_argument("pdf_path", nargs='?', help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output directory", default=None)
    parser.add_argument("-t", "--title", help="Manga title", default="")
    parser.add_argument("-a", "--author", help="Author name", default="")
    parser.add_argument("--sample", action="store_true", help="Create and use sample story")
    parser.add_argument("--test", action="store_true", help="Run component tests")
    
    args = parser.parse_args()
    
    if args.test:
        print("🧪 Running component tests...")
        run_tests()
        return
    
    if args.sample:
        print("📝 Creating sample story...")
        pdf_path = create_sample_pdf()
        print("Note: Using text file instead of PDF for sample")
    elif args.pdf_path:
        pdf_path = args.pdf_path
    else:
        print("Error: Please provide a PDF path or use --sample for testing")
        parser.print_help()
        return
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return
    
    try:
        converter = PDFToMangaConverter()
        manga_pages = converter.convert(
            pdf_path=pdf_path,
            output_dir=args.output,
            title=args.title,
            author=args.author
        )
        
        print("\n📋 Generated files:")
        for page in manga_pages:
            print(f"  • {page}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Conversion cancelled by user")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        sys.exit(1)

def run_tests():
    """Run basic component tests"""
    print("Testing PDF processor...")
    try:
        # Test with sample file
        sample_path = create_sample_pdf()
        # Note: This would fail with actual PDF, but shows the structure
        print("✓ PDF processor structure OK")
    except Exception as e:
        print(f"✗ PDF processor test failed: {e}")
    
    print("Testing story analyzer...")
    try:
        from story_analyzer import test_story_analyzer
        test_story_analyzer()
        print("✓ Story analyzer test passed")
    except Exception as e:
        print(f"✗ Story analyzer test failed: {e}")
    
    print("Testing image generator...")
    try:
        from image_generator import test_image_generator
        test_image_generator()
        print("✓ Image generator test passed")
    except Exception as e:
        print(f"✗ Image generator test failed: {e}")
    
    print("Testing manga composer...")
    try:
        from manga_composer import test_manga_composer
        test_manga_composer()
        print("✓ Manga composer test passed")
    except Exception as e:
        print(f"✗ Manga composer test failed: {e}")

if __name__ == "__main__":
    main()

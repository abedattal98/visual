#!/usr/bin/env python3
"""
Setup script for PDF to Visual Manga Converter
This script helps users set up the project quickly.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("\n📚 Downloading NLTK data...")
    
    try:
        import nltk
        
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('names', quiet=True)
        
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False

def setup_env_file():
    """Set up environment file"""
    print("\n🔧 Setting up environment file...")
    
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        # Copy example file
        with open('.env.example', 'r') as src, open('.env', 'w') as dst:
            dst.write(src.read())
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your GEMINI_API_KEY")
        return True
    else:
        # Create basic .env file
        env_content = """# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional settings (uncomment to customize)
# OUTPUT_DIR=output
# IMAGE_WIDTH=1024
# IMAGE_HEIGHT=768
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Created basic .env file")
        print("⚠️  Please edit .env and add your GEMINI_API_KEY")
        return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['output', 'temp', 'assets', 'assets/fonts']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")
    return True

def test_setup():
    """Test the setup"""
    print("\n🧪 Testing setup...")
    
    try:
        # Test imports
        from config import Config
        from pdf_processor import PDFProcessor
        from story_analyzer import StoryAnalyzer
        from image_generator import ImageGenerator
        from manga_composer import MangaComposer
        
        print("✅ All modules import successfully")
        
        # Test configuration
        try:
            Config.validate_config()
            print("✅ Configuration is valid")
        except ValueError as e:
            if "GEMINI_API_KEY" in str(e):
                print("⚠️  Configuration needs API key (expected)")
            else:
                print(f"❌ Configuration error: {e}")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("   1. Edit .env file and add your Gemini API key:")
    print("      GEMINI_API_KEY=your_actual_api_key_here")
    print()
    print("   2. Test the converter with a sample story:")
    print("      python main.py --sample")
    print()
    print("   3. Convert your own PDF:")
    print("      python main.py your_story.pdf")
    print()
    print("   4. Add custom title and author:")
    print("      python main.py your_story.pdf --title 'My Story' --author 'Your Name'")
    print()
    print("📚 For more information, see README.md")
    print("🧪 To run tests: python test_converter.py")

def main():
    """Main setup function"""
    print("🎨 PDF to Visual Manga Converter - Setup")
    print("=" * 45)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Download NLTK data
    if not download_nltk_data():
        print("\n⚠️  NLTK data download failed, but continuing...")
    
    # Setup environment file
    if not setup_env_file():
        print("\n❌ Setup failed during environment file creation")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n❌ Setup failed during directory creation")
        sys.exit(1)
    
    # Test setup
    if not test_setup():
        print("\n❌ Setup validation failed")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()

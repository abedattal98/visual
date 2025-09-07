# PDF to Visual Manga Converter 📚✨

Transform your PDF stories into beautiful visual manga with Studio Ghibli-style artwork and anime-style dialogue bubbles!

## 🌟 Features

- **PDF Text Extraction**: Automatically extracts text from PDF files
- **Intelligent Story Analysis**: Identifies scenes, characters, and dialogue
- **AI-Powered Image Generation**: Creates Ghibli-style artwork using BlackBox API
- **Manga Composition**: Combines images with anime-style dialogue bubbles
- **Customizable Output**: Configurable layouts, fonts, and styling

## 🎨 What It Does

1. **Reads your PDF story** - Extracts and processes the text content
2. **Analyzes the narrative** - Identifies scenes, characters, dialogue, and settings
3. **Generates beautiful artwork** - Creates Studio Ghibli-style images for each scene
4. **Adds dialogue bubbles** - Places anime-style conversation bubbles on images
5. **Creates manga pages** - Combines everything into professional manga layouts

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- BlackBox API key
- Internet connection for AI image generation

### Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd pdf-to-manga-converter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your BlackBox API key
   ```

4. **Download NLTK data** (first run only)
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('names')"
   ```

### Basic Usage

```bash
# Convert a PDF to manga
python main.py your_story.pdf

# With custom title and author
python main.py your_story.pdf --title "My Amazing Story" --author "Your Name"

# Specify output directory
python main.py your_story.pdf --output ./my_manga

# Try with sample story
python main.py --sample
```

## 📖 Detailed Usage

### Command Line Options

```bash
python main.py [PDF_PATH] [OPTIONS]

Arguments:
  PDF_PATH              Path to your PDF file

Options:
  -o, --output DIR      Output directory (default: ./output)
  -t, --title TITLE     Manga title for cover page
  -a, --author AUTHOR   Author name for cover page
  --sample              Create and use a sample story for testing
  --test                Run component tests
  -h, --help            Show help message
```

### Configuration

Edit your `.env` file to customize settings:

```env
# Required
BLACKBOX_API_KEY=your_api_key_here

# Optional customizations
IMAGE_WIDTH=1024
IMAGE_HEIGHT=768
FONT_SIZE_DIALOGUE=16
MAX_SCENE_LENGTH=500
```

## 🎯 How It Works

### 1. PDF Processing
- Extracts text using `pdfplumber` and `PyPDF2`
- Cleans and normalizes the extracted content
- Handles various PDF formats and layouts

### 2. Story Analysis
- Uses NLTK for natural language processing
- Identifies characters, dialogue, and scene breaks
- Analyzes emotions and speech patterns
- Determines scene settings and moods

### 3. Image Generation
- Creates detailed prompts for each scene
- Uses BlackBox API with Gemini-2.5-Pro model
- Generates Studio Ghibli-style artwork
- Incorporates character descriptions and settings

### 4. Manga Composition
- Creates dialogue bubbles with appropriate styling
- Positions bubbles to avoid overlapping
- Combines multiple scenes into manga pages
- Adds borders and professional layout

## 📁 Project Structure

```
pdf-to-manga-converter/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── pdf_processor.py       # PDF text extraction
├── story_analyzer.py      # Story analysis and scene detection
├── image_generator.py     # AI image generation
├── manga_composer.py      # Final manga composition
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── output/               # Generated manga files (created automatically)
    ├── images/           # Individual scene images
    ├── manga_page_001.png
    ├── manga_page_002.png
    └── ...
```

## 🎨 Output Examples

The converter generates:

- **Individual scene images** - Ghibli-style artwork for each scene
- **Manga pages** - Professional layouts with dialogue bubbles
- **Title page** - Custom cover with title and author
- **Complete manga** - Ready-to-read visual story

## ⚙️ Advanced Configuration

### Custom Fonts

Place custom fonts in `assets/fonts/`:
- `dialogue.ttf` - For character dialogue
- `narration.ttf` - For narrative text
- `title.ttf` - For titles and headers

### Scene Detection

Customize scene splitting in `config.py`:
```python
MAX_SCENE_LENGTH = 500  # Maximum characters per scene
MIN_SCENE_LENGTH = 50   # Minimum characters per scene
```

### Image Settings

Adjust image generation:
```python
IMAGE_WIDTH = 1024      # Generated image width
IMAGE_HEIGHT = 768      # Generated image height
GHIBLI_STYLE_PROMPT = "Studio Ghibli style, anime art..."
```

## 🔧 Troubleshooting

### Common Issues

**"BLACKBOX_API_KEY is required"**
- Make sure you've created a `.env` file with your API key
- Check that the key is valid and has sufficient credits

**"Could not extract any text from the PDF file"**
- Ensure the PDF contains readable text (not just images)
- Try a different PDF or check if it's password-protected

**"Error calling BlackBox API"**
- Check your internet connection
- Verify your API key is correct and active
- Check if you've exceeded rate limits

**Font-related errors**
- The system will fall back to default fonts if custom fonts aren't found
- Install system fonts or place custom fonts in `assets/fonts/`

### Performance Tips

- **Large PDFs**: The converter processes scenes sequentially. Large stories may take time.
- **API Limits**: Be aware of BlackBox API rate limits and costs.
- **Memory Usage**: Large images and many scenes can use significant memory.

## 🧪 Testing

Run the built-in tests:

```bash
# Test all components
python main.py --test

# Test with sample story
python main.py --sample
```

## 📝 Example Workflow

1. **Prepare your PDF story**
   - Ensure it's a text-based PDF (not scanned images)
   - Stories with clear dialogue work best

2. **Run the converter**
   ```bash
   python main.py "my_story.pdf" --title "My Adventure" --author "Me"
   ```

3. **Check the output**
   - Individual images in `output/images/`
   - Manga pages as `manga_page_001.png`, etc.
   - Title page as `manga_title_page.png`

4. **Enjoy your manga!**
   - View the pages in order
   - Share with friends
   - Print for physical reading

## 🤝 Contributing

This project is designed to be extensible:

- **Add new image generators** - Support for different AI services
- **Improve text analysis** - Better character and scene detection
- **Enhance layouts** - More manga panel arrangements
- **Add effects** - Sound effects, motion lines, etc.

## 📄 License

This project is open source. Please respect the terms of service of any AI APIs you use.

## 🙏 Acknowledgments

- **Studio Ghibli** - For inspiring the art style
- **BlackBox AI** - For providing the image generation API
- **NLTK** - For natural language processing capabilities
- **Pillow** - For image processing and manipulation

---

**Happy manga creating!** 🎨📚✨

Transform your stories into visual adventures and bring your imagination to life!

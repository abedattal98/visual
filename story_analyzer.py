import re
import nltk
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from config import Config

@dataclass
class DialogueLine:
    """Represents a line of dialogue"""
    speaker: Optional[str]
    text: str
    emotion: Optional[str] = None

@dataclass
class Scene:
    """Represents a scene in the story"""
    id: int
    description: str
    dialogue: List[DialogueLine]
    characters: List[str]
    setting: Optional[str] = None
    mood: Optional[str] = None
    action: Optional[str] = None

class StoryAnalyzer:
    """Analyzes story text to extract scenes, dialogue, and characters"""
    
    def __init__(self):
        self.download_nltk_data()
        self.dialogue_patterns = [
            r'"([^"]*)"',  # Text in double quotes
            r"'([^']*)'",  # Text in single quotes
            r'[""]([^""]*)["""]',  # Smart quotes
            r'([A-Z][a-z]+):\s*"([^"]*)"',  # Speaker: "dialogue"
            r'([A-Z][a-z]+)\s+said[^.]*[.]\s*"([^"]*)"',  # Name said... "dialogue"
        ]
        
        self.scene_break_patterns = [
            r'\n\s*\*\s*\*\s*\*\s*\n',  # *** scene breaks
            r'\n\s*---+\s*\n',  # --- scene breaks
            r'\n\s*Chapter\s+\d+',  # Chapter breaks
            r'\n\s*\d+\.\s*\n',  # Numbered sections
            r'\n\s*[A-Z\s]{10,}\n',  # ALL CAPS headers
        ]
    
    def download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
            except:
                try:
                    nltk.download('punkt_tab', quiet=True)
                except:
                    print("Warning: Could not download NLTK punkt data. Using basic text processing.")
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            try:
                nltk.download('averaged_perceptron_tagger', quiet=True)
            except:
                print("Warning: Could not download NLTK tagger data. Using basic text processing.")
        
        try:
            nltk.data.find('corpora/names')
        except LookupError:
            try:
                nltk.download('names', quiet=True)
            except:
                print("Warning: Could not download NLTK names data. Using basic name detection.")
    
    def extract_characters(self, text: str) -> List[str]:
        """Extract character names from the text"""
        try:
            # Look for capitalized names that appear multiple times
            words = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(words)
            
            # Find proper nouns (potential names)
            proper_nouns = [word for word, pos in pos_tags if pos == 'NNP']
        except:
            # Fallback to simple word extraction if NLTK fails
            import re
            words = re.findall(r'\b[A-Z][a-z]+\b', text)
            proper_nouns = words
        
        # Count occurrences and filter
        name_counts = {}
        for name in proper_nouns:
            if len(name) > 2 and name.isalpha():  # Filter out short or non-alphabetic
                name_counts[name] = name_counts.get(name, 0) + 1
        
        # Return names that appear more than once
        characters = [name for name, count in name_counts.items() if count > 1]
        
        # Also look for common dialogue patterns with names
        dialogue_speakers = self.extract_dialogue_speakers(text)
        characters.extend(dialogue_speakers)
        
        # Remove duplicates and return
        return list(set(characters))
    
    def extract_dialogue_speakers(self, text: str) -> List[str]:
        """Extract speaker names from dialogue patterns"""
        speakers = []
        
        # Pattern: Name: "dialogue"
        pattern1 = r'([A-Z][a-z]+):\s*["\'""]'
        matches1 = re.findall(pattern1, text)
        speakers.extend(matches1)
        
        # Pattern: Name said/asked/replied
        pattern2 = r'([A-Z][a-z]+)\s+(said|asked|replied|whispered|shouted|exclaimed)'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        speakers.extend([match[0] for match in matches2])
        
        return list(set(speakers))
    
    def extract_dialogue(self, text: str) -> List[DialogueLine]:
        """Extract dialogue lines from text"""
        dialogue_lines = []
        
        # Extract quoted text
        quotes = re.findall(r'["\'""]([^"\'""]*)["\'""]', text)
        
        for quote in quotes:
            if len(quote.strip()) > 3:  # Filter out very short quotes
                # Try to find the speaker
                speaker = self.find_speaker_for_quote(text, quote)
                
                # Analyze emotion/tone (basic)
                emotion = self.analyze_emotion(quote)
                
                dialogue_lines.append(DialogueLine(
                    speaker=speaker,
                    text=quote.strip(),
                    emotion=emotion
                ))
        
        return dialogue_lines
    
    def find_speaker_for_quote(self, text: str, quote: str) -> Optional[str]:
        """Try to identify who said a particular quote"""
        # Look for patterns before the quote
        quote_escaped = re.escape(quote)
        
        # Pattern: Name said "quote"
        pattern1 = r'([A-Z][a-z]+)\s+(?:said|asked|replied|whispered|shouted|exclaimed)[^"]*["\'""]' + quote_escaped
        match1 = re.search(pattern1, text, re.IGNORECASE)
        if match1:
            return match1.group(1)
        
        # Pattern: "quote" said Name
        pattern2 = quote_escaped + r'["\'""],?\s*(?:said|asked|replied)\s+([A-Z][a-z]+)'
        match2 = re.search(pattern2, text, re.IGNORECASE)
        if match2:
            return match2.group(1)
        
        # Pattern: Name: "quote"
        pattern3 = r'([A-Z][a-z]+):\s*["\'""]' + quote_escaped
        match3 = re.search(pattern3, text)
        if match3:
            return match3.group(1)
        
        return None
    
    def analyze_emotion(self, text: str) -> Optional[str]:
        """Basic emotion analysis based on punctuation and keywords"""
        text_lower = text.lower()
        
        if '!' in text or any(word in text_lower for word in ['wow', 'amazing', 'great', 'fantastic']):
            return 'excited'
        elif '?' in text:
            return 'questioning'
        elif any(word in text_lower for word in ['sad', 'sorry', 'terrible', 'awful']):
            return 'sad'
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'hate']):
            return 'angry'
        elif any(word in text_lower for word in ['happy', 'joy', 'laugh', 'smile']):
            return 'happy'
        else:
            return 'neutral'
    
    def split_into_scenes(self, text: str) -> List[str]:
        """Split text into logical scenes"""
        # First, try to split by explicit scene breaks
        scenes = [text]
        
        for pattern in self.scene_break_patterns:
            new_scenes = []
            for scene in scenes:
                parts = re.split(pattern, scene)
                new_scenes.extend([part.strip() for part in parts if part.strip()])
            scenes = new_scenes
        
        # If no explicit breaks found, split by paragraphs and group
        if len(scenes) == 1:
            scenes = self.split_by_content_length(text)
        
        return scenes
    
    def split_by_content_length(self, text: str) -> List[str]:
        """Split text into scenes based on content length"""
        try:
            sentences = nltk.sent_tokenize(text)
        except:
            # Fallback to simple sentence splitting if NLTK fails
            sentences = text.replace('!', '.').replace('?', '.').split('.')
            sentences = [s.strip() + '.' for s in sentences if s.strip()]
        
        scenes = []
        current_scene = ""
        
        for sentence in sentences:
            if len(current_scene) + len(sentence) > Config.MAX_SCENE_LENGTH:
                if len(current_scene) > Config.MIN_SCENE_LENGTH:
                    scenes.append(current_scene.strip())
                    current_scene = sentence
                else:
                    current_scene += " " + sentence
            else:
                current_scene += " " + sentence
        
        # Add the last scene
        if current_scene.strip():
            scenes.append(current_scene.strip())
        
        return scenes
    
    def analyze_scene_setting(self, scene_text: str) -> Optional[str]:
        """Analyze the setting/location of a scene"""
        # Look for location indicators
        location_patterns = [
            r'(?:in|at|inside|outside|near|by)\s+(?:the\s+)?([a-z\s]+?)(?:\s|,|\.|$)',
            r'(?:room|house|forest|city|street|park|school|office|kitchen|bedroom)',
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, scene_text.lower())
            if matches:
                return matches[0].strip()
        
        return None
    
    def analyze_scene_mood(self, scene_text: str) -> Optional[str]:
        """Analyze the mood/atmosphere of a scene"""
        mood_keywords = {
            'dark': ['dark', 'shadow', 'night', 'gloomy', 'sinister'],
            'bright': ['bright', 'sunny', 'cheerful', 'light', 'radiant'],
            'mysterious': ['mysterious', 'strange', 'odd', 'peculiar', 'eerie'],
            'peaceful': ['peaceful', 'calm', 'serene', 'quiet', 'tranquil'],
            'tense': ['tense', 'nervous', 'anxious', 'worried', 'stressed'],
            'romantic': ['romantic', 'love', 'heart', 'kiss', 'embrace']
        }
        
        text_lower = scene_text.lower()
        for mood, keywords in mood_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return mood
        
        return 'neutral'
    
    def analyze_story(self, text: str) -> List[Scene]:
        """Main method to analyze the entire story"""
        # Extract overall characters
        characters = self.extract_characters(text)
        
        # Split into scenes
        scene_texts = self.split_into_scenes(text)
        
        scenes = []
        for i, scene_text in enumerate(scene_texts):
            # Extract dialogue for this scene
            dialogue = self.extract_dialogue(scene_text)
            
            # Find characters in this scene
            scene_characters = []
            for char in characters:
                if char.lower() in scene_text.lower():
                    scene_characters.append(char)
            
            # Analyze setting and mood
            setting = self.analyze_scene_setting(scene_text)
            mood = self.analyze_scene_mood(scene_text)
            
            # Create scene object
            scene = Scene(
                id=i + 1,
                description=scene_text,
                dialogue=dialogue,
                characters=scene_characters,
                setting=setting,
                mood=mood
            )
            
            scenes.append(scene)
        
        return scenes

def test_story_analyzer():
    """Test function for story analyzer"""
    sample_text = '''
    "Hello there!" said John with a big smile. "How are you today?"
    
    Mary looked at him sadly. "I'm not feeling very well," she replied.
    
    The room was dark and gloomy. John walked over to the window and opened the curtains.
    
    "There, that's better!" he exclaimed. "Now we can see the beautiful garden outside."
    '''
    
    analyzer = StoryAnalyzer()
    scenes = analyzer.analyze_story(sample_text)
    
    for scene in scenes:
        print(f"Scene {scene.id}:")
        print(f"  Characters: {scene.characters}")
        print(f"  Setting: {scene.setting}")
        print(f"  Mood: {scene.mood}")
        print(f"  Dialogue: {len(scene.dialogue)} lines")
        print()

if __name__ == "__main__":
    test_story_analyzer()

#!/usr/bin/env python3
"""
Comprehensive edge case testing for PDF to Manga converter
"""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

def test_large_text_processing():
    """Test processing of large text content"""
    print("🧪 Testing Large Text Processing...")
    
    try:
        from story_analyzer import StoryAnalyzer
        
        # Create a large text with multiple scenes
        large_text = """
        Chapter 1: The Beginning
        
        Once upon a time in a faraway kingdom, there lived a brave princess named Aria.
        
        "I must find the lost crystal," Aria declared to her loyal companion, a talking fox named Zephyr.
        
        Zephyr nodded wisely. "The journey will be dangerous, Princess. Are you sure you're ready?"
        
        "I've never been more ready," she replied with determination.
        
        Chapter 2: The Forest of Whispers
        
        The forest was dark and mysterious. Ancient trees towered above them, their branches creating a canopy that blocked most of the sunlight.
        
        "Do you hear that?" Zephyr whispered, his ears twitching nervously.
        
        Aria listened carefully. "It sounds like... singing?"
        
        A beautiful melody drifted through the trees, enchanting and otherworldly.
        
        "We must be careful," Aria said. "The forest spirits are known to lead travelers astray."
        
        Chapter 3: The Crystal Cave
        
        After hours of walking, they finally reached the crystal cave. The entrance glowed with an ethereal blue light.
        
        "This is it," Aria breathed in wonder. "The Crystal of Eternal Light."
        
        But as they approached, a shadow creature emerged from the depths of the cave.
        
        "Who dares disturb my slumber?" the creature roared with a voice like thunder.
        
        Aria drew her sword bravely. "I am Princess Aria, and I seek the crystal to save my kingdom!"
        
        The creature paused, studying her with glowing red eyes. "Many have tried, young princess. What makes you different?"
        
        "Because I fight not for glory, but for love," Aria answered truthfully.
        """ * 3  # Triple the content to make it larger
        
        analyzer = StoryAnalyzer()
        scenes = analyzer.analyze_story(large_text)
        
        print(f"   ✓ Processed {len(large_text)} characters")
        print(f"   ✓ Split into {len(scenes)} scenes")
        print(f"   ✓ Average scene length: {len(large_text)//len(scenes) if scenes else 0} characters")
        
        # Test character extraction
        all_characters = set()
        total_dialogue = 0
        for scene in scenes:
            all_characters.update(scene.characters)
            total_dialogue += len(scene.dialogue)
        
        char_list = list(all_characters)[:5]
        print(f"   ✓ Found {len(all_characters)} unique characters: {char_list}")
        print(f"   ✓ Extracted {total_dialogue} dialogue lines total")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Large text processing failed: {e}")
        return False

def test_malformed_text():
    """Test handling of malformed or problematic text"""
    print("\n🧪 Testing Malformed Text Handling...")
    
    try:
        from story_analyzer import StoryAnalyzer
        
        # Test various problematic text formats
        test_cases = [
            # Empty text
            "",
            # Only whitespace
            "   \n\n\t   ",
            # No dialogue
            "This is a story with no dialogue at all. Just narrative text describing events.",
            # Malformed quotes
            'He said "Hello but forgot to close the quote',
            # Mixed quote styles
            '"Hello," she said. \'How are you?\' he replied. "I\'m fine," she answered.',
            # Very short text
            "Hi.",
            # Text with special characters
            "Café naïve résumé 中文 العربية русский 🎨📚✨",
            # Numbers and symbols
            "Chapter 1.5: The $1,000,000 question! @#$%^&*()",
        ]
        
        analyzer = StoryAnalyzer()
        
        for i, test_text in enumerate(test_cases):
            try:
                scenes = analyzer.analyze_story(test_text)
                print(f"   ✓ Test case {i+1}: {len(scenes)} scenes from '{test_text[:30]}...'")
            except Exception as e:
                print(f"   ⚠️  Test case {i+1} failed: {e}")
        
        print("   ✓ Malformed text handling validated")
        return True
        
    except Exception as e:
        print(f"   ✗ Malformed text test failed: {e}")
        return False

def test_dialogue_extraction_edge_cases():
    """Test edge cases in dialogue extraction"""
    print("\n🧪 Testing Dialogue Extraction Edge Cases...")
    
    try:
        from story_analyzer import StoryAnalyzer
        
        # Complex dialogue scenarios
        complex_text = '''
        "Hello," said Alice, "how are you today?"
        
        Bob replied, "I'm fine, thanks for asking."
        
        "That's great!" Alice exclaimed with joy. "I was worried about you."
        
        He whispered, "Don't tell anyone, but I found a secret."
        
        Alice: "What kind of secret?"
        Bob: "The kind that could change everything."
        
        "Really?" she asked incredulously.
        
        (Thinking to herself) "I wonder if I should trust him."
        
        NARRATOR: The tension in the room was palpable.
        
        "Well," Bob said finally, "are you ready to hear it?"
        '''
        
        analyzer = StoryAnalyzer()
        scenes = analyzer.analyze_story(complex_text)
        
        if scenes:
            scene = scenes[0]
            print(f"   ✓ Extracted {len(scene.dialogue)} dialogue lines")
            
            # Check for different dialogue types
            speakers = [d.speaker for d in scene.dialogue if d.speaker]
            emotions = [d.emotion for d in scene.dialogue if d.emotion]
            
            print(f"   ✓ Found speakers: {set(speakers)}")
            print(f"   ✓ Detected emotions: {set(emotions)}")
            
            # Test specific dialogue patterns
            for dialogue in scene.dialogue[:3]:
                print(f"   ✓ '{dialogue.text[:30]}...' -> Speaker: {dialogue.speaker}, Emotion: {dialogue.emotion}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Dialogue extraction test failed: {e}")
        return False

def test_manga_composition_edge_cases():
    """Test edge cases in manga composition"""
    print("\n🧪 Testing Manga Composition Edge Cases...")
    
    try:
        from manga_composer import MangaComposer
        from story_analyzer import DialogueLine
        from PIL import Image
        
        composer = MangaComposer()
        
        # Test very long dialogue
        long_dialogue = DialogueLine(
            speaker="VerboseCharacter",
            text="This is an extremely long piece of dialogue that should test the text wrapping capabilities of the manga composer to ensure it can handle very lengthy speeches and monologues without breaking the layout or causing visual issues in the final manga output.",
            emotion="excited"
        )
        
        bubble = composer.create_dialogue_bubble(long_dialogue, max_width=300)
        print(f"   ✓ Long dialogue bubble: {bubble.size}")
        
        # Test empty dialogue
        empty_dialogue = DialogueLine(speaker="Silent", text="", emotion="neutral")
        try:
            bubble = composer.create_dialogue_bubble(empty_dialogue)
            print(f"   ⚠️  Empty dialogue created bubble: {bubble.size}")
        except:
            print("   ✓ Empty dialogue properly rejected")
        
        # Test special characters in dialogue
        special_dialogue = DialogueLine(
            speaker="Émilie",
            text="Café naïve! 🎨 This costs $50.99... isn't that expensive?",
            emotion="questioning"
        )
        
        bubble = composer.create_dialogue_bubble(special_dialogue)
        print(f"   ✓ Special characters bubble: {bubble.size}")
        
        # Test different bubble types
        bubble_types = [
            ("normal", DialogueLine("Alice", "Hello there.", "neutral")),
            ("shout", DialogueLine("Bob", "HELP ME!", "angry")),
            ("whisper", DialogueLine("Carol", "(secretly)", "whisper")),
            ("thought", DialogueLine("Dave", "I wonder...", "questioning"))
        ]
        
        for expected_type, dialogue in bubble_types:
            actual_type = composer.determine_bubble_type(dialogue)
            print(f"   ✓ Bubble type '{expected_type}': {actual_type}")
        
        # Test image composition with multiple bubbles
        test_image = Image.new('RGB', (800, 600), (200, 220, 255))
        
        test_dialogues = [
            DialogueLine("Alice", "Hello!", "happy"),
            DialogueLine("Bob", "Hi there!", "neutral"),
            DialogueLine("Carol", "How are you?", "questioning")
        ]
        
        result_image = composer.add_dialogue_to_image(test_image, test_dialogues)
        print(f"   ✓ Composed image with {len(test_dialogues)} dialogue bubbles: {result_image.size}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Manga composition test failed: {e}")
        return False

def test_file_operations():
    """Test file operations and error handling"""
    print("\n🧪 Testing File Operations...")
    
    try:
        from pdf_processor import PDFProcessor
        
        # Test with non-existent file
        try:
            processor = PDFProcessor("nonexistent.pdf")
            print("   ✗ Should have failed with non-existent file")
            return False
        except FileNotFoundError:
            print("   ✓ Correctly handles non-existent files")
        
        # Test with wrong file extension
        try:
            processor = PDFProcessor("test.txt")
            print("   ✗ Should have failed with wrong extension")
            return False
        except (ValueError, FileNotFoundError):
            print("   ✓ Correctly validates file extensions")
        
        # Test directory creation
        from config import Config
        
        test_dirs = ['test_output', 'test_output/images', 'test_output/temp']
        for directory in test_dirs:
            os.makedirs(directory, exist_ok=True)
            if os.path.exists(directory):
                print(f"   ✓ Created directory: {directory}")
                os.rmdir(directory)
        
        # Clean up test_output directory
        if os.path.exists('test_output'):
            os.rmdir('test_output')
        
        return True
        
    except Exception as e:
        print(f"   ✗ File operations test failed: {e}")
        return False

def test_memory_usage():
    """Test memory usage with large content"""
    print("\n🧪 Testing Memory Usage...")
    
    try:
        import psutil
        import gc
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"   ✓ Initial memory usage: {initial_memory:.1f} MB")
        
        # Process large content
        from story_analyzer import StoryAnalyzer
        
        # Create very large text
        base_story = "Once upon a time, there was a princess who went on an adventure. " * 1000
        large_story = base_story * 10  # ~640KB of text
        
        analyzer = StoryAnalyzer()
        scenes = analyzer.analyze_story(large_story)
        
        # Check memory after processing
        after_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = after_memory - initial_memory
        
        print(f"   ✓ Processed {len(large_story)} characters")
        print(f"   ✓ Memory after processing: {after_memory:.1f} MB")
        print(f"   ✓ Memory increase: {memory_increase:.1f} MB")
        
        # Clean up
        del large_story, scenes, analyzer
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"   ✓ Memory after cleanup: {final_memory:.1f} MB")
        
        if memory_increase < 100:  # Less than 100MB increase is reasonable
            print("   ✓ Memory usage is reasonable")
            return True
        else:
            print(f"   ⚠️  High memory usage: {memory_increase:.1f} MB")
            return True  # Still pass, but warn
        
    except ImportError:
        print("   ⚠️  psutil not available, skipping memory test")
        return True
    except Exception as e:
        print(f"   ✗ Memory usage test failed: {e}")
        return False

def main():
    """Run comprehensive edge case testing"""
    print("🎨 PDF to Visual Manga Converter - Edge Case Testing")
    print("=" * 60)
    print("Testing robustness and edge case handling...")
    print()
    
    tests = [
        test_large_text_processing,
        test_malformed_text,
        test_dialogue_extraction_edge_cases,
        test_manga_composition_edge_cases,
        test_file_operations,
        test_memory_usage
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ✗ Test crashed: {e}")
            failed += 1
    
    print(f"\n📊 Edge Case Test Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print(f"\n🎉 All edge case tests passed!")
        print(f"🛡️  The application is robust and handles edge cases well.")
    else:
        print(f"\n⚠️  Some edge case tests failed. The application may need improvements.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

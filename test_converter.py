#!/usr/bin/env python3
"""
Test script for the PDF to Visual Manga Converter
This script demonstrates the functionality with a sample story.
"""

import os
import sys
from pathlib import Path

def create_sample_story():
    """Create a sample story file for testing"""
    sample_story = """
The Enchanted Forest Adventure

Chapter 1: The Discovery

Luna had always been curious about the mysterious forest at the edge of her village. The ancient trees seemed to whisper secrets in the wind, and strange lights danced between their branches at night.

"I wonder what's really in there," Luna said to herself as she stood at the forest's edge.

Her grandmother had always warned her: "That forest is full of magic, child. Only those with pure hearts can safely enter."

But Luna's curiosity was stronger than her fear. She took a deep breath and stepped into the forest.

Chapter 2: The Meeting

As Luna walked deeper into the forest, the trees grew taller and the air shimmered with an otherworldly glow. Suddenly, a small creature appeared on the path ahead.

"Hello there!" called out a tiny voice.

Luna gasped. Before her stood a fox with silver fur that sparkled like starlight. "You can talk!"

The fox laughed, a sound like tiny silver bells. "In this forest, all creatures can speak to those who listen with their hearts. I'm Kitsune, guardian of this realm."

"I'm Luna," she replied, her eyes wide with wonder. "Is this place really magical?"

"More magical than you can imagine," Kitsune said with a mysterious smile. "But magic comes with responsibility. Are you ready for an adventure?"

Chapter 3: The Challenge

Kitsune led Luna to a clearing where a crystal fountain bubbled with water that glowed like liquid moonlight.

"This is the Heart of the Forest," Kitsune explained. "But something is wrong. The water has been losing its glow."

Luna noticed that indeed, parts of the fountain seemed dim and lifeless. "What happened?"

"A shadow creature has been stealing the forest's magic," Kitsune said sadly. "Only someone with a pure heart can restore the light."

Luna felt a surge of determination. "Tell me what I need to do!"

"You must find three magical crystals hidden in the forest," Kitsune explained. "The Crystal of Courage, the Crystal of Kindness, and the Crystal of Wisdom. But beware - the shadow creature will try to stop you."

Chapter 4: The Quest Begins

Luna set off on her quest, with Kitsune as her guide. Their first destination was the Grove of Courage, where the red crystal was hidden.

As they approached the grove, the air grew cold and dark shadows began to move between the trees.

"I'm scared," Luna whispered.

"Courage isn't about not being afraid," Kitsune said gently. "It's about doing what's right even when you are afraid."

Luna nodded and stepped forward bravely. "I won't let the forest lose its magic!"

Suddenly, a creature made of pure shadow emerged from the darkness. Its eyes glowed red and its voice was like the sound of dying leaves.

"Turn back, little girl," the shadow hissed. "This forest will be mine!"

But Luna stood her ground. "No! This forest belongs to all the creatures who live here. I won't let you destroy it!"

Her brave words caused a warm light to emanate from her heart, and the first crystal - the Crystal of Courage - appeared in her hands, glowing bright red.

The shadow creature shrieked and retreated deeper into the forest.

Chapter 5: The Return of Light

With all three crystals in hand - Courage, Kindness, and Wisdom - Luna returned to the Heart of the Forest. The fountain was now completely dark, and Kitsune looked very weak.

"Hurry, Luna," Kitsune whispered. "The forest is dying."

Luna approached the fountain and held the three crystals high. "I wish for the forest's magic to return, so all creatures can live here in peace and happiness!"

The crystals began to glow brighter and brighter, then dissolved into pure light that flowed into the fountain. Immediately, the water began to sparkle and glow again, brighter than ever before.

The entire forest came alive with renewed magic. Flowers bloomed, birds sang, and all the forest creatures emerged to celebrate.

"You did it, Luna!" Kitsune exclaimed, now glowing with renewed energy. "You saved our home!"

Luna smiled, feeling proud and happy. She had discovered that the greatest magic of all was the magic within her own heart.

And from that day forward, Luna became the forest's protector, visiting often to ensure that magic and wonder would always flourish there.

The End
    """
    
    # Save as text file (simulating PDF content)
    sample_path = "sample_story.txt"
    with open(sample_path, 'w', encoding='utf-8') as f:
        f.write(sample_story)
    
    return sample_path

def test_components():
    """Test individual components"""
    print("🧪 Testing PDF to Manga Converter Components\n")
    
    # Test 1: Story Analysis
    print("1. Testing Story Analyzer...")
    try:
        from story_analyzer import StoryAnalyzer
        
        sample_text = """
        "Hello there!" said Alice with a big smile. "How are you today?"
        
        Bob looked at her sadly. "I'm not feeling very well," he replied.
        
        The room was dark and gloomy. Alice walked over to the window and opened the curtains.
        
        "There, that's better!" she exclaimed. "Now we can see the beautiful garden outside."
        """
        
        analyzer = StoryAnalyzer()
        scenes = analyzer.analyze_story(sample_text)
        
        print(f"   ✓ Analyzed story into {len(scenes)} scenes")
        print(f"   ✓ Found characters: {scenes[0].characters if scenes else 'None'}")
        print(f"   ✓ Detected dialogue lines: {len(scenes[0].dialogue) if scenes else 0}")
        
    except Exception as e:
        print(f"   ✗ Story analyzer test failed: {e}")
    
    # Test 2: Image Generator Setup
    print("\n2. Testing Image Generator Setup...")
    try:
        from image_generator import ImageGenerator
        from story_analyzer import Scene, DialogueLine
        
        # Create test scene
        test_scene = Scene(
            id=1,
            description="A magical forest with glowing flowers",
            dialogue=[DialogueLine(speaker="Luna", text="What a beautiful place!")],
            characters=["Luna"],
            setting="magical forest",
            mood="peaceful"
        )
        
        generator = ImageGenerator()
        prompt = generator.create_scene_prompt(test_scene)
        
        print(f"   ✓ Image generator initialized")
        print(f"   ✓ Generated prompt: {prompt[:80]}...")
        
    except Exception as e:
        print(f"   ✗ Image generator test failed: {e}")
    
    # Test 3: Manga Composer
    print("\n3. Testing Manga Composer...")
    try:
        from manga_composer import MangaComposer
        from story_analyzer import DialogueLine
        
        composer = MangaComposer()
        test_dialogue = DialogueLine(speaker="Alice", text="Hello world!", emotion="happy")
        bubble = composer.create_dialogue_bubble(test_dialogue)
        
        print(f"   ✓ Manga composer initialized")
        print(f"   ✓ Created dialogue bubble: {bubble.size}")
        
    except Exception as e:
        print(f"   ✗ Manga composer test failed: {e}")
    
    print("\n✅ Component testing completed!")

def main():
    """Main test function"""
    print("🎨 PDF to Visual Manga Converter - Test Suite")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  Warning: .env file not found!")
        print("   Create a .env file with your BLACKBOX_API_KEY to test image generation.")
        print("   You can copy .env.example and add your API key.")
        print()
    
    # Test components
    test_components()
    
    # Create sample story
    print(f"\n📝 Creating sample story...")
    sample_path = create_sample_story()
    print(f"   ✓ Created: {sample_path}")
    
    print(f"\n🚀 Ready to test full conversion!")
    print(f"   Run: python main.py {sample_path} --title 'The Enchanted Forest' --author 'Test Author'")
    print(f"   Or:  python main.py --sample")
    
    print(f"\n📚 Project Structure:")
    print(f"   • PDF Processing: Extract text from PDF files")
    print(f"   • Story Analysis: Identify scenes, characters, dialogue")
    print(f"   • Image Generation: Create Ghibli-style artwork")
    print(f"   • Manga Composition: Add dialogue bubbles and layout")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Add your BlackBox API key to .env file")
    print(f"   2. Install dependencies: pip install -r requirements.txt")
    print(f"   3. Run: python main.py --sample")
    print(f"   4. Check output/ directory for generated manga!")

if __name__ == "__main__":
    main()

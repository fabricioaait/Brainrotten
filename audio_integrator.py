import os
import json
import random
import time
from collections import defaultdict

class AudioIntegrator:
    def __init__(self, sounds_folder='static/sounds'):
        self.sounds_folder = sounds_folder
        
        # Create sounds directory if it doesn't exist
        os.makedirs(sounds_folder, exist_ok=True)
        
        # Define sound categories and their files
        # In a real implementation, these would be actual audio files
        self.sound_categories = {
            "water": ["gentle_stream.mp3", "ocean_waves.mp3", "rainfall.mp3"],
            "nature": ["forest_ambience.mp3", "birds_chirping.mp3", "wind_leaves.mp3"],
            "asmr": ["whispers.mp3", "tapping.mp3", "page_turning.mp3", "writing_sounds.mp3"],
            "ambient": ["soft_music.mp3", "gentle_piano.mp3", "ambient_synth.mp3"],
            "calming": ["heartbeat.mp3", "breathing.mp3", "meditation_bells.mp3"]
        }
        
        # Map content types to appropriate sound categories
        self.content_sound_mapping = {
            "technical": ["typing", "ambient"],
            "conceptual": ["asmr", "ambient"],
            "mathematical": ["water", "ambient"],
            "historical": ["page_turning", "nature"],
            "scientific": ["water", "ambient"],
            "literary": ["nature", "asmr"],
            "philosophical": ["ambient", "calming"],
            "instructional": ["asmr", "ambient"]
        }
        
        # Default sound durations (in seconds)
        self.default_durations = {
            "intro": 5,
            "main": 120,
            "outro": 5
        }
    
    def get_sound_for_content(self, content_type, section="main"):
        """Select appropriate sound for a given content type and section"""
        # Default to ambient if content type not found
        categories = self.content_sound_mapping.get(content_type.lower(), ["ambient", "asmr"])
        
        # Select a random category from the appropriate ones
        category = random.choice(categories)
        
        # Select a random sound file from the category
        if category in self.sound_categories and self.sound_categories[category]:
            sound_file = random.choice(self.sound_categories[category])
            return {
                "category": category,
                "file": sound_file,
                "path": os.path.join(self.sounds_folder, sound_file),
                "duration": self.default_durations.get(section, 30)
            }
        
        # Fallback to a default sound
        return {
            "category": "ambient",
            "file": "soft_music.mp3",
            "path": os.path.join(self.sounds_folder, "soft_music.mp3"),
            "duration": self.default_durations.get(section, 30)
        }
    
    def create_sound_plan(self, video_plan):
        """Create a sound plan for a video generation plan"""
        try:
            # Extract video details
            videos = video_plan.get('videos', [])
            
            # Create sound plans for each video
            sound_plans = []
            
            for video in videos:
                video_id = video.get('video_id')
                title = video.get('title', '')
                
                # Determine content type based on title and tags
                content_type = self._determine_content_type(title, video.get('tags', []))
                
                # Create sound segments for each video segment
                segments = video.get('segments', [])
                sound_segments = []
                
                for i, segment in enumerate(segments):
                    segment_type = segment.get('type', 'main')
                    
                    # Get appropriate sound for this segment
                    sound = self.get_sound_for_content(content_type, segment_type)
                    
                    # Create sound segment
                    sound_segment = {
                        "segment_id": f"{video_id}_segment_{i+1}",
                        "segment_type": segment_type,
                        "sound": sound,
                        "volume": 0.3 if segment_type == "main" else 0.4,  # Lower volume during main content
                        "fade_in": 1.0,
                        "fade_out": 1.0
                    }
                    
                    sound_segments.append(sound_segment)
                
                # Create complete sound plan for this video
                sound_plan = {
                    "video_id": video_id,
                    "content_type": content_type,
                    "segments": sound_segments
                }
                
                sound_plans.append(sound_plan)
            
            return {
                "success": True,
                "sound_plans": sound_plans
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _determine_content_type(self, title, tags):
        """Determine the content type based on title and tags"""
        # Convert everything to lowercase for matching
        title_lower = title.lower()
        tags_lower = [tag.lower() for tag in tags]
        
        # Define keywords for different content types
        content_keywords = {
            "technical": ["code", "programming", "technical", "technology", "software", "hardware"],
            "conceptual": ["concept", "theory", "framework", "model", "paradigm"],
            "mathematical": ["math", "equation", "formula", "calculation", "number"],
            "historical": ["history", "timeline", "era", "period", "ancient", "modern"],
            "scientific": ["science", "experiment", "research", "discovery", "hypothesis"],
            "literary": ["literature", "book", "novel", "poem", "author", "writing"],
            "philosophical": ["philosophy", "ethics", "moral", "existence", "consciousness"],
            "instructional": ["how to", "guide", "tutorial", "instruction", "step by step"]
        }
        
        # Count matches for each content type
        matches = defaultdict(int)
        
        for content_type, keywords in content_keywords.items():
            # Check title for keywords
            for keyword in keywords:
                if keyword in title_lower:
                    matches[content_type] += 2  # Title matches are weighted more
            
            # Check tags for keywords
            for tag in tags_lower:
                for keyword in keywords:
                    if keyword in tag:
                        matches[content_type] += 1
        
        # Find the content type with the most matches
        if matches:
            best_match = max(matches.items(), key=lambda x: x[1])
            return best_match[0]
        
        # Default to conceptual if no matches found
        return "conceptual"
    
    def integrate_sound_with_video(self, video_path, sound_plan):
        """
        Integrate sound with a video based on the sound plan
        In a real implementation, this would use a library like moviepy
        """
        try:
            # Extract sound segments
            segments = sound_plan.get('segments', [])
            
            # In a real implementation, this would:
            # 1. Load the video
            # 2. Load the sound files
            # 3. Apply volume adjustments, fades, etc.
            # 4. Combine the video and audio
            # 5. Save the result
            
            # For the demo, we'll just return success
            return {
                "success": True,
                "video_id": sound_plan.get('video_id'),
                "video_path": video_path,
                "sound_segments": len(segments)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def mock_create_sound_files(self):
        """Create mock sound files for development purposes"""
        # Create placeholder files for each sound category
        for category, files in self.sound_categories.items():
            for file in files:
                file_path = os.path.join(self.sounds_folder, file)
                
                # Create an empty file if it doesn't exist
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        f.write(f"# Placeholder for {category} sound: {file}")
        
        return {
            "success": True,
            "message": "Mock sound files created",
            "files_created": sum(len(files) for files in self.sound_categories.values())
        }

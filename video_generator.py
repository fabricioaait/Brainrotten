import os
import json
import random
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class VideoGenerator:
    def __init__(self, upload_folder='uploads', output_folder='static/videos'):
        self.upload_folder = upload_folder
        self.output_folder = output_folder
        
        # Create output directory if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Font settings
        self.font_path = os.path.join('static', 'fonts', 'OpenSans-Regular.ttf')
        
        # Default settings
        self.default_video_width = 1280
        self.default_video_height = 720
        self.default_duration = 3  # seconds per slide
        self.default_fps = 24
        
        # Background colors
        self.bg_colors = [
            (240, 240, 245),  # Light blue-gray
            (245, 240, 245),  # Light purple-gray
            (240, 245, 240),  # Light green-gray
            (245, 245, 240),  # Light yellow-gray
        ]
        
        # Sound files (would be actual files in production)
        self.sound_files = {
            "water": "static/sounds/water.mp3",
            "typing": "static/sounds/typing.mp3",
            "music": "static/sounds/music.mp3",
            "whisper": "static/sounds/whisper.mp3",
            "tapping": "static/sounds/tapping.mp3",
            "nature": "static/sounds/nature.mp3",
            "breathing": "static/sounds/breathing.mp3",
            "heartbeat": "static/sounds/heartbeat.mp3"
        }
    
    def _create_text_frame(self, text, width, height, bg_color=(240, 240, 245), 
                          text_color=(60, 60, 60), font_size=60):
        """Create a single frame with text"""
        # Create a blank image
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Use default system font if custom font not available
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # Calculate text position (centered)
        text_width, text_height = draw.textsize(text, font=font)
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw text
        draw.text(position, text, font=font, fill=text_color)
        
        return np.array(img)
    
    def generate_concept_video(self, concept, video_id, duration=180):
        """Generate a video for a single concept"""
        try:
            # In a real implementation, this would use moviepy to create videos
            # For the demo, we'll just return a success message
            
            # Extract concept details
            title = concept['name']
            description = concept['explanation']
            
            # Set output path
            output_path = os.path.join(self.output_folder, f"{video_id}.mp4")
            
            # In a real implementation, we would create and save the video here
            # For now, we'll just simulate success
            
            return {
                "success": True,
                "video_path": output_path,
                "duration": 180  # 3 minutes
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_videos_from_plan(self, video_plan):
        """Generate videos based on a video generation plan"""
        try:
            # Extract plan details
            filename = video_plan.get('filename', 'document.pdf')
            videos = video_plan.get('videos', [])
            
            # Results to track generated videos
            results = []
            
            # Generate a video for each concept in the plan
            for video_spec in videos:
                video_id = video_spec['video_id']
                title = video_spec['title']
                description = video_spec['description']
                
                # Create a concept object for the video generator
                concept = {
                    'name': title,
                    'explanation': description,
                    'visuals': [segment['visuals'] for segment in video_spec['segments']],
                    'sounds': [segment['audio'] for segment in video_spec['segments']]
                }
                
                # Generate the video
                result = self.generate_concept_video(concept, video_id)
                
                if result['success']:
                    # Add metadata to the result
                    result['title'] = title
                    result['description'] = description
                    result['tags'] = video_spec.get('tags', [])
                
                results.append(result)
            
            # Return the results
            return {
                "success": True,
                "filename": filename,
                "videos": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def mock_generate_videos(self, video_plan):
        """
        Mock video generation for development purposes.
        In a real implementation, this would actually generate videos.
        """
        try:
            # Extract plan details
            filename = video_plan.get('filename', 'document.pdf')
            videos = video_plan.get('videos', [])
            
            # Results to track generated videos
            results = []
            
            # For each video in the plan
            for video_spec in videos:
                video_id = video_spec['video_id']
                title = video_spec['title']
                description = video_spec['description']
                tags = video_spec.get('tags', [])
                
                # Mock video generation result
                mock_result = {
                    "success": True,
                    "video_id": video_id,
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "video_path": f"/static/videos/{video_id}.mp4",  # This would be a real path in production
                    "duration": random.uniform(120, 180),  # Random duration between 2-3 minutes
                    "thumbnail_path": f"/static/img/video-placeholder.jpg"
                }
                
                results.append(mock_result)
                
                # Simulate processing time
                time.sleep(0.5)
            
            # Return the results
            return {
                "success": True,
                "filename": filename,
                "videos": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

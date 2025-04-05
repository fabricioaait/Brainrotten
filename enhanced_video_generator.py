from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import os
import json
import random
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class EnhancedVideoGenerator:
    def __init__(self, upload_folder='uploads', output_folder='static/videos', asmr_folder='static/asmr_videos'):
        self.upload_folder = upload_folder
        self.output_folder = output_folder
        self.asmr_folder = asmr_folder
        
        # Create necessary directories
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(asmr_folder, exist_ok=True)
        
        # Font settings
        self.fonts = [
            'Arial',
            'Helvetica',
            'Verdana',
            'Georgia',
            'Roboto'
        ]
        
        # ASMR video sources (free stock videos)
        self.asmr_video_sources = [
            # Nature scenes
            "https://www.youtube.com/watch?v=qRTVg8HHzUo",  # Relaxing beach waves
            "https://www.youtube.com/watch?v=eI9G5KgIFME",  # Forest stream
            "https://www.youtube.com/watch?v=Ftm2uv7-Ybw",  # Gentle rain
            
            # ASMR specific
            "https://www.youtube.com/watch?v=DWcJFNfaw9c",  # Tapping sounds
            "https://www.youtube.com/watch?v=3h4zimCrC9c",  # Page turning
            "https://www.youtube.com/watch?v=WY0JWpKsdWQ",  # Soft whispers
            
            # Calming backgrounds
            "https://www.youtube.com/watch?v=n_LcVqqHSY8",  # Gradient colors
            "https://www.youtube.com/watch?v=5f5Ig_U2Bpk",  # Slow motion ink in water
            "https://www.youtube.com/watch?v=xNN7iTA57jM",  # Abstract patterns
        ]
        
        # Default settings
        self.default_video_width = 1280
        self.default_video_height = 720
        self.default_duration = 30  # seconds per concept
        self.default_fps = 24
    
    def download_asmr_video(self, url, output_path=None):
        """Download an ASMR video from YouTube"""
        try:
            if not output_path:
                # Generate a filename based on the video ID
                video_id = url.split("v=")[1].split("&")[0]
                output_path = os.path.join(self.asmr_folder, f"{video_id}.mp4")
            
            # Check if we already have this video
            if os.path.exists(output_path):
                return output_path
            
            # Download the video
            from pytube import YouTube
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            stream.download(output_path=self.asmr_folder, filename=os.path.basename(output_path))
            
            return output_path
        
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            # Return a default video path or None
            return None
    
    def get_random_asmr_video(self):
        """Get a random ASMR video from our sources"""
        # Check if we have any downloaded videos
        existing_videos = [os.path.join(self.asmr_folder, f) for f in os.listdir(self.asmr_folder) if f.endswith('.mp4')]
        
        if existing_videos:
            return random.choice(existing_videos)
        
        # If no videos, download one
        url = random.choice(self.asmr_video_sources)
        return self.download_asmr_video(url)
    
    def create_text_overlay(self, text, font=None, font_size=60, color='white', bg_color=None, 
                           width=None, height=None, position='center'):
        """Create a text overlay for the video"""
        if not font:
            font = random.choice(self.fonts)
        
        if not width:
            width = self.default_video_width
        
        if not height:
            height = self.default_video_height
        
        # Create text clip
        text_clip = TextClip(text, fontsize=font_size, font=font, color=color, bg_color=bg_color,
                            size=(width, None), method='caption', align='center')
        
        # Set position
        if position == 'center':
            text_clip = text_clip.set_position('center')
        elif position == 'top':
            text_clip = text_clip.set_position(('center', 50))
        elif position == 'bottom':
            text_clip = text_clip.set_position(('center', height - text_clip.h - 50))
        
        return text_clip
    
    def generate_concept_video(self, concept, video_id, duration=None):
        """Generate a video for a single concept using ASMR background"""
        try:
            # Extract concept details
            title = concept['name']
            description = concept['explanation']
            
            if not duration:
                duration = self.default_duration
            
            # Get a background ASMR video
            asmr_video_path = self.get_random_asmr_video()
            
            if not asmr_video_path or not os.path.exists(asmr_video_path):
                # For development, create a mock video
                return self.mock_generate_concept_video(concept, video_id, duration)
            
            # Load the background video
            background_clip = VideoFileClip(asmr_video_path).subclip(0, duration)
            
            # Resize to our target dimensions
            background_clip = background_clip.resize(height=self.default_video_height)
            
            # Create text overlays
            title_clip = self.create_text_overlay(
                title, 
                font_size=80, 
                position='top'
            ).set_duration(duration)
            
            description_clip = self.create_text_overlay(
                description, 
                font_size=40, 
                position='bottom'
            ).set_duration(duration)
            
            # Combine clips
            final_clip = CompositeVideoClip([
                background_clip, 
                title_clip, 
                description_clip
            ])
            
            # Set output path
            output_path = os.path.join(self.output_folder, f"{video_id}.mp4")
            
            # Write video file
            final_clip.write_videofile(
                output_path, 
                fps=self.default_fps, 
                codec='libx264', 
                audio_codec='aac', 
                temp_audiofile='temp-audio.m4a', 
                remove_temp=True
            )
            
            return {
                "success": True,
                "video_path": output_path,
                "duration": final_clip.duration
            }
            
        except Exception as e:
            print(f"Error generating video: {str(e)}")
            # Fall back to mock generation
            return self.mock_generate_concept_video(concept, video_id, duration)
    
    def mock_generate_concept_video(self, concept, video_id, duration=None):
        """Generate a mock video for development purposes"""
        # Set output path
        output_path = os.path.join(self.output_folder, f"{video_id}.mp4")
        
        # Create a simple video with text
        try:
            # Extract concept details
            title = concept['name']
            description = concept['explanation']
            
            if not duration:
                duration = self.default_duration
            
            # Create a blank background
            width, height = self.default_video_width, self.default_video_height
            color = (30, 30, 60)  # Dark blue background
            
            # Create a clip with the background color
            from moviepy.editor import ColorClip
            background_clip = ColorClip(size=(width, height), color=color).set_duration(duration)
            
            # Create text overlays
            title_clip = self.create_text_overlay(
                title, 
                font_size=80, 
                position='top'
            ).set_duration(duration)
            
            description_clip = self.create_text_overlay(
                description, 
                font_size=40, 
                position='bottom'
            ).set_duration(duration)
            
            # Combine clips
            final_clip = CompositeVideoClip([
                background_clip, 
                title_clip, 
                description_clip
            ])
            
            # Write video file
            final_clip.write_videofile(
                output_path, 
                fps=self.default_fps, 
                codec='libx264', 
                audio_codec='aac', 
                temp_audiofile='temp-audio.m4a', 
                remove_temp=True
            )
            
            return {
                "success": True,
                "video_path": output_path,
                "duration": final_clip.duration,
                "note": "Mock video generated for development"
            }
            
        except Exception as e:
            print(f"Error generating mock video: {str(e)}")
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

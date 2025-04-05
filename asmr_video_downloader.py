import os
import requests
import json
import random
import time
from pytube import YouTube, Search

class ASMRVideoDownloader:
    def __init__(self, download_folder='static/asmr_videos'):
        self.download_folder = download_folder
        
        # Create download directory if it doesn't exist
        os.makedirs(download_folder, exist_ok=True)
        
        # ASMR video categories and search terms
        self.asmr_categories = {
            "nature": [
                "relaxing beach waves asmr",
                "forest stream sounds asmr",
                "gentle rain sounds asmr",
                "waterfall ambient sounds",
                "ocean waves white noise"
            ],
            "tapping": [
                "asmr tapping sounds",
                "gentle tapping relaxation",
                "asmr finger tapping",
                "soft tapping sounds",
                "rhythmic tapping asmr"
            ],
            "writing": [
                "asmr writing sounds",
                "pencil writing on paper sounds",
                "pen writing asmr",
                "writing sounds for studying",
                "asmr note taking sounds"
            ],
            "page_turning": [
                "asmr page turning",
                "book page turning sounds",
                "magazine flipping sounds",
                "paper sounds asmr",
                "gentle page turning"
            ],
            "whispering": [
                "soft whisper asmr",
                "gentle whispering sounds",
                "asmr whispered reading",
                "calming whispers",
                "whispered affirmations"
            ],
            "visual": [
                "satisfying visual asmr",
                "colorful ink in water",
                "abstract patterns relaxing",
                "gradient colors flowing",
                "calming visual loops"
            ]
        }
        
        # Mapping content types to appropriate ASMR categories
        self.content_asmr_mapping = {
            "technical": ["tapping", "writing"],
            "conceptual": ["visual", "whispering"],
            "mathematical": ["writing", "tapping"],
            "historical": ["page_turning", "whispering"],
            "scientific": ["nature", "visual"],
            "literary": ["page_turning", "whispering"],
            "philosophical": ["nature", "whispering"],
            "instructional": ["writing", "tapping"]
        }
        
        # Cache of downloaded videos by category
        self.video_cache = {}
        
        # Initialize cache from existing files
        self._initialize_cache()
    
    def _initialize_cache(self):
        """Initialize the video cache from existing downloaded files"""
        if not os.path.exists(self.download_folder):
            return
            
        for filename in os.listdir(self.download_folder):
            if filename.endswith('.mp4'):
                # Extract category from filename (format: category_videoid.mp4)
                parts = filename.split('_')
                if len(parts) >= 2:
                    category = parts[0]
                    if category in self.asmr_categories:
                        if category not in self.video_cache:
                            self.video_cache[category] = []
                        self.video_cache[category].append(os.path.join(self.download_folder, filename))
    
    def search_asmr_videos(self, search_term, max_results=5):
        """Search for ASMR videos on YouTube"""
        try:
            # Add "no copyright" to search term to find freely usable content
            search_term = f"{search_term} no copyright"
            
            # Search YouTube
            s = Search(search_term)
            results = []
            
            # Get the first max_results results
            count = 0
            for video in s.results:
                if count >= max_results:
                    break
                    
                # Filter for appropriate videos (avoid very short or very long videos)
                if 30 <= video.length <= 600:  # Between 30 seconds and 10 minutes
                    results.append({
                        "id": video.video_id,
                        "title": video.title,
                        "url": f"https://www.youtube.com/watch?v={video.video_id}",
                        "thumbnail": video.thumbnail_url,
                        "duration": video.length
                    })
                    count += 1
            
            return results
            
        except Exception as e:
            print(f"Error searching for videos: {str(e)}")
            return []
    
    def download_video(self, video_url, category, max_resolution=720):
        """Download a video from YouTube"""
        try:
            # Extract video ID from URL
            if "youtube.com" in video_url:
                video_id = video_url.split("v=")[1].split("&")[0]
            elif "youtu.be" in video_url:
                video_id = video_url.split("/")[-1]
            else:
                video_id = video_url  # Assume it's already an ID
            
            # Create filename with category prefix
            filename = f"{category}_{video_id}.mp4"
            output_path = os.path.join(self.download_folder, filename)
            
            # Check if we already have this video
            if os.path.exists(output_path):
                return output_path
            
            # Download the video
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            
            # Get the appropriate stream based on resolution
            stream = None
            if max_resolution:
                # Try to get a stream with the specified resolution or lower
                streams = yt.streams.filter(progressive=True, file_extension='mp4')
                for s in streams:
                    if s.resolution:
                        res = int(s.resolution.replace('p', ''))
                        if res <= max_resolution:
                            stream = s
                            break
            
            # If no suitable stream found, get the highest quality
            if not stream:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            
            # Download the video
            stream.download(output_path=self.download_folder, filename=filename)
            
            # Add to cache
            if category not in self.video_cache:
                self.video_cache[category] = []
            self.video_cache[category].append(output_path)
            
            return output_path
            
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None
    
    def get_asmr_video_for_content(self, content_type):
        """Get an appropriate ASMR video for a given content type"""
        # Get appropriate categories for this content type
        categories = self.content_asmr_mapping.get(content_type.lower(), ["visual", "nature"])
        
        # Select a random category from the appropriate ones
        category = random.choice(categories)
        
        # Check if we have cached videos for this category
        if category in self.video_cache and self.video_cache[category]:
            # Return a random video from the cache
            return random.choice(self.video_cache[category])
        
        # If no cached videos, search and download a new one
        search_term = random.choice(self.asmr_categories[category])
        search_results = self.search_asmr_videos(search_term)
        
        if search_results:
            # Download the first result
            video_url = search_results[0]["url"]
            return self.download_video(video_url, category)
        
        # If all else fails, return None
        return None
    
    def preload_videos_for_all_categories(self, videos_per_category=2):
        """Preload videos for all categories to ensure availability"""
        for category, search_terms in self.asmr_categories.items():
            # Skip if we already have enough videos for this category
            if category in self.video_cache and len(self.video_cache[category]) >= videos_per_category:
                continue
                
            # Search and download videos for this category
            for i in range(videos_per_category):
                if i < len(search_terms):
                    search_term = search_terms[i]
                    search_results = self.search_asmr_videos(search_term, max_results=1)
                    
                    if search_results:
                        video_url = search_results[0]["url"]
                        self.download_video(video_url, category)
                        
                        # Add a small delay to avoid rate limiting
                        time.sleep(1)
    
    def get_video_metadata(self, video_path):
        """Get metadata for a video"""
        if not video_path or not os.path.exists(video_path):
            return None
            
        try:
            # Extract category and video ID from filename
            filename = os.path.basename(video_path)
            parts = filename.split('_')
            
            if len(parts) >= 2:
                category = parts[0]
                video_id = parts[1].split('.')[0]
                
                return {
                    "path": video_path,
                    "category": category,
                    "video_id": video_id,
                    "filename": filename
                }
            
            return {
                "path": video_path,
                "filename": filename
            }
            
        except Exception as e:
            print(f"Error getting video metadata: {str(e)}")
            return {
                "path": video_path,
                "error": str(e)
            }

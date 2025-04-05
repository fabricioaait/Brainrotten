import os
import json
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import TextClip

class TextOverlayOptimizer:
    def __init__(self, fonts_folder='static/fonts'):
        self.fonts_folder = fonts_folder
        
        # Create fonts directory if it doesn't exist
        os.makedirs(fonts_folder, exist_ok=True)
        
        # Define optimized font settings for different content types
        self.font_settings = {
            "technical": {
                "primary_font": "Roboto-Bold.ttf",
                "secondary_font": "RobotoMono-Regular.ttf",
                "title_size": 70,
                "body_size": 40,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (0, 0, 0, 160),  # RGBA with alpha for transparency
                "body_bg": (0, 0, 0, 140)
            },
            "conceptual": {
                "primary_font": "Montserrat-Bold.ttf",
                "secondary_font": "Montserrat-Regular.ttf",
                "title_size": 80,
                "body_size": 45,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (70, 30, 130, 160),
                "body_bg": (70, 30, 130, 140)
            },
            "mathematical": {
                "primary_font": "OpenSans-Bold.ttf",
                "secondary_font": "OpenSans-Regular.ttf",
                "title_size": 70,
                "body_size": 40,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (30, 70, 130, 160),
                "body_bg": (30, 70, 130, 140)
            },
            "historical": {
                "primary_font": "Merriweather-Bold.ttf",
                "secondary_font": "Merriweather-Regular.ttf",
                "title_size": 70,
                "body_size": 40,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (120, 60, 30, 160),
                "body_bg": (120, 60, 30, 140)
            },
            "scientific": {
                "primary_font": "Lato-Bold.ttf",
                "secondary_font": "Lato-Regular.ttf",
                "title_size": 70,
                "body_size": 40,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (30, 100, 70, 160),
                "body_bg": (30, 100, 70, 140)
            },
            "literary": {
                "primary_font": "PlayfairDisplay-Bold.ttf",
                "secondary_font": "PlayfairDisplay-Regular.ttf",
                "title_size": 70,
                "body_size": 40,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (90, 50, 90, 160),
                "body_bg": (90, 50, 90, 140)
            },
            "philosophical": {
                "primary_font": "EBGaramond-Bold.ttf",
                "secondary_font": "EBGaramond-Regular.ttf",
                "title_size": 70,
                "body_size": 45,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (60, 60, 90, 160),
                "body_bg": (60, 60, 90, 140)
            },
            "instructional": {
                "primary_font": "Nunito-Bold.ttf",
                "secondary_font": "Nunito-Regular.ttf",
                "title_size": 70,
                "body_size": 40,
                "title_color": "white",
                "body_color": "white",
                "title_bg": (50, 100, 100, 160),
                "body_bg": (50, 100, 100, 140)
            }
        }
        
        # Default font settings
        self.default_font_settings = {
            "primary_font": "Arial",
            "secondary_font": "Arial",
            "title_size": 70,
            "body_size": 40,
            "title_color": "white",
            "body_color": "white",
            "title_bg": (0, 0, 0, 160),
            "body_bg": (0, 0, 0, 140)
        }
        
        # Font download URLs (Google Fonts)
        self.font_urls = {
            "Roboto-Bold.ttf": "https://fonts.gstatic.com/s/roboto/v30/KFOlCnqEu92Fr1MmWUlfBBc4.woff2",
            "RobotoMono-Regular.ttf": "https://fonts.gstatic.com/s/robotomono/v22/L0xuDF4xlVMF-BfR8bXMIhJHg45mwgGEFl0_3vq_ROW4.woff2",
            "Montserrat-Bold.ttf": "https://fonts.gstatic.com/s/montserrat/v25/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCuM73w5aXo.woff2",
            "Montserrat-Regular.ttf": "https://fonts.gstatic.com/s/montserrat/v25/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtr6Hw5aXo.woff2",
            "OpenSans-Bold.ttf": "https://fonts.gstatic.com/s/opensans/v34/memSYaGs126MiZpBA-UvWbX2vVnXBbObj2OVZyOOSr4dVJWUgsg-1x4gaVI.woff2",
            "OpenSans-Regular.ttf": "https://fonts.gstatic.com/s/opensans/v34/memSYaGs126MiZpBA-UvWbX2vVnXBbObj2OVZyOOSr4dVJWUgsjZ0B4gaVI.woff2",
            "Merriweather-Bold.ttf": "https://fonts.gstatic.com/s/merriweather/v30/u-4n0qyriQwlOrhSvowK_l52xwNZWMf6.woff2",
            "Merriweather-Regular.ttf": "https://fonts.gstatic.com/s/merriweather/v30/u-440qyriQwlOrhSvowK_l5-fCZM.woff2",
            "Lato-Bold.ttf": "https://fonts.gstatic.com/s/lato/v23/S6u9w4BMUTPHh6UVSwiPGQ.woff2",
            "Lato-Regular.ttf": "https://fonts.gstatic.com/s/lato/v23/S6uyw4BMUTPHjx4wXg.woff2",
            "PlayfairDisplay-Bold.ttf": "https://fonts.gstatic.com/s/playfairdisplay/v30/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKebunDXbtM.woff2",
            "PlayfairDisplay-Regular.ttf": "https://fonts.gstatic.com/s/playfairdisplay/v30/nuFvD-vYSZviVYUb_rj3ij__anPXJzDwcbmjWBN2PKdFvXDXbtM.woff2",
            "EBGaramond-Bold.ttf": "https://fonts.gstatic.com/s/ebgaramond/v26/SlGFmQSNjdsmc35JDF1K5GRwUjcdlttVFm-rI7e8QL99U6g.woff2",
            "EBGaramond-Regular.ttf": "https://fonts.gstatic.com/s/ebgaramond/v26/SlGDmQSNjdsmc35JDF1K5E55YMjF_7DPuGi-6_RUA4V-e6yHgQ.woff2",
            "Nunito-Bold.ttf": "https://fonts.gstatic.com/s/nunito/v25/XRXW3I6Li01BKofAjsOUYevI.woff2",
            "Nunito-Regular.ttf": "https://fonts.gstatic.com/s/nunito/v25/XRXV3I6Li01BKofINeaB.woff2"
        }
        
        # Download fonts if they don't exist
        self._ensure_fonts_available()
    
    def _ensure_fonts_available(self):
        """Download fonts if they don't exist"""
        import requests
        
        for font_name, url in self.font_urls.items():
            font_path = os.path.join(self.fonts_folder, font_name)
            
            # Skip if font already exists
            if os.path.exists(font_path):
                continue
                
            try:
                # Download the font
                response = requests.get(url)
                if response.status_code == 200:
                    with open(font_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded font: {font_name}")
                else:
                    print(f"Failed to download font {font_name}: HTTP {response.status_code}")
            except Exception as e:
                print(f"Error downloading font {font_name}: {str(e)}")
    
    def get_font_settings(self, content_type):
        """Get optimized font settings for a content type"""
        # Default to conceptual if content type not found
        return self.font_settings.get(content_type.lower(), self.font_settings["conceptual"])
    
    def create_optimized_text_clip(self, text, content_type, is_title=False, duration=5, 
                                  width=1280, height=None, position='center', margin=40):
        """Create an optimized text clip for the given content type"""
        # Get font settings for this content type
        settings = self.get_font_settings(content_type)
        
        # Determine which font and size to use
        if is_title:
            font_name = settings["primary_font"]
            font_size = settings["title_size"]
            color = settings["title_color"]
            bg_color = settings["title_bg"]
        else:
            font_name = settings["secondary_font"]
            font_size = settings["body_size"]
            color = settings["body_color"]
            bg_color = settings["body_bg"]
        
        # Get font path
        font_path = os.path.join(self.fonts_folder, font_name)
        
        # If font doesn't exist, use default system font
        if not os.path.exists(font_path):
            font_path = None  # MoviePy will use default font
        
        # Convert RGBA background to string format if needed
        if isinstance(bg_color, tuple) and len(bg_color) == 4:
            # For TextClip, we'll handle transparency differently
            # For now, just use the RGB part
            bg_color = f'rgb({bg_color[0]}, {bg_color[1]}, {bg_color[2]})'
        
        # Create text clip with padding
        txt_clip = TextClip(text, fontsize=font_size, font=font_path, color=color, 
                           bg_color=bg_color, size=(width-2*margin, None), 
                           method='caption', align='center')
        
        # Set duration
        txt_clip = txt_clip.set_duration(duration)
        
        # Set position
        if position == 'center':
            txt_clip = txt_clip.set_position('center')
        elif position == 'top':
            txt_clip = txt_clip.set_position(('center', margin))
        elif position == 'bottom':
            if height:
                txt_clip = txt_clip.set_position(('center', height - txt_clip.h - margin))
            else:
                txt_clip = txt_clip.set_position(('center', 'bottom'))
        
        return txt_clip
    
    def create_fade_effects(self, clip, fade_in=0.5, fade_out=0.5):
        """Add fade in and fade out effects to a clip"""
        return clip.fadein(fade_in).fadeout(fade_out)
    
    def split_text_into_chunks(self, text, max_chars=100):
        """Split long text into chunks for better readability"""
        # If text is short enough, return as is
        if len(text) <= max_chars:
            return [text]
        
        # Split by sentences first
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed max_chars, start a new chunk
            if len(current_chunk) + len(sentence) > max_chars and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def create_sequential_text_clips(self, text, content_type, is_title=False, 
                                    duration_per_chunk=5, width=1280, height=720, 
                                    position='center', max_chars=100):
        """Create a sequence of text clips for long text"""
        # Split text into chunks
        chunks = self.split_text_into_chunks(text, max_chars)
        
        # Create a clip for each chunk
        clips = []
        for chunk in chunks:
            clip = self.create_optimized_text_clip(
                chunk, content_type, is_title, 
                duration=duration_per_chunk, 
                width=width, height=height, 
                position=position
            )
            
            # Add fade effects
            clip = self.create_fade_effects(clip)
            clips.append(clip)
        
        return clips

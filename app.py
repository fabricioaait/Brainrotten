from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
from pdf_processor import PDFProcessor
from ai_integrator import AIIntegrator
from video_generator import VideoGenerator
from audio_integrator import AudioIntegrator

app = Flask(__name__)
app.secret_key = 'brainrot_secret_key'

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize processors
pdf_processor = PDFProcessor(upload_folder=UPLOAD_FOLDER)
ai_integrator = AIIntegrator(upload_folder=UPLOAD_FOLDER)
video_generator = VideoGenerator(upload_folder=UPLOAD_FOLDER, output_folder='static/videos')
audio_integrator = AudioIntegrator(sounds_folder='static/sounds')

# Try to import enhanced components, fall back to basic ones if not available
try:
    from enhanced_video_generator import EnhancedVideoGenerator
    from asmr_video_downloader import ASMRVideoDownloader
    from text_overlay_optimizer import TextOverlayOptimizer
    
    # Initialize enhanced components
    enhanced_video_generator = EnhancedVideoGenerator(
        upload_folder=UPLOAD_FOLDER, 
        output_folder='static/videos',
        asmr_folder='static/asmr_videos'
    )
    asmr_downloader = ASMRVideoDownloader(download_folder='static/asmr_videos')
    text_optimizer = TextOverlayOptimizer(fonts_folder='static/fonts')
    
    # Flag to indicate enhanced features are available
    ENHANCED_FEATURES = True
    print("Enhanced features enabled: Video generation with ASMR content and optimized text overlays")
except ImportError as e:
    # Fall back to basic components
    ENHANCED_FEATURES = False
    print(f"Enhanced features disabled due to import error: {str(e)}")
    print("Using basic video generation features")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', enhanced=ENHANCED_FEATURES)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['pdf_file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return render_template('processing.html', filename=filename, enhanced=ENHANCED_FEATURES)
    
    flash('Invalid file type. Please upload a PDF file.')
    return redirect(url_for('index'))

@app.route('/results')
def results():
    filename = request.args.get('filename', 'document.pdf')
    # In a real app, we would fetch actual videos generated from the PDF
    # For now, we'll just pass the filename to the template
    videos = []  # This will be populated by JavaScript for demo purposes
    return render_template('results.html', filename=filename, videos=videos, enhanced=ENHANCED_FEATURES)

@app.route('/api/extract-text', methods=['POST'])
def extract_text():
    # This endpoint would be used by the actual app to extract text from a PDF
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Extract text from PDF using our processor
        text = pdf_processor.extract_text(filename)
        
        # Get a preview of the text
        preview = text[:500] + "..." if len(text) > 500 else text
        
        return jsonify({
            'success': True,
            'text_preview': preview,
            'text_length': len(text)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-pdf', methods=['POST'])
def analyze_pdf():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    try:
        # Generate content structure from PDF
        content_structure = pdf_processor.generate_content_structure(filename)
        
        if 'error' in content_structure:
            return jsonify({'error': content_structure['error']}), 500
        
        return jsonify({
            'success': True,
            'content_structure': content_structure
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-analyze', methods=['POST'])
def ai_analyze():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    try:
        # Use AI to analyze the PDF content
        analysis_result = ai_integrator.analyze_content(filename)
        
        if 'error' in analysis_result:
            return jsonify({'error': analysis_result['error']}), 500
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-video-plan', methods=['POST'])
def generate_video_plan():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    try:
        # Generate a video plan using AI
        plan_result = ai_integrator.generate_video_plan(filename)
        
        if 'error' in plan_result:
            return jsonify({'error': plan_result['error']}), 500
        
        return jsonify(plan_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-videos', methods=['POST'])
def generate_videos():
    data = request.json
    video_plan = data.get('video_plan')
    
    if not video_plan:
        return jsonify({'error': 'No video plan provided'}), 400
    
    try:
        # Use enhanced video generator if available, otherwise fall back to basic
        if ENHANCED_FEATURES:
            # Try to preload some ASMR videos for use in generation
            try:
                asmr_downloader.preload_videos_for_all_categories(videos_per_category=1)
            except Exception as e:
                print(f"Warning: Failed to preload ASMR videos: {str(e)}")
            
            # Generate videos based on the plan using the enhanced generator
            result = enhanced_video_generator.generate_videos_from_plan(video_plan)
        else:
            # Fall back to basic video generator
            result = video_generator.mock_generate_videos(video_plan)
        
        if not result['success']:
            return jsonify({'error': result.get('error', 'Unknown error')}), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-asmr-video', methods=['POST'])
def download_asmr_video():
    if not ENHANCED_FEATURES:
        return jsonify({'error': 'Enhanced features not available'}), 501
    
    data = request.json
    content_type = data.get('content_type', 'conceptual')
    
    if not content_type:
        return jsonify({'error': 'No content type provided'}), 400
    
    try:
        # Get an appropriate ASMR video for this content type
        video_path = asmr_downloader.get_asmr_video_for_content(content_type)
        
        if not video_path:
            return jsonify({'error': 'Failed to download ASMR video'}), 500
        
        # Get metadata for the video
        metadata = asmr_downloader.get_video_metadata(video_path)
        
        return jsonify({
            'success': True,
            'video_path': video_path,
            'metadata': metadata
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process/<filename>', methods=['GET'])
def process_pdf(filename):
    try:
        # Generate a video plan for the PDF
        plan_result = ai_integrator.generate_video_plan(filename)
        
        if 'error' in plan_result:
            flash(f'Error processing PDF: {plan_result["error"]}')
            return redirect(url_for('index'))
        
        video_plan = plan_result['video_generation_plan']
        
        # Use enhanced video generator if available, otherwise fall back to basic
        if ENHANCED_FEATURES:
            # Try to preload some ASMR videos
            try:
                asmr_downloader.preload_videos_for_all_categories(videos_per_category=1)
            except Exception as e:
                print(f"Warning: Failed to preload ASMR videos: {str(e)}")
            
            # Generate videos based on the plan using the enhanced generator
            video_result = enhanced_video_generator.generate_videos_from_plan(video_plan)
        else:
            # Fall back to basic video generator
            video_result = video_generator.mock_generate_videos(video_plan)
        
        if not video_result['success']:
            flash(f'Error generating videos: {video_result.get("error", "Unknown error")}')
            return redirect(url_for('index'))
        
        # Redirect to results page
        return redirect(url_for('results', filename=filename))
    
    except Exception as e:
        flash(f'Error processing PDF: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

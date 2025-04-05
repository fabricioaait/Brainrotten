# Brainrot App

A web application that transforms PDFs into short, pleasurable educational videos with ASMR-like sounds to enhance learning.

## Features

- **PDF Upload and Processing**: Upload PDF documents and extract text content
- **AI-Powered Content Analysis**: Identify key topics and concepts from PDF content
- **Video Generation**: Transform extracted content into engaging educational videos
- **ASMR Sound Integration**: Add pleasurable sounds to enhance the learning experience
- **Responsive Design**: Works on both desktop and mobile devices
- **Docker & Kubernetes Ready**: Easily deployable to container environments

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **PDF Processing**: PyPDF2, NLTK
- **Video Generation**: PIL, MoviePy
- **Containerization**: Docker
- **Orchestration**: Kubernetes

## Getting Started

### Local Development

1. Clone the repository
2. Set up a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Access the application at http://localhost:5000

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t brainrot-app:latest .
   ```
2. Run the container:
   ```
   docker run -p 5000:5000 brainrot-app:latest
   ```
3. Access the application at http://localhost:5000

### Kubernetes Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Kubernetes.

## Project Structure

```
brainrot_app/
├── app.py                  # Main Flask application
├── pdf_processor.py        # PDF text extraction and processing
├── ai_integrator.py        # AI-based content analysis
├── video_generator.py      # Video generation functionality
├── audio_integrator.py     # ASMR sound integration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── kubernetes/             # Kubernetes configuration files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── persistent-volume-claims.yaml
├── static/                 # Static assets
│   ├── css/
│   ├── js/
│   ├── img/
│   ├── videos/
│   ├── sounds/
│   └── fonts/
├── templates/              # HTML templates
│   ├── index.html
│   ├── processing.html
│   └── results.html
└── uploads/                # Directory for uploaded PDFs
```

## How It Works

1. **Upload**: User uploads a PDF document
2. **Processing**: System extracts text and identifies key topics
3. **AI Analysis**: AI analyzes content and creates a structured video plan
4. **Video Generation**: System generates educational videos with visual elements
5. **Sound Integration**: ASMR-like sounds are added to enhance the learning experience
6. **Delivery**: User receives short, pleasurable educational videos

## Future Enhancements

- Integration with real AI APIs for more sophisticated content analysis
- Advanced video generation with animations and transitions
- User accounts and saved video libraries
- Batch processing of multiple PDFs
- Custom sound preferences for personalized learning experiences

## License

[MIT License](LICENSE)

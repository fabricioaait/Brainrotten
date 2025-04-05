// Enhanced JavaScript for Brainrot App

document.addEventListener('DOMContentLoaded', function() {
    // File input handling
    const fileInput = document.getElementById('pdf_file');
    if (fileInput) {
        const fileLabel = document.querySelector('label[for="pdf_file"]');
        const originalLabelText = fileLabel.textContent;
        
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileLabel.textContent = this.files[0].name;
                fileLabel.classList.add('file-selected');
            } else {
                fileLabel.textContent = originalLabelText;
                fileLabel.classList.remove('file-selected');
            }
        });
    }
    
    // Processing page animation
    const processingPage = document.querySelector('.processing-section');
    if (processingPage) {
        simulateProcessing();
    }
    
    // Results page functionality
    const resultsPage = document.querySelector('.results-section');
    if (resultsPage) {
        // Simulate video loading for demo purposes
        setTimeout(() => {
            const noVideos = document.querySelector('.no-videos');
            if (noVideos) {
                noVideos.style.display = 'none';
                
                // Create sample videos for demonstration
                const videoGrid = document.querySelector('.video-grid');
                if (videoGrid) {
                    createSampleVideos(videoGrid);
                }
            }
        }, 3000);
        
        // Download all videos button
        const downloadBtn = document.getElementById('download-all');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', function() {
                alert('In the full app, this would download all generated videos as a zip file.');
            });
        }
    }
    
    // Add smooth scrolling for all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Add animation to steps on scroll
    const steps = document.querySelectorAll('.step');
    if (steps.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-step');
                }
            });
        }, { threshold: 0.5 });
        
        steps.forEach(step => {
            observer.observe(step);
        });
    }
});

// Simulate the processing steps for demonstration
function simulateProcessing() {
    const steps = document.querySelectorAll('.step-indicator');
    const messages = [
        "Extracting text from your PDF...",
        "Identifying key topics and concepts...",
        "Creating engaging video content...",
        "Adding pleasant ASMR-like sounds..."
    ];
    const processingMessage = document.querySelector('.processing-message');
    
    let currentStep = 0;
    
    // Activate first step immediately
    steps[0].classList.add('active');
    processingMessage.textContent = messages[0];
    
    // Progress through the steps
    const interval = setInterval(() => {
        currentStep++;
        
        if (currentStep < steps.length) {
            // Update active step
            steps.forEach((step, index) => {
                if (index <= currentStep) {
                    step.classList.add('active');
                } else {
                    step.classList.remove('active');
                }
            });
            
            // Update message
            processingMessage.textContent = messages[currentStep];
        } else {
            // All steps complete
            clearInterval(interval);
            processingMessage.textContent = "Processing complete! Your video will be ready soon.";
            
            // In a real app, we would redirect to a results page
            // For now, we'll just show a message and redirect after a delay
            setTimeout(() => {
                window.location.href = '/results?filename=sample.pdf';
            }, 2000);
        }
    }, 3000); // Change steps every 3 seconds
}

// Create sample videos for demonstration
function createSampleVideos(container) {
    const sampleVideos = [
        {
            title: "Introduction to Key Concepts",
            description: "A gentle overview of the main topics covered in your document.",
            tags: ["introduction", "overview", "basics"]
        },
        {
            title: "Deep Dive: Core Principles",
            description: "Detailed explanation of the fundamental principles with ASMR sounds.",
            tags: ["detailed", "principles", "ASMR"]
        },
        {
            title: "Quick Memory Hooks",
            description: "Short memory triggers to help you recall important facts instantly.",
            tags: ["memory", "quick", "recall"]
        },
        {
            title: "Visual Associations",
            description: "Visual metaphors and associations to strengthen your understanding.",
            tags: ["visual", "metaphors", "associations"]
        }
    ];
    
    sampleVideos.forEach((video, index) => {
        const videoCard = document.createElement('div');
        videoCard.className = 'video-card';
        videoCard.style.animationDelay = `${0.1 * (index + 1)}s`;
        
        const tagsHTML = video.tags.map(tag => `<span class="tag">${tag}</span>`).join('');
        
        videoCard.innerHTML = `
            <div class="video-container">
                <video controls poster="/static/img/video-placeholder.jpg">
                    <source src="#" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <div class="video-info">
                <h3>${video.title}</h3>
                <p class="video-description">${video.description}</p>
                <div class="video-tags">
                    ${tagsHTML}
                </div>
            </div>
        `;
        
        container.appendChild(videoCard);
    });
}

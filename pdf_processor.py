import os
import PyPDF2
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

class PDFProcessor:
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        
        # Ensure NLTK resources are downloaded
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def extract_text(self, filename):
        """Extract text from a PDF file"""
        file_path = os.path.join(self.upload_folder, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def preprocess_text(self, text):
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        
        # Tokenize into sentences
        sentences = sent_tokenize(text)
        
        # Process each sentence
        processed_sentences = []
        for sentence in sentences:
            # Tokenize into words
            words = word_tokenize(sentence)
            
            # Remove stop words and lemmatize
            filtered_words = [
                self.lemmatizer.lemmatize(word) 
                for word in words 
                if word not in self.stop_words and len(word) > 2
            ]
            
            if filtered_words:
                processed_sentences.append(' '.join(filtered_words))
        
        return processed_sentences
    
    def identify_topics(self, text, num_topics=5):
        """Identify main topics from the text"""
        processed_sentences = self.preprocess_text(text)
        
        # Combine all processed sentences
        all_words = ' '.join(processed_sentences).split()
        
        # Count word frequencies
        word_freq = Counter(all_words)
        
        # Get the most common words as topics
        topics = word_freq.most_common(num_topics)
        
        return topics
    
    def extract_key_sentences(self, text, topics, sentences_per_topic=3):
        """Extract key sentences related to each topic"""
        sentences = sent_tokenize(text)
        topic_words = [topic[0] for topic in topics]
        
        # Score sentences based on topic relevance
        sentence_scores = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = sum(1 for topic in topic_words if topic in sentence_lower)
            if score > 0:
                sentence_scores.append((sentence, score))
        
        # Sort sentences by score
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top sentences
        top_sentences = [s[0] for s in sentence_scores[:sentences_per_topic * len(topics)]]
        
        return top_sentences
    
    def generate_content_structure(self, filename):
        """Generate a structured content outline from a PDF"""
        try:
            # Extract text from PDF
            text = self.extract_text(filename)
            
            # Identify main topics
            topics = self.identify_topics(text)
            
            # Extract key sentences for each topic
            key_sentences = self.extract_key_sentences(text, topics)
            
            # Create content structure
            content_structure = {
                'filename': filename,
                'topics': [{'name': topic[0], 'weight': topic[1]} for topic in topics],
                'key_sentences': key_sentences,
                'total_text_length': len(text)
            }
            
            return content_structure
        
        except Exception as e:
            return {'error': str(e)}

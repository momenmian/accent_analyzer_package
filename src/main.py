import os
from flask import Flask, render_template, request, jsonify
from utils.audio_extractor import AudioExtractor
from utils.accent_analyzer import AccentAnalyzer
import tempfile

app = Flask(__name__)

# Initialize the audio extractor and accent analyzer
temp_dir = os.path.join(tempfile.gettempdir(), 'accent_analyzer')
os.makedirs(temp_dir, exist_ok=True)

# Routes
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze the accent from a video URL"""
    try:
        # Get the video URL from the request
        data = request.get_json()
        video_url = data.get('url')
        
        if not video_url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Extract audio from the video
        audio_extractor = AudioExtractor(temp_dir=temp_dir)
        audio_path = audio_extractor.extract_from_url(video_url)
        
        # Analyze the accent
        accent_analyzer = AccentAnalyzer()
        analysis_result = accent_analyzer.analyze_audio(audio_path)
        
        # Clean up the audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=5050, debug=True)

from dotenv import load_dotenv
load_dotenv()
import os
import json
from flask import Flask, jsonify, request
from datetime import datetime
import logging
from seo_fetcher import SEOFetcher
from ai_generator import AIGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
seo_fetcher = SEOFetcher()
ai_generator = AIGenerator()

@app.route('/generate', methods=['GET'])
def generate_blog_post():
    try:
        keyword = request.args.get('keyword')
        
        if not keyword:
            return jsonify({
                'error': 'Missing required parameter: keyword'
            }), 400
        keyword = keyword.strip()
        if len(keyword) > 100 or len(keyword) < 2:
            return jsonify({
                'error': 'Keyword must be between 2 and 100 characters'
            }), 400
        
        logger.info(f"Generating blog post for keyword: {keyword}")
        seo_metrics = seo_fetcher.fetch_metrics(keyword)
        blog_post = ai_generator.generate_post(keyword, seo_metrics)
        filename = save_blog_post(keyword, blog_post)
        response = {
            'keyword': keyword,
            'seo_metrics': seo_metrics,
            'blog_post': blog_post,
            'saved_to': filename,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error generating blog post: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

def save_blog_post(keyword, content):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"generated_posts/{keyword.replace(' ', '_')}_{timestamp}.md"
    
    os.makedirs('generated_posts', exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"Blog post saved to {filename}")
    return filename

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

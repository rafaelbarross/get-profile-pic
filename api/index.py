from flask import Flask, request, jsonify
import instaloader
import time
import random

app = Flask(__name__)

def get_instagram_session():
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        request_timeout=30
    )
    
    # Add randomized delay between 1-3 seconds
    time.sleep(random.uniform(1, 3))
    
    # Set custom user agent
    L.context._session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    return L

@app.route('/get_profile_pic', methods=['GET'])
def get_profile_pic():
    username = request.args.get('username')
    
    if not username:
        return jsonify({'error': 'Username parameter is missing.'}), 400
        
    try:
        L = get_instagram_session()
        profile = instaloader.Profile.from_username(L.context, username)
        return jsonify({
            'username': username,
            'profile_pic_url': profile.profile_pic_url
        })
        
    except instaloader.exceptions.ConnectionException as e:
        return jsonify({
            'error': 'Rate limit reached',
            'message': str(e)
        }), 429
        
    except instaloader.exceptions.ProfileNotExistsException:
        return jsonify({
            'error': 'Profile not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'API is running',
        'usage': '/get_profile_pic?username=example_user'
    })

if __name__ == '__main__':
    app.run(debug=False, port=80)

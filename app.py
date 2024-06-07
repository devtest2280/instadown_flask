from flask import Flask, render_template, request
import instaloader
import requests
import os

app = Flask(__name__)

def download_instagram_video(post_url, save_path):
    L = instaloader.Instaloader()

    post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-2])

    if post.is_video:
        video_url = post.video_url
        response = requests.get(video_url)

        with open(save_path, 'wb') as f:
            f.write(response.content)

        return f"http://127.0.0.1:5000/{save_path}"
    else:
        return "The post is not a video."

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        post_url = request.form['post_url']        
        last_piece = post_url.split("reel/")[-1][:-1]        
        save_path = "static/"+last_piece+".mp4"
        video_url = download_instagram_video(post_url, save_path)
        return render_template('index.html', video_url=video_url)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import requests

app = Flask(__name__)

try:
    # Fetch data from the API
    response = requests.get("https://api.npoint.io/43644ec4f0013682fc0d")
    response.raise_for_status()  # Check for errors in the response
    posts = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the API: {e}")
    posts = []

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/blog")
def blog():
    # Pass the 'posts' data to the 'blog.html' template
    return render_template('blog.html', all_posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

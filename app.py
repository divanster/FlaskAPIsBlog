from flask import Flask, render_template, jsonify, request, redirect
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,EmailField, validators
from wtforms.validators import DataRequired
from flask_sslify import SSLify  # Install via pip for enforcing HTTPS
import secrets

app = Flask(__name__)
sslify = SSLify(app)  # Enforce HTTPS

# Use a strong, randomly generated secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Set a secure secret key

class MyForm(FlaskForm):
    name = StringField('Names', validators=[DataRequired()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])


def get_post_by_id(post_id):
    # Placeholder logic to fetch post details from your data source
    all_posts = get_dummy_posts()
    for post in all_posts:
        if post['id'] == post_id:
            return post
    return None

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = get_post_by_id(post_id)
    if post:
        return render_template('post_detail.html', post=post)
    else:
        return render_template('post_not_found.html'), 404

def get_dummy_posts():
    try:
        response = requests.get("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json")
        response.raise_for_status()
        posts = response.json()
        return posts
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return []

@app.route("/api/new_quote", methods=['GET', 'POST'])
def new_quote():
    if request.method == 'GET':
        quote = get_kanye_quote()
        return jsonify({'quote': quote})
    elif request.method == 'POST':
        new_python_quote = get_python_quote()
        return jsonify({'quote': new_python_quote})

def get_kanye_quote():
    try:
        response = requests.get("https://api.kanye.rest/")
        response.raise_for_status()
        data = response.json()
        return data['quote']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return None

def get_python_quote():
    try:
        response = requests.get("https://api.kanye.rest/")
        response.raise_for_status()
        data = response.json()
        return data['quote']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return "Failed to fetch Python-generated quote."

@app.route("/")
def home():
    return render_template('home.html')

# Testing some functionalities in the project
@app.route('/test', methods=['GET', 'POST'])
def test():
    form = MyForm()
    if form.validate_on_submit():
        return "You Did it!"
    return render_template('test.html', form=form)

@app.route("/loging", methods=["POST", "GET"])
def loging():
    if request.method == 'POST':
        name = request.form["username"]
        password = request.form["password"]
        print("Received username:", name)
        print("Received password:", password)
        return f"<h1>Name: {name}, Password: {password}</h1>"
    else:
        return render_template('loging.html')

@app.route("/quotes")
def quotes():
    quote = get_kanye_quote()
    return render_template('dayquote.html', quote=quote, python_quote=get_python_quote())

# ... (remaining code)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts_per_page = 5
    all_posts = get_dummy_posts()
    start_index = (page - 1) * posts_per_page
    end_index = start_index + posts_per_page
    paginated_posts = all_posts[start_index:end_index]
    pagination = {
        'page': page,
        'per_page': posts_per_page,
        'total': len(all_posts),
        'pages': len(all_posts) // posts_per_page + (1 if len(all_posts) % posts_per_page > 0 else 0)
    }
    return render_template('blog.html', posts=paginated_posts, pagination=pagination)

if __name__ == '__main__':
    app.run(debug=True)

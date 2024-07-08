from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'a5e9c7b1f4b08b78a11e65a2d4b8f1d8'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(20), unique=True, nullable=False)  # Asegúrate de que este tamaño sea adecuado para tu caso

    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url

def generate_short_url():
    prefix = "short_url_Pablo."
    characters = string.ascii_letters
    while True:
        random_part = ''.join(random.choice(characters) for _ in range(6))  # Parte aleatoria de 6 caracteres
        short_url = prefix + random_part
        if not URL.query.filter_by(short_url=short_url).first():  # Verificar si el short_url ya existe
            return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        existing_url = URL.query.filter_by(original_url=original_url).first()

        if existing_url:
            flash('Short URL already exists for this URL.')
            return render_template('index.html', short_url=existing_url.short_url)

        short_url = generate_short_url()
        new_url = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

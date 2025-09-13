from flask import Flask, render_template

app = Flask(__name__)

# صفحه اصلی
@app.route('/')
def home():
    products = [
        {"name": "Bedding 1", "image": "bed1.jpg"},
        {"name": "Bedding 2", "image": "bed2.jpg"},
        {"name": "Bedding 3", "image": "bed3.jpg"},
    ]
    return render_template('index.html', products=products)

# صفحه درباره ما
@app.route('/about')
def about():
    return render_template('about.html')

# صفحه تماس با ما
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)

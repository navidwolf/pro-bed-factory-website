from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", title="صفحه اصلی", description="صفحه اصلی کارخانه")

@app.route("/about")
def about():
    return render_template("about.html", title="درباره ما", description="درباره کارخانه و معرفی برند")

@app.route("/products")
def products():
    return render_template("products.html", title="محصولات", description="محصولات کارخانه")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="تماس با ما", description="ارتباط با کارخانه")

if __name__ == "__main__":
    app.run(debug=True)

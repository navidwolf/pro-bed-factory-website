from flask import Flask, render_template, url_for, Response, request, redirect, flash
from datetime import datetime
import os, sqlite3, json

app = Flask(__name__)
app.secret_key = "supersecretkey"  # لازم برای flash messages

# ---------- تنظیمات سایت ----------
SITE_META = {
    'site_name': 'Bed Factory Co.',
    'description': 'تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.',
    'phone': '+98-21-12345678',
    'address': 'تهران، خیابان نمونه، نبش کارخانه',
    'email': 'info@bedfactory.example'
}

DB_FILE = "products.db"

# ---------- تابع ساخت دیتابیس خودکار ----------
def init_db():
    """اگر دیتابیس وجود نداشت، ایجادش کن و داده‌ها رو وارد کن."""
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image TEXT NOT NULL,
            excerpt TEXT,
            desc TEXT,
            details TEXT
        )
        """)
        c.execute("""
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()

        # بارگذاری داده‌های اولیه از products.json
        if os.path.exists("products.json"):
            with open("products.json", "r", encoding="utf-8") as f:
                products = json.load(f)
            for p in products:
                c.execute("INSERT INTO products (title, image, excerpt, desc, details) VALUES (?, ?, ?, ?, ?)",
                          (p["title"], p["image"], p.get("excerpt",""), p.get("desc", ""), p.get("details", "")))
            conn.commit()

        conn.close()

# اجرای خودکار ساخت دیتابیس
init_db()

# ---------- helper اتصال به دیتابیس ----------
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Middleware امنیت ----------
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = "default-src 'self' data: https://cdn.tailwindcss.com;"
    return resp

# ---------- Routes ----------
@app.route('/')
def index():
    conn = get_db()
    products = conn.execute("SELECT id,title,image,excerpt FROM products").fetchall()
    conn.close()
    return render_template('index.html', meta=SITE_META,
                           page_title="خانه | " + SITE_META['site_name'],
                           page_desc=SITE_META['description'],
                           products=products)

@app.route('/products')
def products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('products.html', meta=SITE_META,
                           page_title="محصولات | " + SITE_META['site_name'],
                           page_desc="لیست محصولات تخت‌خواب تولیدی",
                           products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    others = conn.execute("SELECT * FROM products WHERE id!=?", (product_id,)).fetchall()
    conn.close()
    if not product:
        return "محصول یافت نشد", 404
    return render_template('product_detail.html', meta=SITE_META,
                           page_title=product['title'] + " | " + SITE_META['site_name'],
                           page_desc=product['desc'],
                           product=product, products=others)

@app.route('/contact', methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        conn = get_db()
        conn.execute("INSERT INTO messages (name,email,message,created_at) VALUES (?,?,?,?)",
                     (name,email,message,datetime.now().isoformat()))
        conn.commit()
        conn.close()
        flash("پیام شما با موفقیت ثبت شد ✅")
        return redirect(url_for('contact'))
    return render_template('contact.html', meta=SITE_META,
                           page_title="تماس با ما | " + SITE_META['site_name'],
                           page_desc="راه‌های ارتباطی با کارخانه")

@app.route('/sitemap.xml')
def sitemap():
    conn = get_db()
    product_ids = [row['id'] for row in conn.execute("SELECT id FROM products").fetchall()]
    conn.close()

    pages = []
    today = (datetime.now()).date().isoformat()
    pages.append({'loc': url_for('index', _external=True), 'lastmod': today})
    pages.append({'loc': url_for('products', _external=True), 'lastmod': today})
    pages.append({'loc': url_for('contact', _external=True), 'lastmod': today})
    for pid in product_ids:
        pages.append({'loc': url_for('product_detail', product_id=pid, _external=True), 'lastmod': today})

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append('<url>')
        xml.append(f"<loc>{p['loc']}</loc>")
        xml.append(f"<lastmod>{p['lastmod']}</lastmod>")
        xml.append('</url>')
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')

# ---------- Run App ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

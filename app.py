from flask import Flask, render_template, url_for, Response
from datetime import datetime


app = Flask(__name__)


# Basic site data — customize
SITE_META = {
'site_name': 'Bed Factory Co.',
'description': 'تولید کنندهٔ تخت‌خواب‌های با کیفیت — طراحی و ساخت در ایران.',
'phone': '+98-21-12345678',
'address': 'تهران، خیابان نمونه، نبش کارخانه',
'email': 'info@bedfactory.example'
}


@app.route('/')
def index():
products = [
{ 'id': 1, 'title': 'تخت خواب مدل آریا', 'image': url_for('static', filename='images/product1.webp'), 'excerpt': 'کلاف چوبی، راحتی بالا' },
{ 'id': 2, 'title': 'تخت خواب مدل نیلا', 'image': url_for('static', filename='images/product2.webp'), 'excerpt': 'مدرن و شیک' },
]
return render_template('index.html', meta=SITE_META, products=products)


@app.route('/products')
def products():
products = [
{ 'id': 1, 'title': 'تخت خواب مدل آریا', 'image': url_for('static', filename='images/product1.webp'), 'desc': 'کلاف چوبی استاندارد، ابعاد مختلف' },
{ 'id': 2, 'title': 'تخت خواب مدل نیلا', 'image': url_for('static', filename='images/product2.webp'), 'desc': 'مناسب فضاهای مدرن، قابل سفارش' },
]
return render_template('products.html', meta=SITE_META, products=products)


@app.route('/contact')
def contact():
return render_template('contact.html', meta=SITE_META)


@app.route('/sitemap.xml')
def sitemap():
# Simple dynamic sitemap
pages = []
ten_days_ago = (datetime.now()).date().isoformat()
pages.append({'loc': url_for('index', _external=True), 'lastmod': ten_days_ago})
pages.append({'loc': url_for('products', _external=True), 'lastmod': ten_days_ago})
pages.append({'loc': url_for('contact', _external=True), 'lastmod': ten_days_ago})


xml = ['<?xml version="1.0" encoding="UTF-8"?>',
'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages:
xml.append('<url>')
xml.append(f"<loc>{p['loc']}</loc>")
xml.append(f"<lastmod>{p['lastmod']}</lastmod>")
xml.append('</url>')
xml.append('</urlset>')
response = Response('\n'.join(xml), mimetype='application/xml')
return response


if __name__ == '__main__':
app.run(debug=True)
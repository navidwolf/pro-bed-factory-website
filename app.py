from flask import Flask, render_template

app = Flask(__name__)

# صفحه اصلی
@app.route('/')
def home():
    return render_template('index.html')

# درباره ما
@app.route('/about')
def about():
    return render_template('about.html')

# گالری محصولات
@app.route('/gallery')
def gallery():
    # یک لیست ساده از محصولات (می‌توان بعداً JSON یا دیتابیس استفاده کرد)
    products = [
        {'id': 1, 'name': 'تخت چوبی مدل A', 'image': 'bed1.jpg'},
        {'id': 2, 'name': 'تخت فلزی مدل B', 'image': 'bed2.jpg'},
        {'id': 3, 'name': 'تخت طبی مدل C', 'image': 'bed3.jpg'}
        # اضافه کردن محصولات دیگر
    ]
    return render_template('gallery.html', products=products)

# صفحه جزئیات محصول
@app.route('/product/<int:product_id>')
def product(product_id):
    # برای مثال ساده، اطلاعات محصول
    product_details = {
        1: {'name': 'تخت چوبی مدل A', 'description': 'توضیح کوتاه', 'image': 'bed1.jpg'},
        2: {'name': 'تخت فلزی مدل B', 'description': 'توضیح کوتاه', 'image': 'bed2.jpg'},
        3: {'name': 'تخت طبی مدل C', 'description': 'تخت طبی مناسب برای استراحت راحت.', 'image': 'bed3.jpg'}
    }
    product = product_details.get(product_id)
    return render_template('product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sng')
def sng_product():
    return render_template('single-product.html')

if __name__ == "__main__":
    app.run()

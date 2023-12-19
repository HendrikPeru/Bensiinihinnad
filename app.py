from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        location = request.form['location']
        fuel_type = request.form['fuel_type']
        return f"Valitud asukoht: {location}, Valitud kütus: {fuel_type}"
    return "Midagi läks valesti!"

if __name__ == '__main__':
    app.run(debug=True)

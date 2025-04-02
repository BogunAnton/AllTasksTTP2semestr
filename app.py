from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('html.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    email = request.form.get('email')

    # Обработка данных формы
    return f"Thank you, {username}! We received your email: {email}"

if __name__ == '__main__':
    app.run(debug=False)
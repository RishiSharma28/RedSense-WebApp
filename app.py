from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission here
    # Example: data = request.form['input_name']
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)

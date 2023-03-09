from flask import Flask, render_template, request
import string
import random

app=Flask(__name__)

@app.route("/",methods=["GET"])
def main():
    return render_template("index.html",name="Pratham")

@app.route('/generate', methods=['POST',"GET"])
def generate_password():
    if request.method=="POST":     
        # Get user input from request
        length = int(request.form['length'])
        include_letters = request.form.get('letters') == 'on'
        include_numbers = request.form.get('numbers') == 'on'
        include_symbols = request.form.get('symbols') == 'on'

        # Define character sets based on user input
        letters = string.ascii_letters if include_letters else ''
        numbers = string.digits if include_numbers else ''
        symbols = string.punctuation if include_symbols else ''

        # Combine character sets
        char_set = f'{letters}{numbers}{symbols}'

        # Generate password
        password = ''.join(random.choice(char_set) for i in range(length))

        return render_template("generate.html",password=password)
    else:
        return render_template("generate.html")

@app.route("/result",methods=["POST"])
def result():
    if request.method == 'POST':
        length = int(request.form['length'])
        upper = True if request.form.get('upper') else False
        lower = True if request.form.get('lower') else False
        number = True if request.form.get('number') else False
        symbol = True if request.form.get('symbol') else False
        common = True if request.form.get('common') else False
        easy = request.form.get('easy', '123')
        entropy = int(request.form.get('entropy', 50))       
        chars = ''
        if upper:
            chars += string.ascii_uppercase
        if lower:
            chars += string.ascii_lowercase
        if number:
            chars += string.digits
        if symbol:
            chars += string.punctuation

        # Remove common characters if necessary
        if not common:
            for c in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                chars = chars.replace(c, '')

        # Add easy characters if necessary
        if easy:
            chars += easy

        # Calculate the minimum entropy for the password
        min_entropy = length * (entropy / 100)

        # Generate a password with sufficient entropy
        while True:
            password = ''.join(random.choice(chars) for _ in range(length))
            password_entropy = 0
            for c in password:
                if c in string.ascii_lowercase:
                    password_entropy += 4.7
                elif c in string.ascii_uppercase:
                    password_entropy += 5.9
                elif c in string.digits:
                    password_entropy += 3.3
                elif c in string.punctuation:
                    password_entropy += 6.6
            if password_entropy >= min_entropy:
                break
        return render_template("result.html",password=password)
app.run(host="0.0.0.0",port=5000)
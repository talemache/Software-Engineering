from OOZero import create_app
from flask import Flask, render_template, request

app = create_app()

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()

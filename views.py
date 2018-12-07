from flask import render_template, jsonify, request
from app import app, bot


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reply', methods=['POST'])
def reply():
    message = request.json['message']
    reply = bot.reply(message)
    print(reply)
    return jsonify(reply=reply)
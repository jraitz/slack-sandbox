from flask import Flask, request, url_for, jsonify
import random, requests

app = Flask(__name__)
app.secret_key = 'This is really unique and secret'

@app.route('/')
def hello_person():
    return """
        <p>Who do you want me to say "Hi" to?</p>
        <form method="POST" action="%s"><input name="person" /><input type="submit" value="Go!" /></form>
        """ % (url_for('greet'),)

@app.route('/greet', methods=['POST'])
def greet():
    greeting = random.choice(["Hiya", "Hallo", "Hola", "Ola", "Salut", "Privet", "Konnichiwa", "Ni hao"])
    return """
        <p>%s, %s!</p>
        <p><a href="%s">Back to start</a></p>
        """ % (greeting, request.form["person"], url_for('hello_person'))

@app.route('/api/wikiroll', methods=['POST'])
def wikiroll():
    #if key= "wjx3beVcNQpnTc6QF2zEzwqx"
    rndWikiLink = "http://en.wikipedia.org/wiki/Special:Random"
    r1 = requests.get(rndWikiLink)
    r2 = requests.get(rndWikiLink)
    responseText = "Your goal is to get from %s , \nto %s ." % (r1.url, r2.url)
    return jsonify({'text':responseText})

@app.route('/rndwiki', methods=['GET'])
def rndwiki():
    wikiRequest = "http://en.wikipedia.org/wiki/Special:Random"
    r = requests.get(wikiRequest)
    return "<p>The response url was %s.</p>" % r.url
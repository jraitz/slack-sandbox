from flask import Flask, request, jsonify
import random, requests
import re

app = Flask(__name__)
app.secret_key = 'This is really unique and secret'
is_three_word = re.compile('^\w\w\w\w+?\.\w\w\w\w+?\.\w\w\w\w+$')

@app.route('/')
def hello_person():
    return """
        <p>You're not supposed to be here.</p>
        """

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

@app.route('/api/rollG/<int:number>/<int:sides>', methods=['GET','POST'])
def rollG(number=1, sides=6):
    if (1<=number<=20) and (sides>=2):
        rolls=[]
        for x in range(1,number+1):
            rolls.append('roll %s: %s' % (x,random.randint(1,sides)))
        rolltext = '\n'.join(rolls)
        return jsonify({'text':'you asked for %s roll(s) of a d%s.\nYour rolls were:\n%s' % (number, sides, rolltext)})
    else:
        return jsonify({'text':'The number of dice must be between 1 and 20, and sides must be between 2 and 100.'})

@app.route('/api/roll/', methods=['POST'])
def roll():
    fullRequest = request.form['text']
    total=int(0)
    if (8<=len(fullRequest)<=12):
        rollRequest = fullRequest.split(' ')
        splitRequest = rollRequest[1].split('d',1)
        number = int(splitRequest[0])
        sides = int(splitRequest[1])
        #return jsonify({'text':'you asked for %s.' % (splitRequest)})
    else:
        return jsonify({'text':'example request would be \'roll 2d6\''})
    if (1<=number<=20) and (sides>2):
        rolls=[]
        for x in range(1,number+1):
            randRoll=random.randint(1,sides)
            total+=randRoll
            rolls.append('roll %s: %s' % (x,randRoll))
        rolltext = '\n'.join(rolls)
        return jsonify({'text':'you asked for %s roll(s) of a d%s.\nThe Total was %s.\nYour rolls were:\n%s' % (number, sides,total,rolltext)})
    elif (sides==2):
        return jsonify({'text':'Damnit captain, I\'m a dice roller, not a coin flipper!'})
    else:
        return jsonify({'text':'The number of dice must be between 1 and 20, and sides must be between 2 and 100.'})

@app.route('/api/multiroll/', methods=['POST'])
def multiroll():
    #return jsonify({'text':'under construction'})
    #return jsonify({'text':'you asked for %s' % (request.form)})
    fullRequest = request.form['text']
    if (fullRequest == 'multiroll help'):
        return jsonify({'text':'form should be \'multiroll <multiplier> <number>d<sides>[+<modifier>]\''})
    if (10<=len(fullRequest)<=30):
        modifier=0
        command, multiplier, fullRollRequest = fullRequest.split()
        multiplier = int(multiplier)
        if '+' in fullRollRequest:
            rollRequest, modifier = fullRollRequest.split('+',1)
            modifier=int(modifier)
        else:
            modifier=0
            rollRequest = fullRollRequest
        number, sides = rollRequest.split('d',1)
        number = int(number)
        sides = int(sides)
        #return jsonify({'text':'you asked for \nNumber: %s\nSides: %s\nMultiplier: %s\nModifier: %s.' % (number, sides, multiplier, modifier)})
    else:
        return jsonify({'text':'example request would be \'multiroll 7 2d6+4\''})
    if (1<=number<=20) and (sides>2) and (1<=multiplier<=25):
        #return jsonify({'text':'you asked for a %s multiplier of %s rolls of a %s sided die.' % (multiplier, number, sides)})
        multiText = ''
        modifierText = ''
        if (modifier>0):
            modifierText = ' with a +%s modifier' % modifier
        for y in range(1, multiplier+1):
            rolls=[]
            total=0
            rolltext=''
            for x in range(1,number+1):
                randRoll=random.randint(1,sides)+modifier
                total+=randRoll
                rolls.append(randRoll)
            rolltext = 'R%s total: %s, rolls: %s.\n' % (y, total, rolls)
            #return jsonify({'text':'total: %s, rolls: %s.' % (total, rolls)})
            multiText += rolltext
        return jsonify({'text':'you asked for %s roll(s) of %sd%s%s.\nThe result was:\n%s' % (multiplier, number, sides, modifierText,multiText)})
    elif (sides==2):
        return jsonify({'text':'Damnit captain, I\'m a dice roller, not a coin flipper!'})
    else:
        return jsonify({'text':'test'})
        return jsonify({'text':'The multiplier must be 25 or under, \nthe number of dice must be between 1 and 20, \nand sides must be between 2 and 100.'})

@app.route('/api/slacktest/', methods=['GET','POST'])
def slacktest():
    rdata = request.form['text']
    return jsonify({'text': 'message text: %s' % rdata})

@app.route('/api/w3w/', methods=['GET','POST'])
def w3w():
    #modified from https://github.com/samzhang111/slack-w3w/blob/master/app/views.py
    rdata = request.form['text']
    w3w_base = 'http://w3w.co/'
    chunks = [x.strip() for x in rdata.split()]
    responses = []
    for token in chunks:
        if is_three_word.match(token):
            # send link
            response_text = '<{}>'.format(w3w_base + token)
            responses.append(response_text)
    #w3wLinkText = '<{}>'.format(w3w_base + token)
    return jsonify({'text': '\n'.join(responses)})

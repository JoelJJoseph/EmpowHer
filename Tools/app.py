import re
from flask import Flask, render_template, request
import os
import openai

openai.api_key = ""

def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)

app.register_error_handler(404, page_not_found)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())



@app.route('/ideas', methods=["GET", "POST"])
def ideas():

    if request.method == 'POST':
        query = request.form['Idea']
        promptxt=("Generate Startup Ideas for"+" "+query+":\n\n1.")
        print(promptxt)
        response = openai.Completion.create(
        engine="ada-instruct-beta",
        prompt=promptxt,
        temperature=1,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n\n"]
        )
        resp=response['choices'][0]['text']
        print(resp)
        split_string = resp.split("\n", 1)
        string1 = split_string[0]

    return render_template('ideas.html', **locals())



@app.route('/code-explain', methods=["GET", "POST"])
def codeExplain():

    if request.method == 'POST':
        query = request.form['codexp']
        codetxt="# Python 3 \n {} \n\n# Explanation of what the code does\n\n#".format(query)


        response = openai.Completion.create(
        engine="davinci-codex",
        prompt=codetxt,
        temperature=0,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=1,
        presence_penalty=0.0,
        stop=["#"]
        )
        print(response['choices'][0]['text'])
        

        print(query)
        openAIAnswer = response['choices'][0]['text']

    return render_template('code-explain.html', **locals())



@app.route('/bugfix', methods=["GET", "POST"])
def BugFix():

    if request.method == 'POST':
        query = request.form['codefix']
        codetxt="""
        ##### Fix bugs in the below function
    
        ### Buggy Python
        {}
        ### Fixed Python
        """.format(query)

        response = openai.Completion.create(
        engine="davinci-codex",
        prompt=codetxt,
        temperature=0,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["###"]
        )
        print(response['choices'][0]['text'])

        openAIAnswer = response['choices'][0]['text']

    return render_template('bugfix.html', **locals())



@app.route('/startup-name', methods=["GET", "POST"])
def startupName():

    if request.method == 'POST':
        query = request.form['StartupName']
        
        promptxt="This is a product name generator\n\nProduct description: A home milkshake maker\nProduct names: HomeShaker, Fit Shaker, QuickShake, Shake Maker\n\nProduct description: {}.\nProduct names:".format(query)
        response = openai.Completion.create(
        engine="curie",
        prompt=promptxt,
        temperature=1,
        max_tokens=50,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["/n"]
        )
        resp=response['choices'][0]['text']
        split_string = resp.split("\n", 1)
        print(promptxt)
        openAIAnswer = split_string[0]

       
    return render_template('startup-name.html', **locals())


@app.route('/business-pitch', methods=["GET", "POST"])
def businessPitch():

    if request.method == 'POST':
        query = request.form['businessPitch']
        promptxt="This is a Business Pitch generator\n\nProduct Name: FinanceWise\nPitch: is changing the way people think about their finances. They are building the first ever financial health engine. This puts a complete picture of your finances at your fingertips. It also monitors your spending, and gives you a simple way to fix your finances.\n\nProduct Name: {}.\nPitch:".format(query)
        response = openai.Completion.create(
        engine="curie",
        prompt=promptxt,
        temperature=1,
        n=1,
        max_tokens=100,
        top_p=0,
        frequency_penalty=1,
        presence_penalty=0,
        stop=["/n"]
        )
        resp=response['choices'][0]['text']
        split_string = resp.split("Product", 1)
        print(promptxt)
        openAIAnswer = split_string[0]
    return render_template('business-pitch.html', **locals())











if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)

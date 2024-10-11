from flask import Flask, render_template, request, jsonify
import os
import openai
import prompts

app = Flask(__name__)

openai.api_key = prompts.key

def complete(text, messages):
    messages.append({"role": "user", "content": text})
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages
    )

    assistant_message = completion["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": assistant_message})
    
    return messages

messages = [{"role": "system", "content": f"{prompts.prompt1}"}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    global messages
    user_input = request.args.get('msg')
    messages = complete(user_input, messages)
    response = messages[-1]["content"]
    return response



if __name__ == '__main__':
    app.run(debug=True)

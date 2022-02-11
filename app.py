from flask import Flask, render_template, request

# local imports from our chatbot file
from chatbot import predict_class, get_response, intents

## DATETIME TEST




app = Flask(__name__)
app.config['SECRET__KEY'] = "FLIPPING_WELL_SECRETIVE_0192837465"

answer_list = []

@app.route('/')
def home():
    global answer_list
    answer_list.clear()
    return render_template('index.html')

# the chatbot function

@app.route('/chatbot', methods=["POST", "GET"])
def chatbot():
    global answer_list
    if request.method == "POST":
        message = request.form['message']
        ints = predict_class(message)
        response = get_response(ints, intents)
        answer_list.append(response)
        print(answer_list)
        if len(answer_list) > 5:
            answer_list.remove(answer_list[0])
        return render_template('chatbot.html', message=message, answer_list=answer_list )
    return render_template('chatbot.html', message="", answer_list="")
        

if __name__ == "__main__":
    app.run(debug=True)
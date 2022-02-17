from flask import Flask, render_template, request

# local imports from our chatbot file
from chatbot import predict_class, get_response, intents

## DATETIME TEST




app = Flask(__name__)
app.config['SECRET__KEY'] = "FLIPPING_WELL_SECRETIVE_0192837465"

answer_list = []
chat_box = []
question_list = []

@app.route('/')
def home():
    global answer_list
    answer_list.clear()
    question_list.clear()
    chat_box.clear()
    return render_template('index.html')

# the chatbot function

@app.route('/chatbot', methods=["POST", "GET"])
def chatbot():
    global answer_list
    if request.method == "POST":
        message = request.form['message']
        ints = predict_class(message)
        response = get_response(ints, intents)
        chat_box.append(response)
        chat_box.append(message)
        answer_list.append(response)
        question_list.append(message)
        print(chat_box)
        if len(chat_box) > 2:
            answer_list.remove(answer_list[0])
            question_list.remove(question_list[0])
            chat_box.remove(chat_box[0])
            chat_box.remove(chat_box[0])
        return render_template('chatbot.html', message=message, answer_list=answer_list, question_list=question_list, chat_box=chat_box , scroll='message-box')
    return render_template('chatbot.html', message="", answer_list="")
        

if __name__ == "__main__":
    app.run(debug=True)
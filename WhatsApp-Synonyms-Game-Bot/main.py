from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from get_words import get_word
import os


app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]


@app.route("/synonymsgame", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip().lower()

    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == "new game":
        random_word, synonyms = get_word()
        session["num_correct"] = 0
        session["random_word"] = random_word
        session["synonyms"] = synonyms
        msg.body(f"First word: {random_word}. Type a synonym!")
    elif session.get("random_word"):
        random_word = session["random_word"]
        synonyms = session["synonyms"]

        if incoming_msg in synonyms:
            session["num_correct"] += 1
            session.pop("random_word")
            session.pop("synonyms")

            random_word, synonyms = get_word()

            session["random_word"] = random_word
            session["synonyms"] = synonyms

            msg.body(f"Correct! Next word: {random_word}. Type a synonym!")

        else:
            session.pop("random_word")
            session.pop("synonyms")
            score = session["num_correct"]
            msg.body(f"Game over. You got {score} questions correctly.\n\n"
                     f"Synonyms for figure are {synonyms}\n\n"
                     f"Type 'new game' to start a new game.")

    else:
        msg.body("Type 'new game' to start a new game.")

    return str(resp)


if __name__ == "__main__":
    app.run()

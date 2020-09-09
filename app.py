from flask import Flask, request, render_template, redirect, session, jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "abc123"


@app.route("/")
def home_page():
    """Homepage with really big button to start the game"""

    board = boggle_game.make_board()
    session["board"] = board
    nplays = session.get("nplays", 0)
    return render_template("home.html")


@app.route("/game", methods=["POST"])
def game_main():
    """Main form where the game takes place?"""
    return render_template("game.html")


@app.route("/check-word", methods=["GET"])
def check_word():
    """Check word route that takes the word submitted in the guess form and checks to see if it is a real word and\or on the board"""
    user_guess = request.args["word"]
    # print(user_guess)
    valid = boggle_game.check_valid_word(session["board"], user_guess)
    # print(valid)
    return jsonify({"result": valid})


@app.route("/update-stats", methods=["POST"])
def update_stats():
    """this route is for updating the score stats including games played"""
    highscore = 0
    score = request.json["score"]
    if score > highscore:
        highscore = score
    session["highscore"] = highscore
    nplays = session.get("nplays", 0)
    session["nplays"] = nplays + 1
    return jsonify({"score": score})

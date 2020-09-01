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
    return render_template("home.html")


@app.route("/game", methods=["GET", "POST"])
def game_main():
    """Main form where the game takes place?"""
    return render_template("game.html")


@app.route("/check-word", methods=["GET", "POST"])
def check_word():
    user_guess = request.args["word"]
    # print(user_guess)
    valid = boggle_game.check_valid_word(session["board"], user_guess)
    # print(valid)
    return jsonify({"result": valid})

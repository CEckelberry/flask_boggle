from boggle import Boggle
from flask import Flask, request, render_template, redirect, session
from boggle import Boggle


app = Flask(__name__)
app.config["SECRET_KEY"] = "abc123"


@app.route("/")
def home_page():
    """Homepage with really big button to start the game"""
    return render_template("home.html")


@app.route("/game", methods=["POST"])
def game_main():
    """Main form where the game takes place?"""
    words = Boggle.read_dict
    board = Boggle.make_board(words)
    return render_template("game.html", board=board,)


boggle_game = Boggle()

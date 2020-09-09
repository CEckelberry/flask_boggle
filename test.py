from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config["TESTING"] = True

    # Boggle Tests
    def test_read_dict(self):
        """Checks to make sure the text dictionary can be opened"""
        self.assertTrue(Boggle.read_dict(self, "words.txt"))

    # Flask tests
    def test_home(self):
        """Checks that the home page renders all HTML attributes including session variables"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 id="start" class="animated">The button below will start a game of Boggle!</h1>',
                html,
            )
            self.assertIn(
                '<button class="btn btn-mdb-color btn-lg btn-block">Start Boggle</button>',
                html,
            )
            self.assertIn(
                "<p><b>Games Played: &nbsp;</b> &nbsp;| &nbsp;<b>Highest Score: &nbsp;</b></p>",
                html,
            )
            self.assertTrue(session["board"])
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("nplays"))

    def test_check_valid_word(self):
        """Checks the check word function in the Boggle class and its HTML response"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess["board"] = [
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                ]
        response = self.client.get("/check-word?word=cat")
        self.assertEqual(response.json["result"], "ok")

    def test_check_not_on_board_word(self):
        """Checks the check word function to see if a word is valid, but not on the current board"""
        self.client.get("/")
        response = self.client.get("/check-word?word=inconceivable")
        self.assertEqual(response.json["result"], "not-on-board")

    def test_check_not_a_word(self):
        """Checks the check word function to make sure it is picking up invalid words"""
        self.client.get("/")
        response = self.client.get("/check-word?word=dfasdfas")
        self.assertEqual(response.json["result"], "not-word")

from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "rock-paper-scissors-secret-key"

# Same number system used in the original Python program
options = [1, -1, 0]
choices = {"rock": 1, "paper": -1, "scissors": 0}
reverse_choices = {1: "Rock", -1: "Paper", 0: "Scissors"}


def find_result(user_choice, computer_choice):
    """Return whether the player won, lost, or drew."""
    if user_choice == computer_choice:
        return "draw"

    # Paper beats rock, scissors beats paper, and rock beats scissors.
    if (user_choice == -1 and computer_choice == 1) or \
       (user_choice == 0 and computer_choice == -1) or \
       (user_choice == 1 and computer_choice == 0):
        return "win"

    return "lose"


@app.route("/", methods=["GET", "POST"])
def home():
    # Start the score the first time the page is opened.
    if "wins" not in session:
        session["wins"] = 0
        session["losses"] = 0
        session["draws"] = 0

    result = None
    user_choice_name = None
    computer_choice_name = None

    if request.method == "POST":
        user_input = request.form.get("choice", "")

        if user_input in choices:
            user_choice = choices[user_input]
            computer_choice = random.choice(options)

            user_choice_name = reverse_choices[user_choice]
            computer_choice_name = reverse_choices[computer_choice]
            result = find_result(user_choice, computer_choice)

            if result == "win":
                session["wins"] += 1
            elif result == "lose":
                session["losses"] += 1
            else:
                session["draws"] += 1
        else:
            result = "invalid"

    return render_template(
        "index.html",
        result=result,
        user_choice=user_choice_name,
        computer_choice=computer_choice_name,
        wins=session["wins"],
        losses=session["losses"],
        draws=session["draws"]
    )


@app.route("/reset", methods=["POST"])
def reset_score():
    session["wins"] = 0
    session["losses"] = 0
    session["draws"] = 0
    return render_template(
        "index.html",
        result=None,
        user_choice=None,
        computer_choice=None,
        wins=0,
        losses=0,
        draws=0
    )


if __name__ == "__main__":
    app.run(debug=True)


#Used : Python, HTML5, CSS, Flask
#used CMD to render it on web temporarily
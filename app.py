from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from flask import flash
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET KEY'] = "secret"

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route("/")  # step two
def show_start():
    """Select a survey."""

    responses = []

    return render_template("start.html", survey=survey)


@app.route("/questions/<int:qid>")  # STEP3
def show_question(qid):
    """Display current question."""

    responses = RESPONSES_KEY

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/begin", methods=["POST"])  # step two
def start_survey():
    """Clear the session of responses."""

    return redirect("/questions/0")  # directs user to questions/0


@app.route("/answer", methods=["POST"])  # STEP4
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = RESPONSES_KEY
    responses.append(choice)
    # session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/end")  # STEP5
def end():
    """Survey Submitted. Thank you page"""

    return render_template("thanks.html")

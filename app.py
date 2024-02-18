import datetime
import json
import random

from flask import Flask, render_template, request

app = Flask(__name__)

with open("cmudict-0.7b.txt", "r", encoding="latin-1") as file:
    data = file.read()

with open("history.json", "r") as file:
    history = json.load(file)

rhymes = {}
all_words = []
words_to_phonemes = {}

for rhyme in data.split("\n"):
    if not rhyme.startswith(";;;"):
        if "  " not in rhyme:
            continue
        word, phonemes = rhyme.split("  ")
        word = word.lower()
        phonemes = phonemes.strip()  # .replace()
        # get last 3 like EY2 Z from S AO1 R D P L EY2 Z
        phonemes = phonemes.split(" ")[-3:]
        phonemes = " ".join(phonemes)
        if phonemes in rhymes:
            rhymes[phonemes].append(word)
        else:
            rhymes[phonemes] = [word]

        all_words.append(word)
        words_to_phonemes[word] = phonemes


@app.route("/", methods=["GET", "POST"])
def index():
    if history.get(str(datetime.date.today())) is None:
        history[str(datetime.date.today())] = random.choice(all_words)

        with open("history.json", "w") as file:
            json.dump(history, file)

    if request.method == "POST":
        words = request.form["words"]

        words = words.split("\n")
        words = [word.strip() for word in words]

        rhyming_words = []

        phoneme = words_to_phonemes[history[str(datetime.date.today())]]

        for word in words:
            word = word.lower()
            if word in rhymes[phoneme]:
                rhyming_words.append(word)

        return render_template(
            "index.html",
            words=words,
            rhyming_words=rhyming_words,
            word_of_the_day=history[str(datetime.date.today())],
            rhyming_words_count=len(rhyming_words),
        )

    return render_template(
        "index.html", word_of_the_day=history[str(datetime.date.today())]
    )


if __name__ == "__main__":
    app.run(debug=True)

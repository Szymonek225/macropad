from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
CONFIG_PATH = "D:/shortcut_config.json"

# Ustawienia domyślne
DEFAULT_SHORTCUTS = ["" for _ in range(9)]

def load_shortcuts():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return DEFAULT_SHORTCUTS.copy()

def save_shortcuts(shortcuts):
    with open(CONFIG_PATH, "w") as f:
        json.dump(shortcuts, f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        shortcuts = [request.form.get(f"btn{i+1}", "") for i in range(9)]
        save_shortcuts(shortcuts)
        return redirect(url_for("index"))

    shortcuts = load_shortcuts()
    return render_template("index.html", shortcuts=shortcuts)

if __name__ == "__main__":
    app.run(debug=True)


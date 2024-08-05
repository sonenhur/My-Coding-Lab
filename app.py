from flask import Flask, redirect, render_template, request, session, url_for

from battle import battle
from character import Character

app = Flask(__name__)
app.secret_key = "your_secret_key"

CHARACTER_OPTIONS = [
    {"name": "Hero", "health": 100, "attack": 20, "defense": 10},
    {"name": "Warrior", "health": 120, "attack": 18, "defense": 15},
    {"name": "Mage", "health": 80, "attack": 25, "defense": 5},
]

ENEMY_OPTIONS = [
    {"name": "Goblin", "health": 50, "attack": 15, "defense": 5},
    {"name": "Orc", "health": 80, "attack": 18, "defense": 8},
    {"name": "Dragon", "health": 150, "attack": 25, "defense": 15},
]


@app.route("/")
def index():
    if "player" not in session:
        return render_template("character_selection.html", characters=CHARACTER_OPTIONS)
    player = Character.from_dict(session["player"])
    return render_template("index.html", player=player)


@app.route("/select_character", methods=["POST"])
def select_character():
    selected_character = request.form["character"]
    character_data = next(
        char for char in CHARACTER_OPTIONS if char["name"] == selected_character
    )
    player = Character(**character_data)
    session["player"] = player.to_dict()
    return redirect(url_for("index"))


@app.route("/battle")
def battle_page():
    player = Character.from_dict(session["player"])
    enemy_data = ENEMY_OPTIONS[player.level % len(ENEMY_OPTIONS)]
    enemy = Character(**enemy_data)
    session["enemy"] = enemy.to_dict()
    return render_template("battle.html", player=player, enemy=enemy)


@app.route("/action", methods=["POST"])
def action():
    player = Character.from_dict(session["player"])
    enemy = Character.from_dict(session["enemy"])
    action = request.form["action"]
    item_name = request.form.get("item_name", None)

    status, message = battle(player, enemy, action, item_name)

    session["player"] = player.to_dict()
    session["enemy"] = enemy.to_dict()

    if status == "run":
        return redirect(url_for("index"))
    elif status == "lose":
        return redirect(url_for("result", result="lose"))
    elif status == "win":
        return redirect(url_for("result", result="win"))

    return render_template("battle.html", player=player, enemy=enemy, message=message)


@app.route("/result/<result>")
def result(result):
    player = Character.from_dict(session["player"])
    if result == "win":
        message = f"{player.name} won the battle and leveled up!"
    else:
        message = f"{player.name} was defeated."
    return render_template("result.html", message=message, result=result)


@app.route("/rest")
def rest():
    player = Character.from_dict(session["player"])
    player.health = player.max_health
    session["player"] = player.to_dict()
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    session.clear()  # Clear all session data
    return redirect(url_for("index"))  # Redirect to character selection


if __name__ == "__main__":
    app.run(debug=True)

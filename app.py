from flask import Flask, redirect, render_template, request, session, url_for

from battle import battle
from character import Character
from items import buy_item, get_items  # buy_item을 임포트합니다.

app = Flask(__name__)
app.secret_key = "your_secret_key"

CHARACTER_OPTIONS = [
    {"name": "전사", "health": 130, "attack": 16, "defense": 14},
    {"name": "궁수", "health": 100, "attack": 18, "defense": 12},
    {"name": "마법사", "health": 90, "attack": 22, "defense": 8},
]

ENEMY_OPTIONS = [
    {"name": "고블린", "health": 50, "attack": 15, "defense": 5},
    {"name": "오크", "health": 80, "attack": 18, "defense": 8},
    {"name": "드래곤", "health": 150, "attack": 25, "defense": 15},
    {"name": "스켈레톤", "health": 60, "attack": 12, "defense": 10},
    {"name": "트롤", "health": 100, "attack": 20, "defense": 12},
    {"name": "늑대인간", "health": 90, "attack": 20, "defense": 10},
    {"name": "좀비", "health": 70, "attack": 10, "defense": 8},
    {"name": "뱀파이어", "health": 110, "attack": 18, "defense": 12},
    {"name": "하피", "health": 80, "attack": 16, "defense": 9},
    {"name": "슬라임", "health": 40, "attack": 8, "defense": 5},
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
        (char for char in CHARACTER_OPTIONS if char["name"] == selected_character), None
    )
    if character_data is None:
        return "Invalid character selected", 400
    player = Character(**character_data)
    player.gold = 100  # 초기 골드를 설정합니다.
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

    status, message, experience_reward, gold_reward = battle(
        player, enemy, action, item_name
    )

    session["player"] = player.to_dict()
    session["enemy"] = enemy.to_dict()

    if status == "run":
        return redirect(url_for("index"))
    elif status == "lose":
        return redirect(
            url_for(
                "result",
                result="lose",
                experience_reward=experience_reward,
                gold_reward=gold_reward,
            )
        )
    elif status == "win":
        return redirect(
            url_for(
                "result",
                result="win",
                experience_reward=experience_reward,
                gold_reward=gold_reward,
            )
        )

    return render_template("battle.html", player=player, enemy=enemy, message=message)


@app.route("/result/<result>")
def result(result):
    player = Character.from_dict(session["player"])
    experience_reward = request.args.get("experience_reward", 0, type=int)
    gold_reward = request.args.get("gold_reward", 0, type=int)

    if result == "win":
        message = f"{player.name}가 전투에서 승리하고 레벨업했습니다!"
    else:
        message = f"{player.name}가 패배했습니다."

    return render_template(
        "result.html",
        message=message,
        result=result,
        experience_reward=experience_reward,
        gold_reward=gold_reward,
    )


@app.route("/rest")
def rest():
    player = Character.from_dict(session["player"])
    player.health = player.max_health
    session["player"] = player.to_dict()
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    session.clear()  # 모든 세션 데이터를 지웁니다
    return redirect(url_for("index"))  # 캐릭터 선택 화면으로 리디렉션합니다


@app.route("/shop")
def shop():
    player = Character.from_dict(session["player"])
    items = get_items()
    return render_template("shop.html", player=player, items=items)


@app.route("/buy", methods=["POST"])
def buy():
    player = Character.from_dict(session["player"])
    item_name = request.form["item_name"]
    success, message = buy_item(player, item_name)  # buy_item 호출
    session["player"] = player.to_dict()
    return render_template(
        "shop.html", items=get_items(), player=player, message=message
    )


if __name__ == "__main__":
    app.run(debug=True)

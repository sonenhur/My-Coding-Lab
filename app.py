# app.py

import json
import random
import re

from flask import Flask, redirect, render_template, request, session, url_for

from character import Character
from items import buy_item, get_items
from quest import Quest  # 퀘스트 클래스 임포트

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 비밀 키는 안전한 방법으로 설정하는 것이 좋습니다


# 정규 표현식을 사용하여 특수문자 검사를 추가
def is_valid_name(name):
    return re.match("^[a-zA-Z0-9가-힣]+$", name) is not None


def load_character_options(file_path="characters.json"):
    with open(file_path, "r") as file:
        return json.load(file)


def load_enemy_options(file_path="enemies.json"):
    with open(file_path, "r") as file:
        return json.load(file)


CHARACTER_OPTIONS = load_character_options()
ENEMY_OPTIONS = load_enemy_options()


def get_enemy_for_level(level):
    # 적의 레벨 범위 설정
    min_level = max(1, level - 2)  # 현재 레벨에서 -2 레벨까지의 적도 등장 가능하게
    max_enemy_level = min(
        level + 2, len(ENEMY_OPTIONS)
    )  # 현재 레벨에서 +2 레벨까지의 적도 등장 가능하게
    eligible_enemies = ENEMY_OPTIONS[
                       min_level - 1: max_enemy_level
                       ]  # 범위 내의 적 선택
    return random.choice(eligible_enemies)


@app.route("/")
def title():
    return render_template("title.html")


@app.route("/index")
def index():
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("character_selection"))

    player = Character.from_dict(player_data)
    return render_template("index.html", player=player)


@app.route("/character_selection")
def character_selection():
    return render_template("character_selection.html", characters=CHARACTER_OPTIONS)


@app.route("/select_character", methods=["POST"])
def select_character():
    selected_character = request.form.get("character")
    player_name = request.form.get("player_name").strip()

    if not is_valid_name(player_name):
        return "이름에는 영문, 숫자, 한글만 사용할 수 있습니다.", 400

    character_data = next(
        (char for char in CHARACTER_OPTIONS if char["name"] == selected_character), None
    )
    if not character_data:
        return "Invalid character selected", 400

    full_name = f"{character_data['name']} {player_name}"

    # character_data에서 name 키 제거
    character_data.pop("name")

    # character_data에서 level_growth 값을 전달
    player = Character(name=full_name, **character_data)
    player.gold = 100

    quest_kill_5_enemies = Quest("적 5마리 처치", "적을 5번 처치하세요.", 5, 100)
    player.add_quest(quest_kill_5_enemies)

    session["player"] = player.to_dict()
    return redirect(url_for("index"))


@app.route("/battle")
def battle_page():
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    print(f"Player inventory in battle: {player.inventory}")  # 디버깅 출력

    enemy = get_enemy_for_level(player.level)
    enemy = Character(**enemy)
    session["enemy"] = enemy.to_dict()
    return render_template("battle.html", player=player, enemy=enemy)


# app.py

from battle import battle, BattlePhase  # BattlePhase 추가


@app.route("/action", methods=["POST"])
def action():
    player_data = session.get("player")
    enemy_data = session.get("enemy")

    if not player_data or not enemy_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    enemy = Character.from_dict(enemy_data)
    action = request.form.get("action")
    item_index = request.form.get("item_index", type=int)

    # 1. 플레이어 턴
    status, message, experience_reward, gold_reward, next_phase = battle(
        player, enemy, BattlePhase.PLAYER_TURN, action, item_index
    )

    # 2. 적 턴
    if next_phase == BattlePhase.ENEMY_TURN:
        status, enemy_message, experience_reward, gold_reward, next_phase = battle(
            player, enemy, BattlePhase.ENEMY_TURN
        )
        message += f" {enemy_message}"

    # 3. 전투 종료 체크
    if next_phase == BattlePhase.CHECK_END:
        status, end_message, experience_reward, gold_reward, next_phase = battle(
            player, enemy, BattlePhase.CHECK_END
        )
        message += f" {end_message}"

    # 4. 결과에 따라 처리
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
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    experience_reward = request.args.get("experience_reward", 0, type=int)
    gold_reward = request.args.get("gold_reward", 0, type=int)

    if result == "win":
        message = f"{player.name}가 전투에서 승리했습니다!"
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
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    player.health = player.max_health
    session["player"] = player.to_dict()
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    session.clear()  # 세션 데이터 완전히 초기화
    return redirect(url_for("title"))  # 타이틀 화면으로 리디렉션


@app.route("/shop")
def shop():
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    items = get_items()
    return render_template("shop.html", items=items, player=player)


@app.route("/buy", methods=["POST"])
def buy():
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    item_name = request.form.get("item_name")
    success, message = buy_item(player, item_name)
    if success:
        session["player"] = player.to_dict()
        print(
            f"Updated player inventory after purchase: {player.inventory}"
        )  # 디버깅 출력

    items = get_items()
    return render_template("shop.html", items=items, player=player, message=message)


@app.route("/quests")
def quests():
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    return render_template("quests.html", player=player, quests=player.quests)


@app.route("/complete_quest", methods=["POST"])
def complete_quest():
    player_data = session.get("player")
    if not player_data:
        return redirect(url_for("index"))

    player = Character.from_dict(player_data)
    quest_name = request.form.get("quest_name")
    message = player.complete_quest(quest_name)
    session["player"] = player.to_dict()
    return redirect(url_for("quests"))


if __name__ == "__main__":
    app.run(debug=True)

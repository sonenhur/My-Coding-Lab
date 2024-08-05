import random

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack = 10
        self.defense = 5
        self.level = 1
        self.exp = 0
        self.inventory = {"힐링 포션": 3}

    def level_up(self):
        self.level += 1
        self.attack += 2
        self.defense += 1
        self.hp += 20

    def use_item(self, item):
        if item in self.inventory and self.inventory[item] > 0:
            if item == "힐링 포션":
                self.hp += 20
                self.inventory[item] -= 1
                if self.inventory[item] == 0:
                    del self.inventory[item]
                return True
        return False

    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "exp": self.exp,
            "inventory": self.inventory,
        }


class Monster:
    def __init__(self, name, hp, attack, exp, defense=0):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.exp = exp
        self.defense = defense

    def perform_special_attack(self, player):
        if self.special_attack:
            self.special_attack(player)


def get_monster(player_level):
    monsters = [
        Monster(
            "고블린",
            30 + player_level * 2,
            5 + player_level,
            10,
            defense=2 + player_level,
        ),
        Monster(
            "오크",
            50 + player_level * 5,
            10 + player_level,
            20,
            defense=5 + player_level,
        ),
        Monster(
            "늑대",
            40 + player_level * 3,
            8 + player_level,
            15,
            defense=3 + player_level,
        ),
        Monster(
            "정령",
            25 + player_level * 4,
            7 + player_level,
            12,
            defense=3 + player_level,
        ),
        Monster(
            "드래곤",
            100 + player_level * 10,
            20 + player_level * 2,
            50,
            defense=10 + player_level,
        ),
    ]
    available_monsters = [
        m for m in monsters if m.name != "드래곤" or player_level >= 5
    ]
    return random.choice(available_monsters)


# In-memory player storage
players = {}


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/battle-history")
def battle_history():
    return send_from_directory("static", "battle_history.html")


@app.route("/start", methods=["POST"])
def start_game():
    data = request.json
    player_name = data["name"]
    player = Player(player_name)
    players[player_name] = player
    return jsonify(player.to_dict())


@app.route("/attack", methods=["POST"])
def attack():
    data = request.json
    player_name = data["name"]
    player = players.get(player_name)
    if not player:
        return jsonify({"status": "Error", "message": "게임을 시작해주세요."})

    monster = get_monster(player.level)
    log_messages = []

    while player.hp > 0 and monster.hp > 0:
        # Player attack
        damage_to_monster = max(player.attack - monster.defense, 0)
        monster.hp -= damage_to_monster
        log_messages.append(
            f"{player.name}(이)가 {monster.name}(을)를 공격했습니다. {monster.name}의 HP: {monster.hp}"
        )

        if monster.hp <= 0:
            player.exp += monster.exp
            if player.exp >= 10 * player.level:
                player.level_up()
            return jsonify(
                {
                    "status": "Victory",
                    "message": "승리했습니다!",
                    "player": player.to_dict(),
                    "log": log_messages,
                }
            )

        # Monster attack
        damage_to_player = max(monster.attack - player.defense, 0)
        player.hp -= damage_to_player
        log_messages.append(
            f"{monster.name}(이)가 {player.name}(을)를 공격했습니다. {player.name}의 HP: {player.hp}"
        )

        if player.hp <= 0:
            del players[player_name]
            return jsonify(
                {
                    "status": "Game Over",
                    "message": "패배했습니다!",
                    "player": player.to_dict(),
                    "log": log_messages,
                }
            )
    return jsonify(
        {
            "status": "In Progress",
            "message": "전투 중입니다.",
            "player": player.to_dict(),
            "log": log_messages,
        }
    )


@app.route("/use-item", methods=["POST"])
def use_item():
    data = request.json
    player_name = data["name"]
    player = players.get(player_name)
    if not player:
        return jsonify({"status": "Error", "message": "게임을 시작해주세요."})

    if player.use_item("힐링 포션"):
        return jsonify({"status": "Item Used", "player": player.to_dict()})
    else:
        return jsonify(
            {"status": "Item Not Found", "message": "아이템을 찾을 수 없습니다."}
        )


if __name__ == "__main__":
    app.run(debug=True)

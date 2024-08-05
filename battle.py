from character import Character
from items import Item


def battle(player, enemy, action, item_name=None):
    message = ""
    if action == "attack":
        damage = player.attack_target(enemy)
        message = f"{player.name}가 {enemy.name}에게 {damage}의 피해를 입혔습니다."
    elif action == "defend":
        message = f"{player.name}가 방어했습니다."
    elif action == "item" and item_name:
        if item_name == "potion":
            potion = Item("포션", "heal")
            potion.use(player)
            message = f"{player.name}가 포션을 사용했습니다."
        elif item_name == "buff":
            buff = Item("공격력 증가", "buff")
            buff.use(player)
            message = f"{player.name}가 공격력 증가 아이템을 사용했습니다."
    elif action == "run":
        message = f"{player.name}가 도망쳤습니다!"
        return "run", message

    if enemy.is_alive():
        damage = enemy.attack_target(player)
        message += f" {enemy.name}가 {player.name}에게 {damage}의 피해를 입혔습니다."

    if player.is_alive() and not enemy.is_alive():
        player.gain_experience(enemy.level * 5)
        return "win", message
    elif not player.is_alive():
        return "lose", message

    return "continue", message

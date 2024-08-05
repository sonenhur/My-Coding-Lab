from character import Character
from items import Item


def battle(player, enemy, action, item_name=None):
    message = ""
    if action == "attack":
        damage = player.attack_target(enemy)
        message = f"{player.name} attacks {enemy.name} for {damage} damage."
    elif action == "defend":
        message = f"{player.name} defends."
    elif action == "item" and item_name:
        if item_name == "potion":
            potion = Item("Potion", "heal")
            potion.use(player)
            message = f"{player.name} uses a potion."
        elif item_name == "buff":
            buff = Item("Attack Buff", "buff")
            buff.use(player)
            message = f"{player.name} uses an attack buff."
    elif action == "run":
        message = f"{player.name} runs away!"
        return "run", message

    if enemy.is_alive():
        damage = enemy.attack_target(player)
        message += f" {enemy.name} attacks {player.name} for {damage} damage."

    if player.is_alive() and not enemy.is_alive():
        player.gain_experience(enemy.level * 5)
        return "win", message
    elif not player.is_alive():
        return "lose", message

    return "continue", message

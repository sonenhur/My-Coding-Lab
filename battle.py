from character import Character
from items import Item


def battle(player, enemy, action, item_name=None):
    message = ""
    experience_reward = 0
    gold_reward = 0

    if action == "attack":
        damage = player.attack_target(enemy)
        message = f"{player.name}가 {enemy.name}에게 {damage}의 피해를 입혔습니다."
    elif action == "defend":
        message = f"{player.name}가 방어했습니다."
    elif action == "item":
        if not item_name:
            message = "아이템 이름을 입력해 주세요."
        else:
            item = next(
                (
                    item
                    for item in player.inventory
                    if item.name.lower() == item_name.lower()
                ),
                None,
            )
            if item:
                item.use(player)
                message = f"{player.name}가 {item_name}을(를) 사용했습니다."
            else:
                message = f"아이템 '{item_name}'을(를) 찾을 수 없습니다."
    elif action == "run":
        message = f"{player.name}가 도망쳤습니다!"
        return "run", message, experience_reward, gold_reward

    if enemy.is_alive():
        damage = enemy.attack_target(player)
        message += f" {enemy.name}가 {player.name}에게 {damage}의 피해를 입혔습니다."

    if player.is_alive() and not enemy.is_alive():
        experience_reward = enemy.level * 10  # 경험치 보상
        gold_reward = enemy.level * 5  # 골드 보상
        player.gain_experience(experience_reward)
        player.gold += gold_reward
        return "win", message, experience_reward, gold_reward
    elif not player.is_alive():
        return "lose", message, experience_reward, gold_reward

    return "continue", message, experience_reward, gold_reward

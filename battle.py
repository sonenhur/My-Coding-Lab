from character import Character
from items import Item


def battle(player, enemy, action, item_name=None):
    message = ""
    experience_reward = 0
    gold_reward = 0

    # 행동에 따른 처리
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
                item.use(player)  # 아이템 사용
                player.inventory.remove(item)  # 인벤토리에서 아이템 제거
                # 상태가 업데이트된 후 확인
                message = f"{player.name}가 {item_name}을(를) 사용했습니다."
            else:
                message = f"아이템 '{item_name}'을(를) 찾을 수 없습니다."
    elif action == "run":
        message = f"{player.name}가 도망쳤습니다!"
        return "run", message, experience_reward, gold_reward
    else:
        message = "잘못된 행동입니다. 'attack', 'defend', 'item', 'run' 중 하나를 선택해 주세요."
        return "continue", message, experience_reward, gold_reward

    # 적이 살아있는 경우, 적의 반격 처리
    if enemy.is_alive():
        damage = enemy.attack_target(player)
        message += f" {enemy.name}가 {player.name}에게 {damage}의 피해를 입혔습니다."

    # 전투 결과 처리
    if player.is_alive() and not enemy.is_alive():
        experience_reward = enemy.level * 10  # 경험치 보상
        gold_reward = enemy.level * 5  # 골드 보상
        player.gain_experience(experience_reward)
        player.gold += gold_reward
        message += f" {player.name}가 승리하고 {experience_reward} 경험치와 {gold_reward} 골드를 획득했습니다."
        return "win", message, experience_reward, gold_reward
    elif not player.is_alive():
        message += f" {player.name}가 패배했습니다."
        return "lose", message, experience_reward, gold_reward

    return "continue", message, experience_reward, gold_reward

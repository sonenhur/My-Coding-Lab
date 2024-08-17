# battle.py

from character import Character


def battle(player: Character, enemy: Character, action: str, item_index: int = None):
    message = ""
    experience_reward = 0
    gold_reward = 0

    # 행동에 따른 처리
    if action == "attack":
        damage = player.attack_target(enemy)
        message = f"{player.name}(이)가 {enemy.name}에게 {damage}의 피해를 입혔습니다."
    elif action == "defend":
        message = f"{player.name}(이)가 방어했습니다."
    elif action == "item":
        if item_index is None:
            return (
                "continue",
                "아이템 번호를 입력하세요.",
                experience_reward,
                gold_reward,
            )
        item_used, message = use_item(player, item_index)
        if not item_used:
            return "continue", message, experience_reward, gold_reward
    elif action == "run":
        message = f"{player.name}(은)는 도망쳤습니다!"
        return "run", message, experience_reward, gold_reward
    else:
        message = "잘못된 행동입니다. 'attack', 'defend', 'item', 'run' 중 하나를 선택해 주세요."
        return "continue", message, experience_reward, gold_reward

    # 적이 살아있는 경우, 적의 반격 처리
    if enemy.is_alive():
        damage = enemy.attack_target(player)
        message += (
            f" {enemy.name}(이)가 {player.name}에게 {damage}의 피해를 입혔습니다."
        )

    # 전투 결과 처리
    if player.is_alive() and not enemy.is_alive():
        experience_reward = enemy.level * 10  # 경험치 보상
        gold_reward = enemy.level * 5  # 골드 보상
        player.gain_experience(experience_reward)
        player.gold += gold_reward
        message += f" {player.name}(이)가 승리하고 {experience_reward} 경험치와 {gold_reward} 골드를 획득했습니다."
        player.update_quests()  # 퀘스트 진행 상황 업데이트
        return "win", message, experience_reward, gold_reward
    elif not player.is_alive():
        message += f" {player.name}(이)가 패배했습니다."
        return "lose", message, experience_reward, gold_reward

    return "continue", message, experience_reward, gold_reward


def use_item(character, item_index):
    try:
        item = character.inventory[
            item_index - 1
        ]  # 1부터 시작하는 번호를 0 인덱스로 변환
        item.use(character)
        character.inventory.pop(item_index - 1)
        return True, f"{item.name}을(를) 사용했습니다."
    except IndexError:
        return False, "잘못된 아이템 번호입니다."
    except (TypeError, ValueError):
        return False, "아이템 번호는 숫자여야 합니다."

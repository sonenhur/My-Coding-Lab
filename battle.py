# battle.py

# 전투 단계를 관리하는 Enum 정의
from enum import Enum, auto

from character import Character


class BattlePhase(Enum):
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()
    CHECK_END = auto()
    COMPLETE = auto()


def battle(player: Character, enemy: Character, phase: BattlePhase, action: str = None, item_index: int = None):
    message = ""
    experience_reward = 0
    gold_reward = 0

    if phase == BattlePhase.PLAYER_TURN:
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
                    BattlePhase.PLAYER_TURN
                )
            item_used, item_message = use_item(player, item_index)
            message = item_message
            if not item_used:
                return "continue", message, experience_reward, gold_reward, BattlePhase.PLAYER_TURN
        elif action == "run":
            message = f"{player.name}(은)는 도망쳤습니다!"
            return "run", message, experience_reward, gold_reward, BattlePhase.COMPLETE
        else:
            message = "잘못된 행동입니다. 'attack', 'defend', 'item', 'run' 중 하나를 선택해 주세요."
            return "continue", message, experience_reward, gold_reward, BattlePhase.PLAYER_TURN

        # 적의 상태 체크
        return "continue", message, experience_reward, gold_reward, BattlePhase.ENEMY_TURN

    elif phase == BattlePhase.ENEMY_TURN:
        if enemy.is_alive():
            damage = enemy.attack_target(player)
            message = f"{enemy.name}(이)가 {player.name}에게 {damage}의 피해를 입혔습니다."
        return "continue", message, experience_reward, gold_reward, BattlePhase.CHECK_END

    elif phase == BattlePhase.CHECK_END:
        # 전투 종료 조건 체크
        if not player.is_alive():
            message += f" {player.name}(이)가 패배했습니다."
            return "lose", message, experience_reward, gold_reward, BattlePhase.COMPLETE
        elif not enemy.is_alive():
            experience_reward = enemy.level * 10  # 경험치 보상
            gold_reward = enemy.level * 5  # 골드 보상
            player.gain_experience(experience_reward)
            player.gold += gold_reward
            message += f" {player.name}(이)가 승리하고 {experience_reward} 경험치와 {gold_reward} 골드를 획득했습니다."
            player.update_quests()  # 퀘스트 진행 상황 업데이트
            return "win", message, experience_reward, gold_reward, BattlePhase.COMPLETE

        # 전투 계속 진행
        return "continue", message, experience_reward, gold_reward, BattlePhase.PLAYER_TURN

    elif phase == BattlePhase.COMPLETE:
        return "complete", message, experience_reward, gold_reward, BattlePhase.COMPLETE


def use_item(character, item_index):
    try:
        item = character.inventory[item_index - 1]  # 1부터 시작하는 번호를 0 인덱스로 변환
        item.use(character)
        character.inventory.pop(item_index - 1)
        return True, f"{item.name}을(를) 사용했습니다."
    except IndexError:
        return False, "잘못된 아이템 번호입니다."
    except (TypeError, ValueError):
        return False, "아이템 번호는 숫자여야 합니다."

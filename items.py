###items.py###
class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, target):
        if self.effect == "heal":
            target.health += 20
            if target.health > target.max_health:
                target.health = target.max_health
            print(f"{target.name}가 20 HP를 회복했습니다.")
        elif self.effect == "buff":
            target.attack += 5
            print(f"{target.name}의 공격력이 5 증가했습니다.")

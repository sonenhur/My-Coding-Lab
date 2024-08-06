class Item:
    def __init__(self, name, effect, cost):
        self.name = name
        self.effect = effect
        self.cost = cost

    def use(self, target):
        if self.effect == "heal":
            target.health += 20
            if target.health > target.max_health:
                target.health = target.max_health
            print(f"{target.name}가 20 HP를 회복했습니다.")
        elif self.effect == "buff":
            target.attack += 5
            print(f"{target.name}의 공격력이 5 증가했습니다.")


def get_items():
    return [
        Item("포션", "heal", 50),
        Item("공격력 증가", "buff", 100),
    ]


def buy_item(player, item_name):
    items = get_items()
    item = next((item for item in items if item.name == item_name), None)

    if item is None:
        return False, "아이템이 존재하지 않습니다."

    if player.gold < item.cost:
        return False, "골드가 부족합니다."

    player.gold -= item.cost
    item.use(player)
    return True, f"{item.name}를 구매하고 사용했습니다."

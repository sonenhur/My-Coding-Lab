class Item:
    def __init__(self, name, effect, price):
        self.name = name
        self.effect = effect
        self.price = price

    def use(self, target):
        if self.effect == "체력 회복":
            target.health += 20
            if target.health > target.max_health:
                target.health = target.max_health
            print(f"{target.name}가 20 HP를 회복했습니다.")
        elif self.effect == "공격력 증가":
            target.attack += 5
            print(f"{target.name}의 공격력이 5 증가했습니다.")

    def to_dict(self):
        return {
            "name": self.name,
            "effect": self.effect,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], effect=data["effect"], price=data["price"])


def get_items():
    return [Item("Potion", "체력 회복", 20), Item("Elixir", "공격력 증가", 50)]


def buy_item(character, item_name):
    items = get_items()
    item = next(
        (item for item in items if item.name.lower() == item_name.lower()), None
    )
    print(
        f"구매 시도: 아이템 - {item}, 플레이어 골드 - {character.gold}"
    )  # 디버깅 추가
    if item:
        if character.gold >= item.price:
            character.gold -= item.price
            character.inventory.append(item)
            return True, f"아이템 '{item.name}'을(를) 구매했습니다."
        else:
            return False, "골드가 부족합니다."
    else:
        return False, f"아이템 '{item_name}'을(를) 찾을 수 없습니다."

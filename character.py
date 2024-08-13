class Character:
    def __init__(
        self,
        name,
        health,
        attack,
        defense,
        level=1,
        experience=0,
        max_health=None,
        gold=0,
        inventory=None,
    ):
        self.name = name
        self.health = health
        self.max_health = max_health if max_health is not None else health
        self.attack = attack
        self.defense = defense
        self.level = level
        self.experience = experience
        self.gold = gold
        self.inventory = inventory if inventory is not None else []

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)

    def attack_target(self, target):
        damage = max(self.attack - target.defense, 0)
        if damage > 0:
            target.take_damage(damage)
        return damage

    def gain_experience(self, exp):
        self.experience += exp
        while self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack += 2
        self.defense += 1
        self.experience -= self.level * 10
        print(f"{self.name}가 레벨업했습니다! 레벨: {self.level}")

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "inventory": [item.to_dict() for item in self.inventory],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            health=data["health"],
            attack=data["attack"],
            defense=data["defense"],
            level=data["level"],
            experience=data["experience"],
            max_health=data["max_health"],
            gold=data.get("gold", 0),
            inventory=[Item.from_dict(item) for item in data.get("inventory", [])],
        )

    def __str__(self):
        return (
            f"{self.name} - 레벨: {self.level}, HP: {self.health}/{self.max_health}, "
            f"공격력: {self.attack}, 방어력: {self.defense}, 골드: {self.gold}"
        )


class Item:
    def __init__(self, name, effect, price):
        self.name = name
        self.effect = effect
        self.price = price

    def use(self, target):
        effect_methods = {
            "heal": self.apply_heal,
            "buff": self.apply_buff,
        }
        method = effect_methods.get(self.effect)
        if method:
            method(target)
        else:
            print(f"아이템 효과 '{self.effect}'는 지원하지 않습니다.")

    def apply_heal(self, target):
        target.health = min(target.health + 20, target.max_health)
        print(f"{target.name}가 20 HP를 회복했습니다.")

    def apply_buff(self, target):
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
    return [Item("Potion", "heal", 20), Item("Elixir", "buff", 50)]


def buy_item(character, item_name):
    items = get_items()
    item = next(
        (item for item in items if item.name.lower() == item_name.lower()), None
    )

    if item:
        if character.gold >= item.price:
            character.gold -= item.price
            character.inventory.append(item)
            return True, f"아이템 '{item.name}'을(를) 구매했습니다."
        else:
            return False, "골드가 부족합니다."
    else:
        return False, f"아이템 '{item_name}'을(를) 찾을 수 없습니다."

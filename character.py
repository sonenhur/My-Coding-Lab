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
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def attack_target(self, target):
        damage = self.attack - target.defense
        if damage > 0:
            target.take_damage(damage)
        return damage

    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack += 2
        self.defense += 1
        self.experience = 0
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
        character = cls(
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
        return character

    def __str__(self):
        return f"{self.name} - 레벨: {self.level}, HP: {self.health}/{self.max_health}, 공격력: {self.attack}, 방어력: {self.defense}, 골드: {self.gold}"


class Item:
    def __init__(self, name, effect, price):
        self.name = name
        self.effect = effect
        self.price = price

    def use(self, target):
        if self.effect == "heal":
            target.health += 20
            if target.health > target.max_health:
                target.health = target.max_health
            print(f"{target.name}가 20 HP를 회복했습니다.")
        elif self.effect == "buff":
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
    item = next((item for item in items if item.name == item_name), None)
    if item and character.gold >= item.price:
        character.gold -= item.price
        character.inventory.append(item)
        return True
    return False

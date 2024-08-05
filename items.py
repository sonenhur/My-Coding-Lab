class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, target):
        if self.effect == "heal":
            target.health += 20
            if target.health > target.max_health:
                target.health = target.max_health
            print(f"{target.name} healed for 20 HP.")
        elif self.effect == "buff":
            target.attack += 5
            print(f"{target.name}'s attack increased by 5.")

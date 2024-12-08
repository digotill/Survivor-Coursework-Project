# CTRL E for recent stuff
# CTRL W for delete word
# Double shift to find text
# CTRL + SHIFT + F to find in all files
# Double click CTRL to run
# SHIFT + F6 to rename
# CTRL + ALT + L to reformat code

def deal_damage(attacker: Entity, defender: Entity, amount: int) -> None:
    defender.health -= amount



@property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if 0 <= value <= 100:
            self._health = value
        else:
            raise ValueError("Health must be between 0 and 100")


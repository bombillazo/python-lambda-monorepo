import random
import decimal

class Dinosaur:
    def __init__(self, name, diet, period, weight, armor, hybrid, nature=None, attack=None, defense=None, life=None):
        """
        :param name: scientific name of dinosaur
        :param diet: whether dinosaur is 'herbivore' or 'carnivore'
        :param period: geologic period of dinosaur existence
        :param weight: weight of dinosaur (in lbs to nearest 100)
        :param armor: boolean whether dinosaur sports armor or not
        :param hybrid: boolean whether dinosaur is hybrid or not
        :param nature: random value used for calculating attack and defense
        :param attack: attack points for dinodaur
        :param defense: defense points of dinosaur
        :param life: life points of dinosaur
        """
        self.name=name
        self.diet=diet
        self.period=period
        self.weight=int(round(weight,-2))
        self.armor=armor
        self.hybrid=hybrid
        self.nature = nature
        self.attack = attack
        self.defense=defense
        self.life=life

        if self.nature is None:
            if self.diet == 'herbivore':
                self.nature = random.randint(1,8)
            else:
                self.nature = random.randint(5,12)
        if self.attack is None:
            self.initialize_attack()
        if self.defense is None:
            self.initialize_defense()
        if self.life is None:
            self.initialize_life()
    

    def initialize_attack(self):
        self.attack = self.nature
        if self.diet == 'herbivore':
            self.attack += 2
        else:
            self.attack += 5
        self.attack = int(self.attack)


    def initialize_defense(self):
        self.defense = int(self.nature / 2)
        self.defense += int(self.weight / 1000)
        if self.defense == 0:
            self.defense += 5
        if self.armor:
            self.defense += 10
        else:
            self.defense += 2
        self.defense = int(self.defense)


    def initialize_life(self):
        self.life = 0
        if self.diet == 'herbivore':
            self.life += 100
        else:
            self.life += 60
        self.life += (self.weight / 100)
        self.life = int(self.life)


    def make_attack(self):
        attack = 0
        if random.random() > 0.95:
            attack =  self.attack + 25
            print(f'{self.name}\'s attack does {attack} damage!!! That\'s a critical attack! o.O')
            return attack
        attack = self.attack + random.randint(1,5)
        print(f'{self.name}\'s attack does {attack} damage')
        return attack
        

    def update_life(self, attack):
        """
        :param hit: amount to be deducted from life 
        """
        if attack < self.defense:
            attack = int(attack * decimal.Decimal(.75))
        self.life -= attack
        

    def is_dead(self):
        """
        :return: true if dinosaur life points are less than or equal to 0
        """
        return self.life <= 0
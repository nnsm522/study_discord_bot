class Unit:
    typeString = "유닛"
    attack=10
    health=100
    def __init__(self, attack, health):
        self.attack = attack
        self.health = health
    
    def doAttack(self):
        print(f"{self.typeString}이(가) 아군에게 {self.attack} 만큼 공격했다!")
        print("-----------------")
        

class Monster(Unit):
    typeString = "몬스터"


class Human(Unit):
    typeString = "사람"

    def __init__(self, attack=10, health=100, country=None):
        self.country = country
    
    def doAttack(self):
        print(f"{self.typeString}이 아군에게 {self.attack}만큼 공격했다!")
        print(f"{self.typeString}은 똑똑해서 한번 더 {self.attack * 0.5}만큼 공격했다!")
        print(self.country)
        print("-----------------")

class Dog(Unit):
    typeString = "개"
    def bark(self):
        print("왈왈!!")


dog = Dog(20, 30)
human = Human(country="한국")
monster = Monster(5, 100)

dog.doAttack()
dog.bark()
human.doAttack()
monster.doAttack()
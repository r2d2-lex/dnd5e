

class Character:

    def __init__(self,
                 name,
                 race,
                 playername,
                 level=1,
                 expirence=0,
                 strength=8,
                 dexterity=8,
                 constitution=8,
                 intellegence=8,
                 wisdom=8,
                 chrarisma=8,
                 ):
        self.name = name
        self.race = race
        self.playername = playername
        self.level = level
        self.expirence = expirence
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intellegence = intellegence
        self.wisdom = wisdom
        self.chrarisma = chrarisma

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        assert len(name) > 3, "Name must be at least 4 characters"
        self.__name = name


    @property
    def race(self):
        return self.__race

    @race.setter
    def race(self,race):
        self.__race = race


    @property
    def playername(self):
        return self.__playername

    @playername.setter
    def playername(self, playername):
        assert len(playername) > 3, "playername must be at least 4 characters"
        self.__playername = playername


    def __repr__(self):
        return "Character(Name: {0.name!r} Race: {0.race!r}, RealName: {0.playername!r})".format(self)


SPELL_SCHOOL = {
    'неизвестная': 0,
    'воплощение': 1,
    'очарование': 2,
    'ограждение': 3,
    'иллюзия': 4,
    'вызов': 5,
    'некромантия': 6,
    'преобразование': 7,
    'прорицание': 8,
}


class Spell():

    def __init__(self,
            name='',
            level=0,
            school=0,
            comp_is_verbal = False,
            comp_is_somatic = False,
            comp_is_material = False,
            components = '',
            distance='',
            duration='',
            cast_time=' ',
            is_concentrate=False,
            is_ritual = False,
            description=' ',
            gold=0,
            ):

        self.name = name
        self.level = level
        self.school = school
        self.components = components
        self.distance = distance
        self.duration = duration
        self.cast_time = cast_time
        self.is_concentrate = is_concentrate
        self.is_ritual = is_ritual
        self.description = description
        self.comp_is_verbal = comp_is_verbal
        self.comp_is_somatic = comp_is_somatic
        self.comp_is_material = comp_is_material
        self.gold = gold

def main():
    char = Character("Ksardas",'Human','Alex')
    print(char)
    print (char.intellegence,char.playername)
    char.wisdom = 99
    print("Wisdom: ",char.wisdom)
    print("Name: {0}, Race: {1}, Playername:{2}".format(char.name,char.race,char.playername))


if __name__ == "__main__":
    main()

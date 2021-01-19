class Card:
    def __init__(self, name, attacc, protecc, manacost, c_type, imgname):
        self.defence = protecc
        self.attack = attacc
        self.name = name
        self.c_type = c_type
        self.manacost = manacost
        self.imgname = imgname

    def get_name(self):
        return self.name

    def get_def(self):
        return int(self.defence)

    def get_attack(self):
        return int(self.attack)

    def get_manacost(self):
        return int(self.manacost)

    def get_type(self):
        return self.c_type

    def get_imgname(self):
        return self.imgname

    def set_def(self, defence):
        self.defence = int(defence)


class HandCard(Card):
    def __init__(self, name, attacc, protecc, manacost, c_type, imgname):
        super().__init__(name, attacc, protecc, manacost, c_type, imgname)
        self.current = False
        self.active = False

    def is_current(self):
        return self.current

    def is_active(self):
        return self.active

    def set_active(self, active):
        if active:
            self.active = True
        else:
            self.active = False


class CastedCard(HandCard):
    def __init__(self, name, attacc, protecc, manacost, c_type, imgname, coords):
        super().__init__(name, attacc, protecc, manacost, c_type, imgname)
        self.coords = coords

    def set_coords(self, coords):
        self.coords = coords

    def get_coords(self):
        return self.coords

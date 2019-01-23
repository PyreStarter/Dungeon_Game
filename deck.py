from card import Card, CardObject

class Deck:
    def __init__(self):
        self.length = 0
        self.list = []

    def add_card(self, card, count=1):
        self.length += count
        for _ in range(count):
            self.list.append(card)

    def remove_card(self, card):
        for i in self.list:
            if i == card:
                del i
                return 1

    def get_decklist(self):
        decklist = []
        tempdecklist = []
        for i in self.list:
            if i not in tempdecklist:
                decklist.append([i.name, 1])
                tempdecklist.append(i)
            else:
                for j in decklist:
                    if i.name == j[0]:
                        j[1] += 1
        return decklist

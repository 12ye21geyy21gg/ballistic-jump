import game_objects


class Store:
    def __init__(self, num):
        self.max_num = num
        self.slots = dict()
        self.dprice = 0.5
        self.boost = 2
        self.portal_height = 50

    def prepare(self):
        for i in range(self.max_num):
            if i == 0:
                self.slots[i] = ['starting speed', 1, 1]  # name, level, price
            elif i == 1:
                self.slots[i] = ['wind protection', 1, 1]
            elif i == 2:
                self.slots[i] = ['number  of 1 bonuses at start', 1, 1]
            elif i == 3:
                self.slots[i] = ['number  of 2 bonuses at start', 1, 1]
            elif i == 4:
                self.slots[i] = ['number  of 3 bonuses at start', 1, 1]
            elif i == 5:
                self.slots[i] = ['power of bonus jump', 1, 1]
            elif i == 6:
                self.slots[i] = ['height of portal', 1, 1]

    def buy(self, num, player, game):
        if num == 0:
            if self.slots[num][2] <= player.money:
                player.money -= self.slots[num][2]
                self.slots[num][2] += self.dprice
                player.v0 += 10
                self.slots[num][1] += 1
        elif num == 1:
            if self.slots[num][2] <= player.money and player.wind_protection < 1.0:
                player.money -= self.slots[num][2]
                self.slots[num][2] += self.dprice
                self.slots[num][1] += 1
                player.wind_protection += 0.1
                if player.wind_protection > 1.0:
                    player.wind_protection = 1.0
            else:
                print('you have 100% куда больше защиты от ветра')
        elif num == 2:
            if self.slots[num][2] <= player.money:
                player.money -= self.slots[num][2]
                self.slots[num][2] += self.dprice
                self.slots[num][1] += 1
                player.starter_I += 1
        elif num == 3:
            if self.slots[num][2] <= player.money:
                player.money -= self.slots[num][2]
                self.slots[num][2] += self.dprice
                self.slots[num][1] += 1
                player.starter_II += 1
        elif num == 4:
            if self.slots[num][2] <= player.money:
                player.money -= self.slots[num][2]
                self.slots[num][2] += self.dprice
                self.slots[num][1] += 1
                player.starter_III += 1
        elif num == 5:
            if self.slots[num][2] <= player.money:
                print(1)
                player.money -= self.slots[num][2]
                self.slots[num][2] += self.dprice
                self.slots[num][1] += 1
                self.boost += 1
        elif num == 6:
            if self.slots[num][2] <= player.money:
                player.money -= self.slots[num][2]
                self.slots[num][2] += self.dprice
                self.slots[num][1] += 1
                self.portal_height += 20

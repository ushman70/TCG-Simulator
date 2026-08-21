import itertools
import math
import random


class YugiohTCGSimulator:
   
    def __init__(self, pack_price, budget,booster_box_divide, booster_pack_sale_divide):
        self.pack_price = pack_price
        self.budget = budget
        self.booster_box = 0
        self.booster_box_for_sale = 0
        self.booster_box_for_packs = 0
        self.booster_pack_count = 0
        self.booster_box_divide = booster_box_divide
        self.booster_pack_sale_divide = booster_pack_sale_divide
        self.singles_for_sale = []
   
    def use_budget(self):
        #set booster boxes for sale, for individual pack selling,
        self.booster_box = math.floor(self.budget/70)
        self.budget -= self.booster_box * 70
        self.booster_box_for_sale = math.floor(self.booster_box * self.booster_box_divide)
        self.booster_box = self.booster_box - self.booster_box_for_sale
        self.booster_box_for_packs = math.floor(self.booster_box * self.booster_pack_sale_divide)
        self.booster_box = self.booster_box - self.booster_box_for_packs
        self.booster_pack_count = 24 * self.booster_box_for_packs
       
        #print(f"Reamining boxes: {self.booster_box}")
        #print(f"Boxes for sale: {self.booster_box_for_sale}")
        #print(f"Budget remaining: {self.budget}")
        #print(f"Booster packs for sale: {self.booster_pack_count}")

    def determine_rarity_individual(self, slot):
        if slot == 9:
            weight = {"SR": 75.00, "UR": 24.77, "SLR": 0.23}

            rarities = list(weight.keys())
            weights = list(weight.values())

            card = random.choices(rarities, weights=weights, k=1)
            return card
        else:
            return ["common"]

    def determine_price(self, rarity):
        SLR = [13.49, 24.48, 15.48, 17.25, 7.75, 14.00, 8.90]
        UR = [5.00, 1.00, 2.00]
        SR = [1.50, 2.00, 0.80]

        SLR_rng = random.randint(0, len(SLR) - 1)
        UR_rng = random.randint(0, len(UR) - 1)
        SR_rng = random.randint(0, len(SR) - 1)
       
        card = 0
        if rarity == "SLR":
            card = SLR[SLR_rng]
        elif rarity == "UR":
            card = UR[UR_rng]
        elif rarity == "SR":
            card = SR[SR_rng]
       
        if card >= 1.0:
            self.singles_for_sale.append(card)
       
        return card

    def open_pack(self):
        i = 1
        pack = []
        while i < 10:
            card = self.determine_rarity_individual(i)
            pack.append(card)
            i += 1

        return pack

    def open_numbered_packs(self,verbose = False):
        self.use_budget()
       
        hits = []
        profit = 0
        target_rarities = {"UR", "SR", "SLR"}
        count = self.booster_box * 24
        for _ in range(count):
            pack = self.open_pack()
            # Flatten and extract card strings
            flat_pack = [card for sublist in pack for card in sublist]

            if any(card.upper() in target_rarities for card in flat_pack):
                hits.append(flat_pack)

                for a in flat_pack:
                    profit += self.determine_price(a)

        if verbose:
            print(f"=== PACK OPENING RESULTS ===")
            print(f"Total Packs Opened: {count}")
            print(f"Total Hits Found:   {len(hits)}\n")

            for i, pack in enumerate(hits, start=1):

                pack_str = ", ".join(pack)
                # print(f"Hit #{i}: [{pack_str}]")

       
            print(f"PROFIT GENERATED FROM CARDS: {profit}")
       
        return [self.booster_box, self.booster_box_for_sale, self.booster_pack_count,self.budget, self.singles_for_sale]

    def open_till_profit(self, count):
        attempt = 0
        profit = 0

        while True:
            attempt += 1
            profit = self.open_numbered_packs(count)

            if profit > 0.0:
                break

        print(f"ATTEMPTS: {attempt}")
        print(f"PROFIT: {profit}")
       
if __name__ == "__main__":
    sim = YugiohTCGSimulator(4.99,1000,.33,.25)
    print(sim.open_numbered_packs(True))
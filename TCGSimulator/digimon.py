import itertools
import math
import random


class DigimonTCGSimulator:
   
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
        self.booster_box = math.floor(self.budget/80)
        self.budget -= self.booster_box * 80
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

        if slot == 11:
            # rare only
            weight = {
                "Rare": 100.0,
            }

            rarities = list(weight.keys())
            weights = list(weight.values())
            card = random.choices(rarities, weights=weights, k=1)
            return card
        elif slot <= 7:
            return ["common"]
        elif slot > 7 and slot <= 10:
            return ["uncommon"]
        elif slot == 12:
            weight = {"Rare": 62.533, "SR": 33.3, "SEC": 4.167}

            rarities = list(weight.keys())
            weights = list(weight.values())

            card = random.choices(rarities, weights=weights, k=1)
            return card

    def determine_price(self, rarity):
        common = [10, 5]
        uncommon = [55, 4, 2, 1, 1, 1]
        R = [
            194.00,
            35.00,
            24.00,
            15.00,
            20.00,
            14.00,
            8.90,
            10.00,
            2.00,
            0.10,
            0.20,
            0.10,
        ]
        SEC = [280.00, 285.00, 48.00, 34.00, 44.00, 13.00]
        SR = [
            465.00,
            165.00,
            369.00,
            49.00,
            36.00,
            34.00,
            60.00,
            24.00,
            18.50,
            21.00,
            17.00,
            14.00,
            8.00,
            7.00,
            6,
            5,
            4,
            3,
            2,
            1,
            1,
            0.3,
        ]

        # add fodder cards
        j = 0

        while j < 16:
            R.append(0.10)
            j += 1

        j = 0

        while j < 6:
            SR.append(0.50)
            j += 1

        while j < 41:
            common.append(0.10)
            j += 1

        j = 0

        while j < 31:
            uncommon.append(0.10)
            j += 1

        SEC_rng = random.randint(0, len(SEC) - 1)
        R_rng = random.randint(0, len(R) - 1)
        SR_rng = random.randint(0, len(SR) - 1)
        common_rng = random.randint(0, len(common) - 1)
        uncommon_rng = random.randint(0, len(uncommon) - 1)
       
        card = 0
        if rarity == "SEC":
            card = SEC[SEC_rng]
        elif rarity == "Rare":
            card = R[R_rng]
        elif rarity == "SR":
            card = SR[SR_rng]
        elif rarity == "common":
            card = common[common_rng]
        elif rarity == "uncommon":
            card = uncommon[uncommon_rng]
        else:
            return 0
       
       
        if card >= 1.0:
            self.singles_for_sale.append(card)
       
        return card

    def open_pack(self):
        i = 1
        pack = []
        while i < 13:
            card = self.determine_rarity_individual(i)
            pack.append(card)
            i += 1

        return pack

    def open_numbered_packs(self,verbose: bool = False):
        #set values like booster box for sale, booster box openings for singles etc...
        self.use_budget()
       
        hits = []
        profit = 0
        target_rarities = {"SR", "SEC", "Rare", "common", "uncommon"}
        count = self.booster_box * 24
        for _ in range(count):
            pack = self.open_pack()
            #money_spent += booster_pack_price
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
# Direct execution test block
if __name__ == "__main__":
    sim = DigimonTCGSimulator(4.99,1000,.33,.25)
    print(sim.open_numbered_packs(True))
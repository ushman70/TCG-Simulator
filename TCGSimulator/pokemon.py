import itertools
import math
import random
from CSVReader import write_to_csv, read_from_csv

class PokemonTCGSimulator:
   
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
        self.booster_pack_count = 36 * self.booster_box_for_packs
       
        #print(f"Reamining boxes: {self.booster_box}")
        #print(f"Boxes for sale: {self.booster_box_for_sale}")
        #print(f"Budget remaining: {self.budget}")
        #print(f"Booster packs for sale: {self.booster_pack_count}")

    def determine_rarity_individual(self, slot):
        if slot >= 1 and slot <= 4:
            # common
            return ["common"]
        elif slot >= 5 and slot <= 7:
            # uncommon
            return ["uncommon"]
        elif slot == 8:
            # rare or lower
            return ["rare"]
        elif slot == 9:
            # from common to hyper
            weight = {
                "Common": 50.0,
                "Uncommon": 30.0,
                "Rare": 10.96,
                "IR": 7.69,
                "SIR": 1.25,
                "HR": 0.1,
            }

            rarities = list(weight.keys())
            weights = list(weight.values())
            card = random.choices(rarities, weights=weights, k=1)
            return card
        elif slot == 10:
            # rare,DR,UR
            weight = {"Rare": 80.84, "DR": 12.5, "UR": 6.66}

            rarities = list(weight.keys())
            weights = list(weight.values())

            card = random.choices(rarities, weights=weights, k=1)
            return card

    def determine_price(self, rarity):
        rarity_prices = {}
        read_from_csv(rarity_prices, "pokemon_card_prices.csv", delimiter=",")

        SIR = rarity_prices["SIR"]
        UR = rarity_prices["UR"]
        HR = rarity_prices["HR"]
        IR = rarity_prices["IR"]
        DR = rarity_prices["DR"]

        
        #SIR = [200.00, 25.00, 15.00, 21.00, 10.00, 14.00]
        #UR = [10.00, 5.00, 12.00, 4.00, 8.00, 3.00, 2.00, 6.00]
        #HR = [40.00, 25.00, 5.00, 15.00]
        #IR = [1.50, 2.00, 0.80]
        #DR = [1.50, 0.10, 0.50, 0.25]

        SIR_rng = random.randint(0, len(SIR) - 1)
        UR_rng = random.randint(0, len(UR) - 1)
        HR_rng = random.randint(0, len(HR) - 1)
        IR_rng = random.randint(0, len(IR) - 1)
        DR_rng = random.randint(0, len(DR) - 1)
       
        card = 0
        if rarity == "SIR":
            card = SIR[SIR_rng]
        elif rarity == "UR":
            card = UR[UR_rng]
        elif rarity == "DR":
            card = DR[DR_rng]
        elif rarity == "IR":
            card = IR[IR_rng]
        elif rarity == "HR":
            card = HR[HR_rng]
           
        if card >= 1.0:
            self.singles_for_sale.append(card)
           
        return card

    def open_pack(self):
        i = 1
        pack = []
        while i < 11:
            card = self.determine_rarity_individual(i)
            pack.append(card)
            i += 1

        return pack

    def open_numbered_packs(self,verbose=False):
        self.use_budget()
        hits = []
        profit = 0
        target_rarities = {"UR", "HR", "SIR", "DR", "IR"}
        count = self.booster_box * 36
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
    sim = PokemonTCGSimulator(4.99,1000,.33,.25)
    print(sim.open_numbered_packs(True))
import random
import math
from typing import List, Dict


class GundamTCGSimulator:
    """A simulator for opening Gundam TCG booster packs and calculating market value vs. cost."""

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
       

    def determine_rarity_individual(self, slot: int) -> List[str]:
        #determine rarities
        if 1 <= slot <= 6:
            return ["common"]
        elif 7 <= slot <= 10:
            return ["uncommon"]
        elif slot == 11:
            return ["Rare"]
        elif slot == 13:
            # Resource slot
            weight = {"C+": 4.17, "C++": 0.35, "C": 95.48}
            return random.choices(
                list(weight.keys()), weights=list(weight.values()), k=1
            )
        elif slot == 12:
            # True rarity slot
            weight = {"Rare": 85.11, "+": 12.5, "++": 0.35, "SP": 2.04}
            weight_plus = {"C+": 15.0, "LR+": 50.0, "U+": 15.0, "R+": 20.0}
            weight_plus_plus = {"LR++": 100.0}

            card = random.choices(
                list(weight.keys()), weights=list(weight.values()), k=1
            )[0]

            if card == "+":
                return random.choices(
                    list(weight_plus.keys()),
                    weights=list(weight_plus.values()),
                    k=1,
                )
            elif card == "++":
                return random.choices(
                    list(weight_plus_plus.keys()),
                    weights=list(weight_plus_plus.values()),
                    k=1,
                )

            return [card]

        return ["common"]

    def determine_price(self, rarity: str) -> float:
        #determine price
        lr_plus_plus = [500, 530, 15.48]
        c_plus_plus = [16]
        lr_plus = [61, 70, 49, 50, 40, 38, 25, 22, 16, 17, 14, 13]
        u_plus = [13]
        r_plus = [
            91,
            36,
            45,
            27,
            20,
            15,
            18,
            18,
            16,
            15,
            15,
            12,
            9,
            9,
            9,
            6,
            7,
            7,
            5,
            4,
        ]
        sp = [70, 17, 6, 60, 48, 53]
        c_plus = [6, 4, 4, 2, 3, 2, 2, 2, 1.50, 1]
        lr = [9, 9, 5, 6, 3, 1, 1, 1, 0.5, 0.5, 0.5, 0.5]

        # Base Rare pool with bulk filler
        r = [7, 6] + [0.10] * 33

        price_pools: Dict[str, List[float]] = {
            "LR++": lr_plus_plus,
            "C++": c_plus_plus,
            "LR+": lr_plus,
            "U+": u_plus,
            "Rare": r,
            "R+": r_plus,
            "SP": sp,
            "C+": c_plus,
            "LR": lr,
        }

        if rarity in price_pools:
            card_price = random.choice(price_pools[rarity])
           
            if card_price >= 1.0:
                self.singles_for_sale.append(card_price)
                return card_price

        return 0.0

    def open_pack(self) -> List[str]:
       
        pack = []
        for slot in range(1, 14):
            # Flatten lists returned from determine_rarity_individual
            pack.extend(self.determine_rarity_individual(slot))
        return pack

    def open_numbered_packs(self,verbose: bool = False):
        #set the values based on our budget
        self.use_budget()
       
        hits = []
        total_value = 0.0
        target_rarities = {
            "U+",
            "RARE",
            "R+",
            "C+",
            "C++",
            "LR",
            "LR+",
            "LR++",
            "SP",
        }
        #total_cost = count * self.pack_price
        count = self.booster_box * 24
        for _ in range(count):
            pack = self.open_pack()

            if any(card.upper() in target_rarities for card in pack):
                hits.append(pack)
                for card in pack:
                    total_value += self.determine_price(card)

        #net_profit = total_value - total_cost

        if verbose:
            print("=== PACK OPENING RESULTS ===")
            print(f"Total Packs Opened: {count}")
            for i, hit_pack in enumerate(hits, start=1):
                print(f"Hit #{i}: [{', '.join(hit_pack)}]")
            #print(f"Capital Spent:  ${total_cost:.2f}")
            print(f"Card Value:     ${total_value:.2f}")
            #print(f"Net Profit:     ${net_profit:.2f}\n")

        return [self.booster_box, self.booster_box_for_sale, self.booster_pack_count,self.budget, self.singles_for_sale]

    def open_till_profit(self, batch_size: int) -> Dict[str, float]:

        attempts = 0
        profit = 0.0

        while True:
            attempts += 1
            profit = self.open_numbered_packs(batch_size, verbose=False)
            if profit > 0.0:
                break

        print(f"SUCCESS after {attempts} batch attempts!")
        print(f"Final Profit for Batch: ${profit:.2f}")

        return {"attempts": attempts, "profit": profit}


# Allows running a direct test when executing this file directly
if __name__ == "__main__":
    sim = GundamTCGSimulator(4.99,1000,.33,.25)
    print(sim.open_numbered_packs(True))
    #sim.open_till_profit(100)
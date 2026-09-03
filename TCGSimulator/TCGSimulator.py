import random
import math
import gundam
import pokemon
import digimon
import yugioh

class Customer():
    def __init__(self,income_level,total_buying_power,selection_map,online):
        self.income_level = income_level
        self.single_buying_power = total_buying_power[0]
        self.booster_pack_buying_power = total_buying_power[4]
        self.booster_box_buying_power = 0
        self.probability_single = total_buying_power[1]
        self.probability_booster_box = total_buying_power[2]
        self.booster_box_buying_power = total_buying_power[3]
        self.affinity = ""
        self.online = online
        self.selection_map = selection_map #the map that will contain cards being sold etc...
        #The map is dict with tuples for keys
   
    def verify_stats(self):
        print(f"income level:", {self.income_level[0]})
        print(f"single buying power:", {self.single_buying_power})
        print(f"booster pack buying power:", {self.booster_pack_buying_power})
        print(f"booster box buying power:", {self.booster_box_buying_power})
        print(f"probability singles:", {self.probability_single})
        print(f"probably booster box:", {self.probability_booster_box})
        print(f"affinity:", {self.affinity})
       
       
    def choice_degeneration(self):
        if self.income_level[0] >= 30000 and self.income_level[0] <= 50000:
            return .5
        elif self.income_level[0] >= 60000 and self.income_level[0] <= 80000:
            return .4
        elif self.income_level[0] >= 90000 and self.income_level[0] <= 150000:
            return .25
        else:
            return .2
           
    def affinity_singles_money(self):
        if self.affinity == "pokemon":
            return 6.99
        elif self.affinity == "yugioh":
            return 2.99
        elif self.affinity == "gundam":
            return 4.99
        elif self.affinity == "digimon":
            return 4.99
   
    #When buying singles, finding out if we are within 25% the max amount
    def within_range(self,param):
        needle = False
        diff = self.single_buying_power - (self.single_buying_power * .25)
       
        if param >= diff and param <= self.single_buying_power:
            needle = True
       
        return needle
   
    def sliding_window(self):
       
       
           
        needle = False
        r = len(self.selection_map[self.affinity][4])
        m = (0 + r) // 2
        l = random.randrange(0, m) if m > 0 else 0
        summation = sum(self.selection_map[self.affinity][4][l:m + 1])
       
        while l <= m and l >= 0:
            if summation <= self.single_buying_power:
                needle = True
                del self.selection_map[self.affinity][4][l:m + 1]
                break
            else:
                summation -=  self.selection_map[self.affinity][4][m]
                m -= 1
               
                if l - 1 >= 0:
                    summation -=  self.selection_map[self.affinity][4][l]
                    l -= 1
                    summation += self.selection_map[self.affinity][4][l]
                elif m < l:
                    break
           
        if summation < 0:
            summation = 0
       
        return (needle, summation)
                   
       
    def determine_affinity(self):
        #yugioh,pokemon,digimon etc...
       
        weight = {
        "pokemon": 60.0,
        "yugioh": 25.0,
        "gundam": 10.0,
        "digimon": 5.0
        }
       
        rarities = list(weight.keys())
        weights = list(weight.values())
        affinity = random.choices(rarities, weights=weights, k=1)
        self.affinity = affinity[0]
        return self.affinity
   
    def selection(self):
        #need affinity to shop
        self.determine_affinity()
       
        #self.verify_stats()
       
        #buy booster boxes,singles, packs
        bought_booster_box = False
        bought_singles = False
        bought_boosterpack = False
       
        #start by checking booster boxes
       
        p = 100 - self.probability_booster_box
       
        weight = {
        "Buy": self.probability_booster_box,
        "Not Buy": p
        }
       
       
       
        rarities = list(weight.keys())
        weights = list(weight.values())
        choice = random.choices(rarities, weights=weights, k=1)
        #print(choice)
        profit = 0
        if choice[0] == "Buy" and not self.online:
            #print("buying booster box")
            bought_booster_box = True
            self.selection_map[self.affinity][1] -= self.booster_box_buying_power
            profit = 120 * self.booster_box_buying_power
            if self.selection_map[self.affinity][1] < 0:
                while self.selection_map[self.affinity][1] < 0:
                    profit -= 120
                    self.selection_map[self.affinity][1] += 1
           
       
        #next probe singles
       
        reduction = self.probability_single * self.choice_degeneration()
        new_probability = self.probability_single + reduction
       
        p = 100 - self.probability_single if not bought_booster_box else (100 - new_probability)
       
        weight = {
        "Buy": self.probability_single,
        "Not Buy": p
        }
       
        rarities = list(weight.keys())
        weights = list(weight.values())
        choice = random.choices(rarities, weights=weights, k=1)
        rng = random.randint(0, 1)
        #print(choice)
        if choice[0] == "Buy":
            #print("buying singles")
            self.selection_map[self.affinity][4].sort()
            #print(f"rng is:", {rng})
            #perform single selection
            if rng == 0:
                l = 0
                r = len(self.selection_map[self.affinity][4]) - 1
           
                while l <= r:
                    m = (l + r) // 2
                    check = self.within_range(self.selection_map[self.affinity][4][m])
                    if self.selection_map[self.affinity][4][m] > self.single_buying_power:
                        r = m - 1
                    elif self.selection_map[self.affinity][4][m] < self.single_buying_power and check:
                        bought_singles = True
                        inc = self.selection_map[self.affinity][4].pop(m)
                        profit += inc
                        break
                    elif self.selection_map[self.affinity][4][m] < self.single_buying_power and not check:
                        l = m + 1
                    else:
                        bought_singles = True
                        inc = self.selection_map[self.affinity][4].pop(m)
                        profit += inc
                        break
            else:
                #print("buying multiple singles")
                #the other choice where a customer can purchase multiple cards
                perform_selection = self.sliding_window()
                bought_singles = perform_selection[0]
                profit += perform_selection[1]
       
        #probe booster packs
        if not bought_booster_box and bought_singles and not self.online:
            #re-use probability single if singles were
            #purchased but reduce booster packs that would be normally be bought
            #by about 40%
            p = 100 - self.probability_single
       
            weight = {
            "Buy": self.probability_single,
            "Not Buy": p
            }
       
            rarities = list(weight.keys())
            weights = list(weight.values())
            choice = random.choices(rarities, weights=weights, k=1)
           
            if choice[0] == "Buy":
                #print("buying booster packs")
                calc = math.floor(self.booster_pack_buying_power * .4)
                reduced_bought_packs = self.booster_pack_buying_power - calc
                self.selection_map[self.affinity][2] -= reduced_bought_packs
                profit += (self.affinity_singles_money() * reduced_bought_packs)
               
                while self.selection_map[self.affinity][2] < 0:
                    if self.selection_map[self.affinity][2] < 0:
                        self.selection_map[self.affinity][2] += 1
                        profit -= self.affinity_singles_money()
                   
        elif not bought_booster_box and not bought_singles and not self.online:
            #proceed as usual
            #p = 100 - self.probability_single
       
            #weight = {
            #"Buy": self.probability_single,
            #"Not Buy": p
            #}
       
            #rarities = list(weight.keys())
            #weights = list(weight.values())
            #choice = random.choices(rarities, weights=weights, k=1)
           
            #if choice[0] == "Buy":
                #print("buying booster packs")
                #print(self.selection_map[self.affinity][2])
                profit += (self.affinity_singles_money() * self.booster_pack_buying_power)
                self.selection_map[self.affinity][2] -= self.booster_pack_buying_power
               
                while self.selection_map[self.affinity][2] < 0:
                    if self.selection_map[self.affinity][2] < 0:
                        self.selection_map[self.affinity][2] += 1
                        profit -= self.affinity_singles_money()
               
       
        return profit
               
       

def create_customer():
    single_buying_power = 0
    booster_pack_buying_power = 0
    booster_box_buying_power = 0
   
    weight = {
        30000: 10.0,
        40000: 20.0,
        50000:29.0,
        60000:12.0,
        70000: 10.0,
        80000: 8.0,
        90000: 6.5,
        100000: 3,
        150000: 1.0,
        200000:.5
    }
   
    rarities = list(weight.keys())
    weights = list(weight.values())
    income = random.choices(rarities, weights=weights, k=1)
   
    #buying power based on income(probability)
    #For single buy power, the first param is the most money they are willing to spend
    #probability variables are percentages
   
    total_buying_power = ()
    if income[0] >= 30000 and income[0] <= 50000:
        booster_pack_buying_power = random.randrange(1, 2)
        booster_box_buying_power = 1
        probability_booster_box = 5
        probability_single = random.randrange(10, 20)
        single_buying_power = 5
        total_buying_power = (single_buying_power, probability_single,probability_booster_box,booster_box_buying_power,
        booster_pack_buying_power,income)
    elif income[0] >= 60000 and income[0] <= 80000:
        booster_pack_buying_power = random.randrange(2, 4)
        booster_box_buying_power = 1
        probability_booster_box = 10
        probability_single = random.randrange(15, 25)
        single_buying_power = 20
        total_buying_power = (single_buying_power, probability_single,probability_booster_box,booster_box_buying_power,
        booster_pack_buying_power,income)
    elif income[0] >= 90000 and income[0] <= 150000:
        booster_pack_buying_power = random.randrange(4, 6)
        booster_box_buying_power =  random.randrange(1, 2)
        probability_booster_box = 15
        probability_single = random.randrange(20, 30)
        single_buying_power = 100
        total_buying_power = (single_buying_power, probability_single,probability_booster_box,booster_box_buying_power,
        booster_pack_buying_power,income)
    elif income[0] >= 200000:
        booster_pack_buying_power = random.randrange(6, 8)
        booster_box_buying_power =  random.randrange(1, 3)
        probability_booster_box = 15
        probability_single = random.randrange(30, 40)
        single_buying_power = 500
        total_buying_power = (single_buying_power, probability_single,probability_booster_box,booster_box_buying_power,
        booster_pack_buying_power,income)
   
    #print(f"income is:", {income[0]})
    return total_buying_power


if __name__ == "__main__":

    budget_in = input("enter your budget")
    budget = int(budget_in)
    rent_in = input("enter the amount you're paying for rent")
    rent = int(rent_in)
    digimon_booster_box_divide_in = input("percentage of booster boxes you want to sell for digimon?")
    pokemon_booster_box_divide_in = input("percentage of booster boxes you want to sell for pokemon?")
    gundam_booster_box_divide_in = input("percentage of booster boxes you want to sell for gundam?")
    ygo_booster_box_divide_in = input("percentage of booster boxes you want to sell for yugioh?")
    
    digimon_booster_box_divide = int(digimon_booster_box_divide_in) / 100
    pokemon_booster_box_divide = int(pokemon_booster_box_divide_in) / 100
    gundam_booster_box_divide = int(gundam_booster_box_divide_in) / 100
    ygo_booster_box_divide = int(ygo_booster_box_divide_in)/ 100

    digimon_booster_pack_divide_in = input("percentage of booster packs you want to sell for digimon from remaining booster boxes?")
    pokemon_booster_pack_divide_in = input("percentage of booster packs you want to sell for pokemon from remaining booster boxes?")
    gundam_booster_pack_divide_in = input("percentage of booster packs you want to sell for gundam from remaining booster boxes?")
    ygo_booster_pack_divide_in = input("percentage of booster packs you want to sell for yugioh from remaining booster boxes?")

    digimon_booster_pack_divide = int(digimon_booster_pack_divide_in) / 100
    pokemon_booster_pack_divide = int(pokemon_booster_pack_divide_in) / 100
    gundam_booster_pack_divide = int(gundam_booster_pack_divide_in) / 100
    ygo_booster_pack_divide = int(ygo_booster_pack_divide_in)/ 100



   
    selection_map = {"pokemon":[],
    "yugioh":[],
    "gundam":[],
    "digimon":[]
    }
   
    i = 0
    k = 0
    profit = 0
    #percentages assigned to each tcg for our budget
    #pokemon,gudam,digimon,yugioh
    percentage_arr = [.2,.1,.1,.15]
    budget_arr = []
   
    while budget > 0:
        profit = 0
        budget_arr.clear()
       
        for j in percentage_arr:
            budget_arr.append(j * budget)
            budget -= (j * budget)
           
        if budget < 0:
            print("went over budget")
            break
       
        pokemon_sim = pokemon.PokemonTCGSimulator(0.00, budget_arr[0],pokemon_booster_box_divide,pokemon_booster_pack_divide).open_numbered_packs()
        gundam_sim = gundam.GundamTCGSimulator(0.00, budget_arr[1],gundam_booster_box_divide,gundam_booster_pack_divide).open_numbered_packs()
        digimon_sim = digimon.DigimonTCGSimulator(0.0, budget_arr[2],digimon_booster_box_divide,digimon_booster_pack_divide).open_numbered_packs()
        ygo_sim = yugioh.YugiohTCGSimulator(0.0, budget_arr[3],ygo_booster_box_divide,ygo_booster_pack_divide).open_numbered_packs()
        sim_container = [pokemon_sim,gundam_sim,digimon_sim,ygo_sim]
       
        if k == 0:
            selection_map = {"pokemon": pokemon_sim,
                "yugioh": ygo_sim,
                "gundam": gundam_sim,
                "digimon": digimon_sim
            }
        else:
            l = 0
            for j in selection_map.values():
                #the third index is the left over budget
                j[0] += sim_container[l][0]
                j[1] += sim_container[l][1]
                j[2] += sim_container[l][2]
                j[4] += sim_container[l][4]
               
                l += 1
       
        #now create customers
        people = random.randint(50,80)
        online_custs = 0
       
        while i < people:
            online = False
       
            if i % 3 == 0:
                online_custs += 1
                online = True
           
            cust_params = create_customer()
            customer = Customer(cust_params[5],cust_params,selection_map,online)
            res = customer.selection()
            profit += res
            i += 1
       
        i = 0
        k += 1
        print(selection_map)
        for j in selection_map.values():
            budget += j[3]
       
        print(f"Total customers for the month:",{people})
        print(f"Online Customers:",{online_custs})
        print(f"Money earned:",{profit})
        #add the profit to our current budget
        budget += profit
        #rent money
        budget -= rent
       
        #collection salary
        budget -= 2200
        print(f"remaining budget:",{budget})
   
    print(f"Business survived:",{k}," months")

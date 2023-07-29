from PIL import Image
import random, math

def get_item_stats(item):
    """
    returns a dict with item stats, rarity, slot and image sprite
    returns None if item is not found
    armour pieces have no specific class
    """
    c = None
    # Rookie set
    if item == 'Rookie Helmet':
        hp = 50
        atk = 25
        defense = 20
        spd = 0
        rarity = 'Common'
        slot = 'head'
        image = Image.open(f"textures/{slot}/rookie_helmet.png")
    elif item == 'Rookie Chestplate':
        hp = 70
        atk = 20
        defense = 30
        spd = 0
        rarity = 'Common'
        slot = 'chest'
        image = Image.open(f"textures/{slot}/rookie_chestplate.png")
    elif item == 'Rookie Leggings':
        hp = 40
        atk = 20
        defense = 20
        spd = 1
        rarity = 'Common'
        slot = 'legs'
        image = Image.open(f"textures/{slot}/rookie_leggings.png")
    elif item == 'Rookie Boots':
        hp = 30
        atk = 15
        defense = 15
        spd = 2
        rarity = 'Common'
        slot = 'feet'
        image = Image.open(f"textures/{slot}/rookie_boots.png")
    elif item == 'Rookie Sword':
        hp = 10
        atk = 30
        defense = 10
        spd = 1
        rarity = 'Common'
        c = 'Warrior'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/rookie_sword.png")

    elif item == "Great Claymore":
        hp = 30
        atk = 20
        defense = 20
        spd = -1
        rarity = "Common"
        c = "Warden"
        slot = "hand"
        image = Image.open(f"textures/{slot}/great_claymore.png")
    
    # Shop items
    elif item == 'Gladiator Helmet':
        hp = 40
        atk = 40
        defense = 30
        spd = 1
        rarity = 'Rare'
        slot = 'head'
        image = Image.open(f"textures/{slot}/gladiator_helmet.png")
    elif item == 'Steel Chestplate':
        hp = 60
        atk = 15
        defense = 40
        spd = 0
        rarity = 'Rare'
        slot = 'chest'
        image = Image.open(f"textures/{slot}/steel_chestplate.png")
    elif item == 'Winter Leggings':
        hp = 55
        atk = 20
        defense = 20
        spd = 2
        rarity = 'Rare'
        slot = 'legs'
        image = Image.open(f"textures/{slot}/winter_leggings.png")
    elif item == 'Lucky Boots':
        hp = 40
        atk = 25
        defense = 20
        spd = 3
        rarity = 'Rare'
        slot = 'feet'
        image = Image.open(f"textures/{slot}/lucky_boots.png")
    elif item == 'Rustic Sword':
        hp = 15
        atk = 50
        defense = 10
        spd = 2
        rarity = 'Rare'
        c = 'Warrior'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/rustic_sword.png")
    
    elif item == 'Whirlwind':
        hp = 15
        atk = 50
        defense = 15
        spd = 3
        rarity = 'Rare'
        c = 'Mage'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/whirlwind.png")
    
    # Elden set
    elif item == 'Elden Crown':
        hp = 40
        atk = 40
        defense = 30
        spd = 2
        rarity = 'Mythic'
        slot = 'head'
        image = Image.open(f"textures/{slot}/elden_crown.png")
    elif item == 'Elden Leggings':
        hp = 50
        atk = 40
        defense = 30
        spd = 3
        rarity = 'Mythic'
        slot = 'legs'
        image = Image.open(f"textures/{slot}/elden_leggings.png")
    elif item == 'Elden Boots':
        hp = 40
        atk = 40
        defense = 20
        spd = 5
        rarity = 'Mythic'
        slot = 'feet'
        image = Image.open(f"textures/{slot}/elden_boots.png")
        
    elif item == 'Fancy Hat':
        hp = 20
        atk = 40
        defense = 20
        spd = 5
        rarity = 'Mythic'
        slot = 'head'
        image = Image.open(f"textures/{slot}/fancy_hat.png")
    elif item == 'Special Tuxedo':
        hp = 30
        atk = 20
        defense = 55
        spd = 1
        rarity = 'Mythic'
        slot = 'chest'
        image = Image.open(f"textures/{slot}/special_tuxedo.png")
    
    elif item == 'Sacred Tome of Light':
        hp = 40
        atk = 40
        defense = 20
        spd = 1
        rarity = 'Mythic'
        c = 'Cleric'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/sacred_tome_of_light.png")
    elif item == 'Arcane Robes':
          hp = 50
          atk = 40
          defense = 20
          spd = 1
          rarity = 'Mythic'
          slot = 'chest'
          image = Image.open(f'textures/{slot}/arcane_robes.png')
        
    elif item == "Sentinel's Blade":
        hp = 30
        atk = 65
        defense = 15
        spd = 1
        rarity = 'Mythic'
        c = 'Warrior'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/sentinels_blade.png")
    elif item == 'Excalibur':
        hp = 20
        atk = 80
        defense = 10
        spd = 2
        rarity = 'Legendary'
        c = 'Warrior'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/excalibur.png")
    elif item == "Reaper's Blessing":
        hp = 20
        atk = 85
        defense = 5
        spd = 2
        rarity = 'Legendary'
        c = 'Mage'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/reapers_blessing.png")
    elif item == 'Valor Slasher':
        hp = 50
        atk = 45
        defense = 20
        spd = -1
        rarity = 'Legendary'
        c = 'Warden'
        slot = 'hand'
        image = Image.open(f"textures/{slot}/valor_slasher.png")
        
    try:
        return {'hp': hp, 'atk': atk, 'def': defense, 'spd': spd, 'rarity': rarity, 'class': c, 'slot': slot, 'image': image}
    except: 
        return None
    

def get_base_stats(char):
    char = char.lower()
    if char == 'main':
        hp = 80
        atk = 70
        defense = 20
        spd = 100
        c = 'Warrior'
        moves = ['Smack', 'Wack']
        combo_trait = Moves({'hp': hp, 'atk': atk, 'def': defense, 'spd': spd}).debuff(2, 'def', 2)
  
    elif char == 'auric':
        hp = 120
        atk = 50
        defense = 40
        spd = 90
        c = 'Warden'
        moves = ['Bash', 'Protective Embrace']
        combo_trait = Moves({'hp': hp, 'atk': atk, 'def': defense, 'spd': spd}).debuff(3, 'spd', 2)
  
    elif char == 'lyra':
        hp = 60
        atk = 80
        defense = 20
        spd = 95
        c = 'Mage'
        moves = ['Arcane Blast', 'Temporal Shift']
        combo_trait = Moves({'hp': hp, 'atk': atk, 'def': defense, 'spd': spd}).incapacitate()
  
    elif char == 'luna':
        hp = 100
        atk = 40
        defense = 30
        spd = 95
        c = 'Cleric'
        moves = ['Divine Smite', 'Benediction Aura']
        combo_trait = Moves({'hp': hp, 'atk': atk, 'def': defense, 'spd': spd}).dot(2, 2)

    elif char == 'aurelia':
        hp = 110
        atk = 35
        defense = 25
        spd = 90
        c = 'Cleric'
        moves = ['Retribution', 'Blessing Of Light']
        combo_trait = Moves({'hp': hp, 'atk': atk, 'def': defense, 'spd': spd}).dot(2, 2)
  
    try: return {'hp': hp, 'atk': atk, 'def': defense, 'spd': spd, 'class': c, 'moves': moves, 'combo_trait': combo_trait}
    except: None

class Moves:
    def __init__(self, char_stats_dict):
        self.char_stats_dict = char_stats_dict
      
    def get_move_stats(self, move):
        effect = None
        targets = 1
        mana = 0
    
        # main
        if move == 'Smack':
            atk = 35
            targets = 1
        elif move == 'Wack':
            atk = 25
            targets = 2
            mana = 40
    
        # auric
        elif move == 'Bash':
            atk = 25
            targets = 1
        elif move == 'Protective Embrace':
            atk = 0
            targets = 1
            mana = 50
            effect = [self.buff(1, 'hp', 'hp', 2)]
    
        # lyra
        elif move == 'Arcane Blast':
            atk = 35
            targets = 1
        elif move == 'Temporal Shift':
            atk = 40
            targets = 3
            mana = 55
    
        # luna
        elif move == 'Divine Smite':
            atk = 20
            targets = 1
            effect = [self.debuff(2, 'spd', 2)]
        elif move == 'Benediction Aura':
            atk = 0
            targets = 2
            mana = 50
            effect = [self.buff(3, 'atk', 'hp', 2)]
    
        # aurelia
        elif move == 'Retribution':
            atk = 20
            targets = 1
        elif move == 'Blessing Of Light':
            atk = 0
            targets = 1
            mana = 50
            effect = [self.buff(2, 'hp', 'hp', None), self.cleanse()]
    
        # BlightWalker
        elif move == 'Cursed Blades':
            atk = 25
            effect = [self.debuff(1, 'spd', 2), self.debuff(1, 'atk', 2)]
        elif move == 'Corrosive Nova':
            atk = 30
            targets = 3
            effect = [self.debuff(1, 'atk', 2)]
        elif move == 'Shadow Bolt':
            atk = 35
            targets = 3 
            
        # Dreadscythe
        elif move == 'Decapitate':
            atk = 35
            targets = 1
        elif move == 'Withering':
            atk = 10
            targets = 2
            effect = [self.dot(2, 2)]
        elif move == 'Blade of Death':
            atk = 25
            targets = 3
    
        # Mummy
        elif move == "Crucify":
            atk = 35
            targets = 1
        elif move == "Screech":
            atk = -40
            targets = 2
            effect = [self.debuff(2, "spd", 1), self.debuff(2, "def", 1)]
    
        # Archon Icarus
        elif move == "Tsuki":
            atk = 30
            targets = 1
        elif move == "Hiraki Ashi": ##
            atk = 25
            targets = 1
            effect = [self.buff(6, 'spd', 'hp', 2)]
        elif move == "Kachinuki":
            atk = 30
            targets = 2
        elif move == "Katate Waza":
            atk = 30
            targets = 1
            effect = [self.incapacitate(1)]
    
        # dynanimatoad
        elif move == "Detonation":
            atk = 40
            targets = 3
        elif move == "Body Slam":
            atk = 25
            targets = 2
            effect = [self.incapacitate(1)]
        elif move == "Residue":
            atk = 20
            targets = 1
            effect = [self.dot(2, 2)]
    
        # shadowstalker
        elif move == 'Shadowstep':
            atk = 30
            targets = 1
        elif move == 'Nightmare Visage':
            atk = 25
            targets = 2
            effect = [self.debuff(2, "def", 1), self.incapacitate(1)]
        elif move == 'Shadow Veil':
            atk = 0
            targets = 5
            effect = [self.buff(2, 'spd', 'hp', 1), self.buff(2, 'def', 'hp', 1)]
    
        # emberfiend
        elif move == 'Magma Surge':
            atk = 30
            targets = 2
            effect = [self.dot(1, 2)]
        elif move == 'Inferno Shield':
            atk = 0
            targets = 1
            effect = [self.buff(3, 'def', 'hp', 1)]
        elif move == 'Erupting Tremor':
            atk = 30
            targets = 10
        elif move == 'Lava Burst':
            atk = 30
            targets = 1
            effect = [self.incapacitate(1), self.dot(1, 1)]
        
        try: return atk, targets, effect, mana
        except Exception as e: print('error', e); return None
      
    def debuff(self, multiplier, type, duration=1):
        reduction = int(self.char_stats_dict['atk']*multiplier*0.17) * -1
        return {'value': reduction, 'duration': duration, 'type': type, 'effect': 'debuff'}
  
    def dot(self, multiplier, duration=1):
        dmg = int(self.char_stats_dict['atk']*multiplier*0.2) * -1
        return {'value': dmg, 'duration': duration, 'type': None, 'effect': 'dot'}
  
    def buff(self, multiplier, type, scaling, duration=1):
        increase = int(self.char_stats_dict[scaling] * multiplier * 0.66)
        return {'value': increase, 'duration': duration, 'type': type, 'effect': 'buff'}
    
    def incapacitate(self, duration=1):
        return {'value': None, 'duration': duration, 'type': None, 'effect': 'incapacitate'}
    
    def cleanse(self):
        return {'value': None, 'duration': None, 'type': None, 'effect': 'cleanse'}
  
  


class LootChests:
    rarities = ['Common', 'Rare', 'Mythic', 'Legendary', 'Grand']
      
    def open_chest(self, rarity):
        if rarity == 'Common':
          loot = self.get_loot(credits=(20, 100), xp=(20, 50), ore=1, items=self.Common.items, k=3)
        elif rarity == 'Rare':
          loot = self.get_loot(credits=(100, 200), xp=(40, 75), ore=1, items=self.Rare.items+self.Rare.items+self.Common.items, k=4)
        elif rarity == 'Mythic':
          loot = self.get_loot(credits=(350, 500), xp=(60, 90), ore=2, items=self.Mythic.items+self.Mythic.items+self.Rare.items, k=5)
        elif rarity == 'Legendary':
          loot = self.get_loot(credits=(500, 750), xp=(75, 100), ore=3, items=self.Legendary.items+self.Legendary.items+self.Mythic.items, k=6)
        elif rarity == 'Grand':
          pass
        
        loot.sort()
        return loot # ['34 XP', '465 Credits', 'Fancy Hat']
  
    def get_loot(self, credits, xp, ore, items, k):
        loot = []
        credits_get = random.randint(credits[0], credits[1])
        xp_get = random.randint(xp[0], xp[1])
        ores_get = []
        ores = ['Iron', 'Gold', 'Diamond']
        for i in range(k-1):
            choice = random.choices(['credits', 'xp', 'ore', 'item'], weights=[20, 20, 30, 25])[0]
            if choice == 'credits':
                credits_get += random.randint(credits[0], credits[1])
            elif choice == 'xp':
                xp_get += random.randint(xp[0], xp[1])
            elif choice == 'ore':
              for i in range(random.randint(1,3)):
                ore_choice = random.choice(ores[:ore])
                ores_get.append(ore_choice)
            else:
                loot.append(random.choice(items))
        for o in ores:
          if count := ores_get.count(o):
            loot.append(f'{count} {o} ore')
        loot.extend([f'{credits_get} Credits', f'{xp_get} XP'])
        return loot

    class Common:
        items = ['Rookie Sword', 'Rookie Helmet', 'Rookie Chestplate', 'Rookie Leggings', 'Rookie Boots', "Great Claymore"]
        
    class Rare:
        items = ['Rustic Sword', 'Gladiator Helmet', 'Steel Chestplate', 'Winter Leggings', 'Lucky Boots', 'Whirlwind']
    
    class Mythic:
        items = ['Elden Crown', 'Elden Leggings', 'Elden Boots', 'Fancy Hat', 'Special Tuxedo', "Sentinel's Blade", 'Sacred Tome of Light', 'Arcane Robes']
        
    class Legendary:
        items = ['Excalibur', "Reaper's Blessing", 'Valor Slasher']


def get_level_multiplier(level, mode):
  if mode == 'hp':
    return 2.23 + (1.01 * level)
  elif mode == 'atk':
    return 2 + (0.32 * level)
  elif mode == 'def':
    return 1 + 0.013 * level
  elif mode == 'spd':
    return 1 + (math.floor(0.003720930233 * level))


class Relics:
    def get_relic_data(self, relic, level=1):
        if relic == 'Phoenix Talisman':
            value = 0.20 * level
            effect = {'type': 'mana_regen', 'value': value}
            description = f"Increases mana regeneration by {value*100}%"
            image = Image.open("textures/relics/phoenix_talisman.png")
        elif relic == 'Holy Grail':
            value = 0.10 * level
            effect = {'type': 'hp', 'value': value}
            description = f"Increases HP by {value*100}%"
            image = Image.open("textures/relics/holy_grail.png")
        try:
            return {'effect': effect, 'description': description, "image": image}
        except:
            return None


class ArkCove:
    name = "Ark Cove"
    snake_case = "ark_cove"
    fp = "objects/ark_cove.png"
    locations = ["Townsquare", "Gift Shop", "Shop", "Inn"]
    class Elvis:
        name = "Elvis"
        location = "Inn"
        dialogue = {
            "default": "Welcome to the Inn, how may I help you?",
            "default_1": "We have various room options available, ranging from cozy singles to spacious suites.",
            "default_2": "There are several attractions nearby, such as the scenic beach and the historical museum.",
            "default_3": "Certainly! We offer room service for our guests. Please let me know what you would like to order.",
        }
        dialogue_options = {
            "default": [
                "1. Ask about available rooms",
                "2. Inquire about nearby attractions",
                "3. Request room service"
            ],
            "The Forgotten Legacy_1": [
                "I'm here about the commission"
            ],
            "The Forgotten Legacy_2": [
                "And what do I get?",
                "For free?"
            ]
        }

    class Alex:
        name = "Alex"
        location = "Gift Shop"
        dialogue = {
            "default": "Welcome to the Gift Shop, where you can buy whatever you so please.",
            "default_1": "Feel free to explore our wide range of products, including clothing, accessories, and souvenirs.",
            "default_2": "We currently have a special discount on selected items. Don't miss out!",
            "default_3": "Certainly! We offer gift wrapping service to make your purchase extra special.",
        }
        dialogue_options = {
            "default": [
                "1. Browse the merchandise",
                "2. Ask about special deals",
                "3. Inquire about gift wrapping service"
            ],
            
        }

    class Samantha:
        name = "Samantha"
        location = "Shop"
        dialogue = {
            "default": "Welcome to the Shop, how can I assist you?",
            "default_1": "We have just received new arrivals, including trendy fashion items and unique accessories.",
            "default_2": "Currently, we are offering a special discount on selected items. Take advantage of the savings!",
            "default_3": "Of course! I'm here to help you with your purchase. Let me know what you need assistance with.",
        }
        dialogue_options = {
            "default": [
                "1. Ask about the latest arrivals",
                "2. Inquire about discounts",
                "3. Request assistance with a purchase"
            ],
            
        }

    class Jeffrey:
        name = "Jeffrey"
        location = "Townsquare"
        dialogue = {
            "default": "Welcome to the Townsquare, how can I help you?",
            "default_1": "There are several exciting local events happening this week, including a music festival and an art exhibition.",
            "default_2": "There are plenty of great restaurants nearby, offering a variety of cuisines to suit every taste.",
            "default_3": "Sure! Let me know the name or address of the place you're looking for, and I'll provide you with directions.",
        }
        dialogue_options = {
            "default": [
                "1. Ask about local events",
                "2. Inquire about nearby restaurants",
                "3. Request directions to a specific place"
            ],
            "The Forgotten Legacy_4": [
                "I'm looking for Auric",
                "Do you know who Auric is?",
                "Where can I find Auric?"
            ],
            "The Forgotten Legacy_21": [
                "Fictional mummies",
                "Video game",
                "From a movie"
            ],
        }
    
    people = [Elvis, Alex, Samantha, Jeffrey]

areas = [ArkCove()]

# No assigned area
class Auric:
    name = "Auric"
    dialogue_options = {
        "The Forgotten Legacy_6": [
            "Purple crystals and green labelled boxes",
            "Red labelled and Blue crystals boxes",
            "Blue crystals and Purple crystals boxes",
            "Red labelled and green labelled boxes"
        ],
        "The Forgotten Legacy_19": [
            "Loud thudding...",
            "Strange noises...",
            "More and more frequent..."
        ],
        "The Forgotten Legacy_20": [
            "How do we move forward?",
            "What now?"
        ],
        "The Forgotten Legacy_22": [
            "Why ask?"
        ],
        "The Forgotten Legacy_23": [
            "I...",
            "don't...",
            "know..."
        ],
        "The Forgotten Legacy_25": [
            "Behind you!"
        ],
        "The Forgotten Legacy_28": [
            "Auric?"
        ],
        "The Forgotten Legacy_31": [
            "Looks like another puzzle"
        ],
        "The Forgotten Legacy_38": [
            "We saw other things..."
        ],
        "The Forgotten Legacy_41": [
            "I don't know",
            "Never met him",
            "I think his name was Icarus"
        ]
    }
    
class Archaeologist:
    name = "Archaeologist"
    dialogue_options = {
        "The Forgotten Legacy_12": [
            "Aren't you supposed to know?",
            "Why would we know?",
            "We are none the wiser",
        ],
        "The Forgotten Legacy_13": [
            "Have you seen anything strange?",
            "Anything unusual lately?",
        ],
        "The Forgotten Legacy_14": [
            "Thank you"
        ],
        "The Forgotten Legacy_15": [
            "Seen anything weird?",
            "Ever tried finding out?"
        ]
    }

class Unknown:
    name = "???"
    dialogue_options = {
        "The Forgotten Legacy_34": [
            "What are you talking about?",
            "Wrong person",
            "You're speaking gibberish",
        ],
    }
    
no_area_people = {'auric': Auric(), 'archaeologist': Archaeologist(), '???': Unknown()}


def dialogue_response(dialogue, dialogue_type, option_index):
    """
    returns a dialogue response
    dialogue is the dict of dialogue from the npc
    dialogue_type is a str (key of dialogue) "default"
    option_index is the index of the option chosen (index notation)
    returns None if not found
    """
    option_index += 1
    for k, v in dialogue.items():
        if k.startswith(dialogue_type) and k.endswith(f"_{option_index}"):
            return v
    else:
        return None


class Quest:
    """
    Queues are always at the end of a text body
    Starts with "$queue" then an action
    This is handled in main.py
    $queue switch_speaker is generally always at the end
    $queue custom_area is usually behind switch_speaker
    $queue battle {enemy_names} {enemy_level} 
    enemy_names separated with a space, enemy_level is the last argument
    battle is always at the end and cannot continue
    """
    def __init__(self):
        self.quests = Quest.__subclasses__()

    def match_quest(self, quest_title):
        for quest_object in self.quests:
            if quest_object.title == quest_title:
                return quest_object
    
    def prerequisite_check(self):
        pass

    def level_requirements_check(self, level): #  returns a bool
        return level >= self.minimum_level

    def redirect(self, quest_title, step): #  returns text body of a quest at step
        quest_object = self.match_quest(quest_title)
        return quest_object.text_bodies[step]


class TheForgottenLegacy(Quest):
    title = 'The Forgotten Legacy'
    description = "Uncover the ancient civilization's lost secrets by piecing together fragmented artifacts scattered throughout the realm"
    prerequisites = []
    minimum_level = 1
    rewards = ["2400 Credits",
               "1000 Universal XP",
               "Phoenix Talisman",
               "2 Diamond ore"]
    tasks = [
        "Talk to Elvis at the Inn",
        "Find out about the commission from Elvis",
        "Find out about the commission from Elvis",
        "Talk to Jeffrey to find Auric",
        "Find out about Auric from Jeffrey", # 5
        "Find out about Auric from Jeffrey",
        "Find out more from Auric",
        "Find out more from Auric",
        "Head to the escavation site with Auric",
        "Defeat the mummies", # 10
        "Talk with the Archaeologist",
        "Discuss with Auric and the Archaeologist",
        "Discuss with Auric and the Archaeologist",
        "Find out more from the Archaeologists",
        "Find out more from the Archaeologists", # 15
        "Find out more from the Archaeologists",
        "Hear from Auric",
        "Talk to Jeffrey and find Auric at the Townsquare",
        "Find out more from Auric", 
        "Find out more from Auric", # 20
        "Talk with Auric and Jeffrey",
        "Discuss with Auric and Jeffrey",
        "Talk with Auric",
        "Talk with Auric",
        "Continue to the Excavation Site", # 25
        "Talk with Auric", 
        "Defeat the mummies",
        "Continue onward",
        "Talk with Auric",
        "Solve the puzzle", # 30
        "Defeat the enemies",
        "Talk with Auric",
        "Solve the puzzle",
        "Continue onward", 
        "Talk with ???", # 35
        "Defeat Archon Icarus",
        "Talk to Jeffrey at the Townsquare of your findings",
        "Discuss with Auric and Jeffrey", 
        "Talk with Auric and Jeffrey",
        "Discuss with Auric and Jeffrey", # 40
        "Discuss with Auric",
        "Talk with Auric", 
        "Quest End", # 43
        ]
    text_bodies = [
            [
                "Ah, a new traveller! I remember each and every face that walks through that door. What can I do for you?"
            ],
            [
                "After long years of disparity, emerged a cruel yet powerful ruler. From the raw and rubble, he ordered the nation to urgently build up to modernity. In the span of just a few decades, the nation was rushed into the land you see around you. Yet, it seems like we've forgotten about the legacy we had held so proudly all the way back then.",
                "Well, at least according to the legend. A tale told countless times to younglings. But we have reason to believe that the details have remained. Over this decade, we have discovered empty space down beneath the soil we step on. But movement was also detected there.",
                "We would like you to find this mysterious place and retrieve our precious bequest."
            ],
            [
                "What's in it for you? Why not think about our heritage? I'm kidding, of course there will be rewards.",
                "Joining you would be the noble **Auric**, you can meet with him at the **Townsquare**",
                "*It is through hardship do you earn the most important reward; knowledge.*",
                "$queue checkpoint"
            ],
            [
                "Welcome to the Townsquare! How may I help you?"
            ],
            [ # 5
                "Ah, you must be that traveller. Right this way!",
                "$queue switch_speaker auric"
            ],
            [
                "This mission won't be so easy, so here's a riddle to get your mind going. Funnily enough, this situation happened last week.",
                "4 Boxes of crystals were ready for shipment. But **two** were incorrectly labelled. Purple crystals have to be labelled red, and boxes labelled green must contain Blue crystals. This was urgent, using the wrong crystals would cause a mass explosion in the factory. The boxes were as follows,\nA red labelled box, a box with Blue crystals, a box with Purple crystals and a green labelled box.",
                "Our surveillance team immediately knew which two boxes were wrongly labelled. Do you?"
            ],
            [
                "The answer is: Purple crystals and green labelled boxes",
                "The box with blue crystals doesn't need to be labelled green. Only green labelled boxes have to contain blue crystals, so check this box. \nRed labelled boxes also do not need to contain purple crystals by the same logic",
                "This was just a practice, let's head over to the site.",
                "$queue make_character auric continue",
                "$queue custom_area Archaeology Site continue",
                "$queue switch_speaker archaeologist"
            ],
            [
                "Hold on there, this is an archaeology site. You aren't allowed to be here.",
                "Oh, Auric, it's you. Well...",
                "$queue switch_speaker auric"
            ],
            [
                "Watch out!",
                "$queue battle mummy mummy 1",
            ],
            [ # 10
                "$queue switch_speaker archaeologist"
            ],
            [
                "Where on earth did those come from?",
                "$queue switch_speaker auric" 
            ],
            [
                "They looked like mummies, we better be careful around here.",
                "It's better if we keep this a secret, not to freak out the public.",
                "We should find out more about this quick before anything catastrophic happens.",
                "Let's interrogate some of the people here, split up.",
                "$queue switch_speaker archaeologist"
            ],
            [
                "Yes, how may I help you? Try not to get in the way of our work."
            ],
            [
                "I don't remember seeing or hearing anything, other than the occasional thuds. Not sure where those come from.",
                "Talked to the others and we assume that it was some work going on, but it really seems like it is coming from down below.",
                "It's probably nothing right? It's not like living things can live underneath us."
            ],
            [ # 15
                "We all assume it's nothing, but you can hear loud thuds on site. It's been becoming more frequent lately. I don't know what's going on or where they come from, but there must be some logical reason."
            ],
            [
                "I try my best to stay out of this. If there is something dangerous going on, I'm staying away.",
                "$queue switch_speaker auric"
            ],
            [
                "*I've gone back to town for something, meet me at the Townsquare*",
                "$queue checkpoint"
            ],
            [
                "$queue switch_speaker auric",
            ],
            [
                "So, I guess we can start with your findings."
            ],
            [ # 20
                "I pretty much heard the same thing. At least none of them have seen the mummies.",
                "I think we...",
                "$queue switch_speaker jeffrey"
            ],
            [
                "should have told me.",
                "You've just been to the archaeology site, and now you're talking about mummies. I'm not fooled that easily. Besides, the archaeologist told me.",
                "According to legend, mummies from underground are from forbidden cities. Locked down below for their aggression and ruthlessness.",
                "Just an old tale commonly told to children to scare them from anything dangerous.",
                "Mummies spotted at the archaeology site...",
                "We need to go deeper. Stop any from going to the surface. Excavators will be sent to the site tomorrow, archaeologists have been ordered to stay home. We can check out the situation then.",
                "$queue custom_area Archaeology Site continue",
                "$queue switch_speaker auric"
            ],
            [
                "So {user}, where are you from?"
            ],
            [
                "Granted we're doing this mission together, thought I should get to know you better.",
                "I assume you're not from around here. What brings you here, and where exactly did you come from?"
            ],
            [
                "$queue custom_area Excavation Site continue",
                "Let's begin, shall we?",
                "$queue switch_speaker auric"
            ],
            [ # 25
"https://cdn.discordapp.com/attachments/1046831128553734217/1132363261359173682/light_up.gif"
            ],
            [ 
                "$queue battle mummy mummy 2"
            ],
            [
                "We should take one of these on our expedition.",
"https://cdn.discordapp.com/attachments/1046831128553734217/1132535768460558416/step_27.png"
            ],
            [
                "$queue checkpoint continue",
                "We need to find the source of these mummies.",
"https://cdn.discordapp.com/attachments/1046831128553734217/1132565769583083540/door_locked.png",
"https://cdn.discordapp.com/attachments/1046831128553734217/1132569478857760839/light_out.gif"
            ],
            [
                "I'm here. The torch went out and the door is locked.",
                "Wait, there's some writing on the floor.",
                '"In front of you are 100 cards, one side white, the other black.\nSplit them into 2 piles, each pile having an equal number of cards facing white side up.\nThere are 30 cards facing white side up initially."',
                "Step29Puzzle"
            ],
            [ # 30
                "$queue checkpoint continue",
"https://cdn.discordapp.com/attachments/1046831128553734217/1132565483481214996/door_opening.gif",
"https://cdn.discordapp.com/attachments/1046831128553734217/1132625013476958259/mummies.png",
                "An ambush.",
                "$queue battle mummy mummy dreadscythe 1"
            ],
            [
                "Where are we?",
"https://cdn.discordapp.com/attachments/1046831128553734217/1133321254913450035/blocks_puzzle.png"
            ],
            [
                "Step32Puzzle"
            ],
            [
                "$queue checkpoint continue",
"""https://cdn.discordapp.com/attachments/1046831128553734217/1133379469176995930/34.gif      
                                                    """,
"https://cdn.discordapp.com/attachments/1046831128553734217/1133332801916256387/34.png",
                "Who Are You? And What Do You Want From Us?",
                "$queue switch_speaker ???"
            ],
            [ # 35
                "$queue checkpoint continue",
                "DON'T DEFEND HIM!",
                "You don't know what he has done to me",
                """To us...                                                          
        """,
                "To all of us.",
            ],
            [
"https://cdn.discordapp.com/attachments/1046831128553734217/1133394557787176970/archon_icarus_boss.png",
                "Step36Boss",
                "$queue checkpoint"
            ],
            [
                ""  
            ],
            [
                "Welcome back. What happened?",
                "$queue switch_speaker auric"
            ],
            [
                "We think the mummy problem should be fixed."
            ],
            [
                "$queue switch_speaker jeffrey",
            ],
            [ # 40
                "Is that so? There have been reports of a loud boom from the site. But we checked and detected space far surpass what you've gone through. With more movement.",
                """It should be all fine for now.                                             
                                                                  """,
                "$queue switch_speaker auric"
            ],
            [
                "So,                                             ",
                "What's with you and that guy?"
            ],
            [
                "Whoever he is, this will probably not be the last time we see him.",
                "$queue quest_end"
            ]
        ]

custom_area_images = {"Archaeology Site": [
    "https://cdn.discordapp.com/attachments/1046831128553734217/1131239927745626182/archaeology.png",
"https://cdn.discordapp.com/attachments/1046831128553734217/1131220730592378890/worker_speech.png"
                                        ],
                     "Excavation Site": [
"https://cdn.discordapp.com/attachments/1046831128553734217/1132354265017503744/excavation_site.png"
                                        ]
                     }


class Enemy:
    def __init__(self):
        self.enemies = Enemy.__subclasses__()

    def match_enemy(self, name):
        for enemy_object in self.enemies:
            if enemy_object().name.lower() == name:
                return enemy_object
    
    def move(self, stats_dict=None):
        stats_dict = stats_dict or self.stats_dict
        attack_move = random.choice(self.moves)
        m = Moves(stats_dict)
        move_stats = m.get_move_stats(attack_move)
        return attack_move, move_stats


class BlightWalker(Enemy):
    def __init__(self, level=1):
        self.hp = math.floor(50 * get_level_multiplier(level, 'hp'))
        self.atk = math.floor(40 * get_level_multiplier(level, 'atk'))
        self.defense = math.floor(20 * get_level_multiplier(level, 'def'))
        self.spd = math.floor(100 * get_level_multiplier(level, 'spd'))
        self.name = 'Blight Walker'
        self.stats_dict = {'hp': self.hp, 'atk': self.atk, 'def': self.defense, 'spd': self.spd, 'level': level}
        self.moves = ['Cursed Blades', 'Corrosive Nova', 'Shadow Bolt']


class Mummy(Enemy):
    def __init__(self, level=1):
        self.hp = math.floor(60 * get_level_multiplier(level, 'hp'))
        self.atk = math.floor(30 * get_level_multiplier(level, 'atk'))
        self.defense = math.floor(10 * get_level_multiplier(level, 'def'))
        self.spd = math.floor(90 * get_level_multiplier(level, 'spd'))
        self.name = 'Mummy'
        self.stats_dict = {'hp': self.hp, 'atk': self.atk, 'def': self.defense, 'spd': self.spd, 'level': level}
        self.moves = ['Crucify', 'Corrosive Nova', 'Screech']


class Dreadscythe(Enemy):
    def __init__(self, level=1):
        self.hp = math.floor(40 * get_level_multiplier(level, 'hp'))
        self.atk = math.floor(50 * get_level_multiplier(level, 'atk'))
        self.defense = math.floor(10 * get_level_multiplier(level, 'def'))
        self.spd = math.floor(110 * get_level_multiplier(level, 'spd'))
        self.name = 'Dreadscythe'
        self.stats_dict = {'hp': self.hp, 'atk': self.atk, 'def': self.defense, 'spd': self.spd, 'level': level}
        self.moves = ['Decapitate', 'Withering', 'Blade of Death']


class ArchonIcarus(Enemy):
    def __init__(self, level=1):
        self.hp = math.floor(110 * get_level_multiplier(level, 'hp'))
        self.atk = math.floor(30 * get_level_multiplier(level, 'atk'))
        self.defense = math.floor(7 * get_level_multiplier(level, 'def'))
        self.spd = math.floor(95 * get_level_multiplier(level, 'spd'))
        self.name = 'Archon Icarus'
        self.stats_dict = {'hp': self.hp, 'atk': self.atk, 'def': self.defense, 'spd': self.spd, 'level': level}
        self.moves = ['Tsuki', 'Hiraki Ashi', 'Katate Waza', 'Kachinuki']
        
    def move(self, stats_dict=None):
        stats_dict = stats_dict or self.stats_dict
        attack_move = random.choices(self.moves,
                                    weights=[6, 4, 4, 6])[0]
        m = Moves(stats_dict)
        move_stats = m.get_move_stats(attack_move)
        return attack_move, move_stats


class DynaminaToad(Enemy):
    def __init__(self, level=1):
        self.hp = math.floor(60 * get_level_multiplier(level, 'hp'))
        self.atk = math.floor(40 * get_level_multiplier(level, 'atk'))
        self.defense = math.floor(15 * get_level_multiplier(level, 'def'))
        self.spd = math.floor(90 * get_level_multiplier(level, 'spd'))
        self.name = 'Dynamina Toad'
        self.stats_dict = {'hp': self.hp, 'atk': self.atk, 'def': self.defense, 'spd': self.spd, 'level': level}
        self.moves = ['Body Slam', 'Detonation', 'Residue']


class Shadowstalker(Enemy): 
    def __init__(self, level=1):
        self.hp = math.floor(50 * get_level_multiplier(level, 'hp'))
        self.atk = math.floor(30 * get_level_multiplier(level, 'atk'))
        self.defense = math.floor(15 * get_level_multiplier(level, 'def'))
        self.spd = math.floor(120 * get_level_multiplier(level, 'spd'))
        self.name = 'Shadowstalker'
        self.stats_dict = {'hp': self.hp, 'atk': self.atk, 'def': self.defense, 'spd': self.spd, 'level': level}
        self.moves = ['Shadowstep', 'Nightmare Visage', 'Shadow Veil']


class Emberfiend(Enemy): 
    def __init__(self, level=1):
        self.hp = math.floor(40 * get_level_multiplier(level, 'hp'))
        self.atk = math.floor(40 * get_level_multiplier(level, 'atk'))
        self.defense = math.floor(20 * get_level_multiplier(level, 'def'))
        self.spd = math.floor(80 * get_level_multiplier(level, 'spd'))
        self.name = 'Emberfiend'
        self.stats_dict = {'hp': self.hp, 'atk': self.atk, 'def': self.defense, 'spd': self.spd, 'level': level}
        self.moves = ['Magma Surge', 'Inferno Shield', 'Erupting Tremor', 'Lava Burst']    

# Classes are more organised
class CelestialConvergence:
    def __init__(self):
        self.floors = CelestialConvergence.__subclasses__()


class Floor1(CelestialConvergence):
    floor = "Floor 1"
    rewards = [
       "500 Credits",
       "200 Universal XP",
       "3 Gold ore"
    ]
    enemies = {
        "wave 1": [
            BlightWalker(level=8),
            Dreadscythe(level=8),
            BlightWalker(level=8),
                ],
        "wave 2": [
            Mummy(level=10),
            DynaminaToad(level=10)
        ]
            }
    waves = 2
    loot_chest_rarities = [LootChests().rarities[0]]


class Floor2(CelestialConvergence):
    floor = "Floor 2"
    rewards = [
       "700 Credits",
       "400 Universal XP",
       "2 Diamond ore"
    ]
    enemies = {
        "wave 1": [
            DynaminaToad(level=10),
            Dreadscythe(level=8),
            DynaminaToad(level=10),
                ],
        "wave 2": [
            BlightWalker(level=12),
            Shadowstalker(level=10),
            BlightWalker(level=12),
        ]
            }
    waves = 2
    loot_chest_rarities = LootChests().rarities[:1]


class Floor3(CelestialConvergence):
    floor = "Floor 3"
    rewards = [
       "100 Credits",
       "500 Universal XP",
       "5 Diamond ore",
       "aurelia"
    ]
    enemies = {
        "wave 1": [
            Mummy(level=15),
            DynaminaToad(level=15),
            Mummy(level=15),
                ],
        "wave 2": [
            Shadowstalker(level=20),
            ArchonIcarus(level=30),
            Shadowstalker(level=20),
                  ]
            }
    waves = 2
    loot_chest_rarities = LootChests().rarities[:3]


      
# Ice stone
# Lightning slash
# fire slash
# Hot blast
# hellfire

# Items to create
# royal sword
# more relics
# endless content
# full test

import os, json, asyncio, requests
import math, random
from io import BytesIO
import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
import questable_stats as qstats

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='r!', intents=intents)

#  Initialising dict data from the jsons into a variable
with open("inventory.json", encoding='utf-8') as f:
    try:
      inventory = json.load(f)
    except:
      inventory = {}

with open("stats.json", encoding='utf-8') as f:
    try:
        stats = json.load(f)
    except:
        stats = {}

with open("quests.json", encoding="utf-8") as f:
    try:
        quests = json.load(f)
    except:
        quests = {}

@bot.event
async def on_ready():
    await asyncio.sleep(1)
    await quests_reset()
    print("Ready")

# Initialising levels dict through calculation
levels = {}
a = 10
c = 10
for i in range(1, 500):
    c += a
    levels[i] = c
    a += 10
    
class PastelColor(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.select(
        options=[
        discord.SelectOption(label="Lemon Chiffon", value="750348220571451562"),
        discord.SelectOption(label="Bluish White", value="1050423633731919962"),
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        roles = [interaction.guild.get_role(int(o.value)) for o in select.options]
        await interaction.user.remove_roles(*roles, atomic=True)
        await interaction.user.add_roles(interaction.guild.get_role(int(select.values[0])))
        await interaction.response.send_message(f"Ты выбрал цвет <@&{select.values[0]}>", ephemeral=True)

# @bot.command(name='test')
# async def test(ctx):
#     await make_relic(ctx.author, "Phoenix Talisman")
#     await make_relic(ctx.author, "Holy Grail")
#     grid = Image.open("objects/Step32_grid.png")
#     main_sprite = Image.open("objects/characters/main_sprite.png")
#     block_sprite = Image.open("objects/block.png")
#     grid.paste(main_sprite, tuple([3, 73]), mask=main_sprite)
#     block_coordinates = [104, 40] # top left 
#     starting_block_coordinates = [104, 40]
#     grid_list = [
#                             [None, None, None, None, None, None],
#                             [None, "block", "block", "air", "air", None],
#                             [None, "air",   "air",   "block", "air", None], 
#                             [None, "block", "block", "block", "air", None], 
#                             [None, "main",  "block", "air", "air", None],
#                             [None, None, None, None, None, None],
#                             ] 
#     for row in grid_list[1:-1]:
#         block_coordinates = starting_block_coordinates.copy()
#         for column in row[1:-1]:
#             if column == "block":
#                 grid.paste(block_sprite, tuple(block_coordinates),
#                           mask=block_sprite)
#             block_coordinates[0] += 36
#             block_coordinates[1] += 22
#         starting_block_coordinates[0] -= 36
#         starting_block_coordinates[1] += 22
#     img = await pil_image_to_discord_file(grid)
#     embed = discord.Embed(title="The Forgotten Legacy")
#     embed.set_image(url="attachment://image.png")
    
#     await ctx.reply(embed=embed, view=Step32Puzzle(ctx.author, None), file=img)

# @bot.command(name='save') 
# async def save(ctx):
#     with open('inventory.json', 'w+') as f:
#         json.dump(inventory, f) 
#     with open('quests.json', 'w+') as f:
#         json.dump(quests, f)  
#     with open('stats.json', 'w+') as f:
#         json.dump(stats, f)  
#     await ctx.reply('done')

def dump_json(f):
    if f == "inventory":
        with open('inventory.json', 'w+') as f:
            json.dump(inventory, f) 
    elif f == "stats":
        with open('stats.json', 'w+') as f:
            json.dump(stats, f)  
    elif f == "quests":
        with open('quests.json', 'w+') as f:
            json.dump(quests, f)  


# @bot.command(name='truncate')
# async def truncate_jsons(ctx):
#     if ctx.author.id != 561372656134520842: return
#     global inventory, stats, quests
#     with open('inventory.json', 'w+') as f:
#         json.dump({}, f) 
#     with open('quests.json', 'w+') as f:
#         json.dump({}, f)  
#     with open('stats.json', 'w+') as f:
#         json.dump({}, f)  
#     inventory = {}
#     stats = {}
#     quests = {}
#     await ctx.reply('done')

bot.remove_command('help')
@bot.command(name='help', description='Shows a list of commands')
async def help_command(ctx):
    return await manual(ctx)


def profile_check(character=False):
    def profile_check_decorator(func):
        async def profile_check_wrapper(ctx, *args, **kwargs):
          if str(ctx.author.id) not in inventory:
              return await ctx.reply("Start with `r!start`")
          elif character and args and args[0].lower() not in stats[str(ctx.author.id)]:
              return await ctx.reply("You don't have this character")
          else:
              return await func(ctx, *args, **kwargs)
        return profile_check_wrapper
    return profile_check_decorator

def individual_item_stat(item, stat, iv, level):
    item_base_stats = qstats.get_item_stats(item)
    level_multiplier = 1 + ((level - 1) * 0.77)
    if stat == 'spd':
        return math.floor((0.1 * (2 * item_base_stats[stat] + iv) * level_multiplier))
    return math.floor((0.1 * (2 * item_base_stats[stat] + iv * 4) * level_multiplier))

async def make_item(user, item, level=1, cap=None): 
    print(item)
    while True:
        atkiv = random.randint(0,11)
        defiv = random.randint(0,11)
        hpiv = random.randint(0,11)
        spdiv = random.randint(0,11)
        totaliv = atkiv + defiv + hpiv + spdiv
        percent = totaliv / 44 * 100
        if cap is None or percent <= cap:
            break
    inventory[str(user.id)]['items']['id'] += 1
    item_id = str(inventory[str(user.id)]['items']['id'])
    inventory[str(user.id)]['items'][item_id] = {item: {}}
    hp = individual_item_stat(item, 'hp', hpiv, level)
    atk = individual_item_stat(item, 'atk', atkiv, level)
    defen = individual_item_stat(item, 'def', defiv, level)
    spd = individual_item_stat(item, 'spd', spdiv, level)
    power = round(percent, 2)
    inventory[str(user.id)]['items'][item_id][item]['hp'] = hp
    inventory[str(user.id)]['items'][item_id][item]['atk'] = atk
    inventory[str(user.id)]['items'][item_id][item]['def'] = defen
    inventory[str(user.id)]['items'][item_id][item]['spd'] = spd
    inventory[str(user.id)]['items'][item_id][item]['level'] = level
    inventory[str(user.id)]['items'][item_id][item]['xp'] = 0 if level == 1 else levels[level]
    inventory[str(user.id)]['items'][item_id][item]['power'] = power
    inventory[str(user.id)]['items'][item_id][item]['id'] = item_id
    dump_json("inventory")

async def make_relic(user, relic, level=1):
    inventory[str(user.id)]['items']['id'] += 1
    item_id = str(inventory[str(user.id)]['items']['id'])
    relic_stats = qstats.Relics().get_relic_data(relic, level)
    inventory[str(user.id)]['items'][item_id] = {}
    inventory[str(user.id)]['items'][item_id][relic] = {"effect": relic_stats['effect'],
                                                       "level": level}
    dump_json("inventory")


def update_item_stats(user, item_id, prev_level):
    item_dict = inventory[str(user.id)]['items'][item_id]
    item_name = get_first_key(item_dict)
    def get_new_stat(stat_name, stat_value):
        prev_level_multiplier = 1 + ((prev_level - 1) * 0.77)
        new_level_multiplier = 1 + ((level - 1) * 0.77)
        return math.floor(stat_value / prev_level_multiplier * new_level_multiplier)

    level = inventory[str(user.id)]['items'][item_id][item_name]['level']
    hp = inventory[str(user.id)]['items'][item_id][item_name]['hp']
    atk = inventory[str(user.id)]['items'][item_id][item_name]['atk']
    defen = inventory[str(user.id)]['items'][item_id][item_name]['def'] 
    spd = inventory[str(user.id)]['items'][item_id][item_name]['spd']
    
    inventory[str(user.id)]['items'][item_id][item_name]['hp'] = get_new_stat('hp', hp)
    inventory[str(user.id)]['items'][item_id][item_name]['atk'] = get_new_stat('atk', atk)
    inventory[str(user.id)]['items'][item_id][item_name]['def'] = get_new_stat('def', defen)
    inventory[str(user.id)]['items'][item_id][item_name]['spd'] = get_new_stat('spd', spd)
    
    dump_json("inventory")
  
async def make_character(user, character):
    stats[str(user.id)][character] = {key: value for key, value in qstats.get_base_stats(character).items() if key in {'hp', 'atk', 'def', 'spd'}} 
    stats[str(user.id)][character]['level'] = 1
    stats[str(user.id)][character]['xp'] = 0
    stats[str(user.id)][character]['mana_regen'] = 1
    inventory[str(user.id)]['equipped'][character] = {'head': None, 'chest': None, 'legs': None, 'feet': None, 'hand': None, 'relics': {}}


async def tutorial_sequence(ctx):
    """
    Starts tutorial sequence for user
    Shows the inventory, view, equip
    Starts battle and starts in the next sequence (tutorial_sequence_2)
    """
    user = ctx.author
    await ctx.channel.send(f'{user.mention}, to get you started, I have given you some starting items')
    embed = discord.Embed(title='Obtained', 
                          description="""
                          Rookie Helmet 1x
                          Rookie Chestplate 1x
                          Rookie Leggings 1x
                          Rookie Boots 1x
                          Rookie Sword 1x
                          Iron Ore 10x
                          """, colour=discord.Colour.green())
    await asyncio.sleep(1.5)
    msg = await ctx.channel.send(embed=embed)
    await msg.reply('You can see what you have with `r!inventory`')
    await bot.wait_for('message',
                          check=lambda m: (m.content.startswith('r!inventory') or \
                                          m.content.startswith('r!inv')) and \
                                          m.author.id == user.id
                      )
    await asyncio.sleep(2)
    await ctx.channel.send('See what you have currently equipped with `r!view`')
    await bot.wait_for('message',
                          check=lambda m: (m.content.startswith('r!view') or \
                                          m.content.startswith('r!v')) and \
                                          m.author.id == user.id
                      )
    await asyncio.sleep(3)
    await ctx.channel.send('Put on the items you have in your inventory with `r!equip main {item_id}` \nor equip multiple items at once by separating item ids *with a space*. \nE.g. `r!equip main 1 2 3 4 5`')
    await bot.wait_for('message', check=lambda m: m.content.startswith('r!equip main') and \
                                                  m.author.id == user.id
                      )
    await asyncio.sleep(2)
    await ctx.channel.send('Now, you can see your new stats and equipped items with `r!view` again.')
    await bot.wait_for('message',
                          check=lambda m: (m.content.startswith('r!view') or \
                                          m.content.startswith('r!v')) and \
                                          m.author.id == user.id
                      )
    await asyncio.sleep(3)
    await ctx.channel.send('Time for you to start battling')
    await asyncio.sleep(2)
    enemies = [qstats.BlightWalker(level=1)]
    team_no = inventory[str(ctx.author.id)]['teams']['selected']
    team = [i for i in inventory[str(ctx.author.id)]['teams'][team_no] if i is not None]
    bt = asyncio.create_task(battle(ctx, team, [enemies]))
    tutorial_sq2 = asyncio.create_task(tutorial_sequence_2(ctx))
    await tutorial_sq2
    await bt

async def tutorial_sequence_2(ctx):
    """
    Second part of the tutorial sequence
    Shows battle, moves
    info commands: move_info, character_info, info, item_info
    Explains item enhancement to level up items
    """
    user = ctx.author
    msg = await bot.wait_for('message', check=  \
                             lambda m: m.author.id == bot.user.id and \
                                       m.embeds != [] and \
                                       m.embeds[0].title == 'Battle'
                            )
    await msg.reply('The first move will always consume no mana, but the second move might.\n`Smack` does single target damage while `Wack` attacks 2 enemies at once.\nIf there were 2 enemies, selecting enemy 1 would attack enemy 1 and the enemy to its right, enemy 2. Selecting enemy 2 would only hit enemy 2 unless the move targets more than 2 enemies.')
    await asyncio.sleep(5)
    await ctx.channel.send('To start attacking, click on a move. Then, click on a target enemy. In this case, it would be the level 1 BlightWalker')
    await asyncio.sleep(4)
    await ctx.channel.send('You can always see what your moves do with `r!move_info {move_name}`')
    msg = await bot.wait_for('message', check=  \
                             lambda m: m.author.id == bot.user.id and \
                                       m.embeds != [] and \
                                       m.embeds[0].description in {'Battle won', 'Battle lost'}
                      )
    if msg.embeds[0].description == 'Battle won':
        await msg.reply('Fantastic job! You got a chest out of that win. Chests will always drop XP and Credits, items are much rarer!')
    elif msg.embeds[0].description == 'Battle lost':
        await msg.reply("Looks like you aren't strong enough, try equipping the rest of your items")
    await asyncio.sleep(3)
    await ctx.channel.send("It's important to know what your characters and moves do. You can check it out with `r!character_info {character_name}` or `r!move_info {move_name}`")
    await asyncio.sleep(3.5)
    await ctx.channel.send("You can see your item's stats with `r!info {item_id}` or view its base stats with `r!item_info {item_name}`")
    await asyncio.sleep(4)
    await ctx.channel.send("Use `r!enhance {item_id}` to bring up the enhance menu\nE.g. `r!enhance 5`")
    msg = await bot.wait_for('message', check=  \
                      lambda m: m.author.id == bot.user.id and \
                                m.embeds != [] and \
                                m.embeds[0].title.startswith('Item Enhancement: ')
                      )
    await asyncio.sleep(1)
    await ctx.channel.send('Different ores give different amounts of experience, Diamond giving the most\nYou currently have 10 Iron ore.')
    await asyncio.sleep(1)
    await ctx.channel.send('Select Iron in the select menu')
    await bot.wait_for('message', check=  \
                      lambda m: m.author.id == bot.user.id and \
                                m.content == 'Enter the amount of Iron you would like to use:'
                      )
    await msg.reply('Input the amount in the chat')
    await bot.wait_for('message', check=  \
                      lambda m: m.author.id == bot.user.id and \
                                m.embeds != [] and \
                                m.embeds[0].title.endswith('levelled up!')
                      )
    await ctx.channel.send('Your item increased in level!\nCheck its new stats with `r!info {item_id}`')
    await bot.wait_for('message', check=  \
                       lambda m: (m.content.startswith('r!info ') or \
                                  m.content.startswith('r!i ')) and \
                                 m.author.id == user.id
                      )
    await asyncio.sleep(2)
    await ctx.channel.send("Nice! Check out available quests in your quest book with `r!quest book`")
    await bot.wait_for('message', check= \
                      lambda m:  m.embeds != [] and \
                                 m.embeds[0].title == "Quest Book" and \
                                 m.author.id == bot.user.id)
    await asyncio.sleep(2)
    await ctx.channel.send("Click on a quest to start, you can only start one quest at a time\nUse `r!map` to travel to different parts of the map and talk to different people")
    await asyncio.sleep(4)
    await ctx.channel.send("Mastering battles also include building teams, check it out with `r!team`")
    await bot.wait_for('message', check= \
                      lambda m:  m.embeds != [] and \
                                 m.embeds[0].title.startswith("Displaying team ") and \
                                 m.author.id == bot.user.id)
    await asyncio.sleep(5)
    await ctx.channel.send("You're all set! You can always check the `r!manual` whenever you need to")


@bot.command(name='start')
async def start(ctx):
    if str(ctx.author.id) in inventory:
        await ctx.reply("You've already started")
        return

    inventory[str(ctx.author.id)] = {'balance': 100, 
                                   'profile_toggle': {'private': False, 'show_balance': True},
                                   'teams': {'selected': '1',
                                             '1': ['main', None, None, None], 
                                             '2': [None, None, None, None], 
                                             '3': [None, None, None, None], 
                                             '4': [None, None, None, None]},
                                   'items': {'id': 0}, 'relics': {},
                                   'ores': {'Iron': 10, 'Gold': 0, 'Diamond': 0},
                                   'equipped': {'items': []},
                                   'location': 'Ark Cove'
                                    }
    items = ['Rookie Helmet', 'Rookie Chestplate', 'Rookie Leggings', 'Rookie Boots', 'Rookie Sword']
    for i in items:
        await make_item(ctx.author, i, cap=55)
    stats[str(ctx.author.id)] = {}
    await make_character(ctx.author, 'main')
    quests[str(ctx.author.id)] = {}
    dump_json("stats")
    dump_json("quests")
    embed = discord.Embed(
      title=f'Dear {ctx.author.name},',
      description=
      'I am delighted to hear that you have joined our adventure. This is Questable, and there are quite a few things to know in your adventure. Use `r!manual` to see.'
      )
    embed.set_image(url=
'https://cdn.discordapp.com/attachments/1046831128553734217/1125389078377005138/welcome_screen.png'
    )
    await ctx.reply(embed=embed)
    await asyncio.sleep(1.25)
    await tutorial_sequence(ctx)

ORE_ENHANCEMENT_VALUES = {'Iron': 100, 'Gold': 250, 'Diamond': 750}
class EnhanceView(discord.ui.View):
    def __init__(self, author, item_id):
        super().__init__()
        self.author = author
        self.item_id = item_id
        self.add_options()

    def add_options(self):
        #  Checks if user has the ore type, then adds the option to use it
        select_options = []
        if inventory[str(self.author.id)]['ores']['Iron']:
            select_options.append(discord.SelectOption(label="Iron", emoji='🔩', value='Iron'))
        if inventory[str(self.author.id)]['ores']['Gold']:
            select_options.append(discord.SelectOption(label="Gold", emoji='🪙', value='Gold'))
        if inventory[str(self.author.id)]['ores']['Diamond']:
            select_options.append(discord.SelectOption(label="Diamond", emoji='💎', value='Diamond'))

        if not select_options:
            select_options.append(discord.SelectOption(label="You don't have any ore left", value='no ore'))
    
        select_menu = discord.ui.Select(placeholder="Select an ore type", options=select_options)
      
        async def enhance_item(interaction: discord.Interaction): #  Callback
            ore_type = select_menu.values[0]
            if ore_type == 'no ore':
                await interaction.response.edit_message(view=EnhanceView(interaction.user, self.item_id))
                return
            await interaction.response.send_message(f'Enter the amount of {ore_type} you would like to use:')
            try:
                amount_message = await bot.wait_for('message', check=lambda m: m.content.isdigit() and m.author.id == self.author.id, timeout=30)
                amount = int(amount_message.content)
                if amount > inventory[str(self.author.id)]['ores'][ore_type]:
                  return await interaction.channel.send(f"You don't have enough {ore_type} ore to do this. Aborted")
                inventory[str(self.author.id)]['ores'][ore_type] -= amount
                item_dict = inventory[str(self.author.id)]['items'][self.item_id] 
                item_name = get_first_key(item_dict)
                inventory[str(self.author.id)]['items'][self.item_id][item_name]['xp'] += ORE_ENHANCEMENT_VALUES[ore_type] * amount
                new_level = get_level(inventory[str(self.author.id)]['items'][self.item_id][item_name]['xp'])
      
                if new_level != (level := inventory[str(self.author.id)]['items'][self.item_id][item_name]['level']):
                    embed = discord.Embed(title=f"{self.author.name}'s {item_name} levelled up!", description=f'{level} -> {new_level}', color=discord.Color.green())
                    embed.set_footer(text=f'Item id: {self.item_id}')
                    await interaction.channel.send(embed=embed)
                    inventory[str(self.author.id)]['items'][self.item_id][item_name]['level'] = new_level
                    update_item_stats(self.author, self.item_id, level)

          # If item is equipped
                if self.item_id in inventory[str(self.author.id)]['equipped']['items']:
                    item_path = get_item_equipped_path(self.item_id, inventory[str(self.author.id)]['equipped'])
                    inventory[str(self.author.id)]['equipped'][item_path['character']][item_path['slot']] = self.item_id
                    await calculate_stats(self.author, item_path['character'])
                
                dump_json("inventory")
          
            except asyncio.TimeoutError:
                  original_response = await interaction.original_response()
                  await original_response.reply('Timed out. Aborted.')
            await interaction.message.edit(view=EnhanceView(interaction.user, self.item_id))

        select_menu.callback = enhance_item
        self.add_item(select_menu)
    
    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id

@bot.command(name='enhance')
@profile_check()
async def enhance(ctx, item_id):
  if item_id not in inventory[str(ctx.author.id)]['items']:
      return await ctx.reply("You don't have this item")
  item = get_first_key(inventory[str(ctx.author.id)]['items'][item_id])
  if qstats.get_item_stats(item) is None:
      return await ctx.reply("Cannot enhance relic, use `r!augment`")

  user_ores = inventory[str(ctx.author.id)]['ores']
  embed = discord.Embed(title=f'Item Enhancement: {item}', 
                        description=f'''\
                        🔩 Iron ore {user_ores['Iron']}x
                        🪙 Gold ore {user_ores['Gold']}x
                        💎 Diamond ore {user_ores['Diamond']}x
                        ''')
  await ctx.reply(embed=embed, view=EnhanceView(ctx.author, item_id))

def get_item_equipped_path(item_dict, dictionary):
  for dict_key, dict_value in dictionary.items():
    if dict_key == 'items':
      continue
    if dict_value == item_dict:
      return dict_key
    if type(dict_value) == dict:
      slot = get_item_equipped_path(item_dict, dict_value)
      if slot:
        return {'character': dict_key, 'slot': slot}
  return None

@bot.command(name='ores', aliases=['show_ores'])
@profile_check()
async def show_ores(ctx):
  user_ores = inventory[str(ctx.author.id)]['ores']
  embed = discord.Embed(title='Enhancement Materials', 
                        description=f'''\
                        🔩 Iron ore {user_ores['Iron']}x
                        🪙 Gold ore {user_ores['Gold']}x
                        💎 Diamond ore {user_ores['Diamond']}x
                        ''')
  await ctx.reply(embed=embed)


@bot.command(name="balance")
@profile_check()
async def show_balance(ctx):
    balance = inventory[str(ctx.author.id)]['balance']
    embed = discord.Embed(title=f"{ctx.author.name}'s balance",
                          description=f"{balance} Credits",
                          colour=discord.Colour.green())
    await ctx.reply(embed=embed)


@bot.group(name='profile')
async def profile(ctx, user: discord.Member=None):
    if ctx.invoked_subcommand is not None: return
    user = user or ctx.author
    if str(ctx.author.id) not in inventory:
        return await ctx.reply("Start with `r!start`")
    elif str(user.id) not in inventory:
        return await ctx.reply(content=f"{user.mention} has not started", silent=True)
    if str(user.id) not in inventory:
        await ctx.reply(f'{user.name} has not started'); return
    if inventory[str(user.id)]['profile_toggle']['private']:
        await ctx.reply(f"{user.name}'s profile is private"); return

    balance = inventory[str(user.id)]['balance']
    embed = discord.Embed(title=f"{user.name}'s profile", 
                    description='You can edit your profile with rprofile_edit (it will show a menu of options).',
                        color=discord.Color.green())
  
    if inventory[str(user.id)]['profile_toggle']['show_balance']:
        embed.description += f'\nCredits: {balance}'

    selected_team = inventory[str(user.id)]['teams']['selected']
    for character in inventory[str(user.id)]['teams'][selected_team]:
        if character is None: continue
        character_dict = stats[str(user.id)][character]
        value = '\n'.join([f'{stat.upper()}: {character_dict[stat]}' for stat in character_dict if stat in {'hp', 'atk', 'def', 'spd', 'level', 'xp', 'class'}])
        value += "/" + str(levels[stats[str(user.id)][character]['level']+1])
        embed.add_field(name=character, value=value)
    await ctx.reply(embed=embed)

class ProfileEditView(discord.ui.View):
  def __init__(self, author):
    super().__init__()
    self.author = author
    self.add_buttons()
  def add_buttons(self):
    if inventory[str(self.author.id)]['profile_toggle']['private']:
      private_button = discord.ui.Button(label='Private', style=discord.ButtonStyle.red)
    else:
      private_button = discord.ui.Button(label='Public', style=discord.ButtonStyle.green)
      
    async def private_button_callback(interaction: discord.Interaction):
      inventory[str(self.author.id)]['profile_toggle']['private'] = False if inventory[str(self.author.id)]['profile_toggle']['private'] else True
      await interaction.response.edit_message(view=ProfileEditView(interaction.user))
      dump_json("inventory")

    if inventory[str(self.author.id)]['profile_toggle']['show_balance']:
      balance_button = discord.ui.Button(label='Show Balance', style=discord.ButtonStyle.green)
    else:
      balance_button = discord.ui.Button(label='Hide Balance', style=discord.ButtonStyle.red)

    async def balance_button_callback(interaction: discord.Interaction):
      inventory[str(self.author.id)]['profile_toggle']['show_balance'] = False if inventory[str(self.author.id)]['profile_toggle']['show_balance'] else True
      await interaction.response.edit_message(view=ProfileEditView(interaction.user))
      dump_json("inventory")
    
    private_button.callback = private_button_callback
    balance_button.callback = balance_button_callback
    self.add_item(private_button)
    self.add_item(balance_button)
    

  async def interaction_check(self, interaction):
    return self.author.id == interaction.user.id

@profile.command(name='edit')
@profile_check()
async def profile_edit(ctx):
  pass


@bot.command(name='augment', description='Combine duplicate relics to make them stronger.')
@profile_check()
async def augmentation(ctx, *item_ids):
    relics = [inventory[str(ctx.author.id)]["items"][item_id] for item_id in item_ids]
    relic_name = get_first_key(relics[0])
    if not all(get_first_key(name) == relic_name for name in relics):
        return await ctx.reply("Can only augment duplicate relics")
    if len(relics) < 2:
        return await ctx.reply("Can only combine more than 1 duplicate relics")
    for relic in relics:
        relic_name = get_first_key(relic)
        if (relic_data := qstats.Relics().get_relic_data(relic_name)) is None:
            return await ctx.reply(f"{relic_name} is not a relic")
            
    new_relic_level = relic[relic_name]["level"] + len(relics)-1
    new_relic_data = qstats.Relics().get_relic_data(relic_name, new_relic_level)
    inventory[str(ctx.author.id)]["items"][item_ids[0]][relic_name] = {
                                        "effect": new_relic_data["effect"],
                                        "level": new_relic_level
                                                                        }
    for item_id in item_ids[1:]:
        del inventory[str(ctx.author.id)]["items"][item_id]
    # testing for equipped on character
    for character in stats[str(ctx.author.id)]:
        for item_id in item_ids[:-1]:
            if inventory[str(ctx.author.id)]["equipped"][character]["relics"] == item_id:
                inventory[str(ctx.author.id)]["equipped"][character]["relics"] = None
                calculate_stats(ctx.author, character)
    dump_json("inventory")
    embed = discord.Embed(title=f"Augmentation: {relic_name}",
                         description=f"{relic_data['description']}\n↓\n{new_relic_data['description']}")
    img = await pil_image_to_discord_file(new_relic_data["image"])
    embed.set_image(url="attachment://image.png")
    await ctx.reply(embed=embed, file=img)


SHOP_ITEMS = {'Gladiator Helmet': 500, 'Steel Chestplate': 600, 'Winter Leggings': 600, 'Lucky Boots': 500, 'Rustic Sword': 550}
SHOP_ITEM_EMOJIS = ['<:gladiator_helmet:1111614692859850853>', '<:steel_chestplate:1111614540795367445>', 
                    '<:winter_leggings:1111614640670126090>', '<:lucky_boots:1111630064933675029>', 
                    '<:rustic_sword:1111614595581354054>']
@bot.group(name='shop')
async def shop(ctx):
  if ctx.invoked_subcommand is not None: return
  embed = discord.Embed(title='Market Shop', description='Use `r!shop buy {item}` to purchase.', colour=discord.Color.red())
  for i, item in enumerate(SHOP_ITEMS):
    embed.add_field(name=f'{SHOP_ITEM_EMOJIS[i]} {item}', value=f'Price: {SHOP_ITEMS[item]}')
  embed.set_thumbnail(
url='https://cdn.discordapp.com/attachments/1046831128553734217/1111616302977663077/shop.png'
  )
  await ctx.reply(embed=embed)

@shop.command(name='buy')
@profile_check()
async def shop_buy(ctx, *item):
  item = title(' '.join(item))
  if item not in SHOP_ITEMS:
    await ctx.reply('Item is not in the shop.'); return
  if SHOP_ITEMS[item] > inventory[str(ctx.author.id)]['balance']:
    await ctx.reply('You do not have enough money to buy this item.'); return
    
  inventory[str(ctx.author.id)]['balance'] -= SHOP_ITEMS[item]
  await make_item(ctx.author, item)
  dump_json("inventory")
  await ctx.reply(f'Successfully purchased {item} for {SHOP_ITEMS[item]}.')
  
@bot.command(name='add_character', aliases=['ac'])
@profile_check()
async def trial_battle(ctx, authorid, character):
    if ctx.author.id != 561372656134520842: return
    await make_character(bot.get_user(int(authorid)), character)
    await ctx.reply("done")

ongoing_battles = {}
async def battle(ctx, char, enemy_waves, 
                 user=None, wave_index=0, started=True,
                characters_stats=None, original_stats=None, mana_regen=None,
                loot_chest_rarities=None, mana=90):
  
  if started:
        battle_start_embed = discord.Embed(title="Battle starting...",
                                            colour=discord.Colour.from_str("#FFFFFF"))
        battle_start_embed.set_image(
        url="https://cdn.discordapp.com/attachments/1046831128553734217/1132637128308826112/crack.gif"
          )
        msg = await ctx.channel.send(embed=battle_start_embed)
        user = user or ctx.author
        
        # Initialising
        characters_stats = characters_stats or {'player': {}, 'enemies': {}}
        original_stats = original_stats or {'player': {}, 'enemies': {}}
        mana_regen = 1
        for character in char:
            characters_stats['player'][character] = stats[str(user.id)][character].copy()
            mana_regen += stats[str(user.id)][character]["mana_regen"]
            original_stats['player'][character] = stats[str(user.id)][character].copy()
            mana_regen += stats[str(user.id)][character]["mana_regen"]

  enemies = enemy_waves[wave_index]
    
  enemy_count = {enemy_name: 0 for enemy_name in set(e.name for e in enemies)}
  enemy_names = [e.name for e in enemies]
  for enemy in enemies:
    name = enemy.name
    if enemy_names.count(enemy.name) > 1:
        enemy_count[enemy.name] += 1
        name += f' {enemy_count[enemy.name]}'
    original_stats['enemies'][name] = enemy.stats_dict.copy()
    characters_stats['enemies'][name] = [enemy.stats_dict.copy(), enemy]
  print(enemy_count)
  ongoing_battles[user.id] = {}
  ongoing_battles[user.id]['moved'] = []
  ongoing_battles[user.id]['combo'] = {
                'requirements_met': False,
                'started': False
                                            }
  rounds = -1
  turn = 0
  effect = False
  effects = {'enemies': {}, 'player': {}}
  order = None
  #print(characters_stats)
  async def get_percentage(max, amount):
    return int(amount/max * 100)

  await asyncio.sleep(2)
  if started:
        await msg.edit(embed=discord.Embed(title="Battle starting...",
                                    colour=discord.Colour.from_str("#FFFFFF")))
  # Battle
  while user.id in ongoing_battles and \
  (player_live := any([characters_stats['player'][character]['hp'] > 0 for character in characters_stats['player']])) and \
  (enemy_live := any([characters_stats['enemies'][enemy][0]['hp'] > 0 for enemy in characters_stats['enemies']])):
      rounds += 1
      # ongoing_battles[ctx.author.id]['moved'] = True
      print(characters_stats)
      print()
      print(effects)
    
      # Determining turn order
      player_max_spd = max([characters_stats['player'][character]['spd'] for character in characters_stats['player']])
      ememies_max_spd = max(characters_stats['enemies'][enemy][0]['spd'] for enemy in characters_stats['enemies'])
      base_spd = max(player_max_spd, ememies_max_spd)
      relative_speeds = []
      for character in [chr for chr in characters_stats['player'] if characters_stats['player'][chr]['hp'] > 0]:
        relative_speeds.append({'spd': base_spd - characters_stats['player'][character]['spd'], 'name': character, 'side': 'player'})
      for i, enemy in enumerate([enmy for enmy in characters_stats['enemies'] if characters_stats['enemies'][enmy][0]['hp'] > 0]):
        relative_speeds.append({'spd': base_spd - characters_stats['enemies'][enemy][0]['spd'], 'name': enemy, 'side': 'enemy'})
      if order is not None:
          order.extend(sorted(relative_speeds, key=lambda x: x['spd']))
      else:
          order = sorted(relative_speeds, key=lambda x: x['spd'])
      order.append('End Turn')

      # try:
      if order[rounds] == 'End Turn': 
          mana += 5 * mana_regen
          if mana > 100:
            mana = 100
          apply_dot_text = ''
          for target in effects['enemies'].copy(): #  Calculating enemy effects
            for i, effect in enumerate(effects['enemies'][target]):
              if characters_stats['enemies'][target][0]['hp'] < 0: continue
              if effect['effect'] == 'dot':
                enemy_def = characters_stats['enemies'][target][0]['def']
                def_multiplier = 1 - (enemy_def // (enemy_def + 100 + 10 * characters_stats['enemies'][target][0]['level']))
                dmg = int(effect['value'] * def_multiplier * 0.64)
                characters_stats['enemies'][target][0]['hp'] -= abs(dmg)
                percentage = await get_percentage(original_stats['enemies'][target]['hp'], abs(dmg))
                apply_dot_text += f'{target} took {percentage}% from DoT\n'
              effects['enemies'][target][i]['duration'] -= 1
              if effects['enemies'][target][i]['duration'] <= 0:
                if effect['return']:
                  characters_stats['enemies'][target][0][effect['type']] -= effect['value']
                effects['enemies'][target].pop(i)
            if not effects['enemies'][target]: 
              del effects['enemies'][target]
                
          for target in effects['player'].copy(): #  Calculating player effects
            for i, effect in enumerate(effects['player'][target]):
              if characters_stats['player'][target]['hp'] < 0: continue
              if effect['effect'] == 'dot':
                player_def = characters_stats['player'][target]['def']
                def_multiplier = 1 - (player_def // (player_def + 100 + 10 * characters_stats['player'][target]['level']))
                dmg = int(effect['value'] * def_multiplier * 0.64)
                characters_stats['player'][target]['hp'] -= abs(dmg)
                if target in effects['player']: #  If there is hp buff
                    for i, effect in enumerate(effects['player'][target]):
                        if effect['effect'] == 'buff' and effect['type'] == 'hp' and effect['duration'] is not None:
                            effects['player'][target][i]['value'] -= dmg
                percentage = await get_percentage(original_stats['player'][target]['hp'], abs(dmg))
                apply_dot_text += f'{target} took {percentage}% from DoT\n'
              effects['player'][target][i]['duration'] -= 1
              if effect['duration'] <= 0:
                  if effect['return']:
                      if effect['effect'] == 'buff' \
                      and effect['type'] == 'hp' \
                      and effect['duration'] is not None: #  if hp buff and >0 left
                          if effects['player'][target][i]['value'] > 0:
                              characters_stats['player'][target][effect['type']] -= effect['value']
                      if effect['type'] is not None:
                          characters_stats['player'][target][effect['type']] -= effect['value']
                  effects['player'][target].pop(i)
              if not effects['player'][target]:
                del effects['player'][target]
          embed = await embed_display()
          embed.description = apply_dot_text
          msg = await ctx.channel.send(embed=embed)
          turn += 1
          effect = True
          continue
          
              
      # except Exception as e: print('e', e)
      
      # Turn starts
      current = order[rounds]
      current_name = current['name']
      current_side = current['side']

      # Continue if dead
      if current_side == 'enemy':
        if characters_stats['enemies'][current_name][0]['hp'] < 0:
          continue
      elif current_side == 'player':
        if characters_stats['player'][current_name]['hp'] < 0:
          continue

      # Display
      async def embed_display():
        embed = discord.Embed(title='Battle', description=f'Mana: {int(mana)}')
        for character in [chr for chr in characters_stats['player'] if characters_stats['player'][chr]['hp'] > 0]:
          player_current_hp = characters_stats['player'][character]['hp']
          player_max_hp = original_stats['player'][character]['hp']
          percentage = await get_percentage(player_max_hp, player_current_hp)
          next_turn_tuple = next(item for item in order[rounds:] if item != 'End Turn' and item['name'] == character)
          next_turn = order[rounds:].index(next_turn_tuple)
          lvl = original_stats['player'][character]['level']
          embed.add_field(name=f'{title(character)} lvl {lvl}: {next_turn}', value=f'HP: {percentage}%')

        embed.add_field(name='​', value='', inline=False)
        
        for enemy in [enmy for enmy in characters_stats['enemies'] if characters_stats['enemies'][enmy][0]['hp'] > 0]:
          enemy_current_hp = characters_stats['enemies'][enemy][0]['hp']
          enemy_max_hp = original_stats['enemies'][enemy]['hp']
          percentage = await get_percentage(enemy_max_hp, enemy_current_hp)
          next_turn_tuple = next(item for item in order[rounds:] if item != 'End Turn' and item['name'] == enemy)
          next_turn = order[rounds:].index(next_turn_tuple)
          lvl = original_stats['enemies'][enemy]['level']
          embed.add_field(name=f'{title(enemy)} lvl {lvl}: {next_turn}', value=f'HP: {percentage}%')
        return embed
      embed = await embed_display()

      if current_side == 'enemy': #  Enemy turn
        if current_name in effects['enemies']: #  If there is an effect
            interrupted = False #  Checks if the enemy turn is interrupted
            for effect in effects['enemies'][current_name]:
                if effect['effect'] == 'incapacitate':
                    embed.description += f'\n{current_name} is incapacitated and unable to move'
                    msg = await ctx.channel.send(embed=embed, view=None)
                    interrupted = True
                    break
            if interrupted: #  If True, skip turn
                continue
        enemy_object = characters_stats['enemies'][current_name][1]
        view = None
        enemy_move = enemy_object.move(characters_stats['enemies'][current_name][0])
        enemy_attack = enemy_move[0]
        enemy_attack_stats = enemy_move[1]
        potential_targets = [chr for chr in characters_stats['player'] if characters_stats['player'][chr]['hp'] > 0] #  For character that isnt dead            
        try: #  Testing for ValueError, sample size more than population
          targets = random.sample(potential_targets, enemy_attack_stats[1])
        except ValueError: #  If so, set targets to all potential targets
          targets = potential_targets
          
        embed.description = f'{current_name} used {enemy_attack} on {", ".join(targets)}.'
        for target in targets: #  Attacking and calculating damage
          player_def = characters_stats['player'][target]['def']
          def_multiplier = 1 - (player_def / (player_def + 90 + 7 * characters_stats['player'][target]['level']))
          enemy_attack_dmg = (enemy_attack_stats[0] + characters_stats['enemies'][current_name][0]['atk']) * def_multiplier
          characters_stats['player'][target]['hp'] -= enemy_attack_dmg
          if target in effects['player']: #  If hp buff
              for i, effect in enumerate(effects['player'][target]):
                  if effect['effect'] == 'buff' and effect['type'] == 'hp':
                      effects['player'][target][i]['value'] -= enemy_attack_dmg
          percentage = await get_percentage(original_stats['player'][target]['hp'], enemy_attack_dmg)
          embed.description += f'\n{enemy_attack} dealt {percentage}% to {target}'
          
          if (debuff := enemy_attack_stats[2]) is not None: #  If there is an effect
            debuff_desc = ''
            for i in debuff:
              print(i)
              if i['effect'] == 'debuff':
                for target in targets:
                  if target not in effects['player']:
                    effects['player'][target] = []
                  multiplier = (original_stats['player'][target][i['type']] - abs(i['value'])) / original_stats['player'][target][i['type']]
                  before_stat = characters_stats['player'][target][i['type']]
                  characters_stats['player'][target][i['type']] *= multiplier
                  decreased_by = before_stat - characters_stats['player'][target][i['type']]
                  effect_dict = i
                  effect_dict['value'] = decreased_by
                  effect_dict['return'] = True
                  effects['player'][target].append(effect_dict)
                debuff_desc += f"\nDecreased {target} {i['type']} by {int(abs(i['value']))} for {i['duration']} turns"
                  
              elif i['effect'] == 'dot':
                for target in targets:
                  if target not in effects['player']:
                    effects['player'][target] = []
                  effect_dict = i
                  effect_dict['return'] = False
                  effects['player'][target].append(effect_dict)
                debuff_desc += f"\nApplied DoT on {target} for {i['duration']} turns"

              elif i['effect'] == 'buff':
                  potential_targets = [chr for chr in characters_stats['enemies'] if characters_stats['enemies'][chr][0]['hp'] > 0]
                  try: #  Testing for ValueError, sample size more than population
                      targets = random.sample(potential_targets, enemy_attack_stats[1])
                  except ValueError: #  If so, set targets to all potential targets
                      targets = potential_targets
                  for target in targets:
                        if target not in effects['enemies']:
                            effects['enemies'][target] = []
                        effect_dict = i
                        effect_dict['return'] = True
                        effects['enemies'][target].append(effect_dict)
                        characters_stats['enemies'][target][0][i['type']] += i['value']
                        debuff_desc += f"\nIncreased {target} {i['type']} by {int(abs(i['value']))} for {i['duration']} turns"

              elif i['effect'] == 'incapacitate':
                for target in targets:
                    if target not in effects['player']:
                        effects['player'][target] = []
                    effect_dict = i
                    effect_dict['return'] = True
                    effects['player'][target].append(effect_dict)
                    debuff_desc += f"\nIncapacitated {target} for {i['duration']} turns"

              elif i['effect'] == 'cleanse':
                  potential_targets = [chr for chr in characters_stats['enemies'] if characters_stats['enemies'][chr][0]['hp'] > 0]
                  try: #  Testing for ValueError, sample size more than population
                      targets = random.sample(potential_targets, enemy_attack_stats[1])
                  except ValueError: #  If so, set targets to all potential targets
                      targets = potential_targets
                  for target in targets:
                      if target in effects['enemies']:
                          del effects['enemies'][target]
          
        if debuff:
          embed.description += debuff_desc

    
      # Preparing player turn and applying DoT
      elif current_side == 'player':
        if characters_stats['player'][current_name]['hp'] < 0:  # Continue if dead
          continue
        if current_name in effects['player']: #  If there is an effect
            interrupted = False #  Checks if player turn is interrupted
            for effect in effects['player'][current_name]: 
                if effect['effect'] == 'incapacitate':
                    embed.description += f'\n{current_name} is incapacitated and unable to move'
                    msg = await ctx.channel.send(embed=embed, view=None)
                    interrupted = True
                    break
            if interrupted: #  Skip turn if interrupted
                continue
          
        player_moves = qstats.get_base_stats(current_name)['moves']
        enemy_targets = [enmy for enmy in list(characters_stats['enemies'].keys()) if characters_stats['enemies'][enmy][0]['hp'] > 0]
        player_targets = [plyr for plyr in list(characters_stats['player'].keys()) if characters_stats['player'][plyr]['hp'] > 0]
        character_stats_dict = characters_stats['player'][current_name].copy()
        character_stats_dict['hp'] = stats[str(user.id)][current_name]['hp']
        if len(player_targets) > 1:
            ongoing_battles[user.id]['combo']['requirements_met'] = True
        else:
             ongoing_battles[user.id]['combo']['requirements_met'] = False
        view = BattleMoveSelect(character_stats_dict=character_stats_dict, 
                                mana=mana, moves=player_moves, author=user, 
                                targets={
                                    'enemies': enemy_targets, 
                                    'players': player_targets, 
                                    'current_player': current_name
                                })

      #embed = await embed_display()
      if effect:
        await asyncio.sleep(1)
        await msg.edit(embed=embed, view=view)
        effect = False
      else:
        msg = await ctx.channel.send(embed=embed, view=view)

      # Player's turn
      if current_side == 'player':
        ongoing_battles[user.id]['moved'] = False
        while not ongoing_battles[user.id]['moved']: #  Does nothing until move
          await asyncio.sleep(1)

        #  Initilise with data from move
        targets = ongoing_battles[user.id]['moved'][-1]
        mana = ongoing_battles[user.id]['moved'][3]
        attack_move = ongoing_battles[user.id]['moved'][4]

        embed.description = f'{current_name} used {attack_move} on {", ".join(targets)}.'
        #  Regular attack
        if (debuff := ongoing_battles[user.id]['moved'][2]) is None \
          or not any(effect['effect'] in {'buff', 'cleanse'} for effect in debuff):
            for target in targets:
                enemy_def = characters_stats['enemies'][target][0]['def']
                def_multiplier = 1 - (enemy_def / (enemy_def + 90 + 7 * characters_stats['enemies'][target][0]['level']))
                player_attack = (ongoing_battles[user.id]['moved'][0] + characters_stats['player'][current_name]['atk']) * def_multiplier
                characters_stats['enemies'][target][0]['hp'] -= player_attack
                percentage = await get_percentage(original_stats['enemies'][target]['hp'], player_attack)
                embed.description += f'\n{attack_move} dealt {percentage}% to {target}'
          
        # If debuff
        if debuff is not None:
            debuff_desc = ''
            for i in debuff:
                for target in targets:
                    if target not in effects['player'] \
                    and i['effect'] in {'buff', 'cleanse'}:
                        effects['player'][target] = []
                    elif target not in effects['enemies']:
                        effects['enemies'][target] = []
                    effect_dict = i
                    effect_dict['return'] = False if i['type'] in {'hp', None} else True
                    
                    if i['effect'] == 'dot':
                        effect_dict = i
                        effect_dict['return'] = False
                        effects['enemies'][target].append(effect_dict)
                        debuff_desc += f"\nApplied DoT on {target} for {i['duration']} turns"
                        
                    elif i['effect'] == 'debuff':
                        effects['enemies'][target].append(effect_dict)
                        multiplier = (original_stats['enemies'][target][i['type']] - abs(i['value'])) / original_stats['enemies'][target][i['type']]
                        before_stat = characters_stats['enemies'][target][0][i['type']]
                        characters_stats['enemies'][target][0][i['type']] *= multiplier
                        decreased_by = before_stat - characters_stats['enemies'][target][0][i['type']]
                        effect_dict['value'] = decreased_by
                        debuff_desc += f"\nDecreased {target} {i['type']} by {int(abs(i['value']))} for {i['duration']} turns"
                    
                    elif i['effect'] == 'buff':
                        effects['player'][target].append(effect_dict)
                        characters_stats['player'][target][i['type']] += i['value']
                        debuff_desc += f"\nIncreased {target} {i['type']} by {int(abs(i['value']))} for {i['duration']} turns"

                    elif i['effect'] == 'incapacitate':
                        effects['enemies'][target].append(effect_dict)
                        debuff_desc += f"\nIncapacitated {target} for {i['duration']} turns"

                    elif i['effect'] == 'cleanse':
                        if target in effects['player']:
                            del effects['player'][target]

            embed.description += debuff_desc
    
      await msg.edit(embed=embed)
      await asyncio.sleep(2) #  buffer
  if wave_index >= len(enemy_waves)-1:
        #  Battle end
        embed = await embed_display()
        if player_live:
          embed.description = 'Battle won'
          embed.set_image(
      url='https://cdn.discordapp.com/attachments/1046831128553734217/1125050474765221958/victory.gif'
        )
          await ctx.channel.send(embed=embed)
          rarities = loot_chest_rarities or qstats.LootChests().rarities[:-3]
          weights = [i**1.5 for i in range(2, len(rarities)+2)]
          rarity = random.choices(rarities, weights=weights, k=1)
          print(rarity)
          loot = qstats.LootChests().open_chest(rarity[0])
          for item in loot:
            print(item)
            if item.endswith(' Credits'):
                inventory[str(user.id)]['balance'] += int(''.join([i for i in item if i.isdigit()]))
            
            elif item.endswith(' XP'):
                for character in char:
                    stats[str(user.id)][character]['xp'] += int(''.join([i for i in item if i.isdigit()]))
                new_level = get_level(stats[str(user.id)][character]['xp'])
                if new_level != (level := stats[str(user.id)][character]['level']):
                    embed = discord.Embed(title=f'{title(character)} levelled up!', description=f'{level} -> {new_level}', color=discord.Color.green())
                    stats[str(user.id)][character]['level'] = new_level
                    await calculate_stats(user, character)
                    await ctx.channel.send(embed=embed)
                
            elif item.endswith(' ore'):
                ore_split = item.split()
                ore_type = ore_split[1]
                ore_amount = int(ore_split[0])
                inventory[str(user.id)]['ores'][ore_type] += ore_amount
          
            else:
                if qstats.get_item_stats(item) is None:
                    await make_relic(user, item, level=1)
                else:
                    await make_item(user, item, level=math.floor(new_level*1.1))

          loot_msg = "\n".join(loot)
          embed = discord.Embed(title=f'Obtained {rarity[0]} chest', description=f'Loot:\n {loot_msg}')
          await ctx.channel.send(embed=embed)
          dump_json("inventory")
    
          return "Won"
              
        elif enemy_live:
            embed.description = 'Battle lost'
            embed.set_image(
        url='https://cdn.discordapp.com/attachments/1046831128553734217/1125044173284855919/defeat.gif'
        )
            await ctx.channel.send(embed=embed)
            return "Lost"
  else:
        if enemy_live:
            embed.description = 'Battle lost'
            embed.set_image(
        url='https://cdn.discordapp.com/attachments/1046831128553734217/1125044173284855919/defeat.gif'
        )
            await ctx.channel.send(embed=embed)
            return "Lost"
      
        characters_stats['enemies'] = {}
        original_stats['enemies'] = {}
        await ctx.channel.send("## Next Wave")
        return await battle(ctx, char, enemy_waves, 
                     user=user, wave_index=wave_index+1, started=False,
                    characters_stats=characters_stats, original_stats=original_stats,
                    mana_regen=mana_regen, loot_chest_rarities=loot_chest_rarities,
                    mana=mana)


class BattleMoveSelect(discord.ui.View):
  def __init__(self, character_stats_dict, mana, moves, author, targets):
    super().__init__(timeout=30)
    self.mana = mana
    self.moves = moves
    self.author = author
    self.targets = targets
    self.character_stats_dict = character_stats_dict
    self.add_buttons()
  def add_buttons(self):
    buttons = []
    for move in self.moves:
      move_stats = qstats.Moves(self.character_stats_dict).get_move_stats(move)
      #print(move_stats)
      disable = True if move_stats[3] > self.mana else False
      bt1 = discord.ui.Button(label=move, disabled=disable, style=discord.ButtonStyle.green if move_stats[2] and move_stats[2][0]['effect'] in {'buff', 'cleanse'} else discord.ButtonStyle.blurple)
      #  Buff = green, else blurple
      buttons.append(bt1)
    
    async def move_callbacks(interaction, move_index):
      self.stop()
      m = qstats.Moves(self.character_stats_dict)
      move_stats = list(m.get_move_stats(buttons[move_index].label))
      await interaction.response.edit_message(view=BattleTargetSelect(self.character_stats_dict, move_stats, self.mana, self.moves, buttons[move_index].label, self.targets, interaction.user))
      
    async def move1(interaction: discord.Interaction):
      await move_callbacks(interaction, 0)
    async def move2(interaction: discord.Interaction):
      await move_callbacks(interaction, 1)
      
    buttons[0].callback = move1
    buttons[1].callback = move2
    for i in buttons: 
      self.add_item(i)

    combo_button_disabled = True
    combo_button_label = 'Combo' 
    if ongoing_battles[self.author.id]['combo']['requirements_met']:
        combo_button_disabled = False
        if not (combo_started := ongoing_battles[self.author.id]['combo']['started']) \
        or combo_started == 'awaiting confirmation':
            if combo_started == 'awaiting confirmation': combo_button_disabled = True
          
            async def combo_callback(interaction: discord.Interaction):
                combo_button.disabled = True
                combo_button.style = discord.ButtonStyle.green
                await interaction.response.edit_message(view=self)
                ongoing_battles[self.author.id]['combo']['started'] = 'awaiting confirmation'
                ##
      
        else:
            combo_mana = 75
            if self.targets['current_player'] in ongoing_battles[self.author.id]['combo']['started'] or \
            self.mana < combo_mana:
                combo_button_disabled = True
            combo_button_label = 'Initiate Combo'
            async def combo_callback(interaction: discord.Interaction):
                self.stop()
                combo_trait = qstats.get_base_stats(self.targets['current_player'])['combo_trait']
                ongoing_battles[self.author.id]['combo']['effects'].append(combo_trait)
                effects = ongoing_battles[self.author.id]['combo']['effects']
                move_stats = [60, 5, effects, combo_mana]
                ongoing_battles[self.author.id]['combo'] = {
                  'requirements_met': False,
                  'started': False 
                                              }
                await interaction.response.edit_message(
                    view=BattleTargetSelect(self.character_stats_dict, move_stats, 
                                            self.mana, self.moves, 'Combo', 
                                            self.targets, interaction.user)
                  )

    combo_button = discord.ui.Button(label=combo_button_label, style=discord.ButtonStyle.blurple,
                                        disabled=combo_button_disabled)
    try:  
        combo_button.callback = combo_callback
    except UnboundLocalError: pass
    self.add_item(combo_button)
    
  async def interaction_check(self, interaction: discord.Interaction):
    return interaction.user.id == self.author.id
  async def on_timeout(self):
    m = qstats.Moves(self.character_stats_dict)
    ongoing_battles[self.author.id]['moved'] = list(m.get_move_stats(self.moves[0]))
    ongoing_battles[self.author.id]['moved'][-1] = self.mana
    ongoing_battles[self.author.id]['moved'].append(self.moves[0]) 
    ongoing_battles[self.author.id]['moved'].append(random.sample(self.targets['enemies'], list(m.get_move_stats(self.moves[0]))[1]))


class BattleTargetSelect(discord.ui.View):
  def __init__(self, character_stats_dict, move_stats, mana, moves, move, targets, author):
    super().__init__(timeout=30)
    self.character_stats_dict = character_stats_dict
    self.move_stats = move_stats
    self.mana = mana
    self.moves = moves
    self.move = move
    self.targets = targets
    self.author = author
    self.add_buttons()

  def add_buttons(self):
    def make_function(ind): #  Explained [ctrl F] QuestsView()
      async def selected_target(interaction: discord.Interaction):
        self.stop()
        if ongoing_battles[self.author.id]['combo']['started'] == 'awaiting confirmation':
            ongoing_battles[self.author.id]['combo']['started'] = [self.targets['current_player']]
            combo_trait = qstats.get_base_stats(self.targets['current_player'])['combo_trait']
            ongoing_battles[self.author.id]['combo']['effects'] = [combo_trait]
        num_of_targets = self.move_stats[1]
        move_targets = [targets[ind]]
        count = 1
        for i in range(num_of_targets-1):
          if i % 2 == 0:
            try:
              move_targets.append(targets[ind+count])
            except: pass
          else:
            if ind - count >= 0:
              move_targets.append(targets[ind-count])
            count += 1
        
        self.mana -= self.move_stats[3]
        ongoing_battles[interaction.user.id]['moved'] = self.move_stats
        ongoing_battles[interaction.user.id]['moved'][-1] = self.mana
        ongoing_battles[interaction.user.id]['moved'].append(self.move)
        ongoing_battles[interaction.user.id]['moved'].append(move_targets)
        await interaction.response.edit_message(view=None)
      return selected_target

    if self.move_stats[2] and self.move_stats[2][0]['effect'] in {'buff', 'cleanse'}:
      targets = self.targets['players']
    else:
      targets = self.targets['enemies']
    for i, target in enumerate(targets):
      target_button = discord.ui.Button(label=title(target), style=discord.ButtonStyle.blurple)
      target_button.callback = make_function(i) #  Explained [ctrl F] QuestsView()
      self.add_item(target_button)
    back_button = discord.ui.Button(emoji='◀️', label='Back', style=discord.ButtonStyle.red)
    async def back_button_callback(interaction: discord.Interaction):
      self.stop()
      await interaction.response.edit_message(view=BattleMoveSelect(self.character_stats_dict, self.mana, self.moves, self.author, self.targets))
    back_button.callback = back_button_callback
    self.add_item(back_button)
      
  async def interaction_check(self, interaction: discord.Interaction):
    return interaction.user.id == self.author.id
  async def on_timeout(self):
    m = qstats.Moves(self.character_stats_dict)
    ongoing_battles[self.author.id]['moved'] = list(m.get_move_stats(self.moves[0]))
    ongoing_battles[self.author.id]['moved'][-1] = self.mana
    ongoing_battles[self.author.id]['moved'].append(self.moves[0]) 
    ongoing_battles[self.author.id]['moved'].append(random.sample(self.targets['enemies'], list(m.get_move_stats(self.moves[0]))[1]))

class TeamsView(discord.ui.View):
  def __init__(self, current_team, author):
    super().__init__()
    self.current_team = current_team
    self.author = author
    self.add_buttons()
  def add_buttons(self):
    numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    def make_function(i): #  Explained [ctrl F] QuestsView()
      async def show_team(interaction: discord.Interaction):
        team_set_display = await show_team_set(i, interaction.user)
        file = team_set_display[0]
        embed = team_set_display[1]
        await interaction.response.edit_message(attachments=[file], embed=embed, view=TeamsView(str(i), interaction.user))
        
      return show_team
      
    for number_index, number in enumerate(numbers):
      if str(number_index+1) == self.current_team:
        style = discord.ButtonStyle.green
      else:
        style = discord.ButtonStyle.blurple
      button = discord.ui.Button(label=number, style=style)
      button.callback = make_function(str(number_index+1))
      self.add_item(button)

    if self.current_team == inventory[str(self.author.id)]['teams']['selected']:
      label, disabled = 'Selected', True
    else:
      label = f'Select team {self.current_team}'
      if not any(i for i in inventory[str(self.author.id)]['teams'][self.current_team] if i):
        disabled = True  
      else:
        disabled = False
    select_button = discord.ui.Button(label=label, disabled=disabled, row=1)
    async def select_button_callback(interaction: discord.Interaction):
      inventory[str(interaction.user.id)]['teams']['selected'] = self.current_team
      await interaction.message.edit(view=TeamsView(self.current_team, interaction.user))
      await interaction.response.send_message(content=f'Selected team set {self.current_team}', ephemeral=True)
      dump_json("inventory")
    select_button.callback = select_button_callback
    self.add_item(select_button)
      
  async def interaction_check(self, interaction: discord.Interaction):
    return self.author.id == interaction.user.id
    
@bot.group(name='team')
async def team_command(ctx):
  if ctx.invoked_subcommand is not None: return 
  if str(ctx.author.id) not in inventory:
    return await ctx.reply("Start with `r!start`")
  selected_team = inventory[str(ctx.author.id)]['teams']['selected']
  team_set_display = await show_team_set(selected_team, ctx.author)
  file = team_set_display[0]
  embed = team_set_display[1]
  await ctx.reply(file=file, embed=embed, view=TeamsView(selected_team, ctx.author))

@team_command.command(name='set')
@profile_check()
async def team_set(ctx, team, *characters):
    if await team_check(ctx, team, characters, presence=False): return
    characters_ = []
    for character in characters:
        if character not in characters_:
            characters_.append(character.lower())
    new_characters = characters_[:]
    new_characters.extend( [None] * (4-len(characters_)) )
    inventory[str(ctx.author.id)]['teams'][team] = new_characters
    dump_json("inventory")
    new_characters = ', '.join(characters_)
    await ctx.reply(f'Team {team} set to {new_characters}')

@team_command.command(name='add')
@profile_check()
async def team_add(ctx, team, *characters):
    if await team_check(ctx, team, characters): return
    characters_ = []
    for character in characters:
        if character not in characters_:
            characters_.append(character.lower())
    current_team = [character for character in inventory[str(ctx.author.id)]['teams'][team] if character is not None]
    if len(current_team) + len(characters_) > 4:
        return await ctx.reply('Team size is too large, maximum is 4 characters per team')

    current_team.extend(characters_)
    current_team.extend( [None] * (4-len(characters_)) )
    inventory[str(ctx.author.id)]['teams'][team] = current_team
    dump_json("inventory")
    await ctx.reply(f"Added {', '.join(characters)} to team {team}")

@team_command.command(name='remove')
@profile_check()
async def team_remove(ctx, team, *characters):
    if await team_check(ctx, team, characters, presence=False): return
    characters_ = []
    for character in characters:
        if character not in characters_:
            characters_.append(character.lower())
    current_team = [character for character in inventory[str(ctx.author.id)]['teams'][team] if character is not None]
    if len(current_team) - len(characters_) <= 0 and \
        inventory[str(ctx.author.id)]['teams']['selected'] == team:
        return await ctx.reply('Selected team cannot be empty')

    new_team = [character for character in current_team if character not in characters_]
    new_team.extend( [None] * (4-len(characters_)) )
    inventory[str(ctx.author.id)]['teams'][team] = new_team
    dump_json("inventory")
    await ctx.reply(f"Removed {', '.join(characters_)} from team {team}")

async def show_team_set(selected_team, user):
  embed = discord.Embed(title=f'Displaying team {selected_team}', description=f'Use the numbers below to navigate between team sets.\nTo edit your teams, use `r!team set (team no.) (characters)` to set your team or use `r!team add (team no.) (character)`.', colour=discord.Colour.blurple())
  team_image = Image.open('character_team_empty.png')
  character_position = -11
  text_position = 20
  draw = ImageDraw.Draw(team_image)
  for character in inventory[str(user.id)]['teams'][selected_team]:
    if character is not None:
      character_image = Image.open(f'objects/characters/{character}_sprite.png')
      team_image.paste(character_image, (character_position, 0), mask=character_image)
      draw.text((text_position, 5), character)
    text_position += 43
    character_position += 43
  team_image.resize((team_image.size[0] * 3, team_image.size[1] * 3))
  file = await pil_image_to_discord_file(team_image)
  embed.set_image(url="attachment://image.png")
  return file, embed

async def team_check(ctx, team, characters, presence=True):
  if team not in {key for key in inventory[str(ctx.author.id)]['teams'] if key != 'selected'}:
    return await ctx.reply('Invalid team number')
  for character in characters:
    if character not in stats[str(ctx.author.id)]:
      return await ctx.reply(f"You don't have character `{character}`")
    if presence and character in inventory[str(ctx.author.id)]['teams'][team]:
      return await ctx.reply(f'{character} is already in the team')
  return False


class CharactersCataloguePages(discord.ui.View):
  def __init__(self, author, pages, disable=True):
    super().__init__()
    self.author = author
    self.pages = pages
    self.disable = disable
    self.page_no = 0
    self.add_buttons()

  def add_buttons(self):
    button_one = discord.ui.Button(emoji='◀️', disabled=self.disable)
    button_two = discord.ui.Button(emoji='▶️', disabled=self.disable)

    async def button_one_callback(interaction: discord.Interaction):
        self.page_no -= 1
        if self.page_no <= -1:
            self.page_no = len(self.pages) - 1
        await buttons_callback(interaction)

    async def button_two_callback(interaction: discord.Interaction):
        self.page_no += 1
        if self.page_no >= len(self.pages):
             self.page_no = 0
        await buttons_callback(interaction)

    async def buttons_callback(interaction):
        embed = discord.Embed(title=f"{interaction.user.name}'s characters", color=discord.Color.teal())
        embed.set_image(url="attachment://image.png")
        file = await pil_image_to_discord_file(self.pages[self.page_no])
        embed.set_footer(text=f"Page {self.page_no+1}/{len(self.pages)}")
        await interaction.response.edit_message(embed=embed, view=self, attachments=[file])

    button_one.callback = button_one_callback
    button_two.callback = button_two_callback
    self.add_item(button_one)
    self.add_item(button_two)

  async def interaction_check(self, interaction: discord.Interaction):
    return interaction.user.id == self.author.id

@bot.command(name="characters", aliases=["view_characters", "catalogue"])
@profile_check()
async def characters_catalogue(ctx):
    truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true'
    r = requests.get(truetype_url, allow_redirects=True)
    font = ImageFont.truetype(BytesIO(r.content), size=12)
    pages = []
    for i, character in enumerate(stats[str(ctx.author.id)]):
        if i % 6 == 0 or i == 0:
            img = Image.open("characters_catalogue_empty.png")
            img_draw = ImageDraw.Draw(img)
            text_x, text_y = -47, 4
            sprite_x, sprite_y = -80, 6
        elif i % 3 == 0 and i != 0:
            text_x = -47
            text_y = 100
            sprite_x, sprite_y = -80, 100
            
        text_x += 62
        sprite_x += 62
            
        img_draw.text((text_x, text_y), character, font=font, fill=(0, 0, 0))
        sprite = Image.open(f"objects/characters/{character}_sprite.png")
        img.paste(sprite, (sprite_x, sprite_y), mask=sprite)
        if (i+1) % 6 == 0 and i != 0:
            pages.append(img)
    pages.append(img)
    embed = discord.Embed(title=f"{ctx.author.name}'s characters", color=discord.Color.teal())
    embed.set_image(url="attachment://image.png")
    file = await pil_image_to_discord_file(pages[0])
    embed.set_footer(text=f"Page 1/{len(pages)}")
    disable = True if len(pages) == 1 else False
    await ctx.reply(embed=embed, 
                    file=file,
                    view=CharactersCataloguePages(ctx.author, pages, disable=disable),
                   )


@bot.command(name='unequip')
@profile_check(character=True)
async def unequip(ctx, character, *item_ids):
  character = character.lower()
  items = []
  for item_id in item_ids:
    if item_id in {'0', 'l'}:
      item_id = list(inventory[str(ctx.author.id)]['items'].keys())[-1]
    if item_id not in inventory[str(ctx.author.id)]['items']:
      await ctx.reply(f"You don't have item of id {item_id}"); break
    item = get_first_key(inventory[str(ctx.author.id)]['items'][item_id])
    if item_id not in list(inventory[str(ctx.author.id)]['equipped'][character].values()):
      await ctx.reply(f'Item of id {item_id} is not equipped on {character}'); break

    if (item_stats := qstats.get_item_stats(item)) is None:
        slot = "relics"
    else:
        slot = item_stats['slot']
    inventory[str(ctx.author.id)]['equipped']['items'].remove(item_id)
    inventory[str(ctx.author.id)]['equipped'][character][slot] = None
    items.append(item)

  if items:
    await calculate_stats(ctx.author, character)
    dump_json("inventory")
    items = ', '.join(items)
    await ctx.reply(f'Unequipped {items} on {character}')

@bot.command(name='equip')
@profile_check(character=True)
async def equip(ctx, character, *item_ids):
  character = character.lower()
  items = []
  for item_id in item_ids:
    if item_id in {'0', 'l'}:
      item_id = list(inventory[str(ctx.author.id)]['items'].keys())[-1]
    if item_id not in inventory[str(ctx.author.id)]['items']:
      await ctx.reply(f"You don't have item of id {item_id}"); break
    if item_id in inventory[str(ctx.author.id)]['equipped']['items']:
      await ctx.reply(f'Item of id {item_id} is already equipped'); break
    item = get_first_key(inventory[str(ctx.author.id)]['items'][item_id])
      
    item_stats = qstats.get_item_stats(item)
    if item_stats is not None: #  not relic
        if item_stats['class'] is not None and qstats.get_base_stats(character)['class'] != item_stats['class']:
            await ctx.reply(f"Unable to equip {item}; unmatched classes"); break

        slot = item_stats['slot']
        if (prev_item := inventory[str(ctx.author.id)]['equipped'][character][slot]) is not None:
            inventory[str(ctx.author.id)]['equipped']['items'].remove(prev_item)
        inventory[str(ctx.author.id)]['equipped']['items'].append(item_id)
        inventory[str(ctx.author.id)]['equipped'][character][slot] = item_id
        items.append(item)

    else: #  relic
        print(item_id)
        if (prev_item := inventory[str(ctx.author.id)]['equipped'][character]["relics"]):
            inventory[str(ctx.author.id)]['equipped']['items'].remove(prev_item)
        inventory[str(ctx.author.id)]['equipped']['items'].append(item_id)
        inventory[str(ctx.author.id)]['equipped'][character]["relics"] = item_id
        items.append(item)
        

  if items:
      await calculate_stats(ctx.author, character)
      dump_json("inventory")
      items = ', '.join(items)
      await ctx.reply(f"Equipped {items} on {character}")

def get_user_items(user):
  return [get_first_key(inventory[str(user.id)]['items'][i]) for i in inventory[str(user.id)]['items'] if i != 'id']

empty_head = Image.open(f"textures/head/empty-head.png")
empty_chest = Image.open(f"textures/chest/empty-chest.png")
empty_legs = Image.open(f"textures/legs/empty-legs.png")
empty_feet = Image.open(f"textures/feet/empty-feet.png")
empty_hand = Image.open(f"textures/hand/empty-hand.png")
empty_slot_images = {'head': empty_head, 'chest': empty_chest, 'legs': empty_legs, 'feet': empty_feet, 'hand': empty_hand}
slot_image_positions = [(130, 226), (130, 266), (135, 336), (140, 386), (130, 436)]
@bot.command(name='view', aliases=['v'])
@profile_check(character=True)
async def character_view(ctx, character='main'):
    character = character.lower()
    desc = ''
    userstats = stats[str(ctx.author.id)][character]
    userstats['class'] = qstats.get_base_stats(character)['class']
    for stat_name, stat in zip(userstats, list(userstats.values())):
      if stat_name in {'hp', 'atk', 'def', 'spd', 'level', 'xp', 'class'}:
        desc += f'{stat_name.upper()}: {stat}'
        if stat_name == 'xp':
          desc += f'/{levels[get_level(stat)+1]}'
        desc += '\n'
    embed = discord.Embed(title=f'Character: {character}'.title(), description=desc)
    
    bg = Image.open('textures/background.png')
    equipped = inventory[str(ctx.author.id)]['equipped'][character]
    print(equipped)
    userequipped = {k: v for k, v in equipped.items() if k != 'relics'}
    count = 0
    for slot, item_id in userequipped.items():
        if item_id is None:
            image = empty_slot_images[slot]
        else:
            item_name = get_first_key(inventory[str(ctx.author.id)]['items'][item_id])
            image = qstats.get_item_stats(item_name)['image']
        bg.paste(image, slot_image_positions[count], mask=image)
        count += 1

    item_id = inventory[str(ctx.author.id)]['equipped'][character]["relics"]
    if item_id:
        relic = get_first_key(inventory[str(ctx.author.id)]['items'][item_id])
        relic_stats = qstats.Relics().get_relic_data(relic)
        background = Image.open("textures/relics/relic_back.png")
        relic_image = relic_stats["image"]
        background.paste(relic_image, (0, 0), mask=relic_image)
        bg.paste(background, (127, 505), mask=background)
        
    image_final = bg.crop((120, 236, 240, 590)) #310
    items_image = await pil_image_to_discord_file(image_final)
    embed.set_image(url="attachment://image.png")
  
    character_sprite_image = discord.File(fp=f'objects/characters/{character}_sprite.png', filename=f'{character}_sprite.png')
    embed.set_thumbnail(url=f"attachment://{character}_sprite.png")
    await ctx.reply(files=[items_image, character_sprite_image], embed=embed)


@bot.command(name='info', aliases=['i'])
@profile_check()
async def info(ctx, item_id):
  if item_id == '0' or item_id == 'l':
    item_id = list(inventory[str(ctx.author.id)]['items'].keys())[-1]
  if item_id not in inventory[str(ctx.author.id)]['items']:
    await ctx.reply("You don't have this item"); return
  item = get_first_key(inventory[str(ctx.author.id)]['items'][item_id])
  if qstats.get_item_stats(item) is None: #  relic
      return await relic_info(ctx, item, 
                              level=inventory[str(ctx.author.id)]['items'][item_id][item]['level'])
      
  item_stats = inventory[str(ctx.author.id)]['items'][item_id][item]
  desc = ''
  for stat in list(item_stats.keys())[:-1]:
    desc += f'{stat.upper()}: {item_stats[stat]}'
    if stat == 'xp':
      desc += f'/{levels[get_level(item_stats[stat])+1]}'
    desc += '\n'

  slot = qstats.get_item_stats(item)['slot']
  embed = discord.Embed(title=f'Info: {item}', description=desc, colour=get_rarity_colour(qstats.get_item_stats(item)['rarity']))
  item = '_'.join(item.lower().split())
  file = discord.File(fp=f'textures/{slot}/{item}.png', filename=f'{item}.png')
  embed.set_image(url=f"attachment://{item}.png")
  embed.set_footer(text=f'Displaying item {item_id}')
  await ctx.reply(embed=embed, file=file)

@bot.command(name='item_info', aliases=['ii'])
@profile_check()
async def item_info(ctx, *item):
  item = title(' '.join(item))
  item_stats = qstats.get_item_stats(item)
  if item_stats == None:
    return await ctx.reply(f"Could not find {item}")
    
  desc = ''
  for stat in list(item_stats.keys())[:-1]:
    desc += f'{stat.upper()}: {item_stats[stat]}\n'

  slot = item_stats['slot']
  embed = discord.Embed(title=f'Item info: {item}', description=desc, colour=get_rarity_colour(item_stats['rarity']))
  embed.set_footer(text=f'Displaying item {item}')
  item = '_'.join(item.lower().split())
  item = item.replace("'", "")
  file = discord.File(fp=f'textures/{slot}/{item}.png', filename=f'{item}.png')
  embed.set_image(url=f"attachment://{item}.png")
  await ctx.reply(embed=embed, file=file)
  
def get_rarity_colour(rarity):
  if rarity == 'Common':
    colour = discord.Colour.greyple()
  elif rarity == 'Rare':
    colour = discord.Colour.brand_green()
  elif rarity == 'Mythic':
    colour = discord.Colour.purple()
  elif rarity == 'Legendary':
    colour = discord.Colour.yellow()
  elif rarity == 'Grand':
    colour = discord.Colour.fuschia()
  return colour

@bot.command(name='relic_info', aliases=['ri'])
@profile_check()
async def relic_info(ctx, *relic, level=1):
    relic = title(" ".join(relic))
    relic_stats = qstats.Relics().get_relic_data(relic, level)
    if relic_stats is None:
        return await ctx.reply(f"Could not find {relic}")
    embed = discord.Embed(title=relic,
                         description=relic_stats["description"],
                         colour=discord.Colour.orange())
    img = await pil_image_to_discord_file(relic_stats["image"])
    embed.set_image(url="attachment://image.png")
    await ctx.reply(embed=embed, file=img)

@bot.command(name='move_info', aliases=['mi'])
@profile_check()
async def move_info(ctx, *move):
    move = title(' '.join(move))
    move_stats = qstats.Moves(stats[str(ctx.author.id)]['main']).get_move_stats(move)
    if not move_stats:
        return await ctx.reply(f'Could not find move matching "{move}"')
    embed = discord.Embed(title=f'Move Info: {move}',
                        description=f"""\
ATK: {move_stats[0]}
Targets: {move_stats[1]}
Mana: {move_stats[3]}
                        """, color=discord.Color.blurple())
    if (move_effects := move_stats[2]) is not None:
        for effect in move_effects:
            move_effect_type = effect["effect"]
            t = ""
            if effect["duration"] is not None:
                t += f'Duration: {effect["duration"]}\n'
            if effect["type"] is not None:
                t += f'Type: {effect["type"]}\n'
            embed.description += f"\nEffect: {move_effect_type}\n" + t
    await ctx.reply(embed=embed)
  
@bot.command(name='character_info', aliases=['ci', 'char_info'])
@profile_check()
async def character_info(ctx, character):
  character = character.lower()
  character_base_stats = qstats.get_base_stats(character)
  if character_base_stats is None:
    return await ctx.reply(f'Could not find character "{character}"')
  combo_trait = character_base_stats['combo_trait']
  embed = discord.Embed(title=f'Character Info: {character}', 
                       description=f"""\
                       HP: {character_base_stats['hp']}
                       ATK: {character_base_stats['atk']}
                       DEF: {character_base_stats['def']}
                       SPD: {character_base_stats['spd']}
                       Class: {character_base_stats['class']}
                       Moves: {', '.join(character_base_stats['moves'])}
                       Combo Trait: {combo_trait['effect']} {combo_trait['type']} for {combo_trait['duration']} turns
                       """, color=discord.Color.blurple())
  sprite = discord.File(fp=f"objects/characters/{character}_sprite.png", filename=f'{character}_sprite.png')
  embed.set_image(url=f'attachment://{character}_sprite.png')
  await ctx.reply(embed=embed, file=sprite)
  
class InventoryView(discord.ui.View):
  def __init__(self, author, pages, disable=True):
    super().__init__()
    self.author = author
    self.pages = pages
    self.disable = disable
    self.page_no = 0
    self.add_buttons()

  def add_buttons(self):
    button_one = discord.ui.Button(emoji='◀️', disabled=self.disable)
    button_two = discord.ui.Button(emoji='▶️', disabled=self.disable)

    async def button_one_callback(interaction: discord.Interaction):
      self.page_no -= 1
      if self.page_no <= -1:
          self.page_no = len(self.pages) - 1
      await buttons_callback(interaction)

    async def button_two_callback(interaction: discord.Interaction):
      self.page_no += 1
      if self.page_no >= len(self.pages):
        self.page_no = 0
      await buttons_callback(interaction)

    async def buttons_callback(interaction):
      embed = discord.Embed(title=f"{interaction.user.name}'s inventory",
                            description=self.pages[self.page_no])
      embed.set_footer(text=f"Page {self.page_no+1}/{len(self.pages)}")
      await interaction.response.edit_message(embed=embed, view=self)

    button_one.callback = button_one_callback
    button_two.callback = button_two_callback
    self.add_item(button_one)
    self.add_item(button_two)

  async def interaction_check(self, interaction: discord.Interaction):
    return interaction.user.id == self.author.id


@bot.command(name='inventory', aliases=['inv'])
@profile_check()
async def inventory_command(ctx):
  show_items = '**ID ​ ​ ​• ​ ​ ​ Name ​    ​  ​ ​ • ​ ​ ​ ​  ​   LVL ​ • ​ Power**\n'
  pages = []
  disable_buttons = True
  count = 0
  for key, value in inventory[str(ctx.author.id)]['items'].items():
    count += 1
    if key != 'id':
      item_name = get_first_key(value)
      item_level = value[item_name]['level']
      try:
        item_power = value[item_name]['power']
        show_items += f'`{key}` {item_name} • lvl {item_level} • {item_power}%\n'
      except KeyError:
         show_items += f'`{key}` {item_name} • lvl {item_level}\n' 
      
    if count % 21 == 0:
      disable_buttons = False
      pages.append(show_items)
      show_items = '**ID ​ ​ ​• ​ ​ ​ Name ​    ​  ​ ​ • ​ ​ ​ ​  ​   LVL ​ • ​ Power**\n'
  pages.append(show_items)
  embed = discord.Embed(title=f"{ctx.author.name}'s inventory",
                        description=pages[0])
  embed.set_footer(text=f"Page 1/{len(pages)}")
  await ctx.reply(embed=embed,
                  view=InventoryView(ctx.author, pages, disable_buttons))


class Step32Puzzle(discord.ui.View): 
    def __init__(self, author, interaction, grid=None, coordinates=None):
        super().__init__(timeout=500) 
        self.author = author
        self.interaction = interaction
        self.coordinates = coordinates or [3, 73]
        self.grid = grid or [
                            [None, None, None, None, None, None],
                            [None, "air", "block", "air", "air", None],
                            [None, "air", "block", "block", "air", None], 
                            [None, "block", "block", "air", "air", None], 
                            [None, "main",  "block", "air", "block", None],
                            [None, None, None, None, None, None],
                            ] 
        """[None, None, None, None, None, None],
        [None, "block", "block", "air", "air", None],
        [None, "air",   "air",   "block", "air", None], 
        [None, "block", "block", "block", "air", None], 
        [None, "main",  "block", "air", "air", None],
        [None, None, None, None, None, None],
        ] """
        self.add_buttons()
    
    def add_buttons(self):
        grid = Image.open("objects/Step32_grid.png")
        main_sprite = Image.open("objects/characters/main_sprite.png")
        block_sprite = Image.open("objects/block.png")
        block_coordinates = [104, 40] # top left 
        starting_block_coordinates = [104, 40]
        for row in self.grid[1:-1]:
            block_coordinates = starting_block_coordinates.copy()
            for column in row[1:-1]:
                if column == "block":
                    grid.paste(block_sprite, tuple(block_coordinates),
                              mask=block_sprite)
                block_coordinates[0] += 36
                block_coordinates[1] += 22
            starting_block_coordinates[0] -= 36
            starting_block_coordinates[1] += 22
        grid.paste(main_sprite, tuple(self.coordinates), mask=main_sprite)
 
        empty_button_top_left = discord.ui.Button(label="​",
                                                 disabled=True,
                                                 row=0)
        empty_button_top_right = discord.ui.Button(label="​",
                                                 disabled=True,
                                                 row=0)
        empty_button_bottom_left = discord.ui.Button(label="​",
                                                 disabled=True,
                                                 row=2)
        empty_button_bottom_right = discord.ui.Button(label="​",
                                                 disabled=True,
                                                 row=2)
        empty_button_middle = discord.ui.Button(label="​",
                                                 disabled=True,
                                                 row=1)
        up_button = discord.ui.Button(emoji="🔼", 
                                      style=discord.ButtonStyle.blurple,
                                     disabled=True if "main" in self.grid[1] else False)
        down_button = discord.ui.Button(emoji="🔽", 
                                        style=discord.ButtonStyle.blurple,
                                        row=2,
                                       disabled=True if "main" in self.grid[-2] else False)
        left_button = discord.ui.Button(emoji="◀️", 
                                        style=discord.ButtonStyle.blurple,
                                        row=1,
                                       disabled=True if any(row[1] == "main" for row in self.grid) else False)
        right_button = discord.ui.Button(emoji="▶️", 
                                         style=discord.ButtonStyle.blurple,
                                         row=1,
                                         disabled=True if any(row[-2] == "main" for row in self.grid) else False)

        for i, row in enumerate(self.grid):
            if "main" in row:
                main_pos = (i, row.index("main"))
        
        async def up_button_callback(interaction):
            block_test = main_pos[0]-1, main_pos[1]
            if self.grid[block_test[0]-1][block_test[1]] != "air" and \
            self.grid[block_test[0]][block_test[1]] == "block":
                await interaction.response.send_message(content="Block in the way", ephemeral=True)
            else:
                if self.grid[block_test[0]][block_test[1]] == "block":
                    self.grid[block_test[0]-1][block_test[1]] = "block"
                self.grid[main_pos[0]][main_pos[1]] = "air"
                self.grid[block_test[0]][block_test[1]] = "main"
                self.coordinates[0] += 33
                self.coordinates[1] -= 26
                await display_grid(interaction)
        async def down_button_callback(interaction):
            block_test = main_pos[0]+1, main_pos[1]
            if self.grid[block_test[0]+1][block_test[1]] != "air" and \
            self.grid[block_test[0]][block_test[1]] == "block":
                await interaction.response.send_message(content="Block in the way", ephemeral=True)
            else:
                if self.grid[block_test[0]][block_test[1]] == "block":
                    self.grid[block_test[0]+1][block_test[1]] = "block"
                self.grid[main_pos[0]][main_pos[1]] = "air"
                self.grid[block_test[0]][block_test[1]] = "main"
                self.coordinates[0] -= 33
                self.coordinates[1] += 26
                await display_grid(interaction)
        async def left_button_callback(interaction):
            block_test = main_pos[0], main_pos[1]-1
            if self.grid[block_test[0]][block_test[1]-1] != "air" and \
            self.grid[block_test[0]][block_test[1]] == "block":
                await interaction.response.send_message(content="Block in the way", ephemeral=True)
            else:
                if self.grid[block_test[0]][block_test[1]] == "block":
                    self.grid[block_test[0]][block_test[1]-1] = "block"
                self.grid[main_pos[0]][main_pos[1]] = "air"
                self.grid[block_test[0]][block_test[1]] = "main"
                self.coordinates[0] -= 33
                self.coordinates[1] -= 26
                await display_grid(interaction)
        async def right_button_callback(interaction):
            block_test = main_pos[0], main_pos[1]+1
            if self.grid[block_test[0]][block_test[1]+1] != "air" and \
            self.grid[block_test[0]][block_test[1]] == "block":
                await interaction.response.send_message(content="Block in the way", ephemeral=True)
            else:
                if self.grid[block_test[0]][block_test[1]] == "block":
                    self.grid[block_test[0]][block_test[1]+1] = "block"
                self.grid[main_pos[0]][main_pos[1]] = "air"
                self.grid[block_test[0]][block_test[1]] = "main"
                self.coordinates[0] += 33 
                self.coordinates[1] += 26 
                await display_grid(interaction)

        async def display_grid(interaction):
            grid = Image.open("objects/Step32_grid.png")
            main_sprite = Image.open("objects/characters/main_sprite.png")
            block_sprite = Image.open("objects/block.png")
            block_coordinates = [104, 40] # top left 
            starting_block_coordinates = [104, 40]
            for row in self.grid[1:-1]:
                block_coordinates = starting_block_coordinates.copy()
                for column in row[1:-1]:
                    if column == "block":
                        grid.paste(block_sprite, tuple(block_coordinates),
                                  mask=block_sprite)
                    block_coordinates[0] += 36
                    block_coordinates[1] += 22
                starting_block_coordinates[0] -= 36
                starting_block_coordinates[1] += 22
            grid.paste(main_sprite, tuple(self.coordinates), mask=main_sprite)
            img = await pil_image_to_discord_file(grid)
            embed = discord.Embed(title="The Forgotten Legacy")
            embed.set_image(url="attachment://image.png")
            view = Step32Puzzle(interaction.user, interaction, grid=self.grid, coordinates=self.coordinates)
            if self.grid[1][-2] == "main": #  accomplished
                quest_title = get_started_quest(interaction.user)
                quest_info = quests[str(interaction.user.id)][quest_title]["checkpoint"][1]
                view = discord.ui.View()
                button = discord.ui.Button(label="Proceed", style=discord.ButtonStyle.green)
                button.callback = quest_continue_function(interaction.user, quest_info)
                view.add_item(button)
            await interaction.response.edit_message(embed=embed, attachments=[img],
            view=view)
            
            
        self.add_item(empty_button_top_left)
        self.add_item(up_button)
        self.add_item(empty_button_top_right)
        self.add_item(left_button)
        self.add_item(empty_button_middle)
        self.add_item(right_button)
        self.add_item(empty_button_bottom_left)
        self.add_item(down_button)
        self.add_item(empty_button_bottom_right)
        up_button.callback = up_button_callback
        down_button.callback = down_button_callback
        left_button.callback = left_button_callback
        right_button.callback = right_button_callback

        reset_button = discord.ui.Button(label="Reset", style=discord.ButtonStyle.red, row=1)
        async def reset_grid(interaction):
            self.coordinates = [3, 73]
            self.grid = [
                        [None, None, None, None, None, None],
                        [None, "air", "block", "air", "air", None],
                        [None, "air", "block", "block", "air", None], 
                        [None, "block", "block", "air", "block", None], 
                        [None, "main",  "block", "air", "air", None],
                        [None, None, None, None, None, None],
                        ] 
            await display_grid(interaction)
        reset_button.callback = reset_grid
        self.add_item(reset_button)

    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id

    async def on_timeout(self):
        self.stop()
        quest_title = get_started_quest(self.author)
        print(quests[str(self.author.id)][quest_title])
        quest_info = quests[str(self.author.id)][quest_title]["checkpoint"][1]
        view = discord.ui.View()
        button = discord.ui.Button(label="Proceed", style=discord.ButtonStyle.green)
        button.callback = quest_continue_function(self.author, quest_info)
        view.add_item(button)
        await self.interaction.channel.send("You couldn't solve it in time. Quest continued", view=view)


class Step29Puzzle(discord.ui.View):
    def __init__(self, author, interaction, disabled=[True, False, True], pile_1=None, pile_2=None):
        super().__init__(timeout=500)
        self.author = author
        self.interaction = interaction
        self.disabled = disabled
        self.pile_1 = pile_1 or list("W"*30 + "B"*70)
        random.shuffle(self.pile_1)
        self.pile_2 = pile_2 or []
        self.add_buttons()
    def add_buttons(self):
        move_10_to_pile_1_button = discord.ui.Button(label="Move 10 to Pile 1",
                                                    disabled=self.disabled[0])
        move_10_to_pile_2_button = discord.ui.Button(label="Move 10 to Pile 2",
                                                    disabled=self.disabled[1])
        flip_pile_2_button = discord.ui.Button(label="Flip Pile 2",
                                              disabled=self.disabled[2])
        reset_button = discord.ui.Button(label="Reset",
                                        style=discord.ButtonStyle.red)
        async def move_10_to_pile_2(interaction):
            p = self.pile_1[:10].copy()
            del self.pile_1[:10]
            self.pile_2.extend(p)
            self.disabled[2] = False
            self.disabled[0] = False
            if len(self.pile_1) < 10:
                self.disabled[1] = True
            await return_display(interaction)
            
        async def move_10_to_pile_1(interaction):
            p = self.pile_2[:10].copy()
            del self.pile_2[:10]
            self.pile_1.extend(p)
            if len(self.pile_2) < 10:
                self.disabled[0] = True
                self.disabled[2] = True
            await return_display(interaction)
            
        async def return_display(interaction):
            embed = discord.Embed(title="The Forgotten Legacy",
                                 description="In front of you are 100 cards, one side white, the other black.\nSplit them into 2 piles, each pile having an equal number of cards facing **white side up**.\nThere are **30** cards facing white side up initially."
                                 )
            embed.add_field(name="Pile 1", value=len(self.pile_1))
            embed.add_field(name="Pile 2", value=len(self.pile_2))
            if self.pile_1.count("W") == self.pile_2.count("W"):
                self.disabled = (True, True, True)
                quest_title = get_started_quest(self.author)
                quest_info = quests[str(self.author.id)][quest_title]["checkpoint"][1]
                func = quest_continue_function(self.author, quest_info)
                
            await interaction.response.edit_message(embed=embed, 
                                                    view=Step29Puzzle(
                                                                author=interaction.user,
                                                                interaction=interaction,
                                                                disabled=self.disabled,
                                                                pile_1=self.pile_1,
                                                                pile_2=self.pile_2))
            if self.pile_1.count("W") == self.pile_2.count("W"):
                await func(interaction)

        async def flip_pile_2(interaction):
            self.pile_2 = ("".join(self.pile_2)).replace("W", "*")
            self.pile_2 = self.pile_2.replace("B", "W")
            self.pile_2 = self.pile_2.replace("*", "B")
            self.pile_2 = list(self.pile_2)

            await return_display(interaction)

        async def reset_puzzle(interaction):
            embed = discord.Embed(title="The Forgotten Legacy",
                                 description="In front of you are 100 cards, one side white, the other black.\nSplit them into 2 piles, each pile having an equal number of cards facing **white side up**.\nThere are **30** cards facing white side up initially."
                                 )
            embed.add_field(name="Pile 1", value="100")
            embed.add_field(name="Pile 2", value="0")
            await interaction.response.edit_message(embed=embed,
                                                    view=Step29Puzzle(interaction.user, interaction))

        move_10_to_pile_1_button.callback = move_10_to_pile_1
        move_10_to_pile_2_button.callback = move_10_to_pile_2
        flip_pile_2_button.callback = flip_pile_2
        reset_button.callback = reset_puzzle
        self.add_item(move_10_to_pile_1_button)
        self.add_item(move_10_to_pile_2_button)
        self.add_item(flip_pile_2_button)
        self.add_item(reset_button)

    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id

    async def on_timeout(self):
        self.stop()
        quest_title = get_started_quest(self.author)
        quest_info = quests[str(self.author.id)][quest_title]["checkpoint"][1]
        view = discord.ui.View()
        button = discord.ui.Button(label="Proceed", style=discord.ButtonStyle.green)
        button.callback = quest_continue_function(self.author, quest_info)
        view.add_item(button)
        await self.interaction.channel.send("You couldn't solve it in time. Quest continued", view=view)
        

class Step26Choice(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author 
        quest_title = get_started_quest(author)
        quest_info = quests[str(author.id)][quest_title]["checkpoint"][1]
        self.func = quest_continue_function(author, quest_info)
        
    @discord.ui.button(label="Great Claymore")
    async def great_claymore_selected(self, interaction, button):
        self.stop()
        await interaction.message.edit(view=None)
        await make_item(self.author, "Great Claymore", level=3, cap=75)
        await interaction.response.send_message("You obtained Great Claymore")
        await self.func(interaction)
    @discord.ui.button(label="600 Credits")
    async def credits_selected(self, interaction, button):
        self.stop()
        await interaction.message.edit(view=None)
        inventory[str(self.author.id)]['balance'] += 600
        await interaction.response.send_message("You obtained 600 Credits")
        dump_json("inventory")
        await self.func(interaction)
    @discord.ui.button(label="3 Gold ore")
    async def gold_ore_selected(self, interaction, button):
        self.stop()
        await interaction.message.edit(view=None)
        inventory[str(self.author.id)]['ores']['Gold'] += 3
        await interaction.response.send_message("You obtained 3 Gold ore")
        dump_json("inventory")
        await self.func(interaction)
        
    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id


async def action_queue(queue_text, user, context, quest_info):
    queue = " ".join(queue_text.split()[1:])
    continue_bool = False
    quest_title = get_started_quest(user)
    print(queue)
    if queue.endswith("continue"): #  removes continue
        queue = " ".join(s for s in queue.split() if s != "continue") 
        continue_bool = True
    if queue.startswith("switch_speaker "): 
        character = queue.split("switch_speaker ")
        character = character[1] #  First index is empty
        try:
            return qstats.no_area_people[character.lower()]
        except KeyError:
            return [p for p in qstats.ArkCove().people if p.name == title(character)][0]
            
    elif queue.startswith("make_character "):
        character = queue.split("make_character ")
        character = character[1] #  First index is empty
        await make_character(user, character.lower())
        embed = discord.Embed(title=f"{title(character)} has joined your adventure!",
                             colour=discord.Colour.green())
        embed.set_image(url=f"attachment://{character}_sprite.png")
        sprite = discord.File(fp=f"objects/characters/{character}_sprite.png")
        embed.set_footer(text="Use r!view {character} and r!team add {team_no} {character}")
        await context.channel.send(embed=embed, file=sprite)
        
    elif queue.startswith("custom_area "):
        area = queue.split("custom_area ")
        area = area[1] #  First index is empty
        images = qstats.custom_area_images[area]
        embed = discord.Embed(title=area)
        embed.set_image(url=images[0])
        if len(images) > 1:
            embed.set_thumbnail(url=images[1])
        quest_title = get_started_quest(user)
        try:
            quests[str(user.id)][quest_title]["checkpoint"][1] = quest_info
        except IndexError:
            quests[str(user.id)][quest_title]["checkpoint"].append(quest_info)
        dump_json("quests")
        await asyncio.sleep(1.5)
        await context.channel.send(embed=embed)

    elif queue.startswith("checkpoint"):
        quest_title = get_started_quest(user)
        quests[str(user.id)][quest_title]["checkpoint"][0] = quests[str(user.id)][quest_title]["step"]
        quest_object = qstats.Quest().match_quest(quest_title)
        quests[str(user.id)][quest_title]["checkpoint"][1] = quest_info
        quests[str(user.id)][quest_title]["task"] = quest_object.tasks[quests[str(user.id)][quest_title]["step"]]
        try:
            quests[str(user.id)][quest_title]["checkpoint"].remove("battle")
        except ValueError:
            pass
        dump_json("quests")

    elif queue.startswith("battle "):
        enemy_info = queue.split("battle ")[1].split()
        enemy_names = enemy_info[:-1]
        print(enemy_names, enemy_info)
        enemy_level = int(enemy_info[-1])
        enemies = []
        for enemy_name in enemy_names:
            enemy_object = qstats.Enemy().match_enemy(enemy_name)
            enemies.append(enemy_object(level=enemy_level))
        
        team_no = inventory[str(user.id)]['teams']['selected']
        team = [i for i in inventory[str(user.id)]['teams'][team_no] if i is not None]
        battle_result = await battle(context, team, [enemies], user=user)
        if battle_result == "Lost":
            quests[str(user.id)][quest_title]["step"] = quests[str(user.id)][quest_title]["checkpoint"][0]
            await context.channel.send("Make sure to build you team, equip and enhance items on your characters. Try again with `r!quest continue`")
        else:
            step = quests[str(user.id)][quest_title]["step"]
            quests[str(user.id)][quest_title]["checkpoint"] = [step, quest_info, "battle"]
            view = discord.ui.View()
            button = discord.ui.Button(label="Proceed", style=discord.ButtonStyle.green)
            button.callback = quest_continue_function(user, quest_info)
            view.add_item(button)
            await context.channel.send("_ _", view=view)

    elif queue.startswith("quest_end"):
        quests[str(user.id)][quest_title]["started"] = False
        quests[str(user.id)][quest_title]["done"] = True
        dump_json("quests")
        quest_object = qstats.Quest().match_quest(quest_title)
        rewards = quest_object.rewards
        print(rewards)
        for item in rewards:
            if item.endswith(' Credits'):
                inventory[str(user.id)]['balance'] += int(''.join([i for i in item if i.isdigit()]))
            
            elif item.endswith(' Universal XP'):
                for character in stats[str(user.id)]:
                    stats[str(user.id)][character]['xp'] += int(''.join([i for i in item if i.isdigit()]))
                    new_level = get_level(stats[str(user.id)][character]['xp'])
                    if new_level != (level := stats[str(user.id)][character]['level']):
                        embed = discord.Embed(title=f'{title(character)} levelled up!', description=f'{level} -> {new_level}', color=discord.Color.green())
                        stats[str(user.id)][character]['level'] = new_level
                        await calculate_stats(user, character)
                        await context.channel.send(embed=embed)
                        await asyncio.sleep(0.6)
                
            elif item.endswith(' ore'):
                ore_split = item.split()
                ore_type = ore_split[1]
                ore_amount = int(ore_split[0])
                inventory[str(user.id)]['ores'][ore_type] += ore_amount
          
            else:
                if qstats.get_item_stats(item) is None:
                    await make_relic(user, item, level=1)
                else:
                    await make_item(user, item, level=math.floor(new_level*1.1))
    
        loot_msg = "\n".join(rewards)
        embed = discord.Embed(title='Quest Completed', 
                              description=f'Loot:\n {loot_msg}')
        await context.channel.send(embed=embed)
        await asyncio.sleep(1)
        embed = discord.Embed(title=f'{quest_title} Completed', 
                              description='To be continued')
        await context.channel.send(embed=embed)
        dump_json("inventory")
        
    
    if continue_bool:
        return "continue"
    else:
        return None
        

def quest_continue_function(author, quest_info):
    quest_title = quest_info["title"]
    quest_place = quest_info["place"]
    try:
        quest_speaker = qstats.no_area_people[quest_info["speaker"].lower()]    
    except KeyError:
        quest_speaker = [p for p in qstats.ArkCove().people if p.name == quest_info["speaker"]][0]
    print(quest_speaker)
    async def quest_continue(interaction): 
        if interaction.user.id != author.id: return
            
        await interaction.message.edit(view=None)
        nonlocal quest_speaker,quest_info
        if not interaction.response.is_done():
            await interaction.response.defer()
        # Next step
        text_bodies = qstats.Quest().redirect(quest_title, quests[str(author.id)][quest_title]["step"]) 
        quests[str(author.id)][quest_title]["step"] += 1
        quest_object = qstats.Quest().match_quest(quest_title)
        quests[str(author.id)][quest_title]["task"] = quest_object.tasks[quests[str(author.id)][quest_title]["step"]]
        dump_json("quests")
        responded = False
        for text in text_bodies:
            # Check for queue
            if text.startswith("$queue"):
                speaker = await action_queue(text, author, interaction, quest_info)
                if "custom_area" in text:
                    quests[str(author.id)][quest_title]["checkpoint"] = [
                        quests[str(author.id)][quest_title]["step"], 
                        {"title": quest_title, "place": quest_place, "speaker": quest_speaker.name}
                    ]
    
                print(text, speaker)
                await asyncio.sleep(1)
                if speaker == "continue":
                    continue
                if speaker is not None:
                    quest_speaker = speaker
                    await quest_continue(interaction) #  Recursion
                return
            display_text = text.replace("{user}", author.name)
            embed = discord.Embed(title=quest_place,
                                  description=f"{quest_speaker.name}: {display_text}")
            if text.startswith("https://"):
                embed.description = None
                embed.set_image(url=text)
            embed.set_footer(text=quest_title)
            if (quests[str(author.id)][quest_title]["task"].startswith("Find out") \
            or quests[str(author.id)][quest_title]["task"].startswith("Talk with")) \
            and text == text_bodies[-1]:
                view = DialogueOptionsView(author, quest_speaker, 
                                           quest_title, quest_place)
            else:
                view = None

            # Special steps, Close these for readability
            if text == "https://cdn.discordapp.com/attachments/1046831128553734217/1132535768460558416/step_27.png":
                view = Step26Choice(author)
                
            elif text == "Step29Puzzle":
                view = Step29Puzzle(author, interaction)
                embed = discord.Embed(title="The Forgotten Legacy",
                                 description="In front of you are 100 cards, one side white, the other black.\nSplit them into 2 piles, each pile having an equal number of cards facing **white side up**.\nThere are **30** cards facing white side up initially."
                                 )
                embed.add_field(name="Pile 1", value=100)
                embed.add_field(name="Pile 2", value=0)
                await interaction.channel.send(embed=embed, view=view)
                return
                
            elif text == "Step32Puzzle":
                grid = Image.open("objects/Step32_grid.png")
                main_sprite = Image.open("objects/characters/main_sprite.png")
                block_sprite = Image.open("objects/block.png")
                grid.paste(main_sprite, tuple([3, 73]), mask=main_sprite)
                block_coordinates = [104, 40] # top left 
                starting_block_coordinates = [104, 40]
                grid_list = [
                            [None, None, None, None, None, None],
                            [None, "air", "block", "air", "air", None],
                            [None, "air", "block", "block", "air", None], 
                            [None, "block", "block", "air", "block", None], 
                            [None, "main",  "block", "air", "air", None],
                            [None, None, None, None, None, None],
                            ] 
                for row in grid_list[1:-1]:
                    block_coordinates = starting_block_coordinates.copy()
                    for column in row[1:-1]:
                        if column == "block":
                            grid.paste(block_sprite, tuple(block_coordinates),
                          mask=block_sprite)
                        block_coordinates[0] += 36
                        block_coordinates[1] += 22
                    starting_block_coordinates[0] -= 36
                    starting_block_coordinates[1] += 22
                img = await pil_image_to_discord_file(grid)
                embed = discord.Embed(title="The Forgotten Legacy")
                embed.set_image(url="attachment://image.png")
    
                await interaction.channel.send(embed=embed,      
                                               view=Step32Puzzle(interaction.user,
                                                                 interaction), 
                                               file=img)
                return

            elif text == "Step36Boss":
                await asyncio.sleep(2)
                enemies = [qstats.Mummy(level=2),
                           qstats.Dreadscythe(level=2),
                           qstats.Mummy(level=2)]
                another_wave = [qstats.Mummy(level=3),
                                qstats.ArchonIcarus(level=10),
                                qstats.Mummy(level=3)]
                user = interaction.user
                team_no = inventory[str(user.id)]['teams']['selected']
                team = [i for i in inventory[str(user.id)]['teams'][team_no] if i is not None]
                step = quests[str(user.id)][quest_title]["step"]
                quests[str(user.id)][quest_title]["checkpoint"] = [step+1, quest_info, "battle"]
                battle_result = await battle(interaction, team, [enemies, another_wave], 
                                             user=user,
                            loot_chest_rarities=qstats.LootChests().rarities[2:4])
                print(battle_result)
                if battle_result == "Lost":
                    quests[str(user.id)][quest_title]["step"] = quests[str(user.id)][quest_title]["checkpoint"][0]
                    await interaction.channel.send("Make sure to build you team, equip and enhance items on your characters. Try again with `r!quest continue`")
                else:
                    quest_info = quests[str(user.id)][quest_title]["checkpoint"][1]
                    step = quests[str(user.id)][quest_title]["step"]
                    quests[str(user.id)][quest_title]["checkpoint"] = [step, quest_info, "battle"]
                    await interaction.channel.send("Report back to Jeffrey at the Townsquare")
                    text_bodies = qstats.Quest().redirect(quest_title, quests[str(author.id)][quest_title]["step"]) 
                    quests[str(user.id)][quest_title]["step"] += 1
                    quest_object = qstats.Quest().match_quest(quest_title)
                    quests[str(user.id)][quest_title]["task"] = quest_object.tasks[quests[str(user.id)][quest_title]["step"]]
                dump_json("quests")
                quests[str(user.id)][quest_title]["checkpoint"].remove("battle")
                return
                
            if responded:
                await asyncio.sleep(prev_text_time) #  Time based on length of text
                await interaction.channel.send(embed=embed, view=view)
            else:
                if view is None: # view = None would throw an error
                    await interaction.followup.send(embed=embed)
                    responded = True
                else:
                    await interaction.followup.send(embed=embed, view=view)
            prev_text_time = len(text)/43

    return quest_continue

    
class DialogueOptionsView(discord.ui.View):
    def __init__(self, author, person, dialogue, current_place):
        super().__init__()
        self.author = author
        self.person = person
        self.dialogue = dialogue
        self.current_place = current_place
        self.add_buttons()
    def add_buttons(self):
        def make_function(dialogue, dialogue_type, option_index): #  Explained [ctrl F] QuestsView()
            async def dialogue_callback(interaction: discord.Interaction):
                await interaction.message.edit(view=None)
                text =  qstats.dialogue_response(dialogue, dialogue_type, option_index)
                embed = discord.Embed(title=self.current_place,
                                     description=f"{self.person.name}: {text}")
                await interaction.response.send_message(embed=embed)
            return dialogue_callback
        
        # Checking for quest
        for quest_title in quests[str(self.author.id)]: 
            if quests[str(self.author.id)][quest_title]["started"]:
                print(quests[str(self.author.id)][quest_title]["task"])
                step = quests[str(self.author.id)][quest_title]["step"]

                quest_button_callback = quest_continue_function(self.author, 
                                                                {"title": quest_title, 
                                                                "place": self.current_place,
                                                                "speaker": self.person.name})
                if (current_task:=quests[str(self.author.id)][quest_title]["task"]).startswith(f"Talk to {self.person.name}"):
                    quest_button = discord.ui.Button(label=f"Talk to {self.person.name}",
                                                    style=discord.ButtonStyle.blurple)
                    quest_button.callback = quest_button_callback
                    self.add_item(quest_button)
    
                elif current_task.startswith("Find out") or \
                current_task.startswith("Talk with"):
                    dialogue = f"{quest_title}_{step}"
                    for i, dialogue_option in enumerate(self.person.dialogue_options[dialogue]):
                        quest_button = discord.ui.Button(label=dialogue_option,
                                                        style=discord.ButtonStyle.grey)
                        quest_button.callback = quest_button_callback
                        self.add_item(quest_button)
                            
                break    
                
        else: #  No quest
            for i, dialogue_option in enumerate(self.person.dialogue_options[self.dialogue]):
                dialogue_button = discord.ui.Button(label=dialogue_option, style=discord.ButtonStyle.grey)
                dialogue_button.callback = make_function(self.person.dialogue, self.dialogue, i)
                self.add_item(dialogue_button)
    
    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id

    async def on_timeout(self):
        quest_title = get_started_quest(self.author)
        quests[str(self.author.id)][quest_title]["step"] = quests[str(self.author.id)][quest_title]["checkpoint"][0]
        quest_object = qstats.Quest().match_quest(quest_title)
        quests[str(self.author.id)][quest_title]["task"] = quest_object.tasks[quests[str(self.author.id)][quest_title]["step"]]
        dump_json("quests")
            

class QuestableMapView(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author
        self.add_buttons()
    def add_buttons(self):
        def make_function(area_object, current_place): #  Explained [ctrl F] QuestsView()
            async def place_button_callback(interaction: discord.Interaction):
                await interaction.message.edit(view=None)
                person = [p for p in area_object.people if p.location == current_place][0]
                text = person.dialogue["default"]
                embed = discord.Embed(title=current_place,
                                     description=f"{person.name}: {text}")
                await interaction.response.send_message(embed=embed, view=DialogueOptionsView(interaction.user, person, "default", current_place))
                
            return place_button_callback
        location = inventory[str(self.author.id)]['location']
        location_object = [area for area in qstats.areas if area.name == location][0]
        for place in location_object.locations:
            place_button = discord.ui.Button(label=place, style=discord.ButtonStyle.blurple)
            place_button.callback = make_function(location_object, place)
            self.add_item(place_button)

    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id

@bot.command(name='map', description='Shows the map')
@profile_check()
async def questable_map(ctx):
    location = inventory[str(ctx.author.id)]['location']
    location_object = [area for area in qstats.areas if area.name == location][0]
    location_image = discord.File(location_object.fp, filename=f"{location_object.snake_case}.png")
    embed = discord.Embed(title=location_object.name, description=None, color=discord.Color.orange())
    embed.set_image(
    url=f"attachment://{location_object.snake_case}.png"
    )
    await ctx.reply(embed=embed, file=location_image, view=QuestableMapView(ctx.author))


class QuestsView(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author
        #  Disable all buttons if started quest
        self.disable_all = False
        if any(quests[str(author.id)][q]["started"] for q in quests[str(author.id)]):
            self.disable_all = True
    
        self.add_buttons()
    def add_buttons(self):
        # Making a function allows an external argument to be parsed
        # discord button callback will only take interaction arg
        def make_function(quest_object):
            async def quest_button_callback(interaction: discord.Interaction):
                quests[str(self.author.id)][quest_object.title] = {}
                quests[str(self.author.id)][quest_object.title]["started"] = True
                quests[str(self.author.id)][quest_object.title]["step"] = 0
                quests[str(self.author.id)][quest_object.title]["checkpoint"] = [0]
                quests[str(self.author.id)][quest_object.title]["task"] = quest_object.tasks[0]
                embed = discord.Embed(title="Embark on a quest", 
                                      description=
                                      f"""
                                      **{quest_object.title}**
                                      {quest_object.description}
                                      *First task:*
                                      {quest_object.tasks[0]}
                                      """,
                                      colour=discord.Colour.teal()) 
                await interaction.response.send_message(
                                    content=f"Started `{quest_object.title}`",
                                    embed=embed
                                        )
                await interaction.message.edit(view=QuestsView(interaction.user))
                dump_json("quests")
            return quest_button_callback
            
        for quest in qstats.Quest().quests:
            # If the list of started quest titles is not empty and it's title matches
            if (started_quest:=[q for q in quests[str(self.author.id)] if quests[str(self.author.id)][q]["started"]]) and \
            started_quest[0] == quest.title:
                style = discord.ButtonStyle.green
            else:
                style = discord.ButtonStyle.grey

            # Checking requirements
            user_stats = stats[str(self.author.id)]
            if any(quest().level_requirements_check(user_stats[char]["level"]) for char in user_stats):
                disabled = self.disable_all
            else:
                disabled = True
            if (quest.title in quests[str(self.author.id)] \
            and not quests[str(self.author.id)][quest.title]["done"]):
                disabled = True
            quest_button = discord.ui.Button(label=quest.title,
                                             disabled=disabled,
                                             style=style)
            quest_button.callback = make_function(quest)
            self.add_item(quest_button)

    async def interaction_check(self, interaction):
        return self.author.id == interaction.user.id


@bot.group(name='quest', invoked_without_subcommand=False, aliases=['q'])
async def quest_command(ctx):
    return
@quest_command.command(name='continue')
@profile_check()
async def quest_continue_command(ctx):
    quest_title = get_started_quest(ctx.author)
    if quests[str(ctx.author.id)][quest_title]["step"] == 0:
        return await ctx.reply("You just started")
    try:
        print(quests[str(ctx.author.id)][quest_title])
        if quests[str(ctx.author.id)][quest_title]["checkpoint"][0] != quests[str(ctx.author.id)][quest_title]["step"]:
            return await ctx.reply("You are not at a checkpoint")
    except KeyError:
        return await ctx.reply("You are not at a checkpoint")

    if quests[str(ctx.author.id)][quest_title]["checkpoint"][-1] == "battle":
        view = discord.ui.View()
        quest_info = quests[str(ctx.author.id)][quest_title]["checkpoint"][1]
        button = discord.ui.Button(label="Proceed", style=discord.ButtonStyle.green)
        button.callback = quest_continue_function(ctx.author, quest_info)
        view.add_item(button)
        return await ctx.reply("_ _", view=view)

    if quests[str(ctx.author.id)][quest_title]["task"].startswith("Talk to "):
        return await ctx.reply(quests[str(ctx.author.id)][quest_title]["task"])
    
    text_bodies = qstats.Quest().redirect(quest_title, 
                                          quests[str(ctx.author.id)][quest_title]["checkpoint"][0]-1
                                         ) 
    quest_info = quests[str(ctx.author.id)][quest_title]["checkpoint"][1]
    for i, text in enumerate(text_bodies[::-1]): #  checks for the queue in the last text body
        if text.startswith("$queue custom_area "):
            i = (i + 1) * -1
            break
    for text in text_bodies[i:]:
        if text.startswith("$queue"):
            speaker = await action_queue(text, ctx.author, ctx, quest_info)
            if speaker == "continue":
                continue
            if speaker is not None:
                quest_info["speaker"] = speaker.name
            await asyncio.sleep(1)
    quest_continue_func = quest_continue_function(ctx.author, 
                                                  quest_info=quest_info
                                                 )
    view = discord.ui.View()
    button = discord.ui.Button(label="Continue", style=discord.ButtonStyle.blurple)
    button.callback = quest_continue_func
    view.add_item(button)
    await ctx.reply("Click to continue", view=view)
    
    
@quest_command.command(name='book')
@profile_check()
async def quest_book_command(ctx):
    embed = discord.Embed(title='Quest Book', 
                          description='Travelling the world and ended up in this town. New commissions will immediately be updated in your quest book.\nSelect a quest below, you can only start one quest at a time.\n\nUse `r!quest continue` to continue where you left off.',
                          colour=discord.Colour.yellow()
                         )
    for quest in qstats.Quest().quests:
        if quest.title not in quests[str(ctx.author.id)]: continue
        if quests[str(ctx.author.id)][quest.title]["started"]:
            task = quests[str(ctx.author.id)][quest.title]["task"]
            embed.add_field(name=quest.title, 
                            value=f"{quest.description}\n\nTask: {task}"
                            )
            break
    await ctx.reply(embed=embed, view=QuestsView(ctx.author))


def get_started_quest(user):
    for quest_title in quests[str(user.id)]: 
            if quests[str(user.id)][quest_title]["started"]:
                return quest_title
    return None


class Manual_View(discord.ui.View):
  def __init__(self, author):
    super().__init__()
    self.author = author

  @discord.ui.select(placeholder="Select help menu",
                     options=[
    discord.SelectOption(label="Levelling up", emoji='⬆', value='levelling'),
    discord.SelectOption(label="Combat", emoji='⚔️', value='combat'),
    discord.SelectOption(label="Quests", emoji='📜', value='quests'),
    discord.SelectOption(label="Equipment", emoji='🎒', value='equipment'),
    discord.SelectOption(label="Commands", emoji='🪄', value='commands')
                     ])
  async def help(self, interaction: discord.Interaction, select: discord.ui.Select):
    if select.values[0] == "levelling":
      embed = discord.Embed(
        title='Questable Guide: Levelling',
        description="""
You can level up in a few ways; through quests, defeating enemies and completing dungeons. When you level up, you base stats increase. You can also find enhancement materials for your gear in loot chests. Loot chests are randomly found in dungeons.
__*Levelling up gear*__
Use `r!enhance`, select the desired ore type and enter the amount to use.
Each ore type gives different amounts of xp to your gear; iron giving the least and diamond with the most.
__*Levelling up characters*__
You level up your characters by using them in battle, or completing quests.
Levelling up increases your characters' stats which you can display with `r!view {character}` or `r!profile`.
      """)
      embed.set_thumbnail(     url="https://cdn.discordapp.com/attachments/1046831128553734217/1108766482973863957/level_up.gif")
    elif select.values[0] == "combat":
      embed = discord.Embed(
        title='Questable Guide: Combat',
        description="""
Combat is turn-based. Turn order is decided on character speeds. The number of turns before a character's next one is indicated beside its name. Select your moves using the buttons when it's your turn.
Each move could have a certain buff/debuff applied to characters.
__*How to battle*__
First, click a move, then click the target. It's that simple.
Different moves have different abilities and different number of targets, use `r!move_info` to find out more about your characters' moves.

Each character also has a **combo trait**. 
Combos can be started by clicking on *Combo*, and then initiated with *Initiate Combo* on another character. This would combine their combo traits, attacking a maximum of 5 enemies with a powerful blow. However, this also requires a lot of mana. 
You can check your characters' information with `r!character_info` and view their stats with `r!view`.
      """)
    elif select.values[0] == "quests":
        embed = discord.Embed(
            title="Questable Guide: Quests",
            description="""
Quests are filled with story and mystery. Solving puzzles along the way and making new friends.
You can check your available quests with `r!quest book`. 
Some quests have level requirements and/or requirements to complete prerequisites.
Level requirements is based on the highest level character that you have.
You can always check your current task with `r!quest book`.
            """)
        embed.set_thumbnail(
    url="https://cdn.discordapp.com/attachments/1046831128553734217/1130142177423528026/quests.png"
        )
    elif select.values[0] == "equipment":
        embed = discord.Embed(
            title="Questable Guide: Equipment",
            description="""
As you journey along your adventure, you will collect many items, whether it be from loot chests, or rewards. See what you have with `r!inventory` and equip with `r!equip`.
Most of the equipment you collect will be different. Each stat of an item determined by a multiplier. The higher the multipliers, the higher the **power**, which is out of a hundred.
**Relics** offer a great ton of utility. Whether it be from providing extra mana regeneration, or causing your attack to inflict a status effect, relics are an essential part of battle.
            """)
        embed.set_thumbnail(
      url='https://cdn.discordapp.com/attachments/1046831128553734217/1123274990230437888/swords.gif')
    elif select.values[0] == "commands":
        embed = discord.Embed(
            title="Questable Guide: Commands",
            description=
"""
*List of commands*
r!start          
r!info {item_id}     
r!character_info {character_name}
r!item_info {item_name}
r!relic_info {item_name}
r!move_info {move_name}
r!characters
r!inventory
r!view {character_name}
r!enhance {item_id}
r!ores
r!augment {`*`item_ids}
r!equip {item_id}
r!unequip {item_id}
r!team  
r!team add {team_number} {character} 
r!team remove {team_number} {character} 
r!team set {team_number} {`*`characters} 
r!manual         Shows this message
r!map
r!quest book
r!quest continue
r!profile        
r!shop           
r!shop buy      
r!market
r!market sell {item_id} {price}
r!market buy {id}
r!balance
r!celestial convergence
""",
            colour=discord.Colour.from_str("#808080")
        )
        embed.set_footer(text="*Arguments separated by a space")

    await interaction.response.edit_message(embed=embed, view=self)

  async def interaction_check(self, interaction: discord.Interaction):
    return interaction.user.id == self.author.id


@bot.command(name='manual')
async def manual(ctx):
  embed = discord.Embed(
    title='Questable Guide',
    description=
    'Questable is an RPG based game on discord which utilises turn-based combat. It features fun items to play around with in combat to climb in level and power.\nSelect a menu below for more information.')
  embed.set_thumbnail(url=   
"https://cdn.discordapp.com/attachments/1046831128553734217/1108731368545976330/pixil-frame-0.png")
  await ctx.reply(embed=embed, view=Manual_View(ctx.author))


class MarketView(discord.ui.View):
    def __init__(self, author, pages, disable=True):
        super().__init__()
        self.author = author
        self.pages = pages
        self.disable = disable
        self.page_no = 0
        self.add_buttons()

    def add_buttons(self):
        button_one = discord.ui.Button(emoji='◀️', disabled=self.disable)
        button_two = discord.ui.Button(emoji='▶️', disabled=self.disable)

        async def button_one_callback(interaction: discord.Interaction):
            self.page_no -= 1
            if self.page_no <= -1:
                self.page_no = len(self.pages) - 1
            await buttons_callback(interaction)

        async def button_two_callback(interaction: discord.Interaction):
            self.page_no += 1
            if self.page_no >= len(self.pages):
                self.page_no = 0
            await buttons_callback(interaction)

        async def buttons_callback(interaction):
            embed = discord.Embed(title=f"{interaction.user.name}'s inventory",
                            description=self.pages[self.page_no])
            embed.set_footer(text=f"Page {self.page_no+1}/{len(self.pages)}")
            await interaction.response.edit_message(embed=embed, view=self)

        button_one.callback = button_one_callback
        button_two.callback = button_two_callback
        self.add_item(button_one)
        self.add_item(button_two)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


def compare(value, operator, other_value):
    if operator == '<': return value < other_value
    if operator == '>': return value > other_value
    if operator == '=': return value == other_value
    if operator == '!=': return value != other_value
    if operator == '>=': return value >= other_value
    if operator == '<=': return value <= other_value
    return None


@bot.group(name="market", aliases=["m"], invoke_without_command=True)
async def market(ctx, *, filter=None):
    if str(ctx.author.id) not in inventory:
        return await ctx.reply("Start with `r!start`")
    if ctx.invoked_subcommand is not None: return
    embed = discord.Embed(title="Player Market", 
                          description="**ID ​ ​ ​ ​ ​ ​ ​ ​  ​ ​​ ​• ​  ​ ​ ​ ​ ​  ​​ ​ ​ ​  ​​ ​ Name ​    ​  ​ ​ • ​ ​ ​ ​  ​   LVL ​ • ​ Power ​ • ​ Price**\n",
                          colour=discord.Colour.brand_red()) 
    if filter is not None and filter[0].lower() != "=mine":
        try:
            filter = filter.split()
            filter_type = filter[0]
            filter_operator = filter[1]
            if len(filter_operator) > 2:
                raise IndexError('Invalid filter operator')
            filter_value = " ".join(filter[2:])
            if not filter_value.isdigit():
                raise IndexError('Filter value out of range')

        except IndexError:
            return await ctx.reply("Invalid filter, see `r!market help`")

    pages = []
    page = ""
    with open("market.json", "r") as mf:
        m = json.load(mf)
        count = 0
        for item_id in list(reversed(sorted(m.keys()))):
            if item_id == "latest_id": continue
            item_name =  get_first_key(m[item_id]["info"])
            item_stats = m[item_id]["info"][item_name]
            price = m[item_id]["price"]

            if filter is not None:
                if filter_type.lower() in {"=n", "=name"}:
                    if item_name.lower() != filter_value.lower():
                        continue
                elif filter_type.lower() in {"=p", "=price"}:
                    if not compare(price, filter_operator, int(filter_value)):
                        continue
                elif filter_type.lower() == "=power":
                    if not compare(item_stats["power"], filter_operator, int(filter_value)):
                        continue
                elif filter_type.lower() != "=mine":
                    if m[item_id]["owner"] != ctx.author.id:
                        continue

            page += f"`{item_id}` {item_name} • lvl {item_stats['level']} • {item_stats['power']} ​ • ​ {price}\n"
            count += 1
            if count >= 20:
                pages.append(page)
        if pages == [] or pages[-1] != page:
            pages.append(page)
    embed.description += pages[0]

    disable = True if len(pages) == 1 else False
    await ctx.reply(embed=embed, view=MarketView(ctx.author, pages, disable=disable))

@market.command(name="info", aliases=["i"])
async def market_info(ctx, id):
    with open("market.json", "r") as mf:
        m = json.load(mf)
    if id not in m:
        return await ctx.reply(f"Could not find market item matching id {id}")
    price = m[id]["price"]
    item_name = get_first_key(m[id]["info"])
    item_stats = m[id]["info"][item_name]
    desc = ''
    for stat in list(item_stats.keys())[:-1]:
      desc += f'{stat.upper()}: {item_stats[stat]}'
      if stat == 'xp':
        desc += f'/{levels[get_level(item_stats[stat])+1]}'
      desc += '\n'
  
    slot = qstats.get_item_stats(item_name)['slot']
    embed = discord.Embed(title=f'Market Info: {item_name}', description=f"Price: {price}\n{desc}", colour=get_rarity_colour(qstats.get_item_stats(item)['rarity']))
    item = '_'.join(item.lower().split())
    file = discord.File(fp=f'textures/{slot}/{item}.png', filename=f'{item}.png')
    embed.set_image(url=f"attachment://{item_name}.png")
    embed.set_footer(text=f'Displaying market item {id}')
    await ctx.reply(embed=embed, file=file)

@market.command(name="buy", aliases=["b"])
async def market_buy(ctx, id):
    with open("market.json", "r") as mf:
        m = json.load(mf)
    if id not in m:
        return await ctx.reply(f"Could not find market item matching id {id}")
    
    m_info = m[id]
    if ctx.author.id == m_info["owner"]:
        return await ctx.reply("Cannot purchase your own item")
    
    if m_info["price"] > inventory[str(ctx.author.id)]["balance"]:
        return await ctx.reply("Not enough credits")
    
    item_name = get_first_key(m_info['info'])
    async def buy_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id: return
        await interaction.message.edit(view=None)
        inventory[str(ctx.author.id)]["balance"] -= m_info["price"]
        inventory[str(ctx.author.id)]['items']['id'] += 1
        item_id = str(inventory[str(ctx.author.id)]['items']['id'])
        inventory[str(ctx.author.id)]['items'][item_id] = m_info["info"]
        dump_json("inventory")
        owner = bot.get_user(m_info["owner"])
        del m[id]
        with open("market.json", "w") as mf:
            json.dump(m, mf)
        await interaction.response.send_message(f"Purchased {item_name} at {m_info['price']} credits")
        inventory[str(m_info["owner"])]["balance"] += m_info["price"]
        await owner.send(f"Someone purchased your {item_name} at {m_info['price']} credits")

    view = discord.ui.View()
    buy_button = discord.ui.Button(label="Buy", style=discord.ButtonStyle.red)
    buy_button.callback = buy_callback
    view.add_item(buy_button)
    await ctx.reply(f"Are you sure you want to buy {item_name} for {m_info['price']}?\nThis cannot be reversed.", view=view)


@market.command(name="sell", aliases=["s"])
async def market_sell(ctx, item_id, price):
    if item_id == '0' or item_id == 'l':
        item_id = list(inventory[str(ctx.author.id)]['items'].keys())[-1]
    if item_id not in inventory[str(ctx.author.id)]['items']:
      await ctx.reply("You don't have this item"); return
    if not price.isdigit():
        return await ctx.reply("Invalid price")
    
    item = get_first_key(inventory[str(ctx.author.id)]['items'][item_id])
    item_stats = inventory[str(ctx.author.id)]['items'][item_id]
    async def confirm_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id: return
        await interaction.message.edit(view=None)
        with open("market.json", "r") as mf:
            m = json.load(mf)

        m["latest_id"] += 1
        market_id = m["latest_id"] 
        m[str(market_id)] = {"info": item_stats,
                            "owner": ctx.author.id,
                            "price": int(price)}
        with open("market.json", "w") as mf:
            json.dump(m, mf)
        del inventory[str(ctx.author.id)]["items"][item_id]
        if item_id in inventory[str(ctx.author.id)]["equipped"]["items"]:
            for character in stats[str(ctx.author.id)]:
                for i in item_id:
                    for slot in inventory[str(ctx.author.id)]["equipped"][character]:
                        if inventory[str(ctx.author.id)]["equipped"][character][slot] == i:
                            inventory[str(ctx.author.id)]["equipped"][character][slot] = None
                            calculate_stats(ctx.author, character)
            inventory[str(ctx.author.id)]["equipped"]["items"].remove(item_id)
        dump_json("inventory")
        await interaction.response.send_message(f"Added {item} to the market at {price} credits\nID: {m['latest_id']}")

    view = discord.ui.View()
    confirm_button = discord.ui.Button(label="Confirm", style=discord.ButtonStyle.red)
    confirm_button.callback = confirm_callback
    view.add_item(confirm_button)
    await ctx.reply(f"Are you sure you want to sell {item} at {price} credits?\nThis cannot be reversed.", view=view)

@market.command(name="help", aliases=["h"])
async def market_help(ctx):
    embed = discord.Embed(title="Market help",
                          description=
"""
*Market commands*
r!market (Shows latest market listings)
r!market sell {item_id} {price} (Post an item up for sale)
r!market buy {id} (Buy an item off the market)
r!market help (Shows this message)

*Market filters*
r!market {filter}
Syntax:
={type} {operator} {value}
Examples:
=price > 500
=name == Rookie Sword
=power > 50
=mine
""",
                          colour=discord.Colour.green()
                          )
    await ctx.reply(embed=embed)


class CelestialConvergenceStart(discord.ui.View):
    def __init__(self, author, floor_object):
        super().__init__()
        self.author = author
        self.floor_object = floor_object
    
    @discord.ui.button(label="Start", style=discord.ButtonStyle.blurple)
    async def start_convergence(self, interaction, button):
        await interaction.response.edit_message(view=None)
        team_no = inventory[str(interaction.user.id)]['teams']['selected']
        team = [i for i in inventory[str(interaction.user.id)]['teams'][team_no] if i is not None]
        enemy_waves = []
        for wave in range(1, self.floor_object.waves+1):
            enemy_waves.append(self.floor_object.enemies[f"wave {wave}"])
        battle_result = await battle(interaction, team, enemy_waves, 
                                     user=interaction.user, loot_chest_rarities=self.floor_object.loot_chest_rarities)
        if battle_result == "Won":
            rewards = self.floor_object.rewards
            inventory[str(self.author.id)]["Celestial Convergence"]["completed"].append(self.floor_object.floor)
            dump_json("inventory")
            for item in rewards:
                if item.endswith(' Credits'):
                    inventory[str(interaction.user.id)]['balance'] += int(''.join([i for i in item if i.isdigit()]))

                elif item.endswith(' Universal XP'):
                    for character in stats[str(interaction.user.id)]:
                        stats[str(interaction.user.id)][character]['xp'] += int(''.join([i for i in item if i.isdigit()]))
                        new_level = get_level(stats[str(interaction.user.id)][character]['xp'])
                        if new_level != (level := stats[str(interaction.user.id)][character]['level']):
                            embed = discord.Embed(title=f'{title(character)} levelled up!', description=f'{level} -> {new_level}', color=discord.Color.green())
                            stats[str(interaction.user.id)][character]['level'] = new_level
                            await calculate_stats(interaction.user, character)
                            await interaction.channel.send(embed=embed)
                            await asyncio.sleep(0.6)

                elif item.endswith(' ore'):
                    ore_split = item.split()
                    ore_type = ore_split[1]
                    ore_amount = int(ore_split[0])
                    inventory[str(interaction.user.id)]['ores'][ore_type] += ore_amount

                elif qstats.get_base_stats(item) is not None:
                    await make_character(interaction.user, item.lower())
                    embed = discord.Embed(title=f"{title(item)} has joined your adventure!",
                                          colour=discord.Colour.green())
                    embed.set_image(url=f"attachment://{item.lower()}_sprite.png")
                    sprite = discord.File(fp=f"objects/characters/{item.lower()}_sprite.png")
                    embed.set_footer(text="Use r!view {character} and r!team add {team_no} {character}")
                    await interaction.channel.send(embed=embed, file=sprite)

                else:
                    if qstats.get_item_stats(item) is None:
                        await make_relic(interaction.user, item, level=1)
                    else:
                        await make_item(interaction.user, item, level=math.floor(new_level*1.1))
            
            loot_msg = "\n".join(rewards)
            embed = discord.Embed(title=f'Defeated {self.floor_object.floor}', 
                                  description=f'Loot:\n {loot_msg}')
            await interaction.channel.send(embed=embed)
        else: # Loss
            await interaction.channel.send("You've been defeated, try again next time.")

        dump_json("inventory")

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.author.id


class CelestialConvergenceFloors(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author
        self.add_buttons()
    
    def add_buttons(self):
        def make_function(floor_object):
            async def floor_callback(interaction: discord.Interaction):
                embed = discord.Embed(title=f"Celestial Convergence: {floor_object.floor}",
                                      description="Enemies:")
                for wave in range(1, floor_object.waves+1):
                    enemies = floor_object.enemies[f"wave {wave}"]
                    embed.description += f"\n*Wave {wave}*"
                    for enemy in enemies:
                        level = enemy.stats_dict["level"]
                        name = enemy.name
                        embed.description += f"\n{name} Level {level}"

                selected_team = inventory[str(interaction.user.id)]['teams']['selected']
                img = await show_team_set(selected_team, interaction.user)
                img = img[0]
                embed.set_image(url="attachment://image.png")
                await interaction.response.edit_message(embed=embed, attachments=[img],
                                                        view=CelestialConvergenceStart(interaction.user,
                                                                                       floor_object))
                
            return floor_callback

        floors = qstats.CelestialConvergence().floors
        for i, floor in enumerate(floors):
            if floor().floor in inventory[str(self.author.id)]["Celestial Convergence"]["completed"]:
                style = discord.ButtonStyle.green
                disabled = True
            else:
                style = discord.ButtonStyle.blurple
                if floors[i-1].floor in inventory[str(self.author.id)]["Celestial Convergence"]["completed"] \
                or i == 0:
                    disabled = False
                else:
                    disabled = True
            button = discord.ui.Button(label=floor().floor, 
                                       style=style, 
                                       disabled=disabled)
            button.callback = make_function(floor())
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction):
       return interaction.user.id == self.author.id
            
            
for userid in inventory:
    inventory[userid]["Celestial Convergence"] = {}
    inventory[userid]["Celestial Convergence"]["completed"] = []
with open("inventory.json", "w") as f:
    json.dump(inventory, f)

@bot.group(name="celestial", aliases=["c"])
async def celestial(ctx):
    if str(ctx.author.id) not in inventory:
        return await ctx.reply("Start with `r!start`")
    if ctx.invoked_subcommand is None:
        await convergence(ctx)

@celestial.command(name="convergence", aliases=["c"])
async def convergence(ctx):
    embed = discord.Embed(title="Celestial Convergence",
                          description="Monsters emerged from a deep hole from the centre of the Earth. Their numbers are endless. Defeat them and gain valuable rewards")
    embed.set_image(url="attachment://abyss_castle.png")
    await ctx.reply(embed=embed, view=CelestialConvergenceFloors(ctx.author), file=discord.File(fp="objects/abyss_castle.png"))


# Will put user at checkpoint on restart
async def quests_reset():
    for user_id in quests:
        quest_title = get_started_quest(await bot.fetch_user(int(user_id)))
        if quest_title is None:
            continue
        quests[user_id][quest_title]["step"] = quests[user_id][quest_title]["checkpoint"][0]
        quest_object = qstats.Quest().match_quest(quest_title)
        quests[user_id][quest_title]["task"] = quest_object.tasks[quests[user_id][quest_title]["step"]]
    dump_json("quests")


async def calculate_stats(user, char):
    level = stats[str(user.id)][char]['level']
    xp = stats[str(user.id)][char]['xp']
    stats[str(user.id)][char] = qstats.get_base_stats(char)
    stats[str(user.id)][char]['level'] = level
    stats[str(user.id)][char]['xp'] = xp
    stats[str(user.id)][char]['mana_regen'] = 1
    for slot, item_id in inventory[str(user.id)]['equipped'][char].items():
        if slot == "relics":
            continue
        if item_id:
            item_name = get_first_key(inventory[str(user.id)]['items'][item_id])
            item_stats = inventory[str(user.id)]['items'][item_id][item_name]
            for base_stat, item_stat_name in zip(stats[str(user.id)][char], item_stats):
                if base_stat in {'hp', 'atk', 'def', 'spd'}:
                    base = stats[str(user.id)][char][base_stat]
                    item_stat = item_stats[item_stat_name]
                    stats[str(user.id)][char][base_stat] += (base * level // 50)
                    stats[str(user.id)][char][base_stat] += item_stat
    relic_id = inventory[str(user.id)]["equipped"][char]["relics"]
    if relic_id:
        item_name = get_first_key(inventory[str(user.id)]["items"][relic_id])
        relic_stats = inventory[str(user.id)]["items"][relic_id][item_name]["effect"]
        stats[str(user.id)][char][relic_stats["type"]] *= relic_stats["value"] + 1
    dump_json("stats") # "relics": {"Phoenix Talisman": {"level": 1, "effect": {"type": "mana_regen", "value": 0.2}}}


async def pil_image_to_discord_file(pil_image, filename='image.png'):
    bytes = BytesIO()
    pil_image.save(bytes, 'PNG')
    bytes.seek(0)
    return discord.File(fp=bytes, filename=filename)

def get_dict_key(dictionary, info):
    for i in dictionary.items():
        if info in i:
            return i[0]
    return None

def get_level(xp):
    for level in reversed(levels):
        if xp >= levels[level]:
            return level
    return 1


def get_first_key(d):
  try:
    return list(d.keys())[0]
  except:
    return None

def title(s):
  new_s = ''
  n = True
  for letter in s.lower():
    if n:
      new_s += letter.upper()
      n = False
    else:
      if letter.isspace():
        n = True
      new_s += letter
  return new_s

# To-do
# Quests
    # full test
# Update manual
# relics
  # mana regen, disrupt, battlefield manipulation, def shred, dmg reflection
# market search
# worlds / levels
# endless tower
# tutorials
# Create item augmentation
# Customise profiles
# deplete mana boss

# Warrior, Mage, Warden, Cleric
bot.run('')

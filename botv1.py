import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

players = []


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')


@bot.command()
async def hi(ctx):
    await ctx.send('Testing123')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await menu(ctx)


@bot.command()
async def menu(ctx):
    menu_text = """
    Available Commands:
    !list - List all players.
    !add - Add a list of players.
    !rollmap [game] - Roll a map for the specified game (ow, val, r6).
    !clearplayer - Clears the player list.
    !rollteam - Roll the teams.
    !exit - Stop the bot.
    """
    await ctx.send(menu_text)


@bot.command()
async def list(ctx):
    """Gets a list of player names from the user."""
    await ctx.send(players)


@bot.command()
async def add(ctx, *, player_list):
    new_players = player_list.split(",")
    new_players = [player.strip() for player in new_players]

    players.clear()
    players.extend(new_players)

    await ctx.send(f"Players added: {', '.join(new_players)}")


@bot.command()
async def clearplayer(ctx):
    """Clears the player list."""
    players.clear()
    await ctx.send('Player list cleared.')


@bot.command()
async def rollmap(ctx, game=None):
    """Rolls a random map for the specified game or remembers the game for rerolls."""
    maps = {
        'ow': [
            'Circuit Royal', 'Dorado', 'Route 66', 'Junkertown', 'Rialto', 'Havana', 'Watchpoint: Gibraltar',
            'Shambali Monastery',
            'Blizzard World', 'Numbani', 'Hollywood', 'Eichenwalde', "King's Row", 'Midtown', 'Paraiso',
            'Busan', 'Nepal', 'Ilios', 'Oasis', 'Lijiang Tower', 'Antarctic Peninsula',
            'Colosseo', 'Esperanca', 'New Queen Street'
        ],
        'val': [
            'Bind', 'Haven', 'Split', 'Ascent', 'Icebox', 'Breeze', 'Fracture', 'Pearl', 'Lotus'
        ],
        'r6': [
            'Nighthaven Labs', 'Stadium', 'Close Quarter', 'Emerald Plains', 'Bank', 'Border', 'Chalet',
            'Clubhouse', 'Coastline', 'Consulate',
            'Favela', 'Fortress', 'Hereford Base', 'House', 'Kafe Dostoyevsky', 'Kanal', 'Oregon', 'Outback',
            'Presidential Plane', 'Skyscraper',
            'Theme Park', 'Tower', 'Villa', 'Yacht'
        ]
    }

    if game is None:
        # Check if the game is already stored
        if 'game' in bot.loop.__dict__:
            game = bot.loop.game
        else:
            await ctx.send('Please specify a game.')
            return
    else:
        # Store the game for future rerolls
        bot.loop.game = game

    if game not in maps:
        await ctx.send('Invalid game')
        return

    map_list = maps[game]
    selected_map = random.choice(map_list)
    message = await ctx.send(f'Map: {selected_map}')
    await message.add_reaction('🎲')


@bot.command()
async def rollteam(ctx):
    """Rerolls the teams."""
    # Check if the player list is already stored
    if players:
        player_list = players
    else:
        await ctx.send('Please use the `!add` command to add players before rolling the teams.')
        return

    if len(player_list) < 10:
        await ctx.send('There must be at least 10 players to roll teams.')
        return

    team1 = random.sample(player_list, 5)
    team2 = [player for player in player_list if player not in team1]
    message = await ctx.send(f'Team 1: {team1}\nTeam 2: {team2}')
    await message.add_reaction('🎲')


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if str(reaction.emoji) == "🎲":
        channel = reaction.message.channel

        # Check if the reaction is added to a map message or a team message
        if reaction.message.content.startswith('Map:'):
            await rollmap(channel)
        elif reaction.message.content.startswith('Team 1:'):
            await rollteam(channel)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


bot.run('API CODE')

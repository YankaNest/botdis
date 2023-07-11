import discord
from discord.ext import commands
import random

import config

# Создаем экземпляр клиента Discord
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Событие, которое выполняется при успешном подключении бота к серверу
@bot.event
async def on_ready():
    print(f'Бот подключен к серверу: {bot.user.name}')

# Команда, которая будет вызываться при написании "!hello"
@bot.command()
async def hello(ctx):
    await ctx.send('Привет!')

# Команда, которая будет вызываться при написании "!roll" для броска кубика
@bot.command()
async def roll(ctx):
    rolls = random.randint(1, 6)
    await ctx.send(f'Результаты броска: {rolls}')

#Команда, которая будет вызываться при написании "!info" для показа информации о боте
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Информация о боте", description="helper-bot", color=discord.Color.blue())
    embed.set_author(name="Автор: akumulol")
    embed.add_field(name="Команды:", value="!hello - поздороваться\n!roll - бросить кубик\n!info - показать информацию о боте\n!clear - удалить последние 5 сообщений\n!say - отправить сообщщение отимени бота\n!avatar - показать аватара пользователя\n!kick - исключить пользователя с сервера\n!mute - заглушить пользователя на сервере \n!unmute - снять заглушение пользователя на сервере \n!ban - заблокировать пользователя на сервере \n!unban - снять блокировку пользователя на сервере", inline=False)
    await ctx.send(embed=embed)

#Команда, которая будет вызываться при написании "!clear" для удаления сообщений
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'{amount} сообщений было удалено.')
    
# Команда, которая будет вызываться при написании "!say" для отправки сообщения от имени бота
@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

# Команда, которая будет вызываться при написании "!avatar" для показа аватара пользователя
@bot.command()
async def avatar(ctx, member:discord.Member):
    await ctx.send(member.avatar)
        
# Команда, которая будет вызываться при написании "!kick" для исключения пользователя с сервера
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} был исключен с сервера.')

# Команда, которая будет вызываться при написании "!ban" для блокировки пользователя на сервере
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} был забанен на сервере.')

# Команда, которая будет вызываться при написании "!unban" для снятия блокировки с пользователя на сервере
@bot.command()
async def unban(ctx, userId):
    user = discord.Object(id=userId)
    await ctx.guild.unban(user) 
    await ctx.send('Пользователь был разабанен на сервере.')

# Команда, которая будет вызываться при написании "!mute" для заглушения пользователя на сервере
@bot.command()
async def mute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.add_roles(muted_role)
    await ctx.send(f'{member.mention} был заглушен на сервере.')

# Команда, которая будет вызываться при написании "!unmute" для снятия заглушения с пользователя на сервере
@bot.command()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(muted_role)
    await ctx.send(f'{member.mention} больше не заглушен на сервере.')

# Событие, которое выполняется при неправильно написанной команде и передаёт в чат информацио об этом  
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, команда не найдена!', colour = discord.Color.red()))

# Запускаем бота с помощью токена
bot.run(config.TOKEN)


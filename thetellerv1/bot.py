import os
import time
import random
import discord
from discord.ext import commands

from deathroll import deathroll
from myconfig import DISCORD_TOKEN
import sqlbank 

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = 'b!', intents=intents)



BOT_ADMIN_ID = "MY_DISCORD_ID"

@bot.event
async def on_ready():
    print("We online boys")
    await bot.change_presence(activity=discord.Game(name="b!info for help"))


@bot.command(name='info')
async def info(ctx):

    response = "b!ratcopter: fuck around and find out \n\
b!dr @user#0000 ($____): starts deathroll.\
Person who is challenged type the same command to accept \n\
b!league: selects random league champ \n\
b!balance: displays your balance. If you dont have a balance one will be given to you courtesy of the family \n\
b!info: you're already here"

    await ctx.send(response)

@bot.command(name='ratcopter')
async def ratcopter(ctx):
    
    response = ('https://cdn.discordapp.com/attachments/692467048705687666/700811597479936090/received_231826514605682.gif')
    
    
    await ctx.send(response)

@bot.command(name='dr') 
async def drcommand(ctx, member: discord.Member, wager): 
    

    rolls = deathroll(100)
    #to future me: make it so challengee doesnt have to do wager
    outstanding = sqlbank.check_outstanding(ctx.author.id, member.id)
    if outstanding:
        await ctx.send("Hold your horses buddy. We're not gonna let you gamble two people at once.")
        return
    outstanding = False
    
    #Now check if acceptance
    
    outstanding = sqlbank.check_outstanding(member.id, ctx.author.id)
    
    if outstanding:
        for idx,value in enumerate(rolls):    
            if idx %2:
                player = bot.get_user(outstanding.challengee_id)
            else:
                player = bot.get_user(outstanding.challenger_id)
            response = "%s rolls the dice with a mighty throw and comes up with %d!!! \n" %(player.display_name,value)
            await ctx.send(response)
            time.sleep(0.7)
            loser = player
            if player.id == outstanding.challenger_id:
                winner = bot.get_user(outstanding.challengee_id)
            else:
                winner = bot.get_user(outstanding.challenger_id)

        sqlbank.withdrawl(loser.id, outstanding.wager)
        sqlbank.deposit(winner.id, outstanding.wager)
        await ctx.send("Congratulations %s, you just earned %d dollars!! Tough luck %s, I hope it was worth your not so hard earned cash." %(winner.display_name, outstanding.wager, loser.display_name))

    else:
        sqlbank.create_challenge(ctx.author.id, member.id, int(wager))
        #withdrawl wager here
        await ctx.send("Your challenge has been recorded, now we wait for %s to accept (if they're not a coward)" %(member))


    #is this an acceptance
    #result = check_outstanding ctx.author/member
    #if outstanding: commence roll
    #else: log new challenge
    

@bot.command(name='balance')
async def balancecommand(ctx, member: discord.Member):
    


    if ctx.author.id != member.id and ctx.author.id != BOT_ADMIN_ID:
        await ctx.send("This is not permitted. This action will be reported!!")
        return
    p = sqlbank.patron_exists(member.id)
    if not p:
        
        p = sqlbank.create_patron(member.id)
        await ctx.send("Welcome %s to Aperture experimental banking system. \
You are test subject number %d. On behalf of a grateful nation we \
thank you for participating in capitalism. As with all new valued \
test subjects, we have taken the liberty of rolling a 1337 sided \
dice to determine your initial balance. \nCongratulations! your \
starting balance is $%d" %(member.display_name, p.id, p.balance))
    else:
        await ctx.send("We are aware you have no other options in discord \
banking services thus it is difficult to say we really appreciate \
your service, so whatever. \nYour current balance is $%d" %(p.balance))
    
@bot.event
async def on_member_join(member: discord.Member):
    await member.send("Welcome to the LEAGUE OF DRAVEN!")


#query user from database
#if not exist, create new object/commit it
#Welcome member to Aperture experimental banking system. You are test subject number p.id. On behalf of a grateful nation we thank you for participating in capitalism.
#if new: roll dice for initial balance 
#say: warning to all test subjects. all attempts to sieze the means will be dealt with swiftly and immediately


@bot.command(name='league')
async def champs(message):
    if message.author == bot.user:
        return

    champs = ["Aatrox","Ahri","Akali","Alistar","Amumu","Anivia","Annie","Aphelios","Ashe","Aurelion Sol","Azir","Bard","Blitzcrank","Brand","Braum","Caitlyn","Camille","Cassiopeia","Cho'Gath","Corki","Darius","Diana","Dr. Mundo","Draven","Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora","Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Hecarim","Heimerdinger","Illaoi","Irelia","Ivern","Janna","Jarvan IV","Jax","Jayce","Jhin","Jinx","Kai'Sa","Kalista","Karma","Karthus","Kassadin","Katarina","Kayle","Kayn","Kennen","Kha'Zix","Kindred","Kled","Kog'Maw","LeBlanc","Lee Sin","Leona","Lillia","Lissandra","Lucian","Lulu","Lux","Malphite","Malzahar","Maokai","Master Yi","Miss Fortune","Mordekaiser","Morgana","Nami","Nasus","Nautilus","Neeko","Nidalee","Nocturne","Nunu and Willump","Olaf","Orianna","Ornn","Pantheon","Poppy","Pyke","Qiyana","Quinn","Rakan","Rammus","Rek'Sai","Renekton","Rengar","Riven","Rumble","Ryze","Samira","Sejuani","Senna","Seraphine","Sett","Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner","Sona","Soraka","Swain","Sylas","Syndra","Tahm Kench","Taliyah","Talon","Taric","Teemo","Thresh","Tristana","Trundle","Tryndamere","Twisted Fate","Twitch","Udyr","Urgot","Varus","Vayne","Veigar","Vel'Koz","Vi","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah","Xerath","Xin Zhao","Yasuo","Yone","Yorick","Yuumi","Zac","Zed","Ziggs","Zilean","Zoe","Zyra"]
    response = random.choice(champs)
    await message.send(response)



bot.run(DISCORD_TOKEN)
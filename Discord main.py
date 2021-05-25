import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words=["sad","depressed","stressed","frustrated","tired","annoying"]
starter_encouragements=["cheer up!", "you are the best!","I'll always be there for you, my friend","Don't worry, you'll be successful one day"]

if "responding" not in db.keys():
  db["responding"] = True

def inspiring_quotes():
  response= requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote= json_data[0]['q']+" -"+ json_data[0]['a']
  return quote

def  update_encouragements(encouraging_msg):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_msg)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_msg]

def delete_encouragements(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')  

  if message.content.startswith('$inspire'):
    quote=inspiring_quotes()
    await message.channel.send(quote)  
  if db["responding"]:

    options = starter_encouragements
    if "encouragements" in db.keys():
      #options = options + db["encouragements"]
      options.extend(db["encouragements"])

    if any( word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  if message.content.startswith('$new '):
    new_quote = message.content.split("$new ",1)[1]
    update_encouragements(new_quote)
    await message.channel.send("New quote added!")

  if message.content.startswith('$del'):
    encouragements=[]
    if "encouragements" in db.keys():
      index = int (message.content.split('$del ',1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)      

  if message.content.startswith('$list'):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)

  if message.content.startswith('$responding'):
    value = message.content.split('$responding ',1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

my_secret = os.environ['code']

keep_alive()
client.run(my_secret)


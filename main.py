import discord
import smtplib, ssl
import random
import re
import os
import asyncio
from keep_alive import keep_alive
#token_file = eval(open("creds.json","r").read())


token=os.environ['TOKEN']
email=os.environ['email']
passwd=os.environ['pass']
client=discord.Client()

hexed=0

mentor_data=eval(open("mentor_data.data","r").read())
mentor_list=list(mentor_data.keys())
mentee_list=list(mentor_data.values())

pattern='''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''


def send_email(email_id):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = email  
    receiver_email = email_id 
    password = passwd
    otp=str(random.SystemRandom().randint(100000,999999))
    body=otp+" is your otp for GDSC Discord Server Verification."

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, body)
    return otp

@client.event
async def on_ready():
  print("Ready Steady po")
  await client.change_presence(activity=discord.Game(name="  ::verify <email_id>"))

@client.event
async def on_message(message):
    if message.author == client.user:
      return
    elif message.content.startswith('::verify'):
        error_hand=0
        channel = message.channel
        tempmail=message.content.split(" ")[1].strip().lower()
        if bool(re.match(pattern,tempmail)):
            for i in range(0,len(mentor_list)):
                if tempmail in mentee_list[i]:
                    role=mentor_list[i]
                    veriins = await channel.send('Check your inbox for verification code and type the code here')
                    rec_otp=send_email(message.content.split(" ")[1])
                    def check(m):
                        return m.author == message.author and m.channel == channel and m.content==rec_otp
                    try:
                        received_otp = await client.wait_for('message',timeout=120, check=check)
                        
                        await received_otp.delete()
                        hexed = await channel.send('* * * * * *')
                        ver_conf=await channel.send('Verified')
                        var=discord.utils.get(message.guild.roles,name=role)
                        member=message.author
                        await member.add_roles(var)
                        await message.delete()
                        await veriins.delete()
                        await asyncio.sleep(2)
                        await hexed.delete()
                        await ver_conf.delete()
                        error_hand=1
                        break
                    except:
                        error_hand=1
                        errps=await channel.send("Request Timed Out, Try Again!")
                        await asyncio.sleep(4)
                        await errps.delete()
                        await message.delete()
                        await veriins.delete()
            if error_hand!=1:
                not_reg=await channel.send('Email ID Not Registered, Please Contact a Core Member')
                await message.delete()
                await asyncio.sleep(5)
                await not_reg.delete()

            
        else:
            await channel.send("Enter Valid Email ID")
    elif re.match("^[0-9]{1,6}$",message.content):
        print()

    else:
      bif_err=await message.channel.send("```Incorrect Command Please enter details in format ::verify your_email_id```")
      await asyncio.sleep(7)
      await bif_err.delete()
      await message.delete()

keep_alive()
client.run(token)
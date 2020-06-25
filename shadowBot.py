import discord
import msgClass
import re, os
from collections import defaultdict
from dotenv import load_dotenv

listDict = defaultdict(list)
dumpThreshold = 250
listenChannels = ["general-unique", "channel-dva",
                    "border-village", "border-village-votes",
                    "farming-village", "farming-village-votes"]
masterName = "master"
forceCommand ="#push"
ownerName = "Ravenshard"
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        return

    async def on_message(self, message):
        if message.channel.name in listenChannels and message.content == forceCommand and message.author.name == ownerName:
            msgSent(message)
            forceLog()
        if message.channel.name in listenChannels:
            msgSent(message)
        return

    async def on_message_edit(self, before, after):
        if after.channel.name in listenChannels:
            msgSent(after)
        return

    # async def on_message_delete(self, message):
    #     if message.channel.name == "general":
    #         chnlid = message.channel.id
    #         channel = self.get_channel(chnlid)
    #         text = re.sub('\n', '\n > ', message.content)
    #         text = "Deleting messages is ilegal! Here's the message from {}:\n > {}".format(
    #                 message.author, text)
    #         await channel.send(text)
    #     return

    async def on_disconnect(self):
        print("We're logging off now")
        return

def forceLog():
    for name, msgs in listDict.items():
        dumpList(name, msgs)
        listDict[name] = list()
    return

def msgSent(message):
    mcn = "{}-{}".format(message.channel.name, masterName)
    pcn = "{}-{}".format(message.channel.name, message.author.name)
    listDict[mcn].append(msgClass.msg(message))
    listDict[pcn].append(msgClass.msg(message))
    if len(listDict[mcn]) >= dumpThreshold:
        dumpList(mcn, listDict[mcn])
        listDict[mcn] = list()
    if len(listDict[pcn]) >= dumpThreshold:
        dumpList(pcn, listDict[pcn])
        listDict[pcn] = list()
    return

def dumpList(name, msgs):
    logpath = "./logs/{}".format(name)
    if not os.path.exists(logpath):  os.mkdir(logpath)
    dirlist = os.listdir(logpath)

    if len(dirlist) > 0: num = format(int(max(dirlist)[-7:-4]) + 1, '03d')
    else: num = '000'

    fileObj = open("{}/{}Log{}.tsv".format(logpath, name, num), 'w')
    fileObj.write("Author\tId\tContent\tCreated_at\tEdited_at\tMentions\n")
    for item in msgs:
        content = re.sub('\n', ' |newline| ', item.getContent())
        content = re.sub('\t', ' |tab| ', content)
        mentions = ""
        for person in item.getMentions(): mentions = "{},{}".format(mentions,person)
        fileObj.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
            item.getAuthor(), item.getId(), content,
            item.getCreated_at(), item.getEdited_at(), mentions ))
    fileObj.close()

    return


def finalExc():
    for name, msgs in listDict.items():
        dumpList(name, msgs)
    return

def main():
    try:
        load_dotenv()
        TOKEN = os.getenv('DISCORD_TOKEN')
        client = MyClient()
        client.run(TOKEN)
        finalExc()
    except Exception as e:
        finalExc()

if __name__ == '__main__':
    main()

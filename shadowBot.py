import discord
import msgClass
import re, os
from collections import defaultdict
from dotenv import load_dotenv

listDict = defaultdict(list)
filePathDict = dict()
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

def scrubContent(content):
    content = re.sub('\n', ' |nl| ', content)
    content = re.sub('\t', ' |tab| ', content)
    content = re.sub(' ww ', ' werewolf ', content)
    content = re.sub(' wws ', ' werewolves ', content)
    content = re.sub(":werewolf:", "werewolf", content)
    content = re.sub(":sacrifice:", "sacrifice", content)
    content = re.sub(" sac ", " sacrifice ", content)
    return content

def writeRow(item, file):
    fileObj = open(filePathDict(file), 'a')
    mentions = ""
    for person in item.mentions: mentions = "{},{}".format(mentions,person)
    fileObj.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
        item.author.name, item.id, scrubContent(item.content),
        item.created_at, item.edited_at, mentions ))
    fileObj.close()
    return

def createPath(logpath, name, fileType=None):
    logpath = "{}/{}".format(logpath, name)
    if not os.path.exists(logpath):
        print("making dir {}".format(logpath))
        os.mkdir(logpath)
    if fileType is None: return logpath

    dirlist = os.listdir(logpath)
    if len(dirlist) > 0: num = format(int(max(dirlist)[-7:-4]) + 1, '03d')
    else: num = '000'
    return "{}/{}log{}.{}".format(logpath, name, num, fileType)


def checkPaths(guild, channel, filename):
    logpath = createPath(".", "log_test")
    logpath = createPath(logpath, guild)
    logpath = createPath(logpath, channel)
    masterFile = createPath(logpath, filename, fileType="tsv")
    return masterFile

def initTsv(message, dictKey):
    filePathDict[mcn] = checkPaths(message.guild.name, message.channel.name, "master")
    fileObj = open(filePathDict[mcn], 'a')
    fileObj.write("Author\tId\tContent\tCreated_at\tEdited_at\tMentions\n")
    fileObj.close()
    return

def msgSent(message):
    mcn = "{}-{}".format(message.channel.name, masterName)
    pcn = "{}-{}".format(message.channel.name, message.author.name)
    if mcn not in filePathDict.keys(): initTsv(message, mcn)
    if pcn not in filePathDict.keys(): initTsv(message, pcn)
    writeRow(message, mcn)
    writeRow(message, pcn)
    return

def main():
    try:
        load_dotenv()
        TOKEN = os.getenv('DISCORD_TOKEN')
        client = MyClient()
        client.run(TOKEN)

if __name__ == '__main__':
    main()

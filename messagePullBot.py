import discord
import msgClass
import re, os, sys
from collections import defaultdict
from datetime import datetime
from dotenv import load_dotenv

listDict = defaultdict(list)
listenChannels = ["general-unique", "channel-dva",
                    "border-village", "border-village-votes",
                    "farming-village", "farming-village-votes"]
masterName = "master"
listenGuilds = ["Dominion (Card Game)"]
dtDict = {"border-village": datetime(2020,6,23,hour=14,minute=37),
            "border-village-votes": datetime(2020,6,23,hour=14,minute=37),
            "farming-village": datetime(2020, 7, 4, hour=15, minute=34),
            "farming-village-votes" : datetime(2020, 7, 4, hour=15, minute=34)}
msgLimit = 49999

class MyClient(discord.Client):


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        for guild in self.guilds:
            if guild.name in listenGuilds:
                for channel in guild.channels:
                    if channel.name in listenChannels:
                        messages = await channel.history(limit=msgLimit,after=dtDict[channel.name]).flatten()
                        exportMessages(guild, channel, messages)
        exit()
        return

    async def on_disconnect(self):
        print("We're logging off now")
        return


def createPath(logpath, name, fileType=None):
    logpath = "{}/{}".format(logpath, name)
    if not os.path.exists(logpath):
        print("making dir {}".format(logpath))
        # print("fileType is {}".format(fileType))
        os.mkdir(logpath)
    dirlist = os.listdir(logpath)

    if fileType is None:
        return logpath

    if len(dirlist) > 0: num = format(int(max(dirlist)[-7:-4]) + 1, '03d')
    else: num = '000'
    return "{}/{}log{}.{}".format(logpath, name, num, fileType)


def scrubContent(content):
    content = re.sub('\n', ' |newline| ', content)
    content = re.sub('\t', ' |tab| ', content)
    content = re.sub(' ww ', ' werewolf ', content)
    content = re.sub(' wws ', ' werewolves ', content)
    content = re.sub(":werewolf:", "werewolf", content)
    content = re.sub(":sacrifice:", "sacrifice", content)
    content = re.sub(" sac ", " sacrifice ", content)
    return content


def writeFile(file, msgs):
    authorSet = set()
    fileObj = open(file, 'w')
    fileObj.write("Author\tId\tContent\tCreated_at\tEdited_at\tMentions\n")
    for item in msgs:
        authorSet.add(item.author.name)
        mentions = ""
        for person in item.mentions: mentions = "{},{}".format(mentions,person)
        fileObj.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
            item.author.name, item.id, scrubContent(item.content),
            item.created_at, item.edited_at, mentions ))
    fileObj.close()
    return authorSet


def writeMultiFile(authors, msgs, logpath):

    fileObjDict = dict()
    for author in authors:
        fileObjDict[author] = open(createPath(logpath, author, fileType="tsv"), 'w')
        fileObjDict[author].write("Author\tId\tContent\tCreated_at\tEdited_at\tMentions\n")

    for item in msgs:
        mentions = ""
        for person in item.mentions: mentions = "{},{}".format(mentions,person)
        fileObjDict[item.author.name].write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
            item.author.name, item.id, scrubContent(item.content),
            item.created_at, item.edited_at, mentions ))
    for fileObj in fileObjDict.values():
        fileObj.close()
    return


def exportMessages(guild, channel, msgList):
    logpath = createPath(".", "log")
    logpath = createPath(logpath, guild)
    logpath = createPath(logpath, channel)
    masterFile = createPath(logpath, masterName, fileType="tsv")
    authorSet = writeFile(masterFile, msgList)
    writeMultiFile(authorSet, msgList, logpath)
    print("done export")
    return


def exit():
    sys.exit()


def args():
    if len(sys.argv) < 3: return
    global listenChannels, listenGuilds, dt
    for flag, val in zip(sys.argv[1::2], sys.argv[2::2]):
        if flag == "-g": listenGuilds.append(val)
        elif flag == "-c": listenChannels.append(val)
        elif flag == "-go": listenGuilds = [val]
        elif flag == "-co": listenChannels = [val]
        elif flag == "-dt": dt = datetime.strptime(val, '%Y/%m/%d-%H:%M:%S')
        elif flag == "-l": msgLimit = val
    return


def main():
    args()
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = MyClient()
    client.run(TOKEN)
    return


if __name__ == '__main__':
    main()

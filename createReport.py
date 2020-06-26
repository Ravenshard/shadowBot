import os, glob, sys
import pandas as pd
import numpy as np

path = "./log/Dominion (Card Game)/border-village"
reportFolder = "./reports"
reportName = "msgCharStats.csv"

def initWrite(fileName, header, reportFolder, mode='w'):
    fileObj = open("{}/{}".format(reportFolder, fileName), mode)
    fileObj.write("{}\n".format(header))
    return fileObj

def createReport(path, reportName, reportFolder):
    header = "Name,Messages,Chars,Char per Msg"
    fileObj = initWrite(reportName, header, reportFolder)
    for folder in sorted(os.listdir(path)):
        dirs = glob.glob("{}/{}/*".format(path, folder))
        file = max(dirs)
        df = pd.read_csv(file, delimiter="\t")
        ms = len(df["Content"])
        cc = 0
        for x in df["Content"]: cc += len(str(x))
        fileObj.write("{},{},{},{}\n".format(folder,ms,cc,cc/ms))
        # print("File: {}".format(folder))
        # print("Messages: {}".format(messagesSent))
        # print("Chars Sent: {}".format(charCount))
        # print("Char per Message: {}\n".format(charCount/messagesSent))
    fileObj.close()
    return

def args():
    if len(sys.argv) < 3: return
    global path, reportName, reportFolder
    for flag, val in zip(sys.argv[1::2], sys.argv[2::2]):
        if flag == "-p": path = val
        elif flag == "-r": reportName = val
        elif flag == "-f": reportFolder =val
    return

def main():
    args()
    createReport(path, reportName, reportFolder)
    return


if __name__ == '__main__':
    main()

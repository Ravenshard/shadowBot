import os, glob, sys
import pandas as pd
import numpy as np

paths = ["./log/Dominion (Card Game)/border-village", "./log/Dominion (Card Game)/farming-village"]
reportFolder = "./reports"
reportName = "msgCharStats"

def initWrite(fileName, header, reportFolder, number, mode='w', fileExtension =".csv"):
    fileObj = open("{}/{}{}{}".format(reportFolder, fileName, number, fileExtension), mode)
    fileObj.write("{}\n".format(header))
    return fileObj

def createReport(paths, reportName, reportFolder):
    header = "Name,Messages,Chars,Char per Msg"
    for path in paths:
        base,log,guild,channel = path.split("/")
        folders = sorted(os.listdir(path))
        number = max(glob.glob("{}/{}/*".format(path, folders[0])))[-7:-4]
        fileObj = initWrite("{}-{}".format(channel,reportName), header, reportFolder, number)
        for folder in sorted(os.listdir(path)):
            dirs = glob.glob("{}/{}/*".format(path, folder))
            file = max(dirs)
            df = pd.read_csv(file, delimiter="\t")
            ms = len(df["Content"])
            cc = 0
            for x in df["Content"]: cc += len(str(x))
            fileObj.write("{},{},{},{}\n".format(folder,ms,cc,cc/ms))
        fileObj.close()
    return

def args():
    if len(sys.argv) < 3: return
    global paths, reportName, reportFolder
    for flag, val in zip(sys.argv[1::2], sys.argv[2::2]):
        if flag == "-po": paths = [val]
        elif flag == "-p": paths.append(val)
        elif flag == "-pi": paths = [paths[int(val)]]
        elif flag == "-r": reportName = val
        elif flag == "-f": reportFolder =val
    return

def main():
    args()
    createReport(paths, reportName, reportFolder)
    return


if __name__ == '__main__':
    main()

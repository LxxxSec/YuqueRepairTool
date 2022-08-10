import os
import re
import argparse
import logging
import sys
import requests
import uuid

# 下载图片
# 返回文件名
def downloadFile(url):
    fileName = "./images/{}.png".format(uuid.uuid4())
    with open(fileName, "wb+") as f:
        f.write(requests.get(url).content)
    return fileName

# 将图片保存至本地，便于typora批量上传本地图片至图床
# 返回新文件内容
def save2Local(fileContent):
    outFileContent = []
    for line in fileContent:
        url = re.findall(
            r'http[s]?://cdn.nlark.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            line)
        if url:
            if not os.path.exists("./images"):
                os.mkdir("./images")
            lineContent = "![image.png]({})".format(downloadFile(url[0]))
            outFileContent.append(lineContent)
        else:
            outFileContent.append(line)
    return outFileContent

# 去除链接最后的锚点，用于typora
# 返回新文件内容
def replaceUrl(fileContent):
    outFileContent = []
    for line in fileContent:
        url = re.findall(
            r'http[s]?://cdn.nlark.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            line)
        if url:
            lineContent = "![image.png]({})".format(url[0])
            outFileContent.append(lineContent)
        else:
            outFileContent.append(line)
    return outFileContent

# 读取原始文件
# 返回原始文件内容
def readFile(filename):
    fileContent = []
    with open(filename, "r") as f:
        for line in f.read().splitlines():
            fileContent.append(line)
    return fileContent

# 写入文件
def writeFile(newFilename, outFileContent):
    f = open(newFilename, "w")
    for line in outFileContent:
        f.write(line + "\n")

# 修复程序
def fixYuqueDoc(filename, newFilename, isSave2Local):
    if isSave2Local:
        writeFile(newFilename, save2Local(readFile(filename)))
    else:
        writeFile(newFilename, replaceUrl(readFile(filename)))

# 主程序
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="待处理文件名，eg: test.md", type=str)
    parser.add_argument("-o", "--output", help="输出文件名，eg: new_test.md，缺省则命名为new_test.md", type=str)
    parser.add_argument("-s", "--save2local", help="是否将图片保存至本地，eg: 0，缺省则默认为0不保存，1为保存", type=int)
    parser.add_argument("-a", "--all", help="是否使用全处理模式，eg: 1，缺省则默认为0，不采用全处理模式", type=int)
    args = parser.parse_args()
    if not args.filename:
        logging.critical("请输入文件名")
        sys.exit()
    if not args.output:
        args.output = "new_" + args.filename
    if not args.save2local:
        args.save2local = 0
    if args.all != 1:
        args.all = 0
    if args.all == 1:
        filename = os.path.splitext(args.filename)[0] + "（语雀远程图片版）" + os.path.splitext(args.filename)[1]
        fixYuqueDoc(args.filename, filename, False)
        filename = os.path.splitext(args.filename)[0] + "（本地版）" + os.path.splitext(args.filename)[1]
        fixYuqueDoc(args.filename, filename, True)
    else:
        if args.save2local == 0:
            fixYuqueDoc(args.filename, args.output, False)
        else:
            fixYuqueDoc(args.filename, args.output, True)
    print("文档已修复完成！")

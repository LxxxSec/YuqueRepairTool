import os
import re
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
            filename = downloadFile(url[0])
            lineContent = re.sub(r'!\[image\.png\]\((.*?)\)', f"\n\n![image.png]({filename})\n\n", line)
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
            lineContent = re.sub(r'!\[image\.png\]\((.*?)\)', f"\n\n![image.png]({url[0]})\n\n", line)
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
    args = sys.argv
    if len(args) != 2:
        print("[+] usage: python3 {} filename.md".format(args[0]))
        sys.exit(1)
    filename = os.path.splitext(args[1])[0] + "（语雀远程图片版）" + os.path.splitext(args[1])[1]
    fixYuqueDoc(args[1], filename, False)
    filename = os.path.splitext(args[1])[0] + "（本地版）" + os.path.splitext(args[1])[1]
    fixYuqueDoc(args[1], filename, True)
    print("文档已修复完成！")

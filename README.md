# 语雀修复工具

## 背景

由于语雀一些历史遗留问题，导致在语雀导出的Markdown文件无法正常解析图片，因此制作了该修复工具



## 工具效果

### 使用前

![image-20220807142549801](https://lxxx-markdown.oss-cn-beijing.aliyuncs.com/pictures/202208071425901.png)

### 使用后

![image-20220807142752444](https://lxxx-markdown.oss-cn-beijing.aliyuncs.com/pictures/202208071427486.png)

## 使用方法

### 参数介绍

```
python3 YuqueRepairTool.py -h

usage: YuqueRepairTool.py [-h] [-f FILENAME] [-o OUTPUT] [-s SAVE2LOCAL] [-a ALL]

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        待处理文件名，eg: test.md
  -o OUTPUT, --output OUTPUT
                        输出文件名，eg: new_test.md，缺省则命名为new_test.md
  -s SAVE2LOCAL, --save2local SAVE2LOCAL
                        是否将图片保存至本地，eg: 0，缺省则默认为0不保存，1为保存
  -a ALL, --all ALL     是否使用全处理模式，eg: 1，缺省则默认为0，不采用全处理模式
```

### 远程图片

仍使用语雀自带的图床，删除URL后锚点

```
python3 YuqueRepairTool.py -f test.md -o new_test.md -s 0
```

### 本地图片

将语雀的图片下载至本地images文件夹内

```
python3 YuqueRepairTool.py -f test.md -o new_test.md -s 1
```

### 全处理模式
推荐使用，自动下载图片至本地，生成两份文件，一份本地版，一份语雀远程图片版
```
python3 YuqueRepairTool.py -f test.md -a 1
```

## TODO

- 想办法让这个脚本更聪明

## DONE

- 使用uuid4随机生成图片文件名
- 增加全处理模式


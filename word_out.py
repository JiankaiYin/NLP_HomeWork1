import jieba
import os

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('chinesestop_word.txt',encoding="UTF-8").readlines()]
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

# 给出文档路径
path = "G:\\bad_weather\\entropy\\data\\"
out = "G:\\bad_weather\\entropy\\new_data\\"
filenames = os.listdir(path)
for filename in filenames:
    print(filename)
    outfilename = out + filename.replace(".txt","")+"_out.txt"
    filename = path + filename
    inputs = open(filename, 'r', encoding="GB18030")
    outputs = open(outfilename, 'a', encoding="GB18030")

    # 将输出结果写入ou.txt中
    for line in inputs:
        line_seg = seg_depart(line)
        outputs.write(line_seg + '\n')
        # print("-------------------正在分词和去停用词-----------")
    outputs.close()
    inputs.close()
    print("删除停用词和分词成功！！！")
#
# 数据清洗
# 标点符号只保留点号：句号（ 。）、问号（ ？）、感叹号（ ！）、逗号（ ，）顿号（、）、分号（；）和冒号（：）
#
import os  
import re
import xlrd
import xlsxwriter

Quezi="一二三四五六七八九十〇"
# 自有模型训练，处理规则
# ReplaceBox1=['<p>','<juan>','<pin>','<sec>','<#sp>']
# 在线模型训练，处理规则
ReplaceBox1=['<juan>','<pin>','<#sp>','&#;']
# ReplaceBox2=['〈（闕一字）〉','〈（闕二字）〉','〈（闕三字）〉','〈（闕四字）〉','〈（闕五字）〉','〈（闕六字）〉','〈（闕七字）〉','〈（闕八字）〉','〈（闕九字）〉','〈（闕十字）〉','〈（闕十一字）〉','〈（闕十二字）〉','〈（闕十三字）〉','〈（闕十四字）〉','〈（闕十五字）〉','〈（闕十六字）〉','〈（闕十七字）〉','〈（闕十八字）〉','〈（闕十九字）〉','〈（闕二十字）〉','〈（闕二十一字）〉','〈（闕二十二字）〉','〈（闕二十三字）〉','〈（闕二十四字）〉','〈（闕二十五字）〉','〈（闕二十六字）〉','（闕）']
# ReplaceBox3=['（闕一字）','（闕二字）','（闕三字）','（闕四字）','（闕五字）','（闕六字）','（闕七字）','（闕八字）','（闕九字）','（闕十字）','（闕十一字）','（闕十二字）','（闕十三字）','（闕十四字）','（闕十五字）','（闕十六字）','（闕十七字）','（闕十八字）','（闕十九字）','（闕二十字）','（闕二十一字）','（闕二十二字）','（闕二十三字）','（闕二十四字）','（闕二十五字）','（闕二十六字）','（闕）']
punctuation=['。','，','、','：','；','！','？']

cutlist='.?!＂“”‘’＃＄％＆＇＊＋－／<>＜＝＞＠［＼］/○●❥⚏＾＿｀｛｜｝～｟｠【】『』「」｢｣､〃《》〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‛„‟…‧﹏'
six_punt="（）"
string_set='abcdefghijklmnopkrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
number_set='0123456789'
Sanskrit=['a','A','Ā','ā','i','ī','I','Ī','U','Ū','Ṛ','Ṝ','Ḷ','Ḹ','E','Ai','O','Au','Ṃ','Ḥ','ḥ','ṃ','au','o','ai','e','ḹ','ḷ','ṝ','ṛ','ū','u','c','C','k','K','ṭ','Ṭ','t','T','p','P','ph','Ph','ḍ','Ḍ','ṇ','Ṇ','ñ','Ñ','ṅ','Ṅ','ś','Ś','ṣ','Ṣ']
tripitakalist=["藏经类别","子类","经论名称","卷号"]

# 源数据文件夹
file_dir="/home/z/Date0816"
workbook = xlsxwriter.Workbook('藏经-规范处理.xls')
worksheet = workbook.add_worksheet()
#合并重写到一个文件
#fp = open('tripitaka_np.text','w')

tripitakaTpye=[]

row = 0
col = 0

for temp in tripitakalist:
    worksheet.write(row, col, temp)
    col += 1

col = 0
row = 1


for root, dirs, files in os.walk(file_dir):

    for file_temp in sorted(files):

        if file_temp == "Readme.txt":
            pass
        else:
            #源数据路径
            source_path = root+'/'+file_temp
            #重写生成的数据文件路径
            filedir = source_path.replace(file_dir, file_dir+'-out')
            if filedir.find('/') != -1:
                target_path = filedir[0:filedir.rfind("/")]
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            fp = open(filedir, "w+", encoding='utf-8')

            FileData = open(source_path, 'r', encoding='utf-8')
            FileTilte=(FileData.name).split('/')

            for i in range(3,len(FileTilte)):
                worksheet.write(row, col+i-4, FileTilte[i])                
            lines = FileData.read()#读取全部内容
            print("1")
            #while lines:
            context=''.join(lines) 

            
            # 去除大括号“{ }”、中括号“[ ]”、小括号“（ ）”、六角括号“〔〕”、尖括号“〈〉”和方头括号“【】”及其所包含的内容。
            context = re.sub(r'（.+?）', '（', context) 
            context = re.sub(r'（.+?）', '（', context) 
            context = re.sub(r'\(.+?\)', '(', context)
            context = re.sub(r'\(.+?\)', '(', context)
            context = re.sub(r'{.+?}', '{', context)
            context = re.sub(r'{.+?}', '{', context)
            context = re.sub(r'\[.+?\]', '[', context)
            context = re.sub(r'\[.+?\]', '[', context)
            context = re.sub(r'〔.+?〕', '〔', context)
            context = re.sub(r'〔.+?〕', '〔', context)
            context = re.sub(r'【.+?】', '【', context)
            context = re.sub(r'【.+?】', '【', context)
            context = re.sub(r'〈.+?〉', '〈', context)
            context = re.sub(r'〈.+?〉', '〈', context)

            context = context.replace('（','').replace('(','').replace('{','').replace('[','').replace('〔','').replace('【','').replace('〈','').replace(')','').replace('）','')
            
            #台湾标点转换为大陆标点，双引号和单引号转换
            # context=context.replace('「','“')
            # context=context.replace('」','”')
            # context=context.replace('｢','“')
            # context=context.replace('｣','”')
            # context=context.replace("『","‘")
            # context=context.replace("』","’")

            #将连续的书名号替换成顿号
            context=context.replace("》《","、")

            ############################################################
            #数据清洗，
            for i in ReplaceBox1:
                context=context.replace(i,'')
                print("2")
            #清洗所有的阿拉伯数字、英文和梵文字符和异常字符
            for i in string_set:
                context=context.replace(i,'') 
            for i in number_set:
                context=context.replace(i,'')
            for i in Sanskrit:
                context=context.replace(i,'') 
            for i in cutlist:
                context=context.replace(i,'') 
            #for i in range(len(context)):
            #    if context[i]=='（':
#           #         context[i]=''   
            # for i in ReplaceBox2:
            #     context=context.replace(i,'')
            # for i in ReplaceBox3:
            #     context=context.replace(i,'')

            fp.write(context)   
            row=row+1
            col=0

            FileData.close()
            fp.close()

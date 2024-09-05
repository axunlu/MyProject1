import jieba
import re
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

'''
    读文件
'''


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


'''
    预处理文件
'''


def preprocess_text(text):
    # 正则表达式，去掉文本字母、数字、下划线，空白字符
    text = re.sub(r'[^\w\s]', '', text)
    # 用jieba库划分句子
    words = jieba.lcut(text)
    # 最后拼接
    return ' '.join(words)

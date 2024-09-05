import jieba
import re
import sys
import cProfile
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


'''
    计算文本相似度
'''


def calculate_similarity(original_text, plagiarized_text):
    # 预处理源文本和比对文本
    processed_original = preprocess_text(original_text)
    processed_plagiarized = preprocess_text(plagiarized_text)
    # 计算文本相似度
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_original, processed_plagiarized])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity


def main():
    if len(sys.argv) != 4:
        print("用法:python main.py [原文文件] [抄袭版论文的文件] [答案文件] (输入绝对路径)")
        return

    # 获取三个命令行参数
    original_file_path = sys.argv[1]
    plagiarized_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    # 读文件
    original_text = read_file(original_file_path)
    plagiarized_text = read_file(plagiarized_file_path)
    # 计算文本相似度
    similarity = calculate_similarity(original_text, plagiarized_text)
    # 结果保留小数点后两位
    rounded_similarity = round(similarity, 2)
    # 打开答案文件并写入答案
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(str(rounded_similarity))


if __name__ == '__main__':
    cProfile.run("main()", filename="performance_analysis_result")

import pytest
import sys
import os
import main


class TestFunction:
    def test_smoke(self):
        """
        冒烟测试: 测试程序基本功能可以运行
        """
        # 模拟三个命令行参数
        original_file_path = r"D:\pythonProject\MyProject1\3122004748\examples\orig.txt"
        plagiarized_file_path = r"D:\pythonProject\MyProject1\3122004748\examples\orig_0.8_add.txt"
        output_file_path = r"D:\pythonProject\MyProject1\3122004748\answer.txt"
        # 读文件
        original_text = main.read_file(original_file_path)
        plagiarized_text = main.read_file(plagiarized_file_path)
        # 计算文本相似度
        similarity = main.calculate_similarity(original_text, plagiarized_text)
        assert similarity is not None, "计算文本相似度失败"
        # 结果保留小数点后两位
        rounded_similarity = round(similarity, 2)
        assert 0 < rounded_similarity < 1, "相似度不在合理范围内"
        # 打开答案文件并写入答案
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(str(rounded_similarity))

        with open(output_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            text = text.strip()
            assert float(text) == rounded_similarity, "写入的相似度与计算的相似度不一致"

    def test_normal(self):
        os.system(
            r'python main.py D:\pythonProject\MyProject1\3122004748\examples\orig.txt'
            r' D:\pythonProject\MyProject1\3122004748\examples\orig_0.8_add.txt '
            r'D:\pythonProject\MyProject1\3122004748\answer.txt')

    def test_file_path_exist(self):
        """
        原文文件路径存在（预期：正常打开）
        """
        original_file_path = r"D:\pythonProject\MyProject1\3122004748\examples\orig.txt"
        text = main.read_file(original_file_path)
        assert text is not None

    def test_file_path_not_exist(self):
        """
        原文文件路径不存在（预期：抛出异常FileNotFoundError，提示文件路径不存在）
        """
        original_file_path = r"D:\pythonProject\MyProject1\3122004748\examples\345.txt"
        exception_name = main.read_file(original_file_path)
        assert exception_name == "FileNotFoundError"

    def test_file_context_empty(self):
        """
        抄袭版文件内容为空（预期：提示文件为空）
        """
        plagiarized_file_path = r"D:\pythonProject\MyProject1\3122004748\examples\orig_empty.txt"
        exception_name = main.read_file(plagiarized_file_path)
        assert exception_name == "EmptyFile"

    def test_preprocess_normal_text(self):
        """
        纯中文文本,中英文混合文本（预期：去除标点符号、分词和拼接）
        """
        text = "这是一个测试文本，用于检查预处理函数的效果。"
        processed_text = main.preprocess_text(text)
        assert processed_text == "这是 一个 测试 文本 用于 检查 预处理 函数 的 效果"

        text = "This is a test text. 这是另一个测试文本。"
        processed_text = main.preprocess_text(text)
        assert processed_text == "This   is   a   test   text   这 是 另 一个 测试 文本"

    def test_preprocess_empty_text(self):
        """
        检查预处理函数对于空文本的处理。（预期：返回空字符串）
        """
        text = ""
        processed_text = main.preprocess_text(text)
        assert processed_text == ''

    def test_preprocess_punctuation_text(self):
        """
        检查预处理函数对于仅包含标点符号的文本的处理。（预期：返回空字符串）
        """
        text = "！@#￥%……&*（）"
        processed_text = main.preprocess_text(text)
        assert processed_text == ""

    def test_calculate_similarity_valid_inputs(self):
        """
        测试正常输入情况下的文本相似度计算。（预期：返回一个不为 None 的浮点数）
        """
        original_text = "这是一个测试文本。"
        plagiarized_text = "这是一个类似的测试文本。"
        # 预处理
        original_text = main.preprocess_text(original_text)
        plagiarized_text = main.preprocess_text(plagiarized_text)
        # 计算相似度
        similarity = main.calculate_similarity(original_text, plagiarized_text)
        assert similarity is not None
        assert isinstance(similarity, float)
        assert 0 < similarity < 1

    def test_calculate_similarity_none_inputs(self):
        """测试输入为 None 时的情况。（预期：返回 None）"""
        similarity = main.calculate_similarity(None, None)
        assert similarity is None

    def test_calculate_similarity_empty_inputs(self):
        """测试输入为空字符串时的情况。（预期：返回 None）"""
        similarity = main.calculate_similarity("", "")
        assert similarity is None


if __name__ == '__main__':
    pytest.main(['-vs', 'test_cases.py'])

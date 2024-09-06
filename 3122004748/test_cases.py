import pytest
import sys
import main


class TestFunction:
    def test_smoke(self):
        """
        冒烟测试: 测试程序基本功能可以运行
        python main.py
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
        assert 0 < similarity < 1, "相似度不在合理范围内"
        # 打开答案文件并写入答案
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(str(rounded_similarity))

        with open(output_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            text = text.strip()
            assert float(text) == rounded_similarity, "写入的相似度与计算的相似度不一致"


if __name__ == '__main__':
    pytest.main(['-vs', 'test_cases.py'])

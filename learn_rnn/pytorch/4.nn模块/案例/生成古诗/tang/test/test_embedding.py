import unittest
import torch.nn as nn
import torch as t
class TestEmbedding(unittest.TestCase):
    def test_embedding_array_error(self):
        #################这样处理是错误的,nn.Embedding只能处理数字
        str=t.Tensor(["I", "love", "deep", "learning", "!" ])
        embedding=nn.Embedding(len(str),3)
        print(embedding(str))
    """
        最后输入的单词和单词对应的维度的坐标
    """
    def test_embedding_array_true(self):
        # 创建词汇表
        vocab = {"I": 0, "love": 1, "deep": 2, "learning": 3, "!": 4}
        strings=["I", "love", "deep", "learning", "!" ]
        # 将字符串序列转换为整数索引序列
        input = t.LongTensor([vocab[word] for word in strings])
        #注意第一个参数是词汇表的个数，并不是输入单次的长度，你在这里就算填100也不影响最终的输出，这个输入值影响的是算出来的行向量值
        #nn.Embedding模块会随机初始化嵌入矩阵。在深度学习中，模型参数通常会使用随机初始化的方法来开始训练，以便模型能够在训练过程中学习到合适的参数值。
        #在nn.Embedding中，嵌入矩阵的每个元素都会被随机初始化为一个小的随机值，这些值将作为模型在训练过程中学习的可训练参数，可以使用manual_seed固定。
        t.manual_seed(1234)
        embedding=nn.Embedding(len(vocab),3)
        print(embedding(input))
# 运行测试
if __name__ == '__main__':
    unittest.main()
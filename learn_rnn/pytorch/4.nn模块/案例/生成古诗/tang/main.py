
import fire
import torch.nn as nn
import torch as t
from data.dataset import PoetryDataset
from models.model import Net
num_epochs=10
data_root="./data/tang.npz"
batch_size=128
def train(**kwargs):
    datasets=PoetryDataset(data_root)
    data,ix2word,word2ix=datasets.getData()
    data = t.from_numpy(data)
    dataloader = t.utils.data.DataLoader(data, batch_size=batch_size, shuffle=True, num_workers=1)
    #总共有8293的词。模型定义：vocab_size, embedding_dim, hidden_dim = 8293 * 128 * 256
    model=Net(len(word2ix.item()),128,256)
    #定义损失函数
    criterion = nn.CrossEntropyLoss()
    #model=model.cuda()
    optimizer = t.optim.Adam(model.parameters(), lr=1e-3)
    for epoch in range(num_epochs):  # 最大迭代次数为8
        for i, data in enumerate(dataloader):  # 一批次数据 128*125
            data = data.long().contiguous()
            #data = data.cuda()
            optimizer.zero_grad()
            input, target = (data[:-1, :]), (data[1:, :])
            output, _ = model(input)
            loss = criterion(output, target.view(-1))  # torch.Size([15872, 8293]), torch.Size([15872])
            loss.backward()
            optimizer.step()
            if (1 + i) % 575 == 0:  # 每575个batch可视化一次
                print(str(i) + ':' + generate(model, '床前明月光', ix2word, word2ix))
    t.save(model.state_dict(), './checkpoints/model_poet_2.pth')
def generate(model, start_words, ix2word, word2ix):     # 给定几个词，根据这几个词生成一首完整的诗歌
    txt = []
    for word in start_words:
        txt.append(word)
    input = t.Tensor([word2ix['<START>']]).view(1,1).long()      # tensor([8291.]) → tensor([[8291.]]) → tensor([[8291]])
    input = input.cuda()
    hidden = None
    num = len(txt)
    for i in range(48):      # 最大生成长度
        output, hidden = model(input, hidden)
        if i < num:
            w = txt[i]
            input = (input.data.new([word2ix[w]])).view(1, 1)
        else:
            top_index = output.data[0].topk(1)[1][0]
            w = ix2word[top_index.item()]
            txt.append(w)
            input = (input.data.new([top_index])).view(1, 1)
        if w == '<EOP>':
            break
    return ''.join(txt)

if __name__=="__main__":
    fire.Fire()
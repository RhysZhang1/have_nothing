# import torch
#
# # 1. 检查 CUDA 是否可用
# print("CUDA available:", torch.cuda.is_available())
#
# if torch.cuda.is_available():
#     # 2. 查看 GPU 数量
#     print("GPU count:", torch.cuda.device_count())
#     # 3. 获取当前 GPU 名称
#     print("Current GPU:", torch.cuda.get_device_name(torch.cuda.current_device()))
#
#     # 4. 创建一个张量并移动到 GPU
#     x = torch.tensor([1.0, 2.0, 3.0]).cuda()
#     print("Tensor on GPU:", x)
#
#     # 5. 执行简单运算
#     y = x * 2
#     print("Result on GPU:", y)
#
#     # 6. 将结果移回 CPU
#     print("Result on CPU:", y.cpu())
# else:
#     print("CUDA not available. Please check your PyTorch installation.")
#
# print(torch.__version__)               # 应显示类似 2.5.0+cu124（或 cu121）
# print(torch.cuda.is_available())        # 应为 True
# print(torch.cuda.get_device_name(0))    # 应显示 GPU 名称 "NVIDIA GeForce RTX 5060"


def dataset1():
    from torch.utils.data import Dataset
    from PIL import Image
    import os
    class mydata(Dataset):
        def __init__(self,root_dir,label_dir):
            self.root_dir=root_dir #数据集路径：hymenoptera_data/train
            self.label_dir=label_dir #目标：ants
            self.path=os.path.join(self.root_dir,self.label_dir) #拼接路径
            self.img_path=os.listdir(self.path)  #读取具体文件名转为一个列表
        def __getitem__(self, idx):    #定义对象通过索引访问
            img_name=self.img_path[idx]  #取一个文件（图片
            img_item_path=os.path.join(self.root_dir,self.label_dir,img_name) #拼接路径
            img=Image.open(img_item_path) #打开图片
            label=self.label_dir  #目标
            return img,label
        def __len__(self):
            return len(self.img_path)

    root_dir='C:\\Users\\rhys1\\Desktop\\zane_project\\python\\pytorch\\pra\\hymenoptera_data\\train'
    #指定路径
    ants_label_dir='ants' #指定目标
    bees_label_dir='bees'
    ants_dataset=mydata(root_dir,ants_label_dir) #实例化
    bees_dataset=mydata(root_dir,bees_label_dir)
    train_dataset=ants_dataset+bees_dataset      #合并
    img,label=train_dataset[124]
    img.show()
def tensorboard1():#查看数据
    from torch.utils.tensorboard import SummaryWriter
    writer=SummaryWriter('logs') #创建存放文件夹
    for i in range(100):#画函数
        writer.add_scalar('y=x',2*i,i)  #tag：函数（字符串），y轴，x轴
        #在目录下执行命令  tensorboard --logdir=logs  查看（默认本地6006端口
        #修改并运行前，删掉文件夹中的旧文件
    writer.close()  #关闭
def tensorboard2():
    from torch.utils.tensorboard import SummaryWriter
    import numpy as np
    from PIL import Image
    writer=SummaryWriter('logs') #创建文件夹
    image_path='pra/hymenoptera_data/train/ants/0013035.jpg' #指定路径
    img_PIL=Image.open(image_path) #用PIL加载图片
    img_array=np.array(img_PIL) #转换格式
    writer.add_image('test',img_array,1,dataformats='HWC')  #标记，图片，步数，指定每个数字的含义‘长宽色’
    for i in range(100):
        writer.add_scalar('y=x',2*i,i)
    writer.close()
def transform1():     #工具箱：转换图片
    from torchvision import transforms
    from PIL import Image
    from torch.utils.tensorboard import SummaryWriter

    #tensor数据类型:神经网络用的数据

    #Totensor
    img_path='pra/hymenoptera_data/train/ants/0013035.jpg'  #设置路径
    img=Image.open(img_path)  #读取
    trans_totensor=transforms.ToTensor() #实例化（取工具）
    img_tensor=trans_totensor(img) #转化为tensor格式（用工具）
    writer=SummaryWriter('logs')  #创建存放文件夹
    writer.add_image('test',img_tensor) #添加显示(原始图片)

    #Normalize
    tran_norm=transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) #mean均值，std标准差
    #input[channel]=(input[channel]-mean[channel])/std[channel]
    img_norm=tran_norm(img_tensor) #转化
    writer.add_image('test2',img_norm,1)  #添加显示(归一化后的图片)

    #Resize
    trans_resize=transforms.Resize((224,224))  #设置大小(长宽)
    img_resize=trans_resize(img)  #转换图片
    img_resize=trans_totensor(img_resize)  #转换格式（PIL->tensor）
    writer.add_image('test3',img_resize,2) #添加显示

    trans_resize_2=transforms.Resize(100) #设置大小（保持长宽比不变，设置短边为100
    trans_compose=transforms.Compose([trans_resize_2,trans_totensor]) #定义流水线（列表中为步骤：缩放，格式转化
    image_resize_2=trans_compose(img) #用流水线处理图片
    writer.add_image('test4',image_resize_2,3) #添加显示

    # RandomCrop
    trans_random=transforms.RandomCrop(50) #设置大小(写一个数据：正方形；写一个元组两个数据：长宽
    trans_compose_2= transforms.Compose([trans_random, trans_totensor])#定义流水线
    for i in range(10):
        img_crop=trans_compose_2(img)  #对一张图随机裁处10张50*50的图片
        writer.add_image('test5',img_crop,4+i) #添加显示

    writer.close()

    # 在目录下执行命令  tensorboard --logdir=logs  查看（默认本地6006端口
    # 修改并运行前，删掉文件夹中的旧文件

def torchvision1():
    import torchvision
    from torch.utils.tensorboard import SummaryWriter
    dataset_transform=torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
    train_set=torchvision.datasets.CIFAR10(root='./data', train=True,transform=dataset_transform,download=True) #加上download=True自动下载数据集
    test_set=torchvision.datasets.CIFAR10(root='./data', train=False,transform=dataset_transform,download=True) #去官网查有哪些数据集

    writer=SummaryWriter('logs') #创建存放文件夹
    for i in range(10):
        img,target=test_set[i] #取图片
        writer.add_image('train',img,i) #添加显示
    writer.close()
def dataloader1():
    #从dataset：取数据
    #dataset是牌堆，dataloader就是摸牌

    #参数：设置好dataset和少量其他参数即可，除dataset其他参数均有默认值
    #batch_size:(默认1)每次取几张
    #shuffle:(默认False)每次取牌洗不洗牌
    #num_worker:(默认0)采用几线程加载（有概率报错(BrokenPipeError)，可改为0只使用主线程加载
    #drop_last:(默认False)多次抓牌后剩的是舍是抓

    from torch.utils.tensorboard import SummaryWriter
    import torchvision
    from torch.utils.data import DataLoader
    #测试集
    test_data=torchvision.datasets.CIFAR10('./data',train=False,transform=torchvision.transforms.ToTensor(),download=True)
    test_loader=DataLoader(test_data,batch_size=4,shuffle=True,num_workers=0,drop_last=False) #4张一次的取

    writer=SummaryWriter('logs')
    for epoch in range(3):
        step=0
        for data in test_loader:
            img,target=data
            writer.add_images('train'+str(epoch),img,step)   #注意多了个s
            step+=1
        writer.close()
def torch_neural_network1():
    #nn.Module
    from torch import nn
    import torch
    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()

        def forward(self,iput):
            otput=iput+1
            return otput

    z1=zyh_nn()
    x=torch.tensor(1.0)
    otput=z1.forward(x)
    print(otput)

def nn_juanji():
    #输入图像|卷积核-> 输出
    import torch
    import torch.nn.functional as F
    iput=torch.tensor([[1,2,0,3,1],
                       [0,1,2,3,1],
                       [1,2,1,0,0],
                       [5,2,3,1,1],
                       [2,1,0,1,1]])  #当作输入图像
    kenrel=torch.tensor([[1,2,1],
                        [0,1,0],
                        [2,1,0]])  #当作卷积核
    # print(iput.shape)
    # print(kenrel.shape)  #查看尺寸
    iput=torch.reshape(iput,(1,1,5,5))  #batch_size（批大小），channel（通道），高，宽
    kenrel=torch.reshape(kenrel,(1,1,3,3))  #修改尺寸
    # print(iput.shape)
    # print(kenrel.shape)
    otput=F.conv2d(iput,weight=kenrel,stride=1)  #处理的图，卷积核，步长
    #从左上开始，将卷积核叠在图像上，对应位置的数字相乘再求和，记为一个数，向右或向下移动一步，运算，计数，直到右下角
    print(otput)
    otput = F.conv2d(iput, weight=kenrel, stride=3)
    #步长太大，部分数据被忽略了（移动一步后，卷积核覆盖下有空白则放弃
    print(otput)
    otput = F.conv2d(iput, weight=kenrel, stride=3,padding=2) #padding：填充
    #为了不丢失边缘的数据，在图像数据外围上几圈零（padding的值），然后将新图像用于计算
    print(otput)
def nn_juanji2():
    import torch
    from torch import nn
    from torch.nn import Conv2d
    import torchvision
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard import SummaryWriter
    #in_channels输入通道数
    # out_channels输出通道数
    # kernel_size卷积核大小
    # stride=1步长
    # padding=0填充多少
    # dilation=1, groups=1, bias=True, padding_mode='zeros', device=None, dtype=None不常用
    dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=torchvision.transforms.ToTensor(),download=True)
    dataloader=DataLoader(dataset, batch_size=64)
    class z_nn(nn.Module):
        def __init__(self):
            super(z_nn,self).__init__()
            self.conv1=Conv2d(in_channels=3,out_channels=6,kernel_size=3,stride=1,padding=0)

        def forward(self,x):
            x=self.conv1(x)
            return x

    zz=z_nn()
    writer=SummaryWriter('logs')
    step=0
    for data in dataloader:
        img,target=data
        otput=zz(img)
        writer.add_images('input',img,step)
        otput=torch.reshape(otput,(-1,3,30,30))
        writer.add_images('output',otput,step)
        step+=1
    writer.close()
def nn_pooling_layer1():
    #最大池化：提取特征
    from torch import nn
    from torch.nn import MaxPool2d
    import torchvision
    from torch.utils.tensorboard import SummaryWriter
    from torch.utils.data import DataLoader
    #池化核：类似卷积一样叠在图像上，核没有数值，取核范围内的最大值
    #步长就是核大小，
    #ceil_model：True不完全覆盖的范围也保留，False不保留，默认False
    dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=torchvision.transforms.ToTensor(),download=True)
    dataloader=DataLoader(dataset, batch_size=64)

    # iput=torch.tensor([[1,2,0,3,1],
    #                    [0,1,2,3,1],
    #                    [1,2,1,0,0],
    #                    [5,2,3,1,1],
    #                    [2,1,0,1,1]],dtype=torch.float32)
    # iput=torch.reshape(iput,(-1,1,5,5))

    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.maxpool1=MaxPool2d(kernel_size=3,ceil_mode=True)
        def forward(self,iput):
            otput=self.maxpool1(iput)
            return otput

    z_nn=zyh_nn()
    # otput=z_nn(iput)
    # print(otput)

    writers=SummaryWriter('logs')
    step=0
    for data in dataloader:
        img,target=data
        otput=z_nn(img)
        writers.add_images('input',img,step)
        writers.add_images('output',otput,step)
        step+=1
    writers.close()
def nn_relu():
    #非线性激活：relu,sigmid
    #relu：正值不变，负值归零
    import torch
    import torchvision
    from torch.nn import ReLU
    from torch.utils.tensorboard import SummaryWriter
    from torch.utils.data import DataLoader
    from torch import nn
    # iput=torch.tensor([[1,-0.5],
    #                    [-1,3]])
    # otput=torch.reshape(iput,(-1,1,2,2))

    dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=torchvision.transforms.ToTensor(),download=True)
    dataloader = DataLoader(dataset, batch_size=64)

    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.relu=ReLU(inplace=False) #inplace：True则替换原来的值，False则返回新的值

        def forward(self,iput):
            otput=self.relu(iput)
            return otput

    z_nn=zyh_nn()
    # otput=z_nn(iput)
    # print(otput)
    writers=SummaryWriter('logs')
    step=0
    for data in dataloader:
        img,target=data
        otput=z_nn(img)
        writers.add_images('input',img,step)
        writers.add_images('output',otput,step)
        step+=1
    writers.close()

def nn_line():
    #线性层:(MLP
    import torch
    import torchvision
    from torch.nn import Linear
    from torch.utils.tensorboard import SummaryWriter
    from torch.utils.data import DataLoader
    from torch import nn
    dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=torchvision.transforms.ToTensor(),download=True)
    dataloader = DataLoader(dataset, batch_size=64)

    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.linear=Linear(in_features=32,out_features=10)

        def forward(self,iput):
            otput=self.linear(iput)
            return otput
    z_nn=zyh_nn()
    writers=SummaryWriter('logs')
    step=0
    for data in dataloader:
        img,target=data
        writers.add_images('input',img,step)
        otput=torch.flatten(img)    #展平，变成一行
        otput=z_nn(img)
        writers.add_images('output',otput,step)
        step+=1
    writers.close()

def seq():
    import torch
    from torch import nn
    from torch.nn import Conv2d,MaxPool2d, Flatten, Linear
    from torch.utils.tensorboard import SummaryWriter

    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            # #卷积
            # self.conv1=Conv2d(in_channels=3,out_channels=32,kernel_size=5 ,stride=1,padding=2)
            # #池化
            # self.maxpool1=MaxPool2d(kernel_size=2)
            # self.conv2=Conv2d(in_channels=32,out_channels=32,kernel_size=5 ,stride=1,padding=2)
            # self.maxpool2=MaxPool2d(kernel_size=2)
            # self.conv3=Conv2d(in_channels=32,out_channels=64,kernel_size=5 ,stride=1,padding=2)
            # self.maxpool3=MaxPool2d(kernel_size=2)
            # #线性
            # self.flatten=Flatten()
            # self.liner1=Linear(in_features=1024,out_features=64)
            # self.liner2=Linear(in_features=64,out_features=10)

            #写成流水线，不用一步步写了
            self.model1=nn.Sequential(
                Conv2d(in_channels=3,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Conv2d(in_channels=32,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Conv2d(in_channels=32,out_channels=64,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Flatten(),
                Linear(in_features=1024,out_features=64),
                Linear(in_features=64,out_features=10)
            )

        def forward(self,iput):
            # iput=self.conv1(input=iput)
            # iput=self.maxpool1(iput)
            # iput=self.conv2(input=iput)
            # iput=self.maxpool2(iput)
            # iput=self.conv3(input=iput)
            # iput=self.maxpool3(iput)
            # iput=self.flatten(iput)
            # iput=self.liner1(iput)
            # iput=self.liner2(iput)

            otput=self.model1(iput)
            return otput

    def test():
        z_nn = zyh_nn()
        iput=torch.ones(64,3,32,32)  #创建一个全是1的测试用例（测试网络对不对
        otput=z_nn(iput)
        writers=SummaryWriter('logs')
        writers.add_graph(z_nn,iput) #查看网络结构
        writers.close()
        #参数不对可以一步步走，改对应层的数据

    test()

def nn_loss():
    #损失函数
    #计算实际输出和目标之间的差距；
    #为更新输出提供一定的依据（反向传播
    import torch
    from torch import nn
    from torch.nn import L1Loss,MSELoss

    iput=torch.tensor([1,2,3],dtype=torch.float)
    target=torch.tensor([1,2,5],dtype=torch.float)

    iput=torch.reshape(iput,(1,1,1,3))
    target=torch.reshape(target,(1,1,1,3))

    loss_l1=L1Loss()   #对应位置差的总和/总位数
    result=loss_l1(iput,target)
    print(result)

    loss_mse=MSELoss()  #对应位置差的平方的总和/总位数   ->  用于回归
    result=loss_mse(iput,target)
    print(result)

    #loss(otput,target)=-otput[target]+ln(sum_j {exp(otput_j)})  ->  用于分类
    #otput：输出（类似一维列表，表示属于不同类的概率，target表示正确结果是第0个，还是第一个等
    #ln：以e为底的对数
    #exp()以e为底的指数
    x=torch.tensor([0.1,0.2,0.3])
    y=torch.tensor([1])
    x=torch.reshape(x,(1,3))
    loss_cross=nn.CrossEntropyLoss()
    result=loss_cross(x,y)
    print(result)

def nn_loss_netlook():
    import torch
    from torch import nn
    import torchvision
    from torch.nn import Conv2d,MaxPool2d, Flatten, Linear
    from torch.utils.data import DataLoader

    dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=torchvision.transforms.ToTensor(),download=True)
    dataloader = DataLoader(dataset, batch_size=64)
    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.model1=nn.Sequential(
                Conv2d(in_channels=3,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Conv2d(in_channels=32,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Conv2d(in_channels=32,out_channels=64,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Flatten(),
                Linear(in_features=1024,out_features=64),
                Linear(in_features=64,out_features=10)
            )
        def forward(self,iput):
            otput=self.model1(iput)
            return otput

    z_nn=zyh_nn()
    loss=nn.CrossEntropyLoss()
    for data in dataloader:
        img,targets=data
        otput=z_nn(img)
        loss_result=loss(otput,targets)
        print(loss_result)
def nn_optim():
    #反向传播，梯度优化
    import torch
    from torch import nn
    from torch.nn import Conv2d,MaxPool2d, Flatten, Linear
    from torch.utils.data import DataLoader
    import torchvision

    dataset = torchvision.datasets.CIFAR10('./data', train=False, transform=torchvision.transforms.ToTensor(),download=True)
    dataloader = DataLoader(dataset, batch_size=64)
    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.model1=nn.Sequential(
                Conv2d(in_channels=3,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Conv2d(in_channels=32,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Conv2d(in_channels=32,out_channels=64,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                Flatten(),
                Linear(in_features=1024,out_features=64),
                Linear(in_features=64,out_features=10)
            )
        def forward(self,iput):
            otput=self.model1(iput)
            return otput

    z_nn=zyh_nn()
    loss=nn.CrossEntropyLoss()
    optim=torch.optim.SGD(z_nn.parameters(),lr=0.01) #lr学习速率
    for _ in range(20):             #学习20轮
        running_loss=0.0
        for data in dataloader:
            img,targets=data
            otput=z_nn(img)
            loss_result=loss(otput,targets)
            optim.zero_grad()              #梯度清零
            loss_result.backward()         #调用损失函数求梯度，反向传播
            optim.step()                   #梯度调优
            running_loss+=loss_result
        print(running_loss)

def model_pretrained():
    # import torchvision
    # import torch
    # from torch import nn
    # vgg16_false=torchvision.models.vgg16(pretrained=False)   #设为False是原始模型
    # vgg16_true=torchvision.models.vgg16(pretrained=True)     #True则是训练后的
    # print(vgg16_true)  #查看网络
    # train_data=torchvision.datasets.CIFAR10('./data', train=True, transform=torchvision.transforms.ToTensor(),download=True)
    # vgg16_true.add_module('add_linear',nn.Linear(1000,10))  #在最后加一个线性层，字符串表示层名
    # vgg16_true.classifier.add_module('add_linear',nn.Linear(120,10)) #多加一个点，表示在指定层（classifier）加
    # vgg16_true.classifier[6]=nn.Linear(4096,10)  #指定模型一层修改
    pass
def model_save_():
    # import torchvision
    # import torch
    # vgg16=torchvision.models.vgg16(pretrained=False)
    # #保存方式
    # torch.save(vgg16,'./vgg16_new.pth')  #前面表示要保存的模型，后面表示新名字和路径，.pth是惯用后缀
    # #保存了整个模型结构和参数
    # #加载模型
    # model=torch.load('./vgg16_new.pth') #括号内指定
    # print(model)   #可见直接就是模型
    # #保存方式2
    # torch.save(vgg16.state_dict(),'./vgg16_new.pth') #以字典格式保存模型参数
    # #加载模型
    # vgg16=torchvision.models.vgg16(pretrained=False) #加载模型
    # vgg16.load_state_dict(torch.load('./vgg16_new.pth'))  #按文件更新参数
    # print(model)   #查看
    pass
def fenlei():
    #正确率：分类问题特有
    import torch

    otput=torch.tensor([[0.1,0.2],
                       [0.3,0.4]])
    preds=otput.argmax(dim=1)  #dim表示方向，1横向，0纵向，返回当前最大值所在的位置索引
    targets=torch.tensor([0,1])
    print(preds==targets)
def train():
    import torch
    from torch import nn
    import torchvision
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard import SummaryWriter
    from torch.nn import Conv2d,MaxPool2d,Flatten,Linear
    #准备训练数据集
    train_data=torchvision.datasets.CIFAR10('./data',train=True,transform=torchvision.transforms.ToTensor(),download=True)
    #测试数据集
    test_data=torchvision.datasets.CIFAR10('./data',train=False,transform=torchvision.transforms.ToTensor(),download=True)

    train_data_size=len(train_data)
    test_data_size=len(test_data)

    train_dataloader=DataLoader(train_data,batch_size=64,shuffle=True)
    test_dataloader=DataLoader(test_data,batch_size=64,shuffle=True)

    # 搭建的神经网络可以将其放到个单独的文件中，用__main__测试，在使用时import
    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.model1=nn.Sequential(
                nn.Conv2d(in_channels=3,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=32,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=32,out_channels=64,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Flatten(),
                nn.Linear(in_features=1024,out_features=64),
                nn.Linear(in_features=64,out_features=10)
            )
        def forward(self,iput):
            otput=self.model1(iput)
            return otput

    z_nn=zyh_nn()
    loss_fn=nn.CrossEntropyLoss()#损失函数
    optimizer=torch.optim.SGD(z_nn.parameters(),lr=0.01) #优化器

    total_train_step=0 #训练次数
    total_test_step=0 #测试次数
    epoch=30 #训练的轮数

    writers=SummaryWriter('logs')
    for i in range(epoch):
        print(f'epoch:{i}________________________')
        z_nn.train()   #调整模型为训练状态（写不写都行，写了更好
        for data in train_dataloader: #取
            img,targets=data
            otput=z_nn(img)  #训练
            loss=loss_fn(otput,targets) #算损失
            optimizer.zero_grad() #梯度清零
            loss.backward() #反向传播
            optimizer.step() #调用优化器
            total_train_step+=1
            if total_train_step%10==0:
                writers.add_scalar('loss',loss.item(),total_train_step)

        #测试
        z_nn.eval()  #调整模型为测试状态（写不写都行，写了更好
        total_test_loss=0
        total_accuracy=0
        with torch.no_grad():
            for data in test_dataloader:
                img,targets=data
                otput=z_nn(img)
                loss=loss_fn(otput,targets)
                total_test_loss+=loss.item()
                accuracy=(otput.argmax(dim=1)==targets).sum()
                total_accuracy=total_accuracy+accuracy
        print(f'test_loss:{total_test_loss}')
        print(f'正确率:{total_accuracy/test_data_size}')
        writers.add_scalar('test_loss',total_test_loss,total_test_step+1)
        writers.add_scalar('test_accuracy',total_accuracy/test_data_size,total_test_step+1)
        total_test_step+=1

        #可以加个保存模型，保存每一步的模型，选loss最小的

def train_gpu():
    # 网络，损失函数，数据，调用cuda使用gpu训练
    # .cuda
    # 用torch.cuda.is_available()判断
    import torch
    from torch import nn
    import torchvision
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard import SummaryWriter
    from torch.nn import MaxPool2d
    train_data=torchvision.datasets.CIFAR10('./data',train=True,transform=torchvision.transforms.ToTensor(),download=True)
    test_data=torchvision.datasets.CIFAR10('./data',train=False,transform=torchvision.transforms.ToTensor(),download=True)

    train_data_size=len(train_data)
    test_data_size=len(test_data)

    train_dataloader=DataLoader(train_data,batch_size=64,shuffle=True)
    test_dataloader=DataLoader(test_data,batch_size=64,shuffle=True)

    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.model1=nn.Sequential(
                nn.Conv2d(in_channels=3,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=32,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=32,out_channels=64,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Flatten(),
                nn.Linear(in_features=1024,out_features=64),
                nn.Linear(in_features=64,out_features=10)
            )
        def forward(self,iput):
            otput=self.model1(iput)
            return otput

    z_nn=zyh_nn()
    loss_fn=nn.CrossEntropyLoss()
    if torch.cuda.is_available():
        z_nn=z_nn.cuda()
        loss_fn=loss_fn.cuda()
    optimizer=torch.optim.SGD(z_nn.parameters(),lr=0.01)

    total_train_step=0
    total_test_step=0
    epoch=30

    writers=SummaryWriter('logs')
    for i in range(epoch):
        print(f'epoch:{i+1}________________________')
        z_nn.train()
        for data in train_dataloader:
            img,targets=data
            if torch.cuda.is_available():
                img = img.cuda()
                targets = targets.cuda()
            otput=z_nn(img)
            loss=loss_fn(otput,targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_train_step+=1
            if total_train_step%10==0:
                writers.add_scalar('loss',loss.item(),total_train_step)

        z_nn.eval()
        total_test_loss=0
        total_accuracy=0
        with torch.no_grad():
            for data in test_dataloader:
                img,targets=data
                if torch.cuda.is_available():
                    img=img.cuda()
                    targets = targets.cuda()
                otput=z_nn(img)
                loss=loss_fn(otput,targets)
                total_test_loss+=loss.item()
                accuracy=(otput.argmax(dim=1)==targets).sum()
                total_accuracy=total_accuracy+accuracy
        print(f'test_loss:{total_test_loss}')
        print(f'accuracy:{total_accuracy/test_data_size}')
        writers.add_scalar('test_loss',total_test_loss,total_test_step+1)
        writers.add_scalar('test_accuracy',total_accuracy/test_data_size,total_test_step+1)
        total_test_step+=1

def train_gup_2():
    # 网络，损失函数，数据，调用cuda使用gpu训练
    # .cuda
    # 用torch.cuda.is_available()判断
    import torch
    from torch import nn
    import torchvision
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard import SummaryWriter
    train_data=torchvision.datasets.CIFAR10('./data',train=True,transform=torchvision.transforms.ToTensor(),download=True)
    test_data=torchvision.datasets.CIFAR10('./data',train=False,transform=torchvision.transforms.ToTensor(),download=True)

    train_data_size=len(train_data)
    test_data_size=len(test_data)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    #定义训练设备(cpu就写cpu，NV显卡写cuda，后面的序号指定第几块
    train_dataloader=DataLoader(train_data,batch_size=64,shuffle=True)
    test_dataloader=DataLoader(test_data,batch_size=64,shuffle=True)

    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.model1=nn.Sequential(
                nn.Conv2d(in_channels=3,out_channels=32,kernel_size=3 ,stride=1,padding=1),
                nn.BatchNorm2d(num_features=32),
                nn.ReLU(inplace=False),
                nn.Conv2d(in_channels=32,out_channels=64,kernel_size=3 ,stride=1,padding=1),
                nn.BatchNorm2d(num_features=64),
                nn.ReLU(inplace=False),
                nn.MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3 ,stride=1,padding=1),
                nn.BatchNorm2d(num_features=128),
                nn.ReLU(inplace=False),
                nn.MaxPool2d(kernel_size=2),
                nn.Flatten(),
                nn.Linear(in_features=8192,out_features=256),
                nn.ReLU(inplace=False),
                nn.Dropout(p=0.5),
                nn.Linear(in_features=256,out_features=10)
            )
        def forward(self,iput):
            otput=self.model1(iput)
            return otput

    z_nn=zyh_nn()
    loss_fn=nn.CrossEntropyLoss()
    z_nn=z_nn.to(device)
    loss_fn=loss_fn.to(device)
    optimizer=torch.optim.SGD(z_nn.parameters(),lr=0.01)

    total_train_step=0
    total_test_step=0
    epoch=30

    writers=SummaryWriter('logs')
    for i in range(epoch):
        print(f'epoch:{i+1}________________________')
        z_nn.train()
        for data in train_dataloader:
            img,targets=data
            img=img.to(device)     #转移
            targets=targets.to(device)
            otput=z_nn(img)
            loss=loss_fn(otput,targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_train_step+=1
            if total_train_step%10==0:
                writers.add_scalar('loss',loss.item(),total_train_step)

        z_nn.eval()
        total_test_loss=0
        total_accuracy=0
        with torch.no_grad():
            for data in test_dataloader:
                img,targets=data
                img=img.to(device)
                targets=targets.to(device)
                otput=z_nn(img)
                loss=loss_fn(otput,targets)
                total_test_loss+=loss.item()
                accuracy=(otput.argmax(dim=1)==targets).sum()
                total_accuracy=total_accuracy+accuracy
        print(f'test_loss:{total_test_loss}')
        print(f'accuracy:{total_accuracy/test_data_size}')
        writers.add_scalar('test_loss',total_test_loss,total_test_step+1)
        writers.add_scalar('test_accuracy',total_accuracy/test_data_size,total_test_step+1)
        total_test_step+=1

def model_test():
    import torch
    from PIL import Image
    from torchvision import transforms
    from torch import nn
    from torch.nn import MaxPool2d

    image_path='./data'  #设置图片路径
    image=Image.open(image_path)  #打开
    transform=transforms.Compose([transforms.Resize((32,32)),
                                  transforms.ToTensor()])  #设置转换流程
    image=transform(image)  #转换

    class zyh_nn(nn.Module):   #网络
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.model1=nn.Sequential(
                nn.Conv2d(in_channels=3,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=32,out_channels=32,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=32,out_channels=64,kernel_size=5 ,stride=1,padding=2),
                MaxPool2d(kernel_size=2),
                nn.Flatten(),
                nn.Linear(in_features=1024,out_features=64),
                nn.Linear(in_features=64,out_features=10)
            )
        def forward(self,iput):
            otput=self.model1(iput)
            return otput

    model=torch.load('./model.pth',map_location=torch.device('cpu'))  #加载保存的模型,指定加载位置
    image=torch.reshape(image,(1,3,32,32)) #转换大小
    model.eval()  #转化为测试模式
    with torch.no_grad():
        otput=model(image)

    print(otput.argmax(dim=1))

def train__2():
    import torch
    from torch import nn
    import torchvision
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard import SummaryWriter
    transform_train = torchvision.transforms.Compose([
        torchvision.transforms.RandomCrop(32, padding=4),  # 先填充再随机裁剪
        torchvision.transforms.RandomHorizontalFlip(),  # 随机水平翻转
        torchvision.transforms.ToTensor(),
        torchvision.transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)),#随机擦除
        torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                         (0.2023, 0.1994, 0.2010))  # CIFAR-10 标准值
    ])
    transform_test = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                         (0.2023, 0.1994, 0.2010))
    ])
    train_data=torchvision.datasets.CIFAR10('./data',train=True,transform=transform_train,download=True)
    test_data=torchvision.datasets.CIFAR10('./data',train=False,transform=transform_test,download=True)

    test_data_size=len(test_data)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    train_dataloader=DataLoader(train_data,batch_size=64,shuffle=True)
    test_dataloader=DataLoader(test_data,batch_size=64,shuffle=True)

    class zyh_nn(nn.Module):
        def __init__(self):
            super(zyh_nn,self).__init__()
            self.model1=nn.Sequential(
                nn.Conv2d(in_channels=3,out_channels=64,kernel_size=3 ,stride=1,padding=1),
                nn.BatchNorm2d(num_features=64), #批归一化
                nn.ReLU(inplace=False),
                nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3 ,stride=1,padding=1),
                nn.BatchNorm2d(num_features=128),
                nn.ReLU(inplace=False),
                nn.MaxPool2d(kernel_size=2),
                nn.Conv2d(in_channels=128,out_channels=256,kernel_size=3 ,stride=1,padding=1),
                nn.BatchNorm2d(num_features=256),
                nn.ReLU(inplace=False),
                nn.MaxPool2d(kernel_size=2),
                nn.AdaptiveAvgPool2d((1, 1)),#全局平均池化
                nn.Flatten(),
                nn.Linear(in_features=256,out_features=256),
                nn.ReLU(inplace=False),
                nn.Dropout(p=0.5),  #随机失活
                nn.Linear(in_features=256,out_features=10)
            )
        def forward(self,iput):
            otput=self.model1(iput)
            return otput

    z_nn=zyh_nn()
    loss_fn=nn.CrossEntropyLoss(label_smoothing=0.1) #0.1：标签平滑
    z_nn=z_nn.to(device)
    loss_fn=loss_fn.to(device)
    optimizer = torch.optim.SGD(z_nn.parameters(), lr=0.1,
                                momentum=0.9, weight_decay=5e-4)#学习率，动量，权重衰减

    total_train_step=0
    total_test_step=0
    epoch=200

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epoch) #余弦退火

    writers=SummaryWriter('logs1')
    for i in range(epoch):
        print(f'epoch:{i+1}________________________')
        z_nn.train()
        for data in train_dataloader:
            img,targets=data
            img=img.to(device)     #转移
            targets=targets.to(device)
            otput=z_nn(img)
            loss=loss_fn(otput,targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_train_step+=1
            if total_train_step%10==0:
                writers.add_scalar('loss',loss.item(),total_train_step)

        z_nn.eval()
        total_test_loss=0
        total_accuracy=0
        with torch.no_grad():
            for data in test_dataloader:
                img,targets=data
                img=img.to(device)
                targets=targets.to(device)
                otput=z_nn(img)
                loss=loss_fn(otput,targets)
                total_test_loss+=loss.item()
                accuracy=(otput.argmax(dim=1)==targets).sum()
                total_accuracy=total_accuracy+accuracy
        print(f'test_loss:{total_test_loss}')
        print(f'accuracy:{total_accuracy/test_data_size}')
        writers.add_scalar('test_loss',total_test_loss,total_test_step+1)
        writers.add_scalar('test_accuracy',total_accuracy/test_data_size,total_test_step+1)
        total_test_step+=1
        scheduler.step()

def train__3():
    import torch
    from torch import nn
    import torchvision
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard import SummaryWriter
    import torch.nn.functional as F
    transform_train = torchvision.transforms.Compose([
        torchvision.transforms.RandomCrop(32, padding=4),  # 先填充再随机裁剪
        torchvision.transforms.RandomHorizontalFlip(),  # 随机水平翻转
        torchvision.transforms.ToTensor(),
        torchvision.transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)),#随机擦除
        torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                         (0.2023, 0.1994, 0.2010))  # CIFAR-10 标准值
    ])
    transform_test = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                         (0.2023, 0.1994, 0.2010))
    ])
    train_data=torchvision.datasets.CIFAR10('./data',train=True,transform=transform_train,download=True)
    test_data=torchvision.datasets.CIFAR10('./data',train=False,transform=transform_test,download=True)

    test_data_size=len(test_data)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    train_dataloader=DataLoader(train_data,batch_size=64,shuffle=True)
    test_dataloader=DataLoader(test_data,batch_size=64,shuffle=True)

    # ---------------------- 基础残差块 ----------------------
    class BasicBlock(nn.Module):
        expansion = 1

        def __init__(self, in_planes, planes, stride=1):
            super(BasicBlock, self).__init__()
            self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3,
                                   stride=stride, padding=1, bias=False)
            self.bn1 = nn.BatchNorm2d(planes)
            self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,
                                   stride=1, padding=1, bias=False)
            self.bn2 = nn.BatchNorm2d(planes)

            self.shortcut = nn.Sequential()
            # 当维度不匹配时（通道加倍或尺寸减半），通过1×1卷积调整
            if stride != 1 or in_planes != self.expansion * planes:
                self.shortcut = nn.Sequential(
                    nn.Conv2d(in_planes, self.expansion * planes,
                              kernel_size=1, stride=stride, bias=False),
                    nn.BatchNorm2d(self.expansion * planes)
                )

        def forward(self, x):
            out = F.relu(self.bn1(self.conv1(x)))
            out = self.bn2(self.conv2(out))
            out += self.shortcut(x)  # 残差连接
            out = F.relu(out)
            return out

    # ---------------------- ResNet-18 主体 ----------------------
    class zyh_nn(nn.Module):
        def __init__(self, num_classes=10):
            super(zyh_nn, self).__init__()
            self.in_planes = 64

            # 关键：第一层改为 3×3, stride=1, 无池化（专门适配 32×32）
            self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1,
                                   padding=1, bias=False)
            self.bn1 = nn.BatchNorm2d(64)
            # 四个残差组，通道数 [64, 128, 256, 512]，每组两小块
            self.layer1 = self._make_layer(64, 2, stride=1)
            self.layer2 = self._make_layer(128, 2, stride=2)
            self.layer3 = self._make_layer(256, 2, stride=2)
            self.layer4 = self._make_layer(512, 2, stride=2)
            # 全局平均池化 + 全连接
            self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
            self.linear = nn.Linear(512 * BasicBlock.expansion, num_classes)

        def _make_layer(self, planes, num_blocks, stride):
            strides = [stride] + [1] * (num_blocks - 1)
            layers = []
            for stride in strides:
                layers.append(BasicBlock(self.in_planes, planes, stride))
                self.in_planes = planes * BasicBlock.expansion
            return nn.Sequential(*layers)

        def forward(self, x):
            out = F.relu(self.bn1(self.conv1(x)))  # 32×32 → 32×32
            out = self.layer1(out)  # 32×32
            out = self.layer2(out)  # 16×16
            out = self.layer3(out)  # 8×8
            out = self.layer4(out)  # 4×4
            out = self.avgpool(out)  # 1×1
            out = out.view(out.size(0), -1) #展平，相当于Flatten()
            out = self.linear(out)
            return out

    z_nn=zyh_nn()
    loss_fn=nn.CrossEntropyLoss(label_smoothing=0.1) #0.1：标签平滑
    z_nn=z_nn.to(device)
    loss_fn=loss_fn.to(device)
    optimizer = torch.optim.SGD(z_nn.parameters(), lr=0.1,
                                momentum=0.9, weight_decay=5e-4)#学习率，动量，权重衰减

    total_train_step=0
    total_test_step=0
    epoch=100

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epoch) #余弦退火

    writers=SummaryWriter('logs4_2')

    sample_img = next(iter(train_dataloader))[0][0:1].to(device)
    writers.add_graph(z_nn, sample_img)

    for i in range(epoch):
        print(f'epoch:{i+1}________________________')
        z_nn.train()
        for data in train_dataloader:
            img,targets=data
            img=img.to(device)     #转移
            targets=targets.to(device)
            otput=z_nn(img)
            loss=loss_fn(otput,targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_train_step+=1
            if total_train_step%10==0:
                writers.add_scalar('loss',loss.item(),total_train_step)

        z_nn.eval()
        total_test_loss=0
        total_accuracy=0
        with torch.no_grad():
            for data in test_dataloader:
                img,targets=data
                img=img.to(device)
                targets=targets.to(device)
                otput=z_nn(img)
                loss=loss_fn(otput,targets)
                total_test_loss+=loss.item()
                accuracy=(otput.argmax(dim=1)==targets).sum()
                total_accuracy=total_accuracy+accuracy
        print(f'test_loss:{total_test_loss}')
        print(f'accuracy:{total_accuracy/test_data_size}')
        writers.add_scalar('test_loss',total_test_loss,total_test_step+1)
        writers.add_scalar('test_accuracy',total_accuracy/test_data_size,total_test_step+1)
        total_test_step+=1
        scheduler.step()

def train__4():
    import torch
    from torch import nn
    import torchvision
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard import SummaryWriter
    import torch.nn.functional as F
    transform_train = torchvision.transforms.Compose([
        torchvision.transforms.RandomCrop(32, padding=4),  # 先填充再随机裁剪
        torchvision.transforms.RandomHorizontalFlip(),  # 随机水平翻转
        torchvision.transforms.ToTensor(),
        torchvision.transforms.RandomErasing(p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)),#随机擦除
        torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                         (0.2023, 0.1994, 0.2010))  # CIFAR-10 标准值
    ])
    transform_test = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                         (0.2023, 0.1994, 0.2010))
    ])
    train_data=torchvision.datasets.CIFAR10('./data',train=True,transform=transform_train,download=True)
    test_data=torchvision.datasets.CIFAR10('./data',train=False,transform=transform_test,download=True)

    test_data_size=len(test_data)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    train_dataloader=DataLoader(train_data,batch_size=64,shuffle=True)
    test_dataloader=DataLoader(test_data,batch_size=64,shuffle=True)

    # ---------------------- 基础残差块 ----------------------
    class BasicBlock(nn.Module):
        expansion = 1

        def __init__(self, in_planes, planes, stride=1):
            super(BasicBlock, self).__init__()
            self.model1=nn.Sequential(
            nn.Conv2d(in_planes, planes, kernel_size=3,stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(planes),
            nn.ReLU(),
            nn.Conv2d(planes, planes, kernel_size=3,stride=1, padding=1, bias=False),
            nn.BatchNorm2d(planes)
            )
            self.shortcut = nn.Sequential()
            # 当维度不匹配时（通道加倍或尺寸减半），通过1×1卷积调整
            if stride != 1 or in_planes != self.expansion * planes:
                self.shortcut = nn.Sequential(
                    nn.Conv2d(in_planes, self.expansion * planes,
                              kernel_size=1, stride=stride, bias=False),
                    nn.BatchNorm2d(self.expansion * planes)
                )

        def forward(self, x):
            out = self.model1(x)
            out += self.shortcut(x)  # 残差连接
            out = F.relu(out)
            return out

    # ---------------------- ResNet-18 主体 ----------------------
    class zyh_nn(nn.Module):
        def __init__(self, num_classes=10):
            super(zyh_nn, self).__init__()
            self.in_planes = 64

            self.model=nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1,padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            # 四个残差组，通道数 [64, 128, 256, 512]，每组两小块
            self._make_layer(64, 2, stride=1),
            self._make_layer(128, 2, stride=2),
            self._make_layer(256, 2, stride=2),
            self._make_layer(512, 2, stride=2),
            # 全局平均池化 + 全连接
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(512 * BasicBlock.expansion, num_classes)
            )

        def _make_layer(self, planes, num_blocks, stride):
            strides = [stride] + [1] * (num_blocks - 1)
            layers = []
            for stride in strides:
                layers.append(BasicBlock(self.in_planes, planes, stride))
                self.in_planes = planes * BasicBlock.expansion
            return nn.Sequential(*layers)

        def forward(self, x):
            out = self.model(x)
            return out

    z_nn=zyh_nn()
    loss_fn=nn.CrossEntropyLoss(label_smoothing=0.1) #0.1：标签平滑
    z_nn=z_nn.to(device)
    loss_fn=loss_fn.to(device)
    optimizer = torch.optim.SGD(z_nn.parameters(), lr=0.1,
                                momentum=0.9, weight_decay=5e-4)#学习率，动量，权重衰减

    total_train_step=0
    total_test_step=0
    epoch=3

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epoch) #余弦退火

    writers=SummaryWriter('logs4_3')

    sample_img = next(iter(train_dataloader))[0][0:1].to(device)
    writers.add_graph(z_nn, sample_img)

    for i in range(epoch):
        print(f'epoch:{i+1}________________________')
        z_nn.train()
        for data in train_dataloader:
            img,targets=data
            img=img.to(device)     #转移
            targets=targets.to(device)
            otput=z_nn(img)
            loss=loss_fn(otput,targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_train_step+=1
            if total_train_step%10==0:
                writers.add_scalar('loss',loss.item(),total_train_step)

        z_nn.eval()
        total_test_loss=0
        total_accuracy=0
        with torch.no_grad():
            for data in test_dataloader:
                img,targets=data
                img=img.to(device)
                targets=targets.to(device)
                otput=z_nn(img)
                loss=loss_fn(otput,targets)
                total_test_loss+=loss.item()
                accuracy=(otput.argmax(dim=1)==targets).sum()
                total_accuracy=total_accuracy+accuracy
        print(f'test_loss:{total_test_loss}')
        print(f'accuracy:{total_accuracy/test_data_size}')
        writers.add_scalar('test_loss',total_test_loss,total_test_step+1)
        writers.add_scalar('test_accuracy',total_accuracy/test_data_size,total_test_step+1)
        total_test_step+=1
        scheduler.step()

train__4()
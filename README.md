# Python Scrapy Crawl 梨视频
（此项目仅供个人学习使用）
## 安装

### 安装Python

至少Python3.5以上

### 安装MongoDB

安装好之后将Mongodb服务开启

### 配置mongodb连接参数

进入sp_qsbk目录，修改settings.py文件
```
MONGO_URI = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'PearVideoDB'
```


#### 安装依赖

```
pip3 install -r requirements.txt
```

#### 运行

```
python3 start.py
```


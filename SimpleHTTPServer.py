现在，很多人都知道，Python 里有个 SimpleHTTPServer，可以拿来方便地共享文件。
比如，你要发送某个文件给局域网里的同学，你只要 cd 到所在路径，然后执行这么一行：
python -m SimpleHTTPServer
人家就可以通过 http://你的IP:8000 来访问你要共享的文件了。

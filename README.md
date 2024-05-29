使用本工具需要以下库:
concurrent.futures
subprocess
requests
socket

pingipsDomains
这个工具主要作用是拿到很多ip或域名之后确定哪些是通的，哪些是有云防御的，加速批量渗透测试效率。你需要将存放ip和域名的txt文件改名为ipsDomains.txt然后直接运行py文件。

scanPorts
这个工具是将pingipsDomains筛选过的在线ip和域名做进一步扫描工作，扫描出开放的端口。你需要在pingipDomains运行结束之后，或将存放ip的txt文件改名为onlineips.txt然后直接运行py文件。

bookhtml
这个工具主要作用是将scanPorts扫描出的端口，尝试用http/https的形式访问，然后做成书签，方便在burpsuitepro的谷歌浏览器一键打开所有可以访问通的页面，加速批量渗透测试效率。你需要在scanPorts运行结束之后直接执行py文件。

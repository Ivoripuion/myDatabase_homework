# myDatabase_homework
就是使用flask+mysql完成的数据库大作业，完成了一些增删查之类的功能，本来想好好写的，后来懒了，就写的很垃圾，纯粹为了完成作业，未使用cookie，几乎没有安全机制。
-----------------------------------------------------------------
## 代码说明
1. sql_all.py中是数据库创建的sqlalchemy代码
2. web.py中是网站的后端代码
3. sql.txt中是数据库创建的原生sql代码
4. onetrigger.txt中是用到的一个触发器代码
5. templates文件夹中是一些模版的代码
-----------------------------------------------------------------
使用方法：
1. 在windows的cmd进入Scripts文件夹中，使用activate的shell文件进入虚拟环境。
2. 使用set FLASK_APP=sql_all.py设置flask临时环境变量，flask shell，导入sql_all包内容，init()初始化数据库。
3. 使用set FLASK_APP=web.py设置flask临时环境变量，flask run开启服务，127.0.0.1:5000进入页面。
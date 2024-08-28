# remotemonkey
自用，简易远程开机客户端

win客户端用到了qt作为gui界面，在conf.ini中配置mqtt服务器和开机密码

单片机用的是esp8266，需要修改wifi参数才能连接

mqtt服务器使用免费的broker.emqx.io，公共账号emqx密码public

个人学习使用，不涉及商业活动，所以没有做复杂的鉴权，只用了简单的字符串匹配开机密码，安全性不高。

# Rumor Crawler

这个爬虫是用来爬取疫情期间[腾讯较真平台](https://vp.fact.qq.com/home)上面的一些关于传言的澄清和证实的。

## data description

结果以`json`的形式存储在`article.json`文件内。每个条目包含以下内容：

* title：传言标题
* subtitle：传言副标题
* label：标签
* point：描述
* source：来源

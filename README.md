
# BILIBILI爬虫项目 哔哩哔哩

## 项目简介

这个项目是一个爬虫应用，旨在从B站提取弹幕数据，评论数据。通过使用Python编程语言及其相关库（如 `requests`, `BeautifulSoup`, `Scrapy` 等），我们能够实现高效、可靠的数据抓取和处理。

参考项目如下：
- [哔哩哔哩-API收集整理](https://github.com/SocialSisterYi/bilibili-API-collect)：这是一个功能很强大的集合项目，我们的主要接口参考了它的思路。
- [Bilibili/B站视频/动态评论爬虫](https://blog.csdn.net/weixin_51869009/article/details/139638650)：我们参考其中的爬虫思路。
- 
## 项目结构

```
bilibili                                
├─ chromedriver-win64                     //浏览器驱动        
│  ├─ chromedriver.exe                  
│  ├─ LICENSE.chromedriver              
│  └─ THIRD_PARTY_NOTICES.chromedriver  
├─ chromedriver_win32                   
│  ├─ chromedriver.exe                  
│  └─ LICENSE.chromedriver                
├─ proto                                  //生成的编译文件
│  ├─ __pycache__                       
│  │  └─ dm_pb2.cpython-39.pyc          
│  ├─ dm.proto                          
│  └─ dm_pb2.py                         
├─ src                                    //项目文件
│  ├─ configs                             //biliibli配置文件
│  │  ├─ __pycache__                    
│  │  │  └─ config.cpython-39.pyc       
│  │  └─ config.py                      
│  ├─ doc                                 //爬到的数据
│  │  ├─ comments                       
│  │  │  └─ 评论_BV1jNmtYcEbY.csv         
│  │  └─ dm                             
│  │     ├─ 历史弹幕_BV14UUAYmExC.csv       
│  │     └─ 历史弹幕_BV1jNmtYcEbY.csv       
│  ├─ bilibiliComments.py                 //评论爬虫
│  ├─ bilibiliDMhistory.py                //历史弹幕爬虫
│  ├─ bilibiliDMshishi.py                 //实时弹幕爬虫
│  └─ bilibiliDMxml.py                    //xml弹幕爬虫
├─ tests                                
│  └─ test_spider.py                    
├─ __pycache__                          
├─ LICENSE                              
├─ README.md                            
└─ requirements.txt                     
                
```

## 依赖项

确保你已经安装了以下Python库。你可以使用 `pip` 来安装这些依赖项：

```bash
pip install -r requirements.txt
```

`requirements.txt` 示例：

```
requests~=2.32.3
google~=3.0.0
pytz~=2024.2
selenium~=4.27.1
urllib3~=2.2.3
```

## 运行指南

1. **安装依赖**：确保你已经安装了所有依赖项。
2. **配置**：如有需要，请根据项目需求修改配置文件或环境变量。
3. **运行爬虫**：在命令行中运行以下命令启动爬虫：

    ```bash
    python src/main.py
    ```

4. **测试**：运行测试代码以确保一切正常运行：

    ```bash
    pytest tests/
    ```

## 数据处理

抓取的数据将被存储在 `data/raw/` 目录下，处理后的数据将存储在 `data/processed/` 目录下。你可以根据具体需求对数据进行进一步处理和分析。

## 注意事项

1. **合规性**：确保爬虫行为符合目标网站的规则和相关法律法规。
2. **异常处理**：合理处理网络请求异常和解析异常，提高代码的健壮性。
3. **性能优化**：针对大规模数据抓取，考虑使用异步请求和多线程/多进程技术。

## 贡献指南

如果你有兴趣为该项目做出贡献，请遵循以下步骤：

1. Fork 本仓库。
2. 创建并切换到新的开发分支。
3. 编写代码或修复Bug。
4. 提交更改并推送到你的分支。
5. 提交Pull Request。

## 联系我们

如果你有任何问题或建议，可以通过以下方式联系我们：

- 项目主页： [项目主页链接](https://gitee.com/reisen7/bilibili-crawler)
- Git Issues： [Issues](https://gitee.com/reisen7/bilibili-crawler/issues)
- 电子邮件： [邮箱](mailto:328170849@qq.com)

---


# Httprunner-suplus

HttpRunner 是一款面向 HTTP(S) 协议的通用测试框架，只需编写维护一份 YAML/JSON 脚本，即可实现自动化测试、性能测试、线上监控、持续集成等多种测试需求。

##项目说明
测试用例分层机制的核心是将接口定义、测试步骤、测试用例、测试场景进行分离，单独进行描述和维护，从而尽可能地减少自动化测试用例的维护成本。

本文除了httprunner自带的校验器本文还通过python脚本从不同角度出发来校验测试结果。


##项目结构
- api ===> 接口封装
- auto_py ===> 自动校验计算的python脚本
- config ===> 存放token等的csv文件
- helpfunc ===> 自定义的辅助函数
- testcases ===> 测试用例
- testcases_excel ===> 测试所需导入的数据文件
- testsuites ===> 测试用例集

##项目部署
下载源码后，通过 pip 工具安装 requirements.txt 依赖，执行命令：
```
pip install -r requirements.txt
```
在根目录下新建.env文件，用于存储项目环境变量，通常用于存储项目敏感信息

注：本项目采用的公司项目，因此可能无法直接使用

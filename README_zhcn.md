# 关于PSAS

PSAS是一个基于插件的API服务器    
使用导入模块的方法实现插件挂载

Language：[en_us](README.md) zh_cn

# 特性

* 极简 单文件核心
* 多语言支持
* 同时兼容PSAS格式的response和flask原生response
* 插件冲突检测
* 专用的调试接口和静态文件存储文件夹
* 易读的toml配置文件

# 部署
> 此处暂不提供虚拟环境部署方法

1.创建文件夹用于存放PSAS/Core
```bash
mkdir PSAS && cd PSAS
```
2.克隆本仓库到本地
```bash
git clone https://github.com/ParrotSimpleAPIServer/Core.git
```
3.切换到文件夹内
```bash
cd Core
```
4.安装依赖
```bash
pip install -r requirements.txt
```
5.从仓库下载i18n支持文件并放入Core文件夹  
`https://github.com/ParrotSimpleAPIServer/i18n/blob/main/i18n.py`  

6.启动
```bash
python main.py
```
PSAS会在第一次启动时自动补全文件夹与配置文件  
通常为这些文件:
* plugins/
* statics/
* configs/main.toml
* configs/staticswhitelist.txt

# 插件系统
插件的文件结构与python模块类似  
关于插件的编写规范，详见本仓库wiki  
可下载[ExamplePlugin](https://github.com/ParrotSimpleAPIServer/ExamplePlugin)仓库中的实例插件用于演示

> [!CAUTION]
> 插件具有直接运行命令的能力，安装未经审查的插件可能导致系统遭受攻击！

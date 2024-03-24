<div align="center">
<a><img src="./logo.png" width="180" height="180"></a>
</div>

<div align="center">

# NekoInteractAPI
_✨ 一个实现MC与MCDReforged双向通信的交互API插件 ✨_  

</div>

> [!WARNING]  
> 需要搭配相应前置mod，本插件在正常情况下不需要手动安装前置mod，请确保您的服务器已经正确安装Fabric Loader

## 插件原理
通过Python的 [Websocket-Client](https://pypi.org/project/websocket-client/) 库与本插件内置mod进行通信, 用户可以通过mod的API对MCDReforged进行一系列的操作. 如`获取MCDR命令建议`和`发送MCDR命令`

前置mod库: [NekoInteractAPI](https://github.com/NekoApplications/NekoInteractAPI)

## 配置
本插件的配置文件`NekoInteractAPI.json`在MCDR根目录下的`config`文件夹内

配置项详解
```
{
    "enable": true,                    # 是否启用插件, 值类型: bool
    "websocket_host": "localhost"      # websocket服务地址, 不建议修改, 值类型: str
}
```

## 文档

- [插件内置服务接口](readme_folder/services_cn.md)

## 许可
本项目遵循 [MIT License](https://mit-license.org/) 许可

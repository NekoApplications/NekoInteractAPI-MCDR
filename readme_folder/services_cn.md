\>\>\> [返回索引](/README.md)

# 传参规范

## 请求
```
{
    "service": "",
    "requestId": "",
    "data": {}
}
```
### 请求体详解
| 参数名       | 类型     | 描述               |
|-----------|--------|------------------|
| service   | String | 调用的服务,见下文        |
| requestId | String | 唯一会话ID, 使用UUID格式 |
| data      | Map    | 传入给插件的参数         |

## 回复
```
{
    "status": 0
    "service": "",
    "requestId": "",
    "message": "",
    "data": {}
}
```
### 回复体详解
| 参数名       | 类型                  | 描述                            |
|-----------|---------------------|-------------------------------|
| status    | Integer             | 状态码, 见[状态码](./status_code.md) |
| service   | String              | 调用的服务, 与请求的相同                 |
| requestId | String              | 唯一会话ID, 与请求的相同                |
| message   | String              | 信息(通常为错误信息)                   |
| data      | Map[String, Object] | 返回的数据, 具体数据根据调用的服务变化          |

### 例子:
假设我要设置xxx的MCDR权限为Owner, 那么应该向插件传入
```
{
    "service": "mcdr_permission_set",
    "requestId": "xxx-xxx-xxx-xxx",
    "data": {
        "player": "xxx",
        "permission": "owner"
    }
}
```

# 内置服务

## mcdr_complete_command
> 用于获取MCDR指令的补全建议

#### 请求参数
| 参数名     | 类型     | 描述     |
|---------|--------|--------|
| command | String | MCDR指令 |

#### 返回参数
| 参数名         | 类型           | 描述   |
|-------------|--------------|------|
| suggestions | List[String] | 指令建议 |

---

## mcdr_send_command
> 向MCDR发送指令

#### 请求参数
| 参数名     | 类型     | 描述      |
|---------|--------|---------|
| command | String | 需要发送的指令 |

#### 返回参数
| 参数名      | 类型     | 描述   |
|----------|--------|------|
| response | String | 指令返回 |

---

## mcdr_permission_list
> 获取MCDR的所有成员权限列表

#### 请求参数
无

#### 返回参数
| 参数名      | 类型                        | 描述         |
|----------|---------------------------|------------|
| response | Map[String, List[String]] | 权限组及其成员Map |

---

## mcdr_permission_get
> 获取某个玩家的权限等级

#### 请求参数
| 参数名    | 类型     | 描述       |
|--------|--------|----------|
| player | String | 需要获取的玩家名 |

#### 返回参数
| 参数名          | 类型      | 描述       |
|--------------|---------|----------|
| player       | String  | 与获取的玩家相同 |
| permission   | String  | 权限等级     |

---

## mcdr_permission_set
> 设置某个玩家的权限等级

#### 请求参数
| 参数名        | 类型              | 描述                                                                                    |
|------------|-----------------|---------------------------------------------------------------------------------------|
| player     | String          | 需要获取的玩家名                                                                              |
| permission | String, Integer | 权限等级, 见[MCDR权限梗概](https://docs.mcdreforged.com/zh-cn/latest/permission.html#overview) |

#### 返回参数
| 参数名      | 类型     | 描述   |
|----------|--------|------|
| response | String | 执行返回 |

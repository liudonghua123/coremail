# Coremail XT 高级API（apiws v3-2）使用手册

## 版权声明

本文档版权归Coremail®所有，并保留一切权利。未经书面许可，任何公司和个人不得将此文档中的任何部分公开、转载或以其他方式散发给第三方。否则，必将追究其法律责任。

## 免责声明

本文档仅提供阶段性信息，所含内容可根据产品的实际情况随时更新，恕不另行通知。如因文档使用不当造成的直接或间接损失，本公司不承担任何责任。

## 文档信息

- **文档更新**: 由Coremail®于2022年10月最后修订
- **公司网站**: http://www.coremail.cn
- **销售咨询热线**: 400-000-1631
- **技术支持热线**: 400-630-7163

### 文档修改记录

| 版本 | 修改日期 | 修改人员 | 修改记录 |
|------|----------|----------|----------|
| V1 | 2022-10-24 | 黄飞飞 | 文档修订 |
| V2 | 2024-10-14 | 黄湖津 | 文档修订 |

## 目录

1. [介绍](#1-介绍)
2. [开始开发](#2-开始开发)
3. [Coremail XT API 接口具体功能应用说明](#3-coremail-xt-api-接口具体功能应用说明)
4. [附录](#4-附录)

## 1. 介绍

### 1.1 服务介绍

- **服务名称**: Coremail XT 高级API
- **服务提供者**: apiws 服务
- **底层服务**: rmisvr 服务
- **封装目的**: 提供更加安全、适用性更强的调用方式

### 1.2 API 版本

- **v1**: webservices 接口，仅支持IP信任，存在安全问题，已不建议使用
- **v2**: webservices 接口，支持IP和API用户授权，更加安全
- **v3**: restful HTTP接口，基于标准JSON格式进行数据交换，调用更加方便，推荐使用
- **v1/v2**: 依赖于Apache CXF 提供SOAP接口服务，存在潜在的安全风险，建议逐渐迁移到v3版本

### 1.3 文档范围

- **说明对象**: v3接口
- **目标用户**: 开发人员和技术支持人员

## 2. 开始开发

### 2.1 获取 app_id 和 secure

#### 2.1.1 云平台客户
如是云平台客户，则联系运维人员SA提供。

#### 2.1.2 自建客户

**步骤1: 创建API用户**
在管理后台创建用户作为API用户，其中邮件地址就是app_id，密码就是对应secure。

**步骤2: 授权**
通过命令行进行授权的执行方法：
```bash
userutil --set-user-attr <user_name> api_acl=<acl_value>
```

**授权格式规范**:
- `"@all"` 是特殊字符串，表示最高授权
- 其余为逗号分隔的授权，每个授权的格式是 `<org>:<permission>` 或 `<org>`
- 前者忽略 `<permission>` 部分表示默认授权，默认的授权为读写授权
- `<permission>` 可以是空串，也是默认授权，除此以外还可以有以下取值：
  - `'r'` / `'ro'` 均表示只读授权
  - `'rw'` 是读写授权

**授权示例**:

1. 授权user1为最高级别，允许操纵所有方法，和IPLimit的授权等同：
   ```bash
   userutil --set-user-attr user1 api_acl=@all
   ```

2. 授权user2的访问：对org1/org3/org4为读写权限，org2为只读权限：
   ```bash
   userutil --set-user-attr user2 api_acl=org1:rw,org2:r,org3,org4
   ```

### 2.2 开发对接相关接口

当应用调用apiws v3接口时，需使用以下规范：

- **协议**: HTTPS
- **数据格式**: JSON
- **编码**: UTF-8
- **访问路径**: `https://<host>/apiws/v3`
- **数据包**: 不需要加密

在每次调用API接口时需要带上`_token`参数。`_token`参数由app_id和secure换取。app_id是应用的标识，每个应用拥有一个唯一个app_id。

当应用调用API接口时，apiws服务根据此次访问的`_token`，校验访问的合法性。

## 3. Coremail XT API 接口具体功能应用说明

### 3.1 Access Token

#### 3.1.1 获取凭证

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/requestToken`
- **请求包结构体**:
```json
{
  "app_id": "api1@api.cn",
  "secret": "admin123"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| app_id | string | 是 | 应用标识 |
| secret | string | 是 | 应用的凭证密钥 |

**权限说明**:
准备好应用ID及密钥。

**返回结果**:
```json
{
  "code": 0,
  "result": "BAIhsYOOtvcxPysxzodDuzbTLhUlOnwD07ff68891ce48bb3a2c53c3712ee8501"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 获取到的授权凭证Token。所有的接口调用都需要带上此Token，才能正常进行接口访问。Token过期时间默认为1个小时（可配置） |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/requestToken" \
-H "Content-Type: application/json" \
-d '{ "app_id" : "api1@api.cn", "secret" : "admin123" }'
```

### 3.2 登录

#### 3.2.1 用户登录

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/userLogin`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "user_at_domain": "a1@dev.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "BAHhsYOOybNsnHMWBlNmFILnEavPFYwD"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 用户登录会话ID (sid) |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userLogin" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "user_at_domain" : "a1@dev.cn" }'
```

#### 3.2.2 用户登录，使用附加参数，并返回额外的信息

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/userLoginEx`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "user_at_domain": "a1@dev.cn",
  "attrs": "remote_ip=192.168.201.165&cookieKey=Coremail&cookiecheck=123"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |
| attrs | string | 否 | 操作属性，格式为urlencode字符串。属性值中如果有特殊字符必须用url的方式编码，如等于号"="编码为"%3D" |

**操作属性说明**:

| 属性名 | 属性含义 |
|--------|----------|
| type | 登录类型：例如"WEB" / "API"（默认）这样的字符串（Coremail XT U3后才支持）。所有支持的类型包括："WEB" / "POP3" / "IMAP" / "SMTP" /"API" |
| remote_ip | 登录用户的IP |
| ipcheck | 仅为"1"时表示需要检查浏览器的IP |
| cookieKey | 检查浏览器的cookie名称 |
| cookiecheck | 检查浏览器的cookie值 |
| face | 登录的风格 |

**权限说明**:
系统应用须拥有用户所在组织权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "sid=BAehsYOOHknssAvQWHORDOnOLEsSNJKD&webname=http://mail.dev.cn"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回为encode的用户属性字符串："sid=[用户的session id]&webname=[web主机前缀]"；web主机前缀包含协议,机器IP,端口部分，并且结尾不包含"/"符号。例如: http://web1.abc.com 又如: http://web2.abc.com:8080 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userLoginEx" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "user_at_domain" : "a1@dev.cn", "attrs": "remote_ip=192.168.201.165&cookieKey=Coremail&cookiecheck=123" }'
```

#### 3.2.3 检查用户是否存在

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/userExist`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "user_at_domain": "a1@dev.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "udid=1"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回用户所在的UD标识 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userExist" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "user_at_domain" : "a1@dev.cn" }'
```

#### 3.2.4 验证用户密码

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/authenticate`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "user_at_domain": "a1@dev.cn",
  "password": "admin1234"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |
| password | string | 是 | 用户密码 |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码，0表示密码验证成功 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/authenticate" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "user_at_domain" : "a1@dev.cn", "password" : "admin1234" }'
```

#### 3.2.5 检查用户的会话，返回用户信息

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/sesTimeOut`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID（sid） |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "uid=a1@dev.cn&domain_id=1&org_id=apitest"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 操作成功时，返回的格式为：uid=...@...&domain_id=...&org_id=...，而uid为user@domain的格式。即用户的邮件地址。 |
| message | 会话检查不成功时返回。错误代码包括：SESSION_NOT_FOUND：session ID不存在或已经过时。或其它值: 其它的session错误 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/sesTimeOut" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD" }'
```

#### 3.2.6 检查用户的会话，并刷新访问时间

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/sesRefresh`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID（sid） |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息，表示传入的是合法的session，并且已经刷新。 |
| message | 会话检查不成功时返回。错误代码包括：SESSION_NOT_FOUND：session ID不存在或已经过时。或其它值: 其它的session错误 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/sesRefresh" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD" }'
```

#### 3.2.7 获取用户session中的变量

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getSessionVar`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD",
  "ses_key": "uidatdomain"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID（sid） |
| ses_key | string | 是 | 要获取的保存在会话的变量名 |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "a1@dev.cn"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 要获取变量值 |
| message | 会话检查不成功时返回。错误代码包括：SESSION_NOT_FOUND：session ID不存在或已经过时。或其它值: 其它的session错误 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getSessionVar" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD", "ses_key" : "uidatdomain" }'
```

#### 3.2.8 注销用户会话

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/userLogout`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID（sid） |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回码没有其它信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userLogout" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD" }'
```

#### 3.2.9 设置用户会话中的变量

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/setSessionVar`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "ses_id": "BAyhsYOOeaCsSVQABZahowtpqTvPFYwD",
  "ses_key": "TEST_VAR",
  "ses_var": "TEST_VAR_VALUE"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID（sid） |
| ses_key | string | 是 | 要设置的变量名 |
| ses_var | string | 是 | 要设置的变量名对应的value |

**权限说明**:
系统应用须拥有用户所在组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 会话检查不成功时返回。错误代码包括：SESSION_NOT_FOUND：session ID不存在或已经过时。或其它值: 其它的session错误 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/setSessionVar" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "ses_id" : "BAyhsYOOeaCsSVQABZahowtpqTvPFYwD", "ses_key" : "TEST_VAR", "ses_var" : "TEST_VAR_VALUE" }'
```

### 3.3 组织维护

#### 3.3.1 创建组织

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/addOrg`
- **请求包结构体**:
```json
{
  "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
  "org_id": "apitest",
  "attrs": {
    "org_name": "API 测试组织",
    "domain_name": "api.cn",
    "cos_id": [1],
    "num_of_classes": [1000],
    "org_status": 0,
    "org_expiry_date": "2025-01-01"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| attrs | string/object | 否 | 企业组织属性 |

**组织属性说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| org_name | string | 组织名称，如不提供则将使用org_id作为组织名称 |
| domain_name | string | 分配域名(将自动创建)，可传递数组同时分配多个域名 |
| cos_id | int/array | 分配服务等级，可传递数组比如[1, 3, 5]同时分配多个服务等级 |
| num_of_classes | int/array | 分配服务等级数量，如果cos_id传递了数组，这里也应传数组，并确保一一对应 |
| res_grp_id | string | 组织资源分组标识 |
| org_assignable_quota | int | 组织可分配容量(MB) |
| org_status | int | 组织状态，0-正常; 1-停用，2-锁定 |
| org_expiry_date | string | 过期日期。NULL或者空表示不过期。格式为:yyyy-MM-dd |
| org_options | int | 组织增值服务 |
| org_active_options | int | 启用的组织增值服务 |
| org_address | string | 组织通讯录地址 |
| org_phone_number | string | 组织联系电话 |
| org_contact | string | 组织联系人 |
| org_access_level | int | 组织可见性，0-公开; 1-组织内及授权用户可见，-1-授权用户可见 |
| org_access_user | string | 组织通讯录授权列表 |
| org_deny_user | string | 组织通讯录禁止列表 |
| org_access_user_l1 | string | 组织通讯录特殊授权 |
| email_allow_user | string | 群发授权列表 |

**权限说明**:
系统应用须拥有站点写权限（SITE_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回码没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addOrg" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8", "org_id" : "apitest", "attrs" : { "org_name" : "API 测试组织", "domain_name" : "api.cn", "cos_id" : [1], "num_of_classes" : [1000], "org_status" : 0, "org_expiry_date" : "2025-01-01" } }'
```

#### 3.3.2 获取组织属性

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getOrgInfo`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "attrs": {
    "org_name": null,
    "domain_name": null,
    "used_quota_delta": null,
    "used_mail_quota_delta": null
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| attrs | string/object | 否 | 要获取的组织属性 |

**组织属性attrs可用属性**:

| 属性名 | 属性含义 |
|--------|----------|
| - | 不传attrs，默认返回所有普通属性，参考[组织属性表]，不包括COS分配内容 |
| cos_info | 分配服务等级信息 |
| total_users | 通过COS分配的用户总数 |
| used_users | 已创建账号数量 |
| used_quota_delta | 已创建账号的额外容量总和(MB，对应org_assignable_quota分配部分) |
| used_mail_quota_delta | 其中，分配给已创建的账号的邮箱额外容量总和 |
| used_nf_quota_delta | 其中，分配给已创建的账号的网盘额外容量总和 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": {
    "org_name": "API 测试组织",
    "org_status": 0,
    "org_expiry_date": "2025-01-01",
    "domain_name": "api.cn",
    "cos_info": "1:1000:0:缺省服务",
    "used_quota_delta": 0,
    "used_mail_quota_delta": 0,
    "used_nf_quota_delta": 0,
    "total_users": 1000,
    "used_users": 0
  }
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 获取的组织属性 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgInfo" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "attrs" : { "org_name" : null, "domain_name" : null, "org_status" : null, "org_expiry_date" : null, "cos_info" : null, "total_users" : null, "used_users" : null, "used_quota_delta" : null, "used_mail_quota_delta" : null, "used_nf_quota_delta" : null } }'
```

#### 3.3.3 修改组织属性

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/alterOrg`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "attrs": {
    "org_name": "API 测试组织- 修改",
    "org_expiry_date": "2024-09-11"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| attrs | string/object | 否 | 企业组织属性请参考[组织属性表]说明，可更新除COS及域名分配以外的属性 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/alterOrg" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "attrs" : { "org_name" : "API 测试组织- 修改", "org_expiry_date" : "2024-09-11" } }'
```

#### 3.3.4 添加组织域名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/addOrgDomain`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "domain_name": "dev.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| domain_name | string | 是 | 域名，域名需要预先创建 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addOrgDomain" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "domain_name" : "dev.cn" }'
```

#### 3.3.5 删除组织域名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/delOrgDomain`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "domain_name": "dev.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| domain_name | string | 是 | 要删除的域名 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delOrgDomain" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "domain_name" : "dev.cn" }'
```

#### 3.3.6 增加组织服务等级

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/addOrgCos`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "cos_id": 8,
  "num_of_classes": 100
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_name | string | 否 | 服务等级名称，cos_name/cos_id二选一，优先使用cos_name |
| cos_id | int | 否 | 服务等级标识 |
| num_of_classes | int | 是 | 可分配用户数 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addOrgCos" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "cos_id" : 8, "num_of_classes" : 100 }'
```

#### 3.3.7 更新组织服务等级

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/alterOrgCos`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "cos_id": 8,
  "num_of_classes": 99
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_name | string | 否 | 服务等级名称，cos_name/cos_id二选一，优先使用cos_name |
| cos_id | int | 否 | 服务等级标识 |
| num_of_classes | int | 是 | 可分配用户数 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/alterOrgCos" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "cos_id" : 8, "num_of_classes" : 99 }'
```

#### 3.3.8 删除组织服务等级

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/delOrgCos`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "cos_id": 8
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_name | string | 否 | 服务等级名称，cos_name/cos_id二选一，优先使用cos_name |
| cos_id | int | 否 | 服务等级标识 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delOrgCos" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "cos_id" : 8 }'
```

#### 3.3.9 列出指定组织某服务等级下的所有用户名列表

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/listUserIdsByCos`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "cos_id": 1
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_name | string | 否 | 服务等级名称，cos_name/cos_id二选一，优先使用cos_name |
| cos_id | int | 否 | 服务等级标识 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "apitest1@api.cn,apitest2@api.cn,apitest3@api.cn"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回为用户名列表，","分隔 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/listUserIdsByCos" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "cos_id" : 1 }'
```

#### 3.3.10 获取组织列表

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getOrgList`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |

**权限说明**:
系统应用须拥有站点读权限（SITE_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "apitest,api"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回为组织标识列表，","分隔 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgList" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13" }'
```

### 3.4 部门维护

#### 3.4.1 创建部门

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/addOrgUnit`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "org_unit_id": "test",
  "attrs": {
    "org_unit_name": "API测试部门",
    "parent_org_unit_id": "1"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| org_unit_id | string | 是 | 部门标识 |
| attrs | string/object | 否 | 部门属性 |

**部门属性说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| org_unit_name | string | 部门名称 |
| parent_org_unit_id | string | 上级部门标识，默认为根部门 |
| org_unit_list_rank | int | 排序号 |
| dont_flush_md | boolean | 是否立即刷新通讯录缓存，false-否，true-是 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addOrgUnit" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "org_unit_id" : "test", "attrs" : { "org_unit_name" : "API测试部门", "parent_org_unit_id" : "1" } }'
```

#### 3.4.2 删除部门

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/delOrgUnit`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "org_unit_id": "test"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| org_unit_id | string | 是 | 部门标识 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delOrgUnit" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "org_unit_id" : "test" }'
```

#### 3.4.3 获取部门属性

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getOrgUnitInfo`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "org_unit_id": "test",
  "attrs": {
    "org_unit_name": null,
    "parent_org_unit_id": null,
    "org_unit_list_rank": null
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| org_unit_id | string | 是 | 部门标识 |
| attrs | string/object | 否 | 要获取的部门属性 |

**部门属性**:

| 属性名 | 属性含义 |
|--------|----------|
| org_unit_name | 部门名称 |
| parent_org_unit_id | 上级部门标识 |
| org_unit_list_rank | 排序号 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": {
    "org_unit_name": "API测试部门",
    "parent_org_unit_id": "1",
    "org_unit_list_rank": 10
  }
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 获取的部门属性 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgUnitInfo" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "org_unit_id" : "test", "attrs" : { "org_unit_name" : null, "parent_org_unit_id" : null, "org_unit_list_rank" : null } }'
```

#### 3.4.4 设置部门属性

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/alterOrgUnit`
- **请求包结构体**:
```json
{
  "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
  "org_id": "apitest",
  "org_unit_id": "test",
  "attrs": {
    "org_unit_name": "API测试部门-修改",
    "org_unit_list_rank": 10
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| org_unit_id | string | 是 | 部门标识 |
| attrs | string/object | 否 | 要修改的部门属性 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/alterOrgUnit" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13", "org_id" : "apitest", "org_unit_id" : "test", "attrs" : { "org_unit_name" : "API测试部门-修改", "org_unit_list_rank" : 10 } }'
```

### 3.5 用户维护

#### 3.5.1 创建用户

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/createUser`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "provider_id": "1",
  "org_id": "apitest",
  "user_at_domain": "apitest3@api.cn",
  "attrs": {
    "org_unit_id": "1",
    "user_status": 0,
    "password": "test123",
    "cos_id": 1,
    "privacy_level": 4,
    "true_name": "测试用户3"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| provider_id | string | - | - |
| org_id | string | 是 | 组织标识 |
| user_at_domain | string | 是 | 账号，别名，主键信息 |
| attrs | string/object | 是 | 用户属性 |

**用户属性说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| primary_email | string | 指定额外的主邮件地址 |
| alias | array of string | 指定额外的别名邮件地址 |
| org_unit_id | string | 部门标识 |
| user_status | int | 用户状态:0-活跃;1-停用;2-维护中；3-代理状态;4-锁定;100-延迟删除 |
| password | string | 用户密码 |
| cos_id | int | 服务等级标识 |
| quota_delta | int | 附加的邮箱空间大小，单位：MB |
| nf_quota_delta | int | 附加的网盘空间大小，单位:MB |
| privacy_level | int | 信息公开(在组织通讯录中显示),0-不公开;2-组织内公开;4-站点内公开 |
| user_list_rank | int | 排序号 |
| true_name | string | 账号名称(姓名) |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别，常用取值:"0"-男，"1"-女 |
| birthday | string | 生日 |
| alt_email | string | 备用邮箱地址 |
| mobile_number | string | 手机号码 |
| home_phone | string | 家庭电话 |
| company_phone | string | 公司电话 |
| fax_number | string | 传真号码 |
| province | string | 省份/州 |
| city | string | 城市 |
| anniversary | string | 周年纪念日 |
| zipcode | string | 邮政编码 |
| address | string | 联系地址 |
| homepage | string | 公司主页 |
| remarks | string | 备注 |
| user_security_role | int | 人员身份 |
| security_level | int | 收信密级 |
| sender_security_level | int | 发信密级 |
| smsaddr | string | 绑定手机号 |
| second_auth_type | int | 二次验证类型, 1-关闭, 2-短信, 4-APP授权 |

**邮件列表相关**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| forwardactive | int | 是否开启转发(邮件列表该属性值必须为1) |
| rejectjunk | int | 垃圾邮件处理方式(邮件列表该属性必须为1) |
| maillist_filter | string | 邮件列表的动态列表规则使用url编码字符串，格式为"^key1=value1&key2=value2&..."，其中可选key及含义为：org_id:组织标识；org_unit_id:部门标识；recursive:是否包含子部门，false-不包含，true-包含；type:用户类型，"U"-用户;"X"-外部联系人;"R"-会议室;"L"-邮件列表；includelist:用户列表，格式"user1,user2,..."；excludelist:除排用户列表，格式与includelist一致 |
| junkfilter | int | 邮件列表的授权范围(用户), 0-允许所有用户; 2-允许列表成员和指定用户; 3-只允许指定用户 |
| safelist | string | 邮件列表的授权列表，格式"user1,user2,..." |
| forwardmaillist | string | 邮件列表的用户列表(成员)，格式"user1,user2,..." |
| maillist_errorto | string | 邮件列表的退信接收地址列表，格式"user1,user2,..." |

**会议室相关**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| access_user | string | 授权使用列表 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/createUser" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "provider_id" : "1", "org_id" : "apitest", "user_at_domain" : "apitest3@api.cn", "attrs" : { "org_unit_id" : "1", "user_status" : 0, "password" : "test123", "cos_id" : 1, "privacy_level" : 4, "true_name" : "测试用户3" } }'
```

#### 3.5.2 删除用户

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/deleteUser`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "user_at_domain": "apitest3@api.cn",
  "preserve_days": 0
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| preserve_days | string | 是 | 延迟删除天数，传参0为立即删除，默认行为(等价于传参-1)取决于系统设定 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/deleteUser" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "user_at_domain" : "apitest3@api.cn", "preserve_days" : 0 }'
```

#### 3.5.3 用户属性获取

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getAttrs`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "user_at_domain": "apitest3@api.cn",
  "attrs": {
    "org_unit_id": null,
    "user_status": null,
    "cos_id": null
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| attrs | object | 否 | 请参考[用户属性表]。不传默认获取全部属性。 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": {
    "org_unit_id": "1",
    "user_status": "0",
    "cos_id": "1",
    "privacy_level": "4",
    "true_name": "测试用户3"
  }
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 获取属性值 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getAttrs" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "user_at_domain" : "apitest3@api.cn", "attrs" : { "org_unit_id" : null, "user_status" : null, "cos_id" : null, "privacy_level" : null, "true_name" : null } }'
```

#### 3.5.4 用户属性变更

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/changeAttrs`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "user_at_domain": "apitest3@api.cn",
  "attrs": {
    "org_unit_id": null,
    "true_name": "测试用户3-修改"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| attrs | object | 否 | 请参考[用户属性表]。 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| result | 获取属性值 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/changeAttrs" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "user_at_domain" : "apitest3@api.cn", "attrs" : { "org_unit_id" : null, "true_name" : "测试用户3-修改" } }'
```

#### 3.5.5 添加别名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/addSmtpAlias`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "user_at_domain": "apitest3@api.cn",
  "alias_user_at_domain": "api3@api.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| alias_user_at_domain | string | 是 | 别名邮件地址 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 错误信息 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addSmtpAlias" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "user_at_domain" : "apitest3@api.cn", "alias_user_at_domain" : "api3@api.cn" }'
```

#### 3.5.6 删除别名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/delSmtpAlias`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "user_at_domain": "apitest3@api.cn",
  "alias_user_at_domain": "api3@api.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| alias_user_at_domain | string | 是 | 要删除的别名邮件地址 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 错误信息 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delSmtpAlias" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "user_at_domain" : "apitest3@api.cn", "alias_user_at_domain" : "api3@api.cn" }'
```

#### 3.5.7 获取别名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getSmtpAlias`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "user_at_domain": "apitest3@api.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "api3@api.cn,api_test3@api.cn,api_test_3@api.cn"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回为要获取的用户smtp别名列表，","分隔 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getSmtpAlias" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "user_at_domain" : "apitest3@api.cn" }'
```

#### 3.5.8 设置用户的管理员身份

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/setAdminType`
- **请求包结构体**:
```json
{
  "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
  "user_at_domain": "apitest3@api.cn",
  "attrs": {
    "admin_type": "OA",
    "role_id": 3
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| attrs | string | 是 | 管理员属性 |

**管理员属性attrs说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| admin_type | string | 管理员级别。没有传默认设置为组织管理员（OA） |
| role_id | int | 管理员角色标识，详见td_admin_role表定义 |
| cross_manage_scope | string | 管理范围, 仅适用于自定义组织管理员(302)和自定义部门管理员(402) |

**权限说明**:
系统应用须拥有站点写权限（SITE_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 错误信息 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/setAdminType" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7", "user_at_domain" : "apitest3@api.cn", "attrs" : { "admin_type" : "OA", "role_id" : 3 } }'
```

#### 3.5.9 获取用户的管理员身份

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getAdminType`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "user_at_domain": "apitest3@api.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "admin_type=OA&role_id=3"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| result | 返回管理员身份信息，参考[设置用户的管理员身份]的管理员属性说明 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getAdminType" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "user_at_domain" : "apitest3@api.cn" }'
```

#### 3.5.10 修改用户主标识

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/renameUser`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "user_at_domain": "apitest3@api.cn",
  "new_user_id": "apitest3_new"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| new_user_id | string | 是 | 新的用户标识 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 错误信息 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18sl/v3/renameUser" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "user_at_domain" : "apitest3@api.cn", "new_user_id" : "apitest3_new" }'
```

#### 3.5.11 用户跨组织移动

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/moveUser`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "user_at_domain": "apitest1@api.cn",
  "attrs": {
    "org_id": "api",
    "org_unit_id": "test"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| attrs | object | 是 | 用户新位置/属性 |
| org_id | - | - | 新组织标识符 |
| org_unit_id | - | - | 新部门标识符，默认为根部门 |

**权限说明**:
系统应用须拥有站点写权限（SITE_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 错误信息 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/moveUser" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "user_at_domain" : "apitest1@api.cn", "attrs" : { "org_id" : "api", "org_unit_id" : "test" } }'
```

### 3.6 联系人维护

#### 3.6.1 创建联系人

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/createObj`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "attrs": {
    "org_id": "apitest",
    "org_unit_id": "1",
    "obj_class": 1,
    "obj_email": "test@coremail.cn"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| attrs | string/object | 是 | 联系人属性 |

**联系人属性attrs说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| org_id | string | 组织标识 |
| org_unit_id | string | 部门标识 |
| obj_class | int | 对象类型，1-外部联系人; 100-影子用户; 101-影子邮件列表 |
| obj_email | string | 外部联系人的邮箱地址 |
| obj_creation_date | string | 外部联系人创建时间，缺省为当前时间 |
| privacy_level | int | 信息公开(在组织通讯录中显示), 0-不公开; 2-组织内公开; 4-站点内公开 |
| obj_list_rank | int | 排序号 |
| true_name | string | 账号名称(姓名) |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别，常用取值: "0"-男，"1"-女 |
| birthday | string | 生日 |
| alt_email | string | 备用邮箱地址 |
| mobile_number | string | 手机号码 |
| home_phone | string | 家庭电话 |
| company_phone | string | 公司电话 |
| fax_number | string | 传真号码 |
| province | string | 省份/州 |
| city | string | 城市 |
| anniversary | string | 周年纪念日 |
| zipcode | string | 邮政编码 |
| address | string | 联系地址 |
| homepage | string | 公司主页 |
| remarks | string | 备注 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0,
  "result": {
    "obj_uid": "1_test_19289d00137"
  }
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回联系人标识。记录这个对象标识obj_uid，之后获取/变更联系人信息和删除联系人需要通过这个对象标识来操作。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/createObj" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "attrs" : { "org_id" : "apitest", "org_unit_id" : "1", "obj_class" : 1, "obj_email" : "test@coremail.cn" } }'
```

#### 3.6.2 联系人属性获取

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getObjAttrs`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "obj_uid": "1_test_19289d00137",
  "attrs": {
    "org_id": null,
    "org_unit_id": null,
    "obj_class": null,
    "obj_email": null
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| obj_uid | string | 是 | 联系人标识，创建联系人返回 |
| attrs | string/object | 否 | 要获取的联系人属性。具体参考[联系人属性表]。不传默认获取全部属性。 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": {
    "org_id": "apitest",
    "org_unit_id": "1",
    "obj_class": 1,
    "obj_email": "test@coremail.cn"
  }
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回要获取的联系人属性 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getObjAttrs" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "obj_uid" : "1_test_19289d00137", "attrs" : { "org_id" : null, "org_unit_id" : null, "obj_class" : null, "obj_email" : null } }'
```

#### 3.6.3 联系人属性变更

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/setObjAttrs`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "obj_uid": "1_test_19289d00137",
  "attrs": {
    "obj_email": "test-change@coremail.cn"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| obj_uid | string | 是 | 联系人标识，创建联系人返回 |
| attrs | string/object | 否 | 要修改的联系人属性。具体参考[联系人属性表]。 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/setObjAttrs" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "obj_uid" : "1_test_19289d00137", "attrs" : { "obj_email" : "test-change@coremail.cn" } }'
```

#### 3.6.4 删除联系人

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/deleteObj`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "obj_uid": "1_test_19289d00137"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| obj_uid | string | 是 | 联系人标识，创建联系人返回 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/deleteObj" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "obj_uid" : "1_test_19289d00137" }'
```

### 3.7 域名维护

#### 3.7.1 检查域名或者域名别名是否存在

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/domainExist`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "domain_name": "api.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 要检查的域名 |

**权限说明**:
系统应用须拥有站点读权限（SITE_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "api.cn"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 存在返回检查的域名 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/domainExist" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "domain_name" : "api.cn" }'
```

#### 3.7.2 列出系统所有域名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getDomainList`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |

**权限说明**:
系统应用须拥有站点读权限（SITE_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "api.cn,test.cn,dev.cn"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回为域名列表，","分隔 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getDomainList" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c" }'
```

#### 3.7.3 增加域名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/addDomain25`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "domain_name": "api2.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 要增加的域名 |

**权限说明**:
系统应用须拥有站点写权限（SITE_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addDomain25" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "domain_name" : "api2.cn" }'
```

#### 3.7.4 删除域名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/delDomain25`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "domain_name": "api2.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 要删除的域名 |

**权限说明**:
系统应用须拥有站点写权限（SITE_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delDomain25" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "domain_name" : "api2.cn" }'
```

#### 3.7.5 增加域别名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/addDomainAlias`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "domain_name": "api.cn",
  "domain_name_alias": "api-alias.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 域名 |
| domain_name_alias | string | 是 | 要增加的域别名 |

**权限说明**:
系统应用须拥有站点写权限（SITE_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addDomainAlias" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "domain_name" : "api.cn", "domain_name_alias" : "api-alias.cn" }'
```

#### 3.7.6 列出指定域的所有域名别名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getDomainAlias`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "domain_name": "api.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 域名 |

**权限说明**:
系统应用须拥有站点读权限（SITE_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "api-alias.cn,api-alias2.cn"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回为指定域名的域别名列表，","分隔 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getDomainAlias" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "domain_name" : "api.cn" }'
```

#### 3.7.7 删除域别名

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/delDomainAlias`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "domain_name": "api.cn",
  "domain_name_alias": "api-alias.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 域名 |
| domain_name_alias | string | 是 | 要删除的域别名 |

**权限说明**:
系统应用须拥有站点写权限（SITE_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delDomainAlias" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "domain_name" : "api.cn", "domain_name_alias" : "api-alias.cn" }'
```

#### 3.7.8 列出使用了指定域名的组织列表

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getOrgListByDomain`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "domain_name": "api.cn"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 域名 |

**权限说明**:
系统应用须拥有站点读权限（SITE_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": "api,apitest"
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回使用了指定域名的组织标识列表，","分隔 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgListByDomain" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "domain_name" : "api.cn" }'
```

### 3.8 邮件维护

#### 3.8.1 列举用户信件

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/listMailInfos`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "user_at_domain": "apitest2@api.cn",
  "options": {
    "limit": 1,
    "fid": 1,
    "skip": 0,
    "order": "receivedDate"
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| options | object | 否 | 查询选项 |

**查询选项options属性说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| limit | int | 限制条数，默认不限制 |
| fid | int | 文件夹标识，默认为收件箱 |
| skip | int | 跳过条数，默认为0 |
| order | string | 排序控制，desc后缀表示倒序排列，默认是按时间倒序排列。支持的排序关键字包括：from-按发件人排序；to-按收件人排序；subject-按主题排序；size-按邮件大小排列；status-按邮件状态排序；date-按发送时间排序；receivedDate-按接收时间排序。支持使用感叹号"!"添加前缀，表示标志位优先排序，并且可以使用"~"表示反向标志位，比如: !~read!date desc:未读邮件优先，按发送日期倒序排列，这也是默认使用的排序；!attached!size desc:有附件的邮件优先，按邮件大小倒序排列。默认值: "~date" |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": {
    "mail": [
      {
        "mid": "1tbiAQAJE2cLeFcAAQAAsZ",
        "msid": 1,
        "fid": 1,
        "flag": 1073741912,
        "from": "postmaster@api.cn",
        "to": "apitest2@api.cn",
        "subject": "欢迎使用Coremail电子邮件系统/Welcome to the Coremail e-mail system",
        "size": 7735,
        "date": "2024-10-13 20:44:35"
      }
    ]
  }
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回用户信件列表 |

**信件属性说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| mid | string | 信件标识 |
| msid | int | 信件所在ms标 |
| fid | int | 信件文件夹标识 |
| flag | int | 标志位 |
| from | string | 发件人 |
| to | string | 收件人 |
| subject | string | 邮件主题 |
| size | int | 邮件大小 |
| date | string | 邮件发送时间 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/listMailInfos" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "user_at_domain" : "apitest2@api.cn", "options" : { "limit" : 1, "fid" : 1, "skip" : 0, "order" : "receivedDate" } }'
```

#### 3.8.2 获取用户未读信件列表

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/getNewMailInfos`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "user_at_domain": "apitest2@api.cn",
  "options": {
    "limit": 1,
    "excludeFidList": [],
    "doubleDecode": false,
    "format": ""
  }
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| options | object | 否 | 查询选项 |

**查询选项options属性说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| limit | int | 限制条数，默认不限制 |
| excludeFidList | array | 排除的文件夹列表 |
| doubleDecode | boolean | 是否对收发件人、邮件主题进行解码 |
| format | string | 返回结果格式，指定为"xml"，才能得到可分析的XML格式的返回结果 |

**权限说明**:
系统应用须拥有对应组织读权限（ORG_READ）

**返回结果**:
```json
{
  "code": 0,
  "result": [
    {
      "mid": "1tbiAQAJE2cLeFcAAQAAsZ",
      "msid": 1,
      "fid": 1,
      "flag": 1073741912,
      "from": "postmaster@api.cn",
      "to": "apitest2@api.cn",
      "subject": "欢迎使用Coremail电子邮件系统/Welcome to the Coremail e-mail system",
      "size": 7735,
      "date": "2024-10-13 20:44:35"
    }
  ]
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码 |
| result | 返回查询未读邮件列表。具体参考[信件属性表]。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getNewMailInfos" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "user_at_domain" : "apitest2@api.cn", "options" : { "limit" : 1, "excludeFidList" : [], "doubleDecode" : false, "format" : "" } }'
```

#### 3.8.3 通过MTA投递信件

**请求说明**:
- **HTTP请求方式**: POST
- **请求地址**: `/apiws/v3/smtpTransport`
- **请求包结构体**:
```json
{
  "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
  "mail_from": "apitest1@api.cn",
  "rcpt_to": "apitest2@api.cn",
  "data": "Subject: Test smtpTransport api\nContent-Type: text/plain; charset=UTF-8\n\nTest smtpTransport api"
}
```

**参数说明**:

| 参数名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| _token | string | 是 | 授权凭证Token |
| mail_from | string | 否 | 发件人。可以不传递或者传递空串，表示直接从data中获取。 |
| rcpt_to | string | 否 | 收件人。可以不传递或者传递空串，表示直接从data中获取。 |
| data | string | 是 | 邮件内容(message/rfc822格式) |
| options | object | 否 | 投递选项 |

**投递选项options属性说明**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| remote_ip | string | 远程IP |
| X-Coremail-Context | string | 邮件上下文 |

**权限说明**:
系统应用须拥有对应组织写权限（ORG_WRITE）

**返回结果**:
```json
{
  "code": 0
}
```

| 参数名 | 说明 |
|--------|------|
| code | 返回码。操作成功时，除了返回值没有其它信息。 |
| message | 操作失败会返回出错信息。 |

**cURL示例**:
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/smtpTransport" \
-H "Content-Type: application/json" \
-d '{ "_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c", "mail_from" : "apitest1@api.cn", "rcpt_to" : "apitest2@api.cn", "data" : "Subject: Test smtpTransport api\nContent-Type: text/plain; charset=UTF-8\n\nTest smtpTransport api" }'
```

## 4. 附录

### 4.1 返回信息表

每个http调用均返回一个ReturnInfo结构，该结构有三个属性：

- **code**: 返回码
- **message**: 返回信息，当操作不成功时，返回更具体的信息
- **result**: 返回结果，部分调用，可通过此属性返回操作结果，结果的格式与具体接口相关

建议用户尽量根据返回码来进行错误原因，返回信息仅用于参考和生成终端错误信息。返回码参考见下表：

| 返回值 | 描述 |
|--------|------|
| 42 | 错误的UD属性 |
| 43 | - |
| 44 | - |
| 48 | 会话错误 |
| 49 | 域名已存在 |
| 50 | 服务等级不存在 |
| 51 | 组织不存在 |
| 52 | 组织处于非正常状态(锁定或停用) |
| 53 | 组织已过期 |
| 54 | 组织永不过期 |
| 55 | 别名个数达到最大数 |
| 56 | 别名错误 |
| 59 | 用户数达到许可证最大限制数 |
| 60 | 许可证过期 |
| 61 | 域名个数达到许可证最大限制数 |
| 62 | 组织个数达到许可证最大限制数 |
| 63 | 部门不存在 |
| 64 | 用户名已经被其它站点注册 |
| 65 | 用户别名已经被其它站点注册 |
| 79 | 外部联系人不存在 |
| 92 | 用户未删除 |

### 4.2 组织属性表

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| org_name | string | 组织名称，如不提供则将使用org_id作为组织名称 |
| domain_name | string | 分配域名(将自动创建)，可传递数组同时分配多个域名 |
| cos_id | int/array | 分配服务等级，可传递数组比如[1, 3, 5]同时分配多个服务等级 |
| num_of_classes | int/array | 分配服务等级数量，如果cos_id传递了数组，这里也应传数组，并确保一一对应 |
| res_grp_id | string | 组织资源分组标识 |
| org_assignable_quota | int | 组织可分配容量(MB) |
| org_status | int | 组织状态，0-正常; 1-停用，2-锁定 |
| org_expiry_date | string | 过期日期。NULL或者空表示不过期。格式为: yyyy-MM-dd |
| org_options | int | 组织增值服务 |
| org_active_options | int | 启用的组织增值服务 |
| org_address | string | 组织通讯录地址 |
| org_phone_number | string | 组织联系电话 |
| org_contact | string | 组织联系人 |
| org_access_level | int | 组织可见性，0-公开; 1-组织内及授权用户可见，-1-授权用户可见 |
| org_access_user | string | 组织通讯录授权列表 |
| org_deny_user | string | 组织通讯录禁止列表 |
| org_access_user_l1 | string | 组织通讯录特殊授权 |
| email_allow_user | string | 群发授权列表 |

### 4.3 用户属性表

Coremail属性表包括各种用户信息，包括存储在Coremail MD以及UD模块的字段，客户端可以通过Coremail API完成对用户属性的修改。开发人员应严格按照范例进行开发，避免对用户造成不良影响。

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| primary_email | string | 指定额外的主邮件地址 |
| alias | array of string | 指定额外的别名邮件地址 |
| org_unit_id | string | 部门标识 |
| user_status | int | 用户状态：0-活跃；1-停用；2-维护中；3-代理状态；4-锁定；100-延迟删除 |
| password | string | 用户密码 |
| cos_id | int | 服务等级标识 |
| quota_delta | int | 附加的邮箱空间大小，单位: MB |
| nf_quota_delta | int | 附加的网盘空间大小，单位: MB |
| privacy_level | int | 信息公开(在组织通讯录中显示), 0-不公开; 2-组织内公开; 4-站点内公开 |
| user_list_rank | int | 排序号 |
| true_name | string | 账号名称(姓名) |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别，常用取值: "0"-男，"1"-女 |
| birthday | string | 生日 |
| alt_email | string | 备用邮箱地址 |
| mobile_number | string | 手机号码 |
| home_phone | string | 家庭电话 |
| company_phone | string | 公司电话 |
| fax_number | string | 传真号码 |
| province | string | 省份/州 |
| city | string | 城市 |
| anniversary | string | 周年纪念日 |
| zipcode | string | 邮政编码 |
| address | string | 联系地址 |
| homepage | string | 公司主页 |
| remarks | string | 备注 |
| user_security_role | int | 人员身份 |
| security_level | int | 收信密级 |
| sender_security_level | int | 发信密级 |
| smsaddr | string | 绑定手机号 |
| second_auth_type | int | 二次验证类型, 1-关闭, 2-短信, 4-APP授权 |

**安全锁配置**:
- 空串或null：关闭安全锁
- 使用逗号","分隔多种不同类型的列表
- {fid}：def_sec_folder string 开启安全锁的邮箱文件夹标识
- nf:{fid}：开启安全锁的网盘该村夹标识
- op:{id}：受保护的操作标识: 1-设置自动转发, 2-修改用户密码, 3-设置邮箱共享

**邮件列表相关**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| forwardactive | int | 是否开启转发(邮件列表该属性值必须为1) |
| rejectjunk | int | 垃圾邮件处理方式(邮件列表该属性必须为1) |
| maillist_filter | string | 邮件列表的动态列表规则使用url编码字符串，格式为"^key1=value1&key2=value2&..."，其中可选key及含义为：org_id-组织标识；org_unit_id-部门标识；recursive-是否包含子部门，false-不包含，true-包含；type-用户类型，"U"-用户;"X"-外部联系人;"R"-会议室;"L"-邮件列表；includelist-用户列表，格式"user1,user2,..."；excludelist-除排用户列表，格式与includelist一致 |
| junkfilter | int | 邮件列表的授权范围(用户), 0-允许所有用户; 2-允许列表成员和指定用户; 3-只允许指定用户 |
| safelist | string | 邮件列表的授权列表，格式"user1,user2,..." |
| forwardmaillist | string | 邮件列表的用户列表(成员)，格式"user1,user2,..." |
| maillist_errorto | string | 邮件列表的退信接收地址列表，格式"user1,user2,..." |

**会议室相关**:

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| access_user | string | 授权使用列表 |

### 4.4 联系人属性表

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| org_id | string | 组织标识 |
| org_unit_id | string | 部门标识 |
| obj_class | int | 对象类型，1-外部联系人; 100-影子用户; 101-影子邮件列表 |
| obj_email | string | 外部联系人的邮箱地址 |
| obj_creation_date | string | 外部联系人创建时间，缺省为当前时间 |
| privacy_level | int | 信息公开(在组织通讯录中显示), 0-不公开; 2-组织内公开; 4-站点内公开 |
| obj_list_rank | int | 排序号 |
| true_name | string | 账号名称(姓名) |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别，常用取值: "0"-男，"1"-女 |
| birthday | string | 生日 |
| alt_email | string | 备用邮箱地址 |
| mobile_number | string | 手机号码 |
| home_phone | string | 家庭电话 |
| company_phone | string | 公司电话 |
| fax_number | string | 传真号码 |
| province | string | 省份/州 |
| city | string | 城市 |
| anniversary | string | 周年纪念日 |
| zipcode | string | 邮政编码 |
| address | string | 联系地址 |
| homepage | string | 公司主页 |
| remarks | string | 备注 |

### 4.5 信件属性表

| 属性名 | 类型 | 属性含义 |
|--------|------|----------|
| mid | string | 信件标识 |
| msid | int | 信件所在ms标识 |
| fid | int | 信件文件夹标识 |
| flag | int | 标志位 |
| from | string | 发件人 |
| to | string | 收件人 |
| subject | string | 邮件主题 |
| size | int | 邮件大小 |
| date | string | 邮件发送时间 |

### 4.6 单点登录链接

| 模块 | 参数 | 首页 |
|------|------|------|
| 单独写信页面 | - | http://coremail.cn/coremail/main.jsp?sid=#sid# |
| 单独收信列表 | mail.list | http://coremail.cn/coremail/XT/detach.jsp?sid=#sid# |
| 读信 | {"fid":1} | http://coremail.cn/coremail/hxphone/sso.html#/framesid/mid |
| hxphone 2.0/3.0 | - | /e 2.0/read/-2/#mid#//?sid=#sid# |
| hxphone 2.0/3.0 | 写信 | http://coremail.cn/coremail/hxphone/sso.html#/frame /compose///?sid=#sid# |
| hxphone 2.0/3.0 | 收件箱 | http://coremail.cn/coremail/hxphone/sso.html#/frame /folder/1?sid=#sid# |
| hxphone 2.0/3.0 | 通讯录 | http://coremail.cn/coremail/hxphone/sso.html#/frame /contactList/?sid=#sid# |
| hxphone 2.0/3.0 | 文件中心 | http://coremail.cn/coremail/hxphone/sso.html#/frame /netFolder?sid=#sid# |
| hxphone e 3.0+ | 未读邮件列表 | http://coremail.cn/coremail/hxphone/sso.html#/frame /folder/-2?sid=#sid# |

**其他单点登录链接**:

| 模块 | 参数 | 链接 |
|------|------|------|
| hxphone | 读信 | http://coremail.cn/coremail/hxphone/sso.html#/frame/sid/mid |
| 读信 | 首页 | http://coremail.cn/coremail/hxphone/sso.html#/frame/read/-2/#mid#?sid=#sid# |
| hxphone | 读信 | http://coremail.cn/coremail/xphone/main.jsp?sid=#sid# |
| 读信 | 首页 | http://coremail.cn/coremail/xphone/main.jsp?sid=#sisid/mid |
| xphone | 写信 | http://coremail.cn/coremail/xphone/main.jsp?sid=#sisid/target |
| 读信 | 邮箱 | #d#&target=compose http://coremail.cn/coremail/xphone/main.jsp?sid=#sisid/target |
| 读信 | 邮箱 | #d#&target=viewMailContent&mid=#mid#sid/target/mi p |

### 4.7 API HTTP 请求定义文件

**apiws-v3.http**

.http文件是IntelliJ IDEA中用于存储和发送HTTP请求的一种特殊文件类型。它可以帮助开发者快速调试和测试RESTful API，提高开发效率。可以把apiws-v3.http文件在IDEA打开与Coremail XT高级API接口调试。

---

## 总结

本文档提供了Coremail XT高级API（apiws v3-2）的完整使用指南，涵盖了以下主要内容：

1. **API概述与版本说明**
2. **开发环境准备与认证设置**
3. **Access Token管理**
4. **用户登录与会话管理**
5. **组织、部门、用户、联系人维护**
6. **域名管理**
7. **邮件操作**
8. **详细的技术规范和参数说明**
9. **错误码和返回值说明**
10. **单点登录配置**

该API采用RESTful设计，基于HTTP/JSON协议，提供了全面的企业邮件系统管理功能。开发者可以根据本手册实现与Coremail XT系统的深度集成。

---

*本手册最后更新：2022年10月*
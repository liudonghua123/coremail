# Coremail XT 高级API(apiws v3-2)使用手册

## 版权声明
本文档版权归Coremail®所有，并保留一切权利。未经书面许可，任何公司和个人不得将此文档中的任何部分公开、转载或以其他方式散发给第三方。否则，必将追究其法律责任。

## 免责声明
本文档仅提供阶段性信息，所含内容可根据产品的实际情况随时更新，恕不另行通知。如因文档使用不当造成的直接或间接损失，本公司不承担任何责任。

## 文档更新
- 修订日期：2022年10月（最后修订）
- 公司网站：http://www.coremail.cn
- 销售咨询热线：400-000-1631
- 技术支持热线：400-630-7163

## 文档修改记录
| 版本 | 修改日期 | 修改人员 | 修改记录 |
| --- | --- | --- | --- |
| V1 | 2022-10-24 | 黄飞飞 | 文档修订 |
| V2 | 2024-10-14 | 黄湖津 | 文档修订 |

## 文档审核记录
| 版本 | 审核日期 | 审核人员 | 审核记录 |
| --- | --- | --- | --- |

---

# 1 介绍
## 1.1 服务介绍
- 服务名称：Coremail XT 高级API
- 服务提供者：apiws 服务
- 底层服务：rmisvr 服务
- 封装目的：提供更加安全、适用性更强的调用方式

## 1.2 API 版本
- v1：webservices 接口，仅支持IP信任，存在安全问题，已不建议使用。
- v2：webservices 接口，支持IP和API用户授权，更加安全。
- v3：restful HTTP接口，基于标准JSON格式进行数据交换，调用更加方便，推荐使用。
- 说明：v1/v2依赖于Apache CXF提供SOAP接口服务，存在潜在的安全风险，建议逐渐迁移到v3版本。

## 1.3 文档范围
- 说明对象：v3接口
- 目标用户：开发人员和技术支持人员

---

# 2 开始开发
## 开发流程
1. 获取app_id和secure
2. 开发对接相关接口

## 2.1 获取app_id 和 secure
### 云平台客户
联系运维人员SA提供。

### 自建客户
1. 创建API用户：在管理后台创建用户作为API用户，邮件地址即为app_id，密码即为对应secure。
2. 授权：通过命令行执行授权，命令格式如下：
   ```bash
   userutil --set-user-attr <uid> api_acl=<acl>
   ```
   - `<acl>`格式规范：
     - "@all"：特殊字符串，表示最高授权。
     - 逗号分隔的授权，格式为`<org_id>`或`<org_id>:<access>`：
       - 忽略`<access>`部分表示默认授权（读写授权）。
       - `<access>`可选值：'r'/'ro'（只读授权）、'rw'（读写授权）。
   - 示例：
     ```bash
     # 授权user1为最高级别，允许操纵所有方法，和IPLimit的授权等同
     userutil --set-user-attr user1 api_acl=@all

     # 授权user2的访问：对org1/org3/org4为读写权限，org2为只读权限
     userutil --set-user-attr user2 api_acl=org1:rw,org2:r,org3,org4
     ```

## 2.2 开发对接相关接口
- 协议：HTTPS
- 数据格式：Json
- 编码：UTF8
- 访问路径：https://<host>/apiws/v3
- 数据包：无需加密
- 必备参数：每次调用API接口需带上`_token`参数（由app_id和secure换取）
- 校验逻辑：apiws服务根据`_token`校验访问合法性

---

# 3 Coremail XT API 接口具体功能应用说明
## 3.1 Access Token
### 3.1.1 获取凭证
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/requestToken
- 请求包结构体：
  ```json
  {
    "app_id": "api1@api.cn",
    "secret": "admin123"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| app_id | string | 是 | 应用标识 |
| secret | string | 是 | 应用的凭证密钥 |

#### 权限说明
准备好应用ID及密钥。

#### 返回结果
```json
{
  "code": 0,
  "result": "BAlhsYOOtvcxPysxzodDuzbTLhUlOnwD07ff68891ce48bb3a2c53c3712ee8501"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 授权凭证Token，所有接口调用需带上此Token。默认过期时间1小时（可配置） |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/requestToken" \
-H "Content-Type: application/json" \
-d '{
"app_id" : "api1@api.cn",
"secret" : "admin123"
}'
```

## 3.2 登录
### 3.2.1 用户登录
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/userLogin
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "user_at_domain": "a1@dev.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "BAHhsYOOybNsnHMWBlNmFILnEavPFYwD"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 用户登录会话ID (sid) |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userLogin" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"user_at_domain" : "a1@dev.cn"
}'
```

### 3.2.2 用户登录（使用附加参数，返回额外信息）
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/userLoginEx
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "user_at_domain": "a1@dev.cn",
    "attrs": "remote_ip=192.168.201.165&cookieKey=Coremail&cookiecheck=123"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |
| attrs | string | 否 | 操作属性，格式为urlencode字符串。属性值含特殊字符需用url编码（如"="编码为"%3D"） |

#### 操作属性说明
| 属性名 | 属性含义 |
| --- | --- |
| type | 登录类型（Coremail XT U3$3$后支持）："WEB"/"POP3"/"IMAP"/"SMTP"/"API"（默认） |
| remote_ip | 登录用户的IP |
| ipcheck | 仅为"1"时表示需要检查浏览器的IP |
| cookieKey | 检查浏览器的cookie名称 |
| cookiecheck | 检查浏览器的cookie值 |
| face | 登录的风格 |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "sid=BAehsYOOHknssAvQWHORDOnOLEsSNJKD&webname=http://mail.dev.cn"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | encode的用户属性字符串："sid=[用户的session id]&webname=[web主机前缀]"。web主机前缀包含协议、机器IP、端口，结尾不含'/' |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userLoginEx" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"user_at_domain" : "a1@dev.cn",
"attrs" : "remote_ip=192.168.201.165&cookieKey=Coremail&cookiecheck=123"
}'
```

### 3.2.3 检查用户是否存在
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/userExist
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "user_at_domain": "a1@dev.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "udid=1"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 返回用户所在的UD标识 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userExist" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"user_at_domain" : "a1@dev.cn"
}'
```

### 3.2.4 验证用户密码
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/authenticate
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "user_at_domain": "a1@dev.cn",
    "password": "admin1234"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮箱地址 |
| password | string | 是 | 用户密码 |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，0表示密码验证成功 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/authenticate" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"user_at_domain" : "a1@dev.cn",
"password" : "admin1234"
}'
```

### 3.2.5 检查用户的会话（返回用户信息）
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/sesTimeOut
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID(sid) |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "uid=a1@dev.cn&domain_id=1&org_id=a"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 成功时格式：uid=...@...&domain_id=...&org_id=...（uid为用户邮件地址） |
| message | 会话检查失败时返回，错误代码包括SESSION_NOT_FOUND（session ID不存在或过时）等 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/sesTimeOut" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
}'
```

### 3.2.6 检查用户的会话（刷新访问时间）
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/sesRefresh
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID(sid) |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/sesRefresh" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
}'
```

### 3.2.7 获取用户session中的变量
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getSessionVar
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD",
    "ses_key": "uidatdomain"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID(sid) |
| ses_key | string | 是 | 要获取的会话变量名 |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "a1@dev.cn"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 要获取的变量值 |
| message | 错误代码包括SESSION_NOT_FOUND（session ID不存在或过时）等 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getSessionVar" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD",
"ses_key" : "uidatdomain"
}'
```

### 3.2.8 注销用户会话
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/userLogout
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "ses_id": "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID(sid) |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/userLogout" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"ses_id" : "BAehsYOOHknssAvQWHORDOnOLEsSNJKD"
}'
```

### 3.2.9 设置用户会话中的变量
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/setSessionVar
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "ses_id": "BAyhsYOOeaCsSVQABZahowtpqTvPFYwD",
    "ses_key": "TEST_VAR",
    "ses_var": "TEST_VAR_VALUE"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| ses_id | string | 是 | 用户会话ID(sid) |
| ses_key | string | 是 | 要设置的会话变量名 |
| ses_var | string | 是 | 要设置的变量值 |

#### 权限说明
系统应用须拥有用户所在组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/setSessionVar" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"ses_id" : "BAyhsYOOeaCsSVQABZahowtpqTvPFYwD",
"ses_key" : "TEST_VAR",
"ses_var" : "TEST_VAR_VALUE"
}'
```

## 3.3 组织维护
### 3.3.1 创建组织
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/addOrg
- 请求包结构体：
  ```json
  {
    "_token": "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
    "org_id": "apitest",
    "attrs": {
      "org_name": "API测试组织",
      "domain_name": "api.cn",
      "cos_id": [1],
      "num_of_classes": [1000],
      "org_status": 0,
      "org_expiry_date": "2025-01-01"
    }
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| attrs | string/object | 否 | 企业组织属性（详见下表） |

#### 组织属性说明
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| org_name | string | 组织名称，不提供则使用org_id作为名称 |
| domain_name | string | 分配域名（自动创建），可传数组分配多个域名 |
| cos_id | int/array | 分配服务等级，可传数组（如[1,3,5]）分配多个 |
| num_of_classes | int/array | 分配服务等级数量，cos_id为数组时需一一对应 |
| res_grp_id | string | 组织资源分组标识 |
| org_assignable_quota | int | 组织可分配容量（MB） |
| org_status | int | 组织状态：0-正常；1-停用；2-锁定 |
| org_expiry_date | string | 过期日期，NULL或空表示不过期（格式：yyyy-MM-dd） |
| org_options | int | 组织增值服务 |
| org_active_options | int | 启用的组织增值服务 |
| org_address | string | 组织通讯录地址 |
| org_phone_number | string | 组织联系电话 |
| org_contact | string | 组织联系人 |
| org_access_level | int | 组织可见性：0-公开；1-组织内及授权用户可见；-1-授权用户可见 |
| org_access_user | string | 组织通讯录授权列表 |
| org_deny_user | string | 组织通讯录禁止列表 |
| org_access_user_l1 | string | 组织通讯录特殊授权 |
| email_allow_user | string | 群发授权列表 |

#### 权限说明
系统应用须拥有站点写权限(SITE_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addOrg" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAqhsYOOqBUhrOwmtRQYXJifZzvPFYwDd2733c3bf4875aaeb3d23d8f7012fbf8",
"org_id" : "apitest",
"attrs" : {
"org_name" : "API测试组织",
"domain_name" : "api.cn",
"cos_id" : [1],
"num_of_classes" : [1000],
"org_status" : 0,
"org_expiry_date" : "2025-01-01"
}
}'
```

### 3.3.2 获取组织属性
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getOrgInfo
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "attrs": {
      "org_name": null,
      "domain_name": null,
      "org_status": null,
      "org_expiry_date": null,
      "cos_info": null,
      "total_users": null,
      "used_users": null,
      "used_quota_delta": null,
      "used_mail_quota_delta": null,
      "used_nf_quota_delta": null
    }
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| attrs | string/object | 否 | 要获取的组织属性（详见下表） |

#### 组织属性attrs可用属性
| 属性名 | 属性含义 |
| --- | --- |
| * | 不传attrs默认返回所有普通属性（参考组织属性表），不包含COS分配内容 |
| cos_info | 逗号分隔列表："cosId1:分配数:分类:名称,cosId2:分配数:分类:名称,..." |
| total_users | 通过COS分配的用户总数 |
| used_users | 已创建账号数量 |
| used_quota_delta | 已创建账号的额外容量总和（MB，对应org_assignable_quota分配部分） |
| used_mail_quota_delta | 已创建账号的邮箱额外容量总和（MB） |
| used_nf_quota_delta | 已创建账号的网盘额外容量总和（MB） |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": {
    "org_name": "API测试组织",
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
| --- | --- |
| code | 返回码 |
| result | 获取的组织属性 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgInfo" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"attrs" : {
"org_name" : null,
"domain_name" : null,
"org_status" : null,
"org_expiry_date" : null,
"cos_info" : null,
"total_users" : null,
"used_users" : null,
"used_quota_delta" : null,
"used_mail_quota_delta" : null,
"used_nf_quota_delta" : null
}
}'
```

### 3.3.3 修改组织属性
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/alterOrg
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "attrs": {
      "org_name": "API测试组织-修改",
      "org_expiry_date": "2024-09-11"
    }
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| attrs | string/object | 是 | 要修改的组织属性（参考组织属性表） |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/alterOrg" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"attrs" : {
"org_name" : "API测试组织-修改",
"org_expiry_date" : "2024-09-11"
}
}'
```

### 3.3.4 添加组织域名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/addOrgDomain
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "domain_name": "dev.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| domain_name | string | 是 | 域名（需预先创建） |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addOrgDomain" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"domain_name" : "dev.cn"
}'
```

### 3.3.5 删除组织域名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/delOrgDomain
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "domain_name": "dev.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| domain_name | string | 是 | 要删除的域名 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delOrgDomain" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"domain_name" : "dev.cn"
}'
```

### 3.3.6 增加组织服务等级
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/addOrgCos
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "cos_id": 8,
    "num_of_classes": 100
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_name | string | 否 | 服务等级名称，cos_name/cos_id二选一，优先使用cos_name |
| cos_id | int | 否 | 服务等级标识 |
| num_of_classes | int | 是 | 可分配用户数 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addOrgCos" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"cos_id" : 8,
"num_of_classes" : 100
}'
```

### 3.3.7 更新组织服务等级
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/alterOrgCos
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "cos_id": 8,
    "num_of_classes": 99
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_name | string | 否 | 服务等级名称，cos_name/cos_id二选一，优先使用cos_name |
| cos_id | int | 否 | 服务等级标识 |
| num_of_classes | int | 是 | 可分配用户数 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/alterOrgCos" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"cos_id" : 8,
"num_of_classes" : 99
}'
```

### 3.3.8 删除组织服务等级
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/delOrgCos
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "cos_id": 8
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_id | int | 是 | 服务等级标识 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delOrgCos" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"cos_id" : 8
}'
```

### 3.3.9 列出指定组织某服务等级下的所有用户名列表
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getOrgCosUser
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "cos_id": 1
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 企业组织标识 |
| cos_id | int | 是 | 服务等级标识 |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "apitest1,apitest2"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 用户名列表，多个用户以','分隔（不含"@domain"信息） |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgCosUser" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"cos_id" : 1
}'
```

### 3.3.10 获取组织列表
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getOrgList
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |

#### 权限说明
系统应用须拥有站点读权限(SITE_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "api,apitest,a"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 组织列表，多个组织以','分隔 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgList" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13"
}'
```

## 3.4 部门维护
### 3.4.1 创建部门
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/addUnit
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "org_unit_id": "1",
    "attrs": {
      "parent_org_unit_id": null,
      "org_unit_name": "测试部门1",
      "org_unit_list_rank": 0
    },
    "dont_flush_md": false
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 组织标识 |
| org_unit_id | string | 是 | 部门标识 |
| attrs | string/object | 是 | 部门属性（详见下表） |
| dont_flush_md | boolean | 否 | 忽略flush md |

#### 部门属性说明
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| parent_org_unit_id | string | 父部门标识，不设置则创建直属部门 |
| org_unit_name | string | 部门名称 |
| org_unit_list_rank | int | 部门排序号 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addUnit" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"org_unit_id" : "1",
"attrs" : {
"parent_org_unit_id" : null,
"org_unit_name" : "测试部门1",
"org_unit_list_rank" : 0
},
"dont_flush_md" : false
}'
```

### 3.4.2 删除部门
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/delUnit
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "org_unit_id": "1"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 组织标识 |
| org_unit_id | string | 是 | 部门标识 |
| dont_flush_md | boolean | 否 | 忽略flush md |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delUnit" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"org_unit_id" : "1"
}'
```

### 3.4.3 获取部门属性
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getUnitAttrs
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "org_unit_id": "1",
    "attrs": {
      "parent_org_unit_id": null,
      "org_unit_name": null,
      "org_unit_list_rank": null,
      "user_count": null,
      "abook_user_count": null
    }
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 组织标识 |
| org_unit_id | string | 是 | 部门标识 |
| attrs | string/object | 否 | 要获取的部门属性（详见下表） |

#### 部门属性attrs可用属性
| 属性名 | 属性含义 |
| --- | --- |
| parent_org_unit_id | 父部门标识 |
| org_unit_name | 部门名称 |
| org_unit_list_rank | 部门排序号 |
| user_count | 统计用户数 |
| abook_user_count | 通讯录用户数 |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": {
    "parent_org_unit_id": null,
    "org_unit_name": "测试部门1",
    "org_unit_list_rank": 0,
    "user_count": 0,
    "abook_user_count": 0
  }
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 获取的部门属性 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getUnitAttrs" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"org_unit_id" : "1",
"attrs" : {
"parent_org_unit_id" : null,
"org_unit_name" : null,
"org_unit_list_rank" : null,
"user_count" : null,
"abook_user_count" : null
}
}'
```

### 3.4.4 设置部门属性
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/setUnitAttrs
- 请求包结构体：
  ```json
  {
    "_token": "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
    "org_id": "apitest",
    "org_unit_id": "1",
    "attrs": {
      "parent_org_unit_id": null,
      "org_unit_name": "测试部门1-修改",
      "org_unit_list_rank": 10
    },
    "dont_flush_md": false
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| org_id | string | 是 | 组织标识 |
| org_unit_id | string | 是 | 部门标识 |
| attrs | string/object | 是 | 部门属性（参考部门属性表） |
| dont_flush_md | boolean | 否 | 忽略flush md |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/setUnitAttrs" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAOnsYOODTynVIAnbQOlAtZqfPbdETwDdb0445f6af8d99cfdb940bebc7792d13",
"org_id" : "apitest",
"org_unit_id" : "1",
"attrs" : {
"parent_org_unit_id" : null,
"org_unit_name" : "测试部门1-修改",
"org_unit_list_rank" : 10
},
"dont_flush_md" : false
}'
```

## 3.5 用户维护
### 3.5.1 创建用户
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/createUser
- 请求包结构体：
  ```json
  {
    "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
    "providerId": "1",
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| providerId | string | 否 | 提供商ID |
| org_id | string | 是 | 组织标识 |
| user_at_domain | string | 是 | 账号、别名、主键信息 |
| attrs | string/object | 是 | 用户属性（详见下表） |

#### 用户属性说明
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| primary_email | string | 指定额外的主邮件地址 |
| alias | array of string | 指定额外的别名邮件地址 |
| org_unit_id | string | 部门标识 |
| user_status | int | 用户状态：0-活跃；1-停用；2-维护中；3-代理状态；4-锁定；100-延迟删除 |
| password | string | 用户密码 |
| cos_id | int | 服务等级标识 |
| quota_delta | int | 附加的邮箱空间大小（MB） |
| nf_quota_delta | int | 附加的网盘空间大小（MB） |
| privacy_level | int | 信息公开（组织通讯录中显示）：0-不公开；2-组织内公开；4-站点内公开 |
| user_list_rank | int | 排序号 |
| true_name | string | 账号名称（姓名） |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别："0"-男，"1"-女 |
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
| second_auth_type | int | 二次验证类型：1-关闭；2-短信；4-APP授权 |
| def_sec_folder | string | 安全锁，取值：空串/null（关闭）、{fid}（邮箱文件夹）、nf:{fid}（网盘文件夹）、op:{id}（受保护操作：1-自动转发，2-修改密码，3-邮箱共享） |
| forwardactive | int | 是否开启转发（邮件列表必须为1） |
| rejectjunk | int | 垃圾邮件处理方式（邮件列表必须为1） |
| maillist_filter | string | 邮件列表动态规则（url编码）：^key1=value1&key2=value2&...，key包括org_id、org_unit_id、recursive（是否含子部门）、type（用户类型：U-用户/X-外部联系人/R-会议室/L-邮件列表）、includelist、excludelist |
| junkfilter | int | 邮件列表授权范围：0-所有用户；2-成员和指定用户；3-仅指定用户 |
| safelist | string | 邮件列表授权列表（格式：user1,user2,...） |
| forwardmaillist | string | 邮件列表成员列表（格式：user1,user2,...） |
| maillist_errorto | string | 邮件列表退信接收地址（格式：user1,user2,...） |
| access_user | string | 会议室授权使用列表 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/createUser" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"providerId" : "1",
"org_id" : "apitest",
"user_at_domain" : "apitest3@api.cn",
"attrs" : {
"org_unit_id" : "1",
"user_status" : 0,
"password" : "test123",
"cos_id" : 1,
"privacy_level" : 4,
"true_name" : "测试用户3"
}
}'
```

### 3.5.2 删除用户
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/deleteUser
- 请求包结构体：
  ```json
  {
    "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
    "user_at_domain": "apitest3@api.cn",
    "preserve_days": 0
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| preserve_days | int | 是 | 延迟删除天数，0为立即删除，-1（默认）取决于系统设定 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/deleteUser" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"user_at_domain" : "apitest3@api.cn",
"preserve_days" : 0
}'
```

### 3.5.3 用户属性获取
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getAttrs
- 请求包结构体：
  ```json
  {
    "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
    "user_at_domain": "apitest3@api.cn",
    "attrs": {
      "org_unit_id": null,
      "user_status": null,
      "cos_id": null,
      "privacy_level": null,
      "true_name": null
    }
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| attrs | object | 否 | 要获取的用户属性（参考用户属性表），不传默认获取全部 |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
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
| --- | --- |
| code | 返回码 |
| result | 获取的属性值 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getAttrs" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"user_at_domain" : "apitest3@api.cn",
"attrs" : {
"org_unit_id" : null,
"user_status" : null,
"cos_id" : null,
"privacy_level" : null,
"true_name" : null
}
}'
```

### 3.5.4 用户属性变更
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/changeAttrs
- 请求包结构体：
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| attrs | object | 是 | 要修改的用户属性（参考用户属性表） |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/changeAttrs" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"user_at_domain" : "apitest3@api.cn",
"attrs" : {
"org_unit_id" : null,
"true_name" : "测试用户3-修改"
}
}'
```

### 3.5.5 添加别名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/addSmtpAlias
- 请求包结构体：
  ```json
  {
    "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
    "user_at_domain": "apitest3@api.cn",
    "alias_user_at_domain": "api3@api.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| alias_user_at_domain | string | 是 | 别名邮件地址 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addSmtpAlias" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"user_at_domain" : "apitest3@api.cn",
"alias_user_at_domain" : "api3@api.cn"
}'
```


### 3.5.6 删除别名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/delSmtpAlias
- 请求包结构体：
  ```json
  {
    "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
    "user_at_domain": "apitest3@api.cn",
    "alias_user_at_domain": "api3@api.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| alias_user_at_domain | string | 是 | 要删除的别名邮件地址 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delSmtpAlias" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"user_at_domain" : "apitest3@api.cn",
"alias_user_at_domain" : "api3@api.cn"
}'
```


### 3.5.7 获取别名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getSmtpAlias
- 请求包结构体：
  ```json
  {
    "_token": "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
    "user_at_domain": "apitest3@api.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "api3@api.cn,api_test3@api.cn,api_test_3@api.cn"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 用户SMTP别名列表，多个别名以","分隔 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getSmtpAlias" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"user_at_domain" : "apitest3@api.cn"
}'
```


### 3.5.8 设置用户的管理员身份
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/setAdminType
- 请求包结构体：
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |
| attrs | object | 是 | 管理员属性（详见下表） |

#### 管理员属性说明
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| admin_type | string | 管理员级别，默认为组织管理员（OA） |
| role_id | int | 管理员角色标识，参考td_admin_role表定义 |
| cross_manage_scope | string | 管理范围，仅适用于自定义组织管理员（302）和自定义部门管理员（402） |

#### 权限说明
系统应用须拥有站点写权限(SITE_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/setAdminType" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BAYnsYOOjPiUjXICpZPuUFzMYtUlOnwD77e3c3d9c12b12ea236c5eb7c770f2b7",
"user_at_domain" : "apitest3@api.cn",
"attrs" : {
"admin_type" : "OA",
"role_id" : 3
}
}'
```


### 3.5.9 获取用户的管理员身份
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getAdminType
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "user_at_domain": "apitest3@api.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 邮件账号 |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "admin_type=OA&role_id=3"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 管理员身份信息，格式为"admin_type=xxx&role_id=xxx"，参考「设置用户的管理员身份」属性说明 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getAdminType" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"user_at_domain" : "apitest3@api.cn"
}'
```


### 3.5.10 修改用户主标识
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/renameUser
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "user_at_domain": "apitest3@api.cn",
    "new_user_id": "apitest3_new"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 原邮件账号 |
| new_user_id | string | 是 | 新的用户标识（不含域名部分） |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/renameUser" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"user_at_domain" : "apitest3@api.cn",
"new_user_id" : "apitest3_new"
}'
```


### 3.5.11 用户跨组织移动
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/moveUser
- 请求包结构体：
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 待移动的用户邮件账号 |
| attrs | object | 是 | 用户新位置属性（org_id：新组织标识；org_unit_id：新部门标识） |

#### 权限说明
系统应用须拥有站点写权限(SITE_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/moveUser" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"user_at_domain" : "apitest1@api.cn",
"attrs" : {
"org_id" : "api",
"org_unit_id" : "test"
}
}'
```


## 3.6 联系人维护
### 3.6.1 创建联系人
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/createObj
- 请求包结构体：
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| attrs | object | 是 | 联系人属性（详见下表） |

#### 联系人属性说明
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| org_id | string | 组织标识 |
| org_unit_id | string | 部门标识 |
| obj_class | int | 对象类型：1-外部联系人；100-影子用户；101-影子邮件列表 |
| obj_email | string | 外部联系人的邮箱地址 |
| obj_creation_date | string | 创建时间，默认当前时间 |
| privacy_level | int | 信息公开范围：0-不公开；2-组织内公开；4-站点内公开 |
| obj_list_rank | int | 排序号 |
| true_name | string | 姓名 |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别："0"-男，"1"-女 |
| birthday | string | 生日 |
| alt_email | string | 备用邮箱 |
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

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0,
  "result": {
    "obj_uid": "1_test_19289d00137"
  }
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 联系人唯一标识（obj_uid），后续操作（获取/修改/删除）需使用此标识 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/createObj" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"attrs" : {
"org_id" : "apitest",
"org_unit_id" : "1",
"obj_class" : 1,
"obj_email" : "test@coremail.cn"
}
}'
```


### 3.6.2 联系人属性获取
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getObjAttrs
- 请求包结构体：
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| obj_uid | string | 是 | 联系人标识（创建联系人时返回） |
| attrs | object | 否 | 要获取的属性，不传默认获取全部（参考联系人属性表） |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
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
| --- | --- |
| code | 返回码 |
| result | 获取的联系人属性 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getObjAttrs" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"obj_uid" : "1_test_19289d00137",
"attrs" : {
"org_id" : null,
"org_unit_id" : null,
"obj_class" : null,
"obj_email" : null
}
}'
```


### 3.6.3 联系人属性变更
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/setObjAttrs
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "obj_uid": "1_test_19289d00137",
    "attrs": {
      "obj_email": "test-change@coremail.cn"
    }
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| obj_uid | string | 是 | 联系人标识 |
| attrs | object | 是 | 要修改的属性（参考联系人属性表） |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/setObjAttrs" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"obj_uid" : "1_test_19289d00137",
"attrs" : {
"obj_email" : "test-change@coremail.cn"
}
}'
```


### 3.6.4 删除联系人
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/deleteObj
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "obj_uid": "1_test_19289d00137"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| obj_uid | string | 是 | 联系人标识 |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/deleteObj" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"obj_uid" : "1_test_19289d00137"
}'
```


## 3.7 域名维护
### 3.7.1 检查域名/域名别名是否存在
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/domainExist
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "domain_name": "api.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 待检查的域名或域名别名 |

#### 权限说明
系统应用须拥有站点读权限(SITE_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "api.cn"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 存在时返回检查的域名；不存在时无此字段 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/domainExist" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"domain_name" : "api.cn"
}'
```


### 3.7.2 列出系统所有域名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getDomainList
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |

#### 权限说明
系统应用须拥有站点读权限(SITE_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "api.cn,test.cn,dev.cn"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 系统所有域名列表，多个域名以","分隔 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getDomainList" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c"
}'
```


### 3.7.3 增加域名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/addDomain25
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "domain_name": "api2.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 要新增的域名 |

#### 权限说明
系统应用须拥有站点写权限(SITE_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息（如域名已存在） |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addDomain25" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"domain_name" : "api2.cn"
}'
```


### 3.7.4 删除域名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/delDomain25
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "domain_name": "api2.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 要删除的域名 |

#### 权限说明
系统应用须拥有站点写权限(SITE_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息（如域名不存在） |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delDomain25" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"domain_name" : "api2.cn"
}'
```


### 3.7.5 增加域别名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/addDomainAlias
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "domain_name": "api.cn",
    "domain_name_alias": "api-alias.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 主域名 |
| domain_name_alias | string | 是 | 要新增的域别名 |

#### 权限说明
系统应用须拥有站点写权限(SITE_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息（如域别名已存在） |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/addDomainAlias" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"domain_name" : "api.cn",
"domain_name_alias" : "api-alias.cn"
}'
```


### 3.7.6 列出指定域的所有域名别名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getDomainAlias
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "domain_name": "api.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 主域名 |

#### 权限说明
系统应用须拥有站点读权限(SITE_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "api-alias.cn,api-alias2.cn"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 指定主域名的所有域别名，多个别名以","分隔 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getDomainAlias" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"domain_name" : "api.cn"
}'
```


### 3.7.7 删除域别名
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/delDomainAlias
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "domain_name": "api.cn",
    "domain_name_alias": "api-alias.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 主域名 |
| domain_name_alias | string | 是 | 要删除的域别名 |

#### 权限说明
系统应用须拥有站点写权限(SITE_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息（如域别名不存在） |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/delDomainAlias" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"domain_name" : "api.cn",
"domain_name_alias" : "api-alias.cn"
}'
```


### 3.7.8 列出使用指定域名的组织列表
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getOrgListByDomain
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "domain_name": "api.cn"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| domain_name | string | 是 | 域名 |

#### 权限说明
系统应用须拥有站点读权限(SITE_READ)。

#### 返回结果
```json
{
  "code": 0,
  "result": "api,apitest"
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码 |
| result | 使用指定域名的组织标识列表，多个组织以","分隔 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getOrgListByDomain" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"domain_name" : "api.cn"
}'
```


## 3.8 邮件维护
### 3.8.1 列举用户信件
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/listMailInfos
- 请求包结构体：
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮件账号 |
| options | object | 否 | 查询选项（详见下表） |

#### 查询选项说明
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| limit | int | 限制返回条数，默认不限制 |
| fid | int | 文件夹标识，默认收件箱（fid=1） |
| skip | int | 跳过条数，默认0 |
| order | string | 排序规则：<br>- 基础字段：from（发件人）、to（收件人）、subject（主题）、size（大小）、status（状态）、date（发送时间）、receivedDate（接收时间）<br>- 排序方向：desc后缀表示倒序（如"date desc"）<br>- 标志位优先："!"前缀表示标志位优先（如"!~read!date desc"：未读优先+发送时间倒序）<br>- 默认值："~date"（发送时间倒序） |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
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
| --- | --- |
| code | 返回码 |
| result.mail | 用户信件列表，单条信件属性参考「信件属性表」 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/listMailInfos" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"user_at_domain" : "apitest2@api.cn",
"options" : {
"limit" : 1,
"fid" : 1,
"skip" : 0,
"order" : "receivedDate"
}
}'
```


### 3.8.2 获取用户未读信件列表
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/getNewMailInfos
- 请求包结构体：
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

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| user_at_domain | string | 是 | 用户邮件账号 |
| options | object | 否 | 查询选项（详见下表） |

#### 查询选项说明
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| limit | int | 限制返回条数，默认不限制 |
| excludeFidList | array | 排除的文件夹列表（如[2,3]表示排除fid=2和3的文件夹） |
| doubleDecode | boolean | 是否对收发件人、邮件主题进行解码，默认false |
| format | string | 返回格式，仅指定"xml"时返回XML格式，默认JSON |

#### 权限说明
系统应用须拥有对应组织读权限(ORG_READ)。

#### 返回结果
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
| --- | --- |
| code | 返回码 |
| result.mail | 未读信件列表，属性参考「信件属性表」 |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/getNewMailInfos" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"user_at_domain" : "apitest2@api.cn",
"options" : {
"limit" : 1,
"excludeFidList" : [],
"doubleDecode" : false,
"format" : ""
}
}'
```


### 3.8.3 通过MTA投递信件
#### 请求说明
- HTTP请求方式：POST
- 请求地址：/apiws/v3/smtpTransport
- 请求包结构体：
  ```json
  {
    "_token": "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
    "mail_from": "apitest1@api.cn",
    "rcpt_to": "apitest2@api.cn",
    "data": "Subject: Test smtpTransport api\nContent-Type: text/plain; charset=UTF-8\n\nTest smtpTransport api"
  }
  ```

#### 参数说明
| 参数名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| _token | string | 是 | 授权凭证Token |
| mail_from | string | 否 | 发件人，空串或不传则从data中提取 |
| rcpt_to | string | 否 | 收件人，空串或不传则从data中提取 |
| data | string | 是 | 邮件内容（符合message/rfc822格式，包含主题、内容类型、正文等） |
| options | object | 否 | 投递选项（remote_ip：远程IP；X-Coremail-Context：邮件上下文） |

#### 权限说明
系统应用须拥有对应组织写权限(ORG_WRITE)。

#### 返回结果
```json
{
  "code": 0
}
```
| 参数名 | 说明 |
| --- | --- |
| code | 返回码，操作成功时仅返回此信息 |
| message | 操作失败时返回出错信息（如格式错误、收件人不存在） |

#### cURL示例
```bash
curl -X POST --location "http://172.16.18.35/apiws/v3/smtpTransport" \
-H "Content-Type: application/json" \
-d '{
"_token" : "BASnsYOObIyqvRTPisIBwhGVIOOUBRDp4eecc6df086432756b6d739ad092cd8c",
"mail_from" : "apitest1@api.cn",
"rcpt_to" : "apitest2@api.cn",
"data" : "Subject: Test smtpTransport api\nContent-Type: text/plain; charset=UTF-8\n\nTest smtpTransport api"
}'
```


# 4 附录
## 4.1 返回信息表
所有HTTP调用均返回`ReturnInfo`结构，包含以下3个属性：
- `code`：返回码（核心判断依据，建议优先通过返回码处理逻辑）
- `message`：返回信息（操作失败时提供详细错误描述，仅作参考）
- `result`：返回结果（部分接口返回具体操作结果，格式与接口相关）

### 返回码说明
| 返回码 | 描述 |
| --- | --- |
| 0 | 操作成功 |
| 8 | 该账号已存在 |
| 9 | 用户标识错误 |
| 19 | 用户不存在 |
| 20 | 域名不存在 |
| 28 | 会话已过期 |
| 35 | 密码错误 |
| 39 | 参数错误 |
| 42 | 数据库访问出错 |
| 43 | 错误的UD属性 |
| 44 | 邮箱已存在 |
| 45 | 邮箱未存在 |
| 48 | 会话错误 |
| 49 | 域名已存在 |
| 50 | 服务等级不存在 |
| 51 | 组织不存在 |
| 52 | 组织处于非正常状态（锁定或停用） |
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


## 4.2 组织属性表
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| org_name | string | 组织名称，不提供则使用org_id作为名称 |
| domain_name | string/array | 分配域名（自动创建），可传数组分配多个域名 |
| cos_id | int/array | 分配服务等级，可传数组（如[1,3,5]）分配多个 |
| num_of_classes | int/array | 服务等级可分配用户数，cos_id为数组时需一一对应 |
| res_grp_id | string | 组织资源分组标识 |
| org_assignable_quota | int | 组织可分配容量（MB） |
| org_status | int | 组织状态：0-正常；1-停用；2-锁定 |
| org_expiry_date | string | 过期日期，NULL/空表示不过期（格式：yyyy-MM-dd） |
| org_options | int | 组织增值服务 |
| org_active_options | int | 启用的组织增值服务 |
| org_address | string | 组织通讯录地址 |
| org_phone_number | string | 组织联系电话 |
| org_contact | string | 组织联系人 |
| org_access_level | int | 组织可见性：0-公开；1-组织内及授权用户可见；-1-授权用户可见 |
| org_access_user | string | 组织通讯录授权列表 |
| org_deny_user | string | 组织通讯录禁止列表 |
| org_access_user_l1 | string | 组织通讯录特殊授权 |
| email_allow_user | string | 群发授权列表 |


## 4.3 用户属性表
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| primary_email | string | 额外主邮件地址 |
| alias | array of string | 额外别名邮件地址 |
| org_unit_id | string | 部门标识 |
| user_status | int | 用户状态：0-活跃；1-停用；2-维护中；3-代理；4-锁定；100-延迟删除 |
| password | string | 用户密码 |
| cos_id | int | 服务等级标识 |
| quota_delta | int | 附加邮箱空间（MB） |
| nf_quota_delta | int | 附加网盘空间（MB） |
| privacy_level | int | 信息公开范围：0-不公开；2-组织内；4-站点内 |
| user_list_rank | int | 排序号 |
| true_name | string | 姓名 |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别："0"-男，"1"-女 |
| birthday | string | 生日 |
| alt_email | string | 备用邮箱 |
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
| second_auth_type | int | 二次验证类型：1-关闭；2-短信；4-APP授权 |
| def_sec_folder | string | 安全锁：<br>- 空串/null（关闭）<br>- {fid}（邮箱文件夹）<br>- nf:{fid}（网盘文件夹）<br>- op:{id}（受保护操作：1-自动转发，2-改密码，3-邮箱共享） |
| forwardactive | int | 是否开启转发（邮件列表必须为1） |
| rejectjunk | int | 垃圾邮件处理方式（邮件列表必须为1） |
| maillist_filter | string | 邮件列表动态规则（url编码）：^key1=value1&key2=value2&...<br>key包括：org_id、org_unit_id、recursive（是否含子部门）、type（用户类型：U/X/R/L）、includelist、excludelist |
| junkfilter | int | 邮件列表授权范围：0-所有用户；2-成员+指定用户；3-仅指定用户 |
| safelist | string | 邮件列表授权列表（格式：user1,user2,...） |
| forwardmaillist | string | 邮件列表成员列表（格式：user1,user2,...） |
| maillist_errorto | string | 邮件列表退信接收地址（格式：user1,user2,...） |
| access_user | string | 会议室授权使用列表 |


## 4.4 联系人属性表
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| org_id | string | 组织标识 |
| org_unit_id | string | 部门标识 |
| obj_class | int | 对象类型：1-外部联系人；100-影子用户；101-影子邮件列表 |
| obj_email | string | 外部联系人邮箱地址 |
| obj_creation_date | string | 创建时间，默认当前时间 |
| privacy_level | int | 信息公开范围：0-不公开；2-组织内；4-站点内 |
| obj_list_rank | int | 排序号 |
| true_name | string | 姓名 |
| nick_name | string | 昵称 |
| duty | string | 职位 |
| gender | string | 性别："0"-男，"1"-女 |
| birthday | string | 生日 |
| alt_email | string | 备用邮箱 |
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


## 4.5 信件属性表
| 属性名 | 类型 | 属性含义 |
| --- | --- | --- |
| mid | string | 信件唯一标识 |
| msid | int | 信件所在邮件存储（MS）标识 |
| fid | int | 文件夹标识（1-收件箱，2-发件箱等） |
| flag | int | 信件标志位（如未读、已回复、有附件等） |
| from | string | 发件人邮箱地址 |
| to | string | 收件人邮箱地址（多个以","分隔） |
| subject | string | 邮件主题 |
| size | int | 邮件大小（字节） |
| date | string | 邮件发送时间（格式：yyyy-MM-dd HH:mm:ss） |


## 4.6 单点登录链接
### 说明
单点登录链接需替换`#sid#`为用户实际会话ID（sid），`#mid#`为信件标识（可选），不同模块链接格式如下：

| 模块 | 页面类型 | 链接格式 | 依赖参数 |
| --- | --- | --- | --- |
| XT | 首页 | http://coremail.cn/coremail/main.jsp?sid=#sid# | sid |
| XT | 单独写信 | http://coremail.cn/coremail/XT/detach.jsp?sid=#sid##mail.compose|{"to":"foo@bar.cn"} | sid |
| XT | 完整写信 | http://coremail.cn/coremail/XT/index.jsp?sid=#sid##mail.compose|{"to":"foo@bar.cn"} | sid/firstShowPage |
| XT | 单独读信 | http://coremail.cn/coremail/XT/detach.jsp?sid=#sid##mail.read|{"fid":1,"mid":"#mid#"} | sid/mid |
| XT | 完整读信 | http://coremail.cn/coremail/XT/index.jsp?sid=#sid##mail.read|{"fid":1,"mid":"#mid#"} | sid/mid/firstShowPage |
| XT | 单独收信列表 | http://coremail.cn/coremail/XT/detach.jsp?sid=#sid##mail.list|{"fid":1} | sid/fid |
| XT | 完整收信列表 | http://coremail.cn/coremail/XT/index.jsp?sid=#sid##mail.list|{"fid":1} | sid/fid |
| XT3 | 首页 | http://coremail.cn/coremail/main.jsp?sid=#sid# | sid |
| XT3 | 单独写信 | http://coremail.cn/coremail/XT3/compose/main.jsp?sid=#sid# | sid |
| XT3 | 完整写信 | http://coremail.cn/coremail/XT3/index.jsp?sid=#sid#&firstShowPage=compose%2Fmain.jsp%3Fsid%3D#sid# | sid/firstShowPage |
| XT3 | 单独读信 | http://coremail.cn/coremail/XT3/mbox/viewmail.jsp?sid=#sid#&fid=1&mid=#mid# | sid/mid |
| XT3 | 完整读信 | http://coremail.cn/coremail/XT3/index.jsp?sid=#sid#&firstShowPage=mbox%2Fviewmail.jsp%3Fsid%3D#sid#%26fid%3D1%26nav_type%3Dsystem%26mid%3D#mid# | sid/mid/firstShowPage |
| XT5 | 首页 | http://coremail.cn/coremail/main.jsp?sid=#sid# | sid |
| XT5 | 单独写信 | http://coremail.cn/coremail/XT5/detach.jsp?sid=#sid##mail.compose|{"to":"foo@bar.cn"} | sid |
| XT5 | 完整写信 | http://coremail.cn/coremail/XT5/index.jsp?sid=#sid##mail.compose|{"to":"foo@bar.cn"} | sid/firstShowPage |
| XT5 | 单独读信 | http://coremail.cn/coremail/XT5/detach.jsp?sid=#sid##mail.read|{"fid":1,"mid":"#mid#"} | sid/mid |
| XT5 | 完整读信 | http://coremail.cn/coremail/XT5/index.jsp?sid=#sid##mail.read|{"fid":1,"mid":"#mid#"} | sid/mid/firstShowPage |
| hxphone 2.0 | 读信 | http://coremail.cn/coremail/hxphone/sso.html#/frame/read/-2/#mid#//?sid=#sid# | sid/mid |
| hxphone 2.0/3.0 | 写信 | http://coremail.cn/coremail/hxphone/sso.html#/frame/compose///?sid=#sid# | sid |
| hxphone 2.0/3.0 | 收件箱 | http://coremail.cn/coremail/hxphone/sso.html#/frame/folder/1?sid=#sid# | sid |
| hxphone 3.0+ | 读信 | http://coremail.cn/coremail/hxphone/sso.html#/frame/read/-2/#mid#?sid=#sid# | sid/mid |
| xphone | 首页 | http://coremail.cn/coremail/xphone/main.jsp?sid=#sid# | sid |
| xphone | 写信 | http://coremail.cn/coremail/xphone/main.jsp?sid=#sid#&target=compose | sid/target |
| xphone | 读信 | http://coremail.cn/coremail/xphone/main.jsp?sid=#sid#&target=viewMailContent&mid=#mid# | sid/target/mid |


## 4.7 API HTTP 请求定义文件
- **文件类型**：`.http`（IntelliJ IDEA专用格式）
- **用途**：存储和快速调试RESTful API，可直接在IDEA中打开并发送请求
- **使用建议**：将`apiws-v3.http`文件在IDEA中打开，配合Coremail XT高级API接口调试，提高开发效率


## 联系方式与版权
- **官网**：http://www.coremail.cn/
- **购买咨询**：400-000-1631
- **技术支持**：400-630-7163
- **版权声明**：本文档版权归Coremail®所有，未经书面许可不得公开、转载或散发给第三方，违者追究法律责任。
- **免责声明**：本文档内容可随产品更新，因文档使用不当造成的损失，Coremail不承担责任。
- **文档修订**：最后修订于2022年10月，版本记录详见「文档修改记录」。
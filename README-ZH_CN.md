# Coremail SDK for Python

一个用于与 Coremail XT API v3 交互的全面 Python SDK，提供对所有可用 API 端点的便捷访问，用于用户、组织和系统管理。

## 功能特性

- 完整实现 Coremail XT API v3 端点
- 通过环境变量或显式参数轻松配置
- 自动令牌管理和缓存
- 完整的类型提示和文档
- 支持所有主要 API 操作（用户管理、组织管理、会话管理等）

## 安装

```bash
pip install coremail
```

## 配置

在项目根目录创建 `.env` 文件，包含以下变量：

```env
COREMAIL_BASE_URL=http://your-coremail-server:9900/apiws/v3
COREMAIL_APP_ID=your_app_id@your_domain.com
COREMAIL_SECRET=your_secret_key
```

## 使用方法

### 基本用法

```python
from coremail import CoremailClient

# 使用环境变量初始化客户端
client = CoremailClient()

# 或使用显式参数
client = CoremailClient(
    base_url="http://your-host-of-coremail:9900/apiws/v3",
    app_id="your_app_id@your-domain.com",
    secret="your_secret_key"
)

# 示例：请求令牌
token_response = client.requestToken()
print(f"Token Response: {token_response}")

# 示例：获取用户属性
user_attrs_response = client.getAttrs("test_user@your-domain.com")
print(f"User attributes response: {user_attrs_response}")
```

### 用户管理

```python
# 创建新用户
attrs = {
    "display_name": "John Doe",
    "cos_id": 1,
    "quota": 1024
}
create_response = client.createUser("john.doe@your-domain.com", "password123", attrs)
print(f"User creation response: {create_response}")

# 获取用户属性
user_attrs = client.getAttrs("john.doe@your-domain.com")

# 更新用户属性
update_attrs = {"display_name": "Jane Doe", "quota": 2048}
change_response = client.changeAttrs("john.doe@your-domain.com", update_attrs)

# 删除用户
delete_response = client.deleteUser("john.doe@your-domain.com")
```

### 组织管理

```python
# 创建组织
org_attrs = {
    "org_name": "Example Organization",
    "domain_name": "example.com",
    "cos_id": [1],
    "num_of_classes": [100],
    "org_status": 0,
    "org_expiry_date": "2025-12-31"
}
add_org_response = client.addOrg("example_org", org_attrs)

# 获取组织信息
org_info = client.getOrgInfo("example_org")

# 更新组织
update_attrs = {"org_name": "Updated Organization Name"}
alter_response = client.alterOrg("example_org", update_attrs)
```

### 会话管理

```python
# 用户登录获取会话 ID
login_response = client.userLogin("user@domain.com")
print(f"Login response: {login_response}")

# 检查用户会话
session_check = client.sesTimeOut(login_response["result"])
print(f"Session info: {session_check}")

# 用户登出
logout_response = client.userLogout(login_response["result"])
print(f"Logout response: {logout_response}")
```

## 可用方法

SDK 包含所有 Coremail XT API v3 端点的方法：

### 访问令牌
- `requestToken()` - 请求新的访问令牌

### 登录
- `userLogin(user_at_domain)` - 用户登录获取会话ID
- `userLoginEx(user_at_domain, attrs)` - 带附加参数的用户登录
- `userExist(user_at_domain)` - 检查用户是否存在
- `userExist2(user_at_domain)` - 检查用户是否存在(排除别名) (returns boolean)
- `authenticate(user_at_domain, password)` - 验证用户密码
- `sesTimeOut(ses_id)` - 检查用户会话并返回用户信息
- `sesRefresh(ses_id)` - 刷新用户会话
- `getSessionVar(ses_id, ses_key)` - 获取用户会话中的变量
- `userLogout(ses_id)` - 用户登出
- `setSessionVar(ses_id, ses_key, ses_var)` - 设置用户会话中的变量

### 组织管理
- `addOrg(org_id, attrs)` - 创建组织
- `getOrgInfo(org_id, attrs)` - 获取组织信息
- `alterOrg(org_id, attrs)` - 修改组织
- `addOrgDomain(org_id, domain_name)` - 为组织添加域名
- `delOrgDomain(org_id, domain_name)` - 从组织删除域名
- `addOrgCos(org_id, num_of_classes, cos_name, cos_id)` - 添加服务等级
- `alterOrgCos(org_id, num_of_classes, cos_name, cos_id)` - 更新服务等级
- `delOrgCos(org_id, cos_id)` - 删除服务等级
- `getOrgCosUser(org_id, cos_id)` - 获取服务等级中的用户
- `getOrgList()` - 获取组织列表
- `addUnit(org_id, unit_name, attrs)` - 添加组织单元
- `delUnit(org_id, unit_name)` - 删除组织单元
- `getUnitAttrs(org_id, unit_name, attrs)` - 获取组织单元属性
- `setUnitAttrs(org_id, unit_name, attrs)` - 设置组织单元属性

### 用户管理
- `createUser(user_at_domain, password, attrs)` - 创建用户
- `deleteUser(user_at_domain)` - 删除用户
- `getAttrs(user_at_domain, attrs)` - 获取用户属性
- `changeAttrs(user_at_domain, attrs)` - 更改用户属性
- `addSmtpAlias(user_at_domain, alias)` - 为用户添加 SMTP 别名
- `delSmtpAlias(user_at_domain, alias)` - 删除用户的 SMTP 别名
- `getSmtpAlias(user_at_domain)` - 获取用户的 SMTP 别名
- `setAdminType(user_at_domain, admin_type)` - 设置用户的管理员类型
- `getAdminType(user_at_domain)` - 获取用户的管理员类型
- `renameUser(old_user_at_domain, new_user_at_domain)` - 重命名用户
- `moveUser(user_at_domain, target_org_id, target_unit_name)` - 将用户移动到不同组织/单元

### 对象管理
- `createObj(obj_type, obj_name, org_id, attrs)` - 创建对象（如邮件列表）
- `getObjAttrs(obj_type, obj_name, org_id, attrs)` - 获取对象属性
- `setObjAttrs(obj_type, obj_name, org_id, attrs)` - 设置对象属性
- `deleteObj(obj_type, obj_name, org_id)` - 删除对象

### 域名管理
- `domainExist(domain_name)` - 检查域名是否存在
- `getDomainList(start, limit)` - 获取域名列表
- `addDomain25(domain_name, attrs)` - 添加端口25域名（SMTP）
- `delDomain25(domain_name)` - 删除端口25域名（SMTP）
- `addDomainAlias(domain_name, alias_domain_name)` - 添加域名别名
- `getDomainAlias(domain_name)` - 获取域名别名
- `delDomainAlias(domain_name, alias_domain_name)` - 删除域名别名
- `getOrgListByDomain(domain_name)` - 按域名获取组织列表

### 邮件信息
- `listMailInfos(user_at_domain, start_time, end_time, attrs)` - 列出邮件信息
- `getNewMailInfos(user_at_domain, start_time, end_time, attrs)` - 获取新邮件信息

### 传输
- `smtpTransport(sender, recipient, content)` - SMTP 传输邮件

### 用户查询
- `getUserFromCasName(cas_name)` - 根据CAS名称获取用户邮箱地址

## 错误处理

SDK 会返回原始 API 响应，包括 code、result 和 message 字段。应用程序应检查响应中的 code 字段以确定操作是否成功：

```python
response = client.getAttrs("nonexistent_user@domain.com")
if response.get('code') != 0:
    print(f"API Error: {response.get('message', 'Unknown error')}")
```

## 开发

运行示例：

```bash
python example.py
```

## 许可证

本项目根据 MIT 许可证授权 - 详见 LICENSE 文件了解详情。
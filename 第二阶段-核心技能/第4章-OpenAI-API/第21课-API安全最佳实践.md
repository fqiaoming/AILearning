![安全实践](./images/security.svg)
*图：API安全的多层防护架构*

# 第21课：API安全最佳实践 - 保护你的AI应用

> 📚 **课程信息**
> - 所属模块：第二模块 - API与LangChain开发  
> - 章节：第4章 - API调用基础（第6/7课）
> - 学习目标：掌握API安全策略，保护密钥和防止滥用
> - 预计时间：60-70分钟
> - 前置知识：第16-20课

---

## 📢 课程导入

### 前言

你的API密钥不小心提交到GitHub了，第二天账单显示有人用你的密钥调用了10万次API，欠费$3000！或者有恶意用户疯狂请求你的接口，你的服务器直接被打垮！

这不是危言耸听，而是真实发生过无数次的事故！API安全看似不起眼，但一旦出问题，后果非常严重：金钱损失、数据泄露、服务瘫痪、法律风险！

今天这课，我要教你全套API安全防护方案，让你的AI应用固若金汤！

---

### 核心价值点

**第一，API密钥泄露是最常见也最严重的问题。**

看看这些真实案例：
- GitHub上每天有数千个API密钥被泄露
- 开发者不小心把密钥写在代码里提交
- 有人专门写爬虫搜索泄露的密钥
- 被盗用的密钥每天可能被调用几万次

如果你不重视密钥管理，迟早会中招！而学会正确管理密钥，只需要10分钟，但能避免几千几万的损失！

**第二，访问控制是防止滥用的关键。**

没有访问控制的API就像敞开大门的银行！任何人都能：
- 无限制地请求
- 访问所有功能
- 查看其他用户的数据

但有了访问控制：
- 每个用户有独立密钥
- 设置请求频率限制
- 分配不同权限
- 记录所有操作

这就是专业系统和业余系统的区别！

**第三，安全不是一次性的，而是持续的。**

很多人以为做一次安全配置就万事大吉，错！安全是持续的过程：
- 定期轮换密钥
- 审计访问日志
- 监控异常行为
- 及时更新漏洞

大厂的安全团队每天都在做这些事，这不是过度紧张，而是必要措施！

**第四，这是企业级应用的必备能力。**

面试官经常问：
- "如何保护API密钥？"
- "如何防止API被滥用？"
- "如何实现访问控制？"

如果你答不上来，面试官会觉得你缺乏生产经验。但如果你能系统地讲出来，会大大加分！

---

### 行动号召

今天这一课会教你：
- API密钥的安全管理策略
- 环境变量和密钥管理服务
- 访问控制和权限系统
- 速率限制（Rate Limiting）
- 审计日志和监控告警
- 安全检查清单

**学完这课，你的AI应用安全性会提升10倍！**

---

## 📖 知识讲解

### 1. API密钥安全

#
![Api Architecture](./images/api_architecture.svg)
*图：Api Architecture*

### 1.1 常见安全问题

```
❌ 危险做法：

1. 硬编码在代码中
api_key = "sk-xxxxxxxxxxxxx"

2. 提交到Git仓库
git add .env  # .env包含密钥

3. 写在前端代码
const OPENAI_KEY = "sk-xxxxx"  // 用户可见！

4. 打印到日志
print(f"Using API key: {api_key}")

5. 通过URL传递
https://api.example.com?api_key=sk-xxxxx

6. 共享给他人
"这是我的API密钥：sk-xxxxx"

7. 使用默认密钥
从不更换，一直用同一个
```

#### 1.2 正确的密钥管理

**方法1：环境变量**
```bash
# .env文件
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# 加入.gitignore
echo ".env" >> .gitignore

# Python读取
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

**方法2：配置文件（加密）**
```python
import json
from cryptography.fernet import Fernet

class SecureConfig:
    """加密配置管理"""
    
    def __init__(self, key_file="secret.key"):
        # 生成或加载密钥
        try:
            with open(key_file, "rb") as f:
                self.key = f.read()
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.key)
        
        self.cipher = Fernet(self.key)
    
    def encrypt_config(self, config, filename="config.enc"):
        """加密并保存配置"""
        encrypted = self.cipher.encrypt(json.dumps(config).encode())
        with open(filename, "wb") as f:
            f.write(encrypted)
    
    def load_config(self, filename="config.enc"):
        """加载并解密配置"""
        with open(filename, "rb") as f:
            encrypted = f.read()
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted)

# 使用
config_manager = SecureConfig()

# 首次保存
config_manager.encrypt_config({
    "OPENAI_API_KEY": "sk-xxxxx",
    "DEEPSEEK_API_KEY": "sk-yyyyy"
})

# 后续使用
config = config_manager.load_config()
api_key = config["OPENAI_API_KEY"]
```

**方法3：密钥管理服务**
```python
# AWS Secrets Manager
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Azure Key Vault
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net", 
                     credential=credential)
secret = client.get_secret("OpenAI-API-Key")
api_key = secret.value
```

---

### 2. 访问控制

#### 2.1 API密钥系统

```python
import secrets
import hashlib
from datetime import datetime, timedelta

class APIKeyManager:
    """API密钥管理器"""
    
    def __init__(self):
        self.keys = {}  # 实际应该用数据库
    
    def generate_key(self, user_id, name="", expires_in_days=365):
        """生成API密钥"""
        # 生成随机密钥
        key = f"sk-{secrets.token_urlsafe(32)}"
        
        # 存储密钥信息（应该存储hash，不是明文）
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        self.keys[key_hash] = {
            "user_id": user_id,
            "name": name,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(days=expires_in_days),
            "is_active": True,
            "usage_count": 0,
            "last_used": None
        }
        
        return key  # 只返回一次！
    
    def validate_key(self, key):
        """验证密钥"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        if key_hash not in self.keys:
            return {"valid": False, "error": "密钥不存在"}
        
        key_info = self.keys[key_hash]
        
        # 检查是否激活
        if not key_info["is_active"]:
            return {"valid": False, "error": "密钥已禁用"}
        
        # 检查是否过期
        if datetime.now() > key_info["expires_at"]:
            return {"valid": False, "error": "密钥已过期"}
        
        # 更新使用信息
        key_info["usage_count"] += 1
        key_info["last_used"] = datetime.now()
        
        return {
            "valid": True,
            "user_id": key_info["user_id"],
            "usage_count": key_info["usage_count"]
        }
    
    def revoke_key(self, key):
        """撤销密钥"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        if key_hash in self.keys:
            self.keys[key_hash]["is_active"] = False
            return True
        return False
    
    def rotate_key(self, old_key, user_id):
        """轮换密钥"""
        # 撤销旧密钥
        self.revoke_key(old_key)
        
        # 生成新密钥
        new_key = self.generate_key(user_id, name="Rotated Key")
        return new_key


# 使用示例
key_manager = APIKeyManager()

# 生成密钥
new_key = key_manager.generate_key(user_id="user_001", name="Production Key")
print(f"新密钥：{new_key}")

# 验证密钥
result = key_manager.validate_key(new_key)
print(f"验证结果：{result}")

# 撤销密钥
key_manager.revoke_key(new_key)
```

---

### 3. 速率限制（Rate Limiting）

#### 3.1 固定窗口

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """速率限制器（固定窗口）"""
    
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id):
        """检查是否允许请求"""
        now = datetime.now()
        
        # 清理过期记录
        cutoff = now - self.window
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > cutoff
        ]
        
        # 检查是否超限
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # 记录本次请求
        self.requests[user_id].append(now)
        return True
    
    def get_remaining(self, user_id):
        """获取剩余配额"""
        now = datetime.now()
        cutoff = now - self.window
        
        recent_requests = [
            req_time for req_time in self.requests[user_id]
            if req_time > cutoff
        ]
        
        return self.max_requests - len(recent_requests)


# 使用示例
limiter = RateLimiter(max_requests=5, window_seconds=60)

def api_endpoint(user_id, request):
    """API端点（带速率限制）"""
    if not limiter.is_allowed(user_id):
        remaining = limiter.get_remaining(user_id)
        return {
            "error": "Rate limit exceeded",
            "remaining": remaining,
            "reset_in": 60
        }
    
    # 处理请求
    return {"success": True, "data": "..."}
```

#### 3.2 令牌桶算法

```python
import time

class TokenBucket:
    """令牌桶算法"""
    
    def __init__(self, capacity=10, refill_rate=1):
        """
        capacity: 桶容量
        refill_rate: 每秒补充的令牌数
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_refill
        
        # 计算应补充的令牌数
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens=1):
        """消费令牌"""
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def get_available_tokens(self):
        """获取可用令牌数"""
        self._refill()
        return int(self.tokens)


# 使用示例
bucket = TokenBucket(capacity=10, refill_rate=2)  # 每秒补充2个令牌

def protected_api():
    if not bucket.consume(1):
        return {"error": "Rate limit exceeded", 
                "available_tokens": bucket.get_available_tokens()}
    
    # 执行API逻辑
    return {"success": True}
```

---

### 4. 审计日志

```python
import logging
from datetime import datetime
import json

class APIAuditLogger:
    """API审计日志"""
    
    def __init__(self, log_file="api_audit.log"):
        self.logger = logging.getLogger("API_AUDIT")
        self.logger.setLevel(logging.INFO)
        
        # 文件处理器
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_request(self, user_id, endpoint, method, params=None, 
                   response_status=None, response_time=None):
        """记录API请求"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "endpoint": endpoint,
            "method": method,
            "params": params,
            "response_status": response_status,
            "response_time": response_time
        }
        
        self.logger.info(json.dumps(log_entry))
    
    def log_authentication(self, user_id, success, ip_address=None):
        """记录认证尝试"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "authentication",
            "user_id": user_id,
            "success": success,
            "ip_address": ip_address
        }
        
        self.logger.warning(json.dumps(log_entry))
    
    def log_security_event(self, event_type, user_id, details):
        """记录安全事件"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "security",
            "type": event_type,
            "user_id": user_id,
            "details": details
        }
        
        self.logger.error(json.dumps(log_entry))


# 使用示例
audit_logger = APIAuditLogger()

def secure_api_endpoint(api_key, request_data):
    """安全的API端点"""
    start_time = time.time()
    
    # 验证API密钥
    key_validation = key_manager.validate_key(api_key)
    if not key_validation["valid"]:
        audit_logger.log_authentication(
            user_id="unknown",
            success=False,
            ip_address="127.0.0.1"
        )
        return {"error": "Invalid API key"}
    
    user_id = key_validation["user_id"]
    
    # 检查速率限制
    if not limiter.is_allowed(user_id):
        audit_logger.log_security_event(
            event_type="rate_limit_exceeded",
            user_id=user_id,
            details={"endpoint": "/api/chat"}
        )
        return {"error": "Rate limit exceeded"}
    
    # 处理请求
    response = process_request(request_data)
    
    # 记录审计日志
    response_time = time.time() - start_time
    audit_logger.log_request(
        user_id=user_id,
        endpoint="/api/chat",
        method="POST",
        params=request_data,
        response_status=200,
        response_time=response_time
    )
    
    return response
```

---

## 💻 Demo案例：完整的安全API系统

创建`secure_api_system.py`：

```python
"""
完整的安全API系统
集成密钥管理、访问控制、速率限制、审计日志
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict
import time
import logging


class SecureAPISystem:
    """安全的API系统"""
    
    def __init__(self):
        # 密钥存储（实际应用用数据库）
        self.api_keys = {}
        
        # 速率限制器
        self.rate_limits = defaultdict(list)
        self.max_requests_per_minute = 10
        
        # 审计日志
        self.setup_logging()
    
    def setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('api_audit.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    # ===== 密钥管理 =====
    
    def create_api_key(self, user_id, name=""):
        """创建API密钥"""
        key = f"sk-{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        self.api_keys[key_hash] = {
            "user_id": user_id,
            "name": name,
            "created_at": datetime.now(),
            "is_active": True,
            "request_count": 0
        }
        
        self.logger.info(f"[密钥创建] User: {user_id}, Name: {name}")
        
        return key
    
    def validate_api_key(self, key):
        """验证API密钥"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        if key_hash not in self.api_keys:
            self.logger.warning(f"[认证失败] 无效的密钥")
            return None
        
        key_info = self.api_keys[key_hash]
        
        if not key_info["is_active"]:
            self.logger.warning(f"[认证失败] 密钥已禁用: {key_info['user_id']}")
            return None
        
        return key_info
    
    # ===== 速率限制 =====
    
    def check_rate_limit(self, user_id):
        """检查速率限制"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # 清理过期记录
        self.rate_limits[user_id] = [
            req_time for req_time in self.rate_limits[user_id]
            if req_time > minute_ago
        ]
        
        # 检查是否超限
        if len(self.rate_limits[user_id]) >= self.max_requests_per_minute:
            self.logger.warning(f"[速率限制] User: {user_id}, 超过限制")
            return False
        
        # 记录请求
        self.rate_limits[user_id].append(now)
        return True
    
    # ===== API端点 =====
    
    def chat_endpoint(self, api_key, message):
        """聊天API端点"""
        start_time = time.time()
        
        # 1. 验证密钥
        key_info = self.validate_api_key(api_key)
        if not key_info:
            return {
                "success": False,
                "error": "无效的API密钥"
            }
        
        user_id = key_info["user_id"]
        
        # 2. 检查速率限制
        if not self.check_rate_limit(user_id):
            return {
                "success": False,
                "error": "请求过于频繁，请稍后重试"
            }
        
        # 3. 处理请求（这里简化处理）
        response = f"收到消息：{message}"
        
        # 4. 更新统计
        key_info["request_count"] += 1
        
        # 5. 记录审计日志
        elapsed = time.time() - start_time
        self.logger.info(
            f"[API请求] User: {user_id}, "
            f"Message: {message[:50]}..., "
            f"Time: {elapsed:.3f}s"
        )
        
        return {
            "success": True,
            "response": response,
            "user_id": user_id,
            "remaining_requests": self.max_requests_per_minute - 
                                len(self.rate_limits[user_id])
        }
    
    def get_stats(self, api_key):
        """获取统计信息"""
        key_info = self.validate_api_key(api_key)
        if not key_info:
            return {"error": "无效的API密钥"}
        
        user_id = key_info["user_id"]
        
        return {
            "user_id": user_id,
            "total_requests": key_info["request_count"],
            "created_at": key_info["created_at"].isoformat(),
            "remaining_this_minute": self.max_requests_per_minute - 
                                    len(self.rate_limits[user_id])
        }


def demo():
    """演示"""
    print("🔐 安全API系统演示\n")
    
    system = SecureAPISystem()
    
    # 1. 创建API密钥
    print("="*60)
    print("步骤1：创建API密钥")
    print("="*60)
    api_key = system.create_api_key("user_001", "测试密钥")
    print(f"✓ API密钥：{api_key[:20]}...")
    
    # 2. 正常请求
    print("\n" + "="*60)
    print("步骤2：正常请求")
    print("="*60)
    
    for i in range(3):
        result = system.chat_endpoint(api_key, f"测试消息 {i+1}")
        print(f"请求{i+1}：{result['success']}, "
              f"剩余配额：{result.get('remaining_requests', 0)}")
    
    # 3. 测试速率限制
    print("\n" + "="*60)
    print("步骤3：测试速率限制（快速请求）")
    print("="*60)
    
    success_count = 0
    failed_count = 0
    
    for i in range(15):  # 超过限制
        result = system.chat_endpoint(api_key, f"快速请求 {i+1}")
        if result["success"]:
            success_count += 1
        else:
            failed_count += 1
    
    print(f"✓ 成功：{success_count}次")
    print(f"✗ 限流：{failed_count}次")
    
    # 4. 查看统计
    print("\n" + "="*60)
    print("步骤4：查看统计信息")
    print("="*60)
    
    stats = system.get_stats(api_key)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 5. 测试无效密钥
    print("\n" + "="*60)
    print("步骤5：测试无效密钥")
    print("="*60)
    
    result = system.chat_endpoint("invalid_key", "测试")
    print(f"结果：{result}")


if __name__ == "__main__":
    demo()
```

---

## 🎯 安全检查清单

### 开发阶段

```
✅ 密钥管理
  □ 使用环境变量存储密钥
  □ .env文件加入.gitignore
  □ 不在代码中硬编码密钥
  □ 不在日志中打印密钥

✅ 代码安全
  □ 输入验证和清洗
  □ 参数类型检查
  □ SQL注入防护
  □ XSS防护

✅ 访问控制
  □ 实现API密钥系统
  □ 每个用户独立密钥
  □ 密钥定期轮换
```

### 生产环境

```
✅ 部署安全
  □ 使用HTTPS
  □ 配置CORS
  □ 隐藏错误详情
  □ 设置超时限制

✅ 监控告警
  □ 异常请求监控
  □ 速率限制告警
  □ 成本异常告警
  □ 认证失败告警

✅ 审计合规
  □ 记录所有API调用
  □ 保留日志至少90天
  □ 定期安全审计
  □ 合规性检查
```

---

## ✅ 课后检验

完成本课后，你应该能够：

- [ ] 安全管理API密钥
- [ ] 实现访问控制系统
- [ ] 设计速率限制策略
- [ ] 记录审计日志
- [ ] 构建安全的API系统

---

## 📝 下一课预告

**第22课：API调用最佳实践总结**

完成API基础章节的最后一课，我们将：
- 总结API调用的所有要点
- 生产级API服务架构
- 性能优化技巧
- 实战案例分析

**第4章的完美收官！**

---

**🎉 恭喜你完成第21课！**

你的API应用现在既强大又安全！

**进度：21/165课（12.7%完成）** 🚀


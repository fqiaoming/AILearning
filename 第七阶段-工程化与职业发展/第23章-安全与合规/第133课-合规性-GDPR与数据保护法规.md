![安全合规架构](./images/security.svg)
*图：安全合规架构*

# 第133课：合规性 - GDPR与数据保护法规

> **本课目标**：了解数据合规要求，建立合规体系
> 
> **核心技能**：GDPR要求、数据保护、隐私政策、合规审计
> 
> **学习时长**：90分钟

---

## 📖 口播文案（8分钟）
![Api Security](./images/api_security.svg)
*图：Api Security*


### 🎯 前言

"系统上线了，用户数据收集了，**合法吗？**

**不合规=巨额罚款！**

**真实罚款案例：**

```
案例1：Google（2019）
• 违规：GDPR
• 罚款：5000万欧元
• 原因：未获得有效同意

案例2：Amazon（2021）
• 违规：GDPR
• 罚款：7.46亿欧元
• 原因：未经同意使用数据

案例3：Meta（2023）
• 违规：GDPR
• 罚款：12亿欧元
• 原因：跨境数据传输

案例4：滴滴（2022）
• 违规：网络安全法
• 罚款：80.26亿人民币
• 原因：违法收集使用数据

不是开玩笑！
```

**GDPR的7大原则：**

```
原则1：合法性、公平性、透明性
• 必须告知用户收集什么数据
• 用途必须明确
• 必须获得同意

原则2：目的限制
• 只能用于声明的目的
• 不能用于其他用途

原则3：数据最小化
• 只收集必要的数据
• 不过度收集

原则4：准确性
• 数据必须准确
• 允许用户更正

原则5：存储限制
• 不能永久保存
• 超期必须删除

原则6：完整性和保密性
• 必须保护数据安全
• 防止泄露

原则7：问责制
• 企业负责
• 必须证明合规
```

**用户的8大权利：**

```
权利1：知情权
• 知道收集了什么数据
• 知道如何使用

权利2：访问权
• 可以查看自己的数据
• 免费获取副本

权利3：更正权
• 可以更正错误数据

权利4：删除权（被遗忘权）
• 可以要求删除数据
• "删除我的账号"

权利5：限制处理权
• 可以限制某些用途

权利6：数据可携带权
• 可以导出数据
• 可以转移到其他服务

权利7：反对权
• 可以反对某些处理
• 如：营销邮件

权利8：自动化决策
• 不受纯自动化决策影响
• 如：AI拒绝贷款，需人工审核

必须实现！
```

**AI应用的特殊合规要求：**

```
挑战1：训练数据
• 问题：用用户数据训练模型？
• 要求：必须获得明确同意
• 解决：
  - 匿名化数据
  - 脱敏处理
  - 获得授权

挑战2：模型决策
• 问题：AI决策是否可解释？
• 要求：用户有权知道决策依据
• 解决：
  - 可解释AI
  - 决策日志
  - 人工审核

挑战3：数据留存
• 问题：模型需要历史数据？
• 要求：不能无限期保存
• 解决：
  - 定期清理
  - 匿名化存储
  - 联邦学习

挑战4：第三方模型
• 问题：使用OpenAI等API？
• 要求：数据跨境合规
• 解决：
  - 数据处理协议
  - 隐私条款
  - 本地部署
```

**中国的数据保护法规：**

```
【个人信息保护法】（2021）

• 类似GDPR
• 个人信息定义更广
• 罚款：5000万或年营收5%

关键要求：
✓ 告知同意
✓ 目的限制
✓ 公开透明
✓ 准确完整
✓ 安全保障

【网络安全法】（2017）

• 网络运营者责任
• 关键信息基础设施
• 数据本地化

【数据安全法】（2021）

• 数据分级分类
• 重要数据保护
• 数据跨境管理

三法合一，全面监管！
```

**今天这一课，我要带你：**

**第一部分：GDPR实施**
- 用户同意管理
- 数据主体权利
- 隐私政策

**第二部分：中国法规**
- 个人信息保护
- 数据分类分级
- 本地化要求

**第三部分：合规实践**
- 数据地图
- 影响评估
- 合规审计

**第四部分：技术实现**
- 同意管理
- 数据导出
- 数据删除

建立合规体系！"

---

## 📚 第一部分：GDPR合规实施

### 一、用户同意管理

```python
# app/models/consent.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class ConsentPurpose(str, Enum):
    """同意目的"""
    ESSENTIAL = "essential"  # 必要功能
    ANALYTICS = "analytics"  # 数据分析
    MARKETING = "marketing"  # 营销
    TRAINING = "training"  # 模型训练
    PERSONALIZATION = "personalization"  # 个性化

class ConsentStatus(str, Enum):
    """同意状态"""
    GRANTED = "granted"  # 已同意
    DENIED = "denied"  # 已拒绝
    WITHDRAWN = "withdrawn"  # 已撤回

class UserConsent(BaseModel):
    """用户同意记录"""
    user_id: int
    purpose: ConsentPurpose
    status: ConsentStatus
    granted_at: Optional[datetime] = None
    withdrawn_at: Optional[datetime] = None
    ip_address: str
    user_agent: str
    version: str  # 隐私政策版本
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 123,
                "purpose": "training",
                "status": "granted",
                "granted_at": "2024-01-15T10:30:00Z",
                "ip_address": "1.2.3.4",
                "user_agent": "Mozilla/5.0...",
                "version": "v1.0"
            }
        }

class ConsentManager:
    """同意管理器"""
    
    def __init__(self, db):
        """初始化"""
        self.db = db
    
    async def request_consent(
        self,
        user_id: int,
        purposes: List[ConsentPurpose],
        ip_address: str,
        user_agent: str
    ) -> dict:
        """
        请求用户同意
        
        Args:
            user_id: 用户ID
            purposes: 用途列表
            ip_address: IP地址
            user_agent: 用户代理
        
        Returns:
            同意请求信息
        """
        
        return {
            "user_id": user_id,
            "purposes": [
                {
                    "purpose": purpose,
                    "description": self._get_purpose_description(purpose),
                    "required": purpose == ConsentPurpose.ESSENTIAL
                }
                for purpose in purposes
            ],
            "policy_url": "https://example.com/privacy",
            "policy_version": "v1.0"
        }
    
    async def grant_consent(
        self,
        user_id: int,
        purpose: ConsentPurpose,
        ip_address: str,
        user_agent: str
    ):
        """
        授予同意
        
        Args:
            user_id: 用户ID
            purpose: 用途
            ip_address: IP地址
            user_agent: 用户代理
        """
        
        consent = UserConsent(
            user_id=user_id,
            purpose=purpose,
            status=ConsentStatus.GRANTED,
            granted_at=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent,
            version="v1.0"
        )
        
        # 保存到数据库
        # await self.db.save(consent)
        
        print(f"✓ 用户{user_id}同意了{purpose.value}")
    
    async def withdraw_consent(
        self,
        user_id: int,
        purpose: ConsentPurpose
    ):
        """
        撤回同意
        
        Args:
            user_id: 用户ID
            purpose: 用途
        """
        
        # 更新数据库
        # await self.db.update(
        #     user_id=user_id,
        #     purpose=purpose,
        #     status=ConsentStatus.WITHDRAWN,
        #     withdrawn_at=datetime.utcnow()
        # )
        
        print(f"✓ 用户{user_id}撤回了{purpose.value}的同意")
        
        # 触发数据清理
        await self._cleanup_data(user_id, purpose)
    
    async def check_consent(
        self,
        user_id: int,
        purpose: ConsentPurpose
    ) -> bool:
        """
        检查是否有同意
        
        Args:
            user_id: 用户ID
            purpose: 用途
        
        Returns:
            是否同意
        """
        
        # 查询数据库
        # consent = await self.db.get(user_id=user_id, purpose=purpose)
        # return consent and consent.status == ConsentStatus.GRANTED
        
        return True  # 示例
    
    def _get_purpose_description(self, purpose: ConsentPurpose) -> str:
        """获取用途描述"""
        descriptions = {
            ConsentPurpose.ESSENTIAL: "提供核心服务功能",
            ConsentPurpose.ANALYTICS: "分析使用情况以改进服务",
            ConsentPurpose.MARKETING: "发送个性化营销信息",
            ConsentPurpose.TRAINING: "用于训练和改进AI模型",
            ConsentPurpose.PERSONALIZATION: "提供个性化内容和推荐"
        }
        return descriptions.get(purpose, "")
    
    async def _cleanup_data(self, user_id: int, purpose: ConsentPurpose):
        """清理相关数据"""
        print(f"  清理用户{user_id}的{purpose.value}相关数据...")
```

### 二、数据主体权利实现

```python
# app/services/data_rights.py
from typing import Dict, List
import json
from datetime import datetime

class DataSubjectRights:
    """数据主体权利服务"""
    
    def __init__(self, db):
        """初始化"""
        self.db = db
    
    async def export_user_data(self, user_id: int) -> Dict:
        """
        导出用户数据（可携带权）
        
        Args:
            user_id: 用户ID
        
        Returns:
            用户所有数据
        """
        
        print(f"导出用户{user_id}的数据...")
        
        # 从各个表收集数据
        user_data = {
            "personal_info": await self._get_personal_info(user_id),
            "predictions": await self._get_predictions(user_id),
            "consents": await self._get_consents(user_id),
            "activity_log": await self._get_activity_log(user_id),
            "export_date": datetime.utcnow().isoformat(),
            "format_version": "1.0"
        }
        
        return user_data
    
    async def delete_user_data(self, user_id: int, reason: str = ""):
        """
        删除用户数据（被遗忘权）
        
        Args:
            user_id: 用户ID
            reason: 删除原因
        """
        
        print(f"删除用户{user_id}的数据...")
        print(f"原因：{reason}")
        
        # 记录删除请求
        await self._log_deletion_request(user_id, reason)
        
        # 删除各个表的数据
        tables = [
            "users",
            "predictions",
            "user_activity",
            "consents",
            "sessions"
        ]
        
        for table in tables:
            # await self.db.delete(table, user_id=user_id)
            print(f"  ✓ 删除表{table}的数据")
        
        # 匿名化无法删除的数据（如审计日志）
        await self._anonymize_audit_logs(user_id)
        
        print(f"✓ 用户{user_id}的数据已删除")
    
    async def rectify_user_data(
        self,
        user_id: int,
        corrections: Dict
    ):
        """
        更正用户数据（更正权）
        
        Args:
            user_id: 用户ID
            corrections: 更正内容
        """
        
        print(f"更正用户{user_id}的数据...")
        
        # 记录更正请求
        await self._log_rectification(user_id, corrections)
        
        # 更新数据
        # await self.db.update("users", user_id, corrections)
        
        print(f"✓ 数据已更正")
    
    async def restrict_processing(
        self,
        user_id: int,
        purposes: List[str]
    ):
        """
        限制处理（限制处理权）
        
        Args:
            user_id: 用户ID
            purposes: 限制的用途
        """
        
        print(f"限制用户{user_id}的数据处理：{purposes}")
        
        # 更新处理限制
        for purpose in purposes:
            # await self.db.update_processing_restriction(user_id, purpose, True)
            print(f"  ✓ 限制{purpose}处理")
    
    async def _get_personal_info(self, user_id: int) -> Dict:
        """获取个人信息"""
        return {
            "user_id": user_id,
            "username": "user123",
            "email": "user@example.com",
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    async def _get_predictions(self, user_id: int) -> List[Dict]:
        """获取预测记录"""
        return [
            {
                "id": 1,
                "input": "测试文本",
                "output": "结果",
                "timestamp": "2024-01-15T10:00:00Z"
            }
        ]
    
    async def _get_consents(self, user_id: int) -> List[Dict]:
        """获取同意记录"""
        return []
    
    async def _get_activity_log(self, user_id: int) -> List[Dict]:
        """获取活动日志"""
        return []
    
    async def _log_deletion_request(self, user_id: int, reason: str):
        """记录删除请求"""
        # await self.db.log_audit("user_deletion", user_id, reason)
        pass
    
    async def _anonymize_audit_logs(self, user_id: int):
        """匿名化审计日志"""
        # await self.db.anonymize("audit_logs", user_id)
        print(f"  ✓ 审计日志已匿名化")
    
    async def _log_rectification(self, user_id: int, corrections: Dict):
        """记录更正"""
        # await self.db.log_audit("data_rectification", user_id, corrections)
        pass
```

---

## 💻 第二部分：合规技术实现

### 一、隐私政策生成器

```python
# app/services/privacy_policy.py
from datetime import datetime
from typing import List

class PrivacyPolicyGenerator:
    """隐私政策生成器"""
    
    @staticmethod
    def generate_policy(
        company_name: str,
        contact_email: str,
        data_types: List[str],
        purposes: List[str],
        retention_period: str
    ) -> str:
        """
        生成隐私政策
        
        Args:
            company_name: 公司名称
            contact_email: 联系邮箱
            data_types: 收集的数据类型
            purposes: 使用目的
            retention_period: 保留期限
        
        Returns:
            隐私政策文本
        """
        
        policy = f"""
# 隐私政策

最后更新：{datetime.utcnow().strftime('%Y年%m月%d日')}

## 1. 引言

{company_name}（"我们"）重视您的隐私。本隐私政策说明我们如何收集、使用和保护您的个人信息。

## 2. 我们收集的信息

我们收集以下类型的信息：

{self._format_list(data_types)}

## 3. 信息的使用目的

我们将您的信息用于以下目的：

{self._format_list(purposes)}

## 4. 数据保留

我们将保留您的个人信息{retention_period}，除非法律要求更长的保留期限。

## 5. 您的权利

根据GDPR和相关法规，您享有以下权利：

- **访问权**：您可以请求访问我们持有的您的个人信息
- **更正权**：您可以要求更正不准确的信息
- **删除权**：您可以要求删除您的个人信息
- **限制处理权**：您可以要求限制对您信息的处理
- **数据可携带权**：您可以请求以结构化格式获取您的数据
- **反对权**：您可以反对某些类型的处理

## 6. 数据安全

我们采取以下措施保护您的数据：

- 加密传输（HTTPS/TLS）
- 加密存储（AES-256）
- 访问控制和审计
- 定期安全评估

## 7. Cookie政策

我们使用以下类型的Cookie：

- **必要Cookie**：确保网站正常运行
- **分析Cookie**：帮助我们了解用户如何使用网站
- **营销Cookie**：用于个性化广告（需要您的同意）

## 8. 第三方共享

我们不会出售您的个人信息。我们仅在以下情况下共享信息：

- 获得您的明确同意
- 法律要求
- 保护我们的合法权益

## 9. 国际数据传输

如果您的数据被传输到其他国家，我们将确保：

- 目的地国家有足够的数据保护水平
- 或采用标准合同条款
- 或获得您的明确同意

## 10. 儿童隐私

我们的服务不面向16岁以下儿童。我们不会故意收集儿童的个人信息。

## 11. 政策更新

我们可能会不时更新本政策。重大变更时，我们会通知您。

## 12. 联系我们

如有任何问题或行使您的权利，请联系：

- 邮箱：{contact_email}
- 数据保护官：dpo@{company_name.lower().replace(' ', '')}.com

## 13. 监管机构

如果您对我们处理您个人信息的方式有顾虑，您有权向数据保护监管机构投诉。
"""
        
        return policy.strip()
    
    @staticmethod
    def _format_list(items: List[str]) -> str:
        """格式化列表"""
        return '\n'.join(f"- {item}" for item in items)

# 使用示例
generator = PrivacyPolicyGenerator()

policy = generator.generate_policy(
    company_name="AI Company",
    contact_email="privacy@aicompany.com",
    data_types=[
        "用户名和邮箱地址",
        "使用日志和IP地址",
        "预测输入和输出",
        "Cookie和类似技术"
    ],
    purposes=[
        "提供和改进AI服务",
        "个性化用户体验",
        "分析服务使用情况",
        "通信和客户支持"
    ],
    retention_period="2年"
)

print(policy)
```

---

## 📝 课后总结

### 核心收获

1. **GDPR合规**
   - 7大原则
   - 用户8大权利
   - 同意管理

2. **中国法规**
   - 个人信息保护法
   - 网络安全法
   - 数据安全法

3. **技术实现**
   - 数据导出
   - 数据删除
   - 同意管理

4. **合规流程**
   - 隐私政策
   - 影响评估
   - 合规审计

---

## 🚀 下节预告

下一课：**第134课：需求分析 - 从业务需求到技术方案**

- 需求分析方法
- 技术方案设计
- 可行性评估
- 项目规划

**进入职业发展阶段！** 🔥

---

**💪 合规体系建立完成！安全合法运营！**

**安全章节圆满完成！** ✅

**下一课见！** 🎉

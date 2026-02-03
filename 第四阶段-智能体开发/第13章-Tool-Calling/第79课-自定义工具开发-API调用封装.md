![Tool Calling流程](./images/tool_calling.svg)
*图：Tool Calling流程*

# 第79课：自定义工具开发-API调用封装

> **本课目标**：掌握如何将API封装为Agent工具
> 
> **核心技能**：HTTP请求、API认证、错误处理、重试机制
> 
> **实战案例**：封装天气API、翻译API、地图API
> 
> **学习时长**：80分钟

---

## 📖 口播文案（5分钟）
![Tool Chain](./images/tool_chain.svg)
*图：Tool Chain*


### 🎯 前言

"前面我们学习了内置工具的使用。

今天我们要学习：**如何开发自己的工具！**

特别是：**如何把API封装成Agent工具！**

**为什么要封装API？**

因为Agent的真正威力来自于：**连接外部世界！**

看几个真实场景：

**场景1：智能天气助手**
```
用户："明天北京天气怎么样？"

没有API：
"抱歉，我不知道实时天气..."

有天气API：
调用 → 获取实时数据 → 准确回答
"明天北京多云，15-22℃"

✅ 完美！
```

**场景2：智能翻译助手**
```
用户："把这段话翻译成英文：你好世界"

没有API：
可能翻译错误

有翻译API：
调用Google Translate API
→ 准确翻译
"Hello World"

✅ 专业！
```

**场景3：智能地图助手**
```
用户："从北京到上海怎么走？"

没有API：
只能给建议

有地图API：
调用Google Maps API
→ 实时路线
"高铁4.5小时，或飞机2小时"

✅ 实用！
```

**API封装的关键点：**

**1. 统一接口**
```python
class WeatherAPITool:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def run(self, city: str) -> str:
        # 统一的调用接口
        return self._call_api(city)
```

**2. 错误处理**
```python
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.Timeout:
    return "请求超时"
except requests.exceptions.HTTPError:
    return "API返回错误"
```

**3. 认证管理**
```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

**4. 重试机制**
```python
@retry(tries=3, delay=1)
def call_api():
    ...
```

**5. 结果解析**
```python
def parse_response(response):
    data = response.json()
    return self.format_result(data)
```

**实际API封装流程：**

```
【第1步】了解API文档
• 请求方式（GET/POST）
• 请求参数
• 响应格式
• 认证方式

【第2步】实现基础调用
• HTTP请求
• 参数传递
• 结果获取

【第3步】添加错误处理
• 网络错误
• API错误
• 超时处理

【第4步】封装为工具
• 统一接口
• 工具描述
• 参数定义

【第5步】测试验证
• 单元测试
• 边界测试
• 错误测试
```

**今天要封装的3个API：**

**1. OpenWeatherMap API**
```
功能：天气查询
免费额度：60次/分钟
难度：⭐⭐
```

**2. Google Translate API**
```
功能：文本翻译
需要：API Key
难度：⭐⭐⭐
```

**3. Geocoding API**
```
功能：地址解析
应用：地图、位置
难度：⭐⭐
```

**今天这一课，我要带你：**

**第一部分：API调用基础**
- HTTP请求
- 认证方式
- 常见问题

**第二部分：天气API封装**
- OpenWeatherMap
- 完整实现
- 测试验证

**第三部分：翻译API封装**
- Google Translate
- 语言检测
- 批量翻译

**第四部分：通用API封装框架**
- 基类设计
- 错误处理
- 重试机制

**第五部分：最佳实践**
- API Key管理
- 缓存策略
- 性能优化

学完这一课，你将能封装任何API！

准备好了吗？让我们开始！"

---

### 💡 核心理念

```
【API = Agent的超能力】

没有API：
• 只能聊天
• 信息过时
• 能力有限

有了API：
• 连接外部世界
• 获取实时数据
• 能力无限

【好的API工具特征】

1. 易用：接口简单
2. 可靠：错误处理完善
3. 高效：有缓存和重试
4. 安全：API Key安全管理
```

---

## 📚 第一部分：API调用基础

### 一、HTTP请求基础

```python
import requests
from typing import Dict, Any, Optional
import time

class APIClient:
    """API客户端基类"""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 10
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(
        self,
        endpoint: str,
        params: Dict = None,
        headers: Dict = None
    ) -> Dict:
        """GET请求"""
        
        url = f"{self.base_url}/{endpoint}"
        
        # 添加认证
        if headers is None:
            headers = {}
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise APIError("请求超时")
        except requests.exceptions.HTTPError as e:
            raise APIError(f"HTTP错误: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"请求失败: {str(e)}")
    
    def post(
        self,
        endpoint: str,
        data: Dict = None,
        json_data: Dict = None,
        headers: Dict = None
    ) -> Dict:
        """POST请求"""
        
        url = f"{self.base_url}/{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise APIError("请求超时")
        except requests.exceptions.HTTPError as e:
            raise APIError(f"HTTP错误: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"请求失败: {str(e)}")

class APIError(Exception):
    """API错误"""
    pass
```

---

## 💻 第二部分：天气API封装

### 完整的天气API工具

```python
class WeatherAPITool:
    """天气API工具（OpenWeatherMap）"""
    
    def __init__(self, api_key: str):
        self.name = "get_weather"
        self.description = "获取指定城市的实时天气信息"
        
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.client = APIClient(self.base_url, timeout=10)
    
    def run(self, city: str, units: str = "metric") -> str:
        """
        获取天气
        
        Args:
            city: 城市名称
            units: 单位（metric=摄氏度，imperial=华氏度）
        """
        try:
            # 调用API
            data = self._call_weather_api(city, units)
            
            # 解析结果
            result = self._parse_weather_data(data)
            
            return result
            
        except APIError as e:
            return f"获取天气失败：{str(e)}"
        except Exception as e:
            return f"错误：{str(e)}"
    
    def _call_weather_api(self, city: str, units: str) -> Dict:
        """调用天气API"""
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
            "lang": "zh_cn"
        }
        
        return self.client.get("weather", params=params)
    
    def _parse_weather_data(self, data: Dict) -> str:
        """解析天气数据"""
        
        try:
            city = data["name"]
            country = data["sys"]["country"]
            
            # 天气信息
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            humidity = data["main"]["humidity"]
            
            # 天气描述
            weather = data["weather"][0]
            description = weather["description"]
            
            # 风速
            wind_speed = data["wind"]["speed"]
            
            # 格式化结果
            result = f"""
{city}, {country} 天气信息：

天气状况：{description}
当前温度：{temp}°C
体感温度：{feels_like}°C
温度范围：{temp_min}°C - {temp_max}°C
湿度：{humidity}%
风速：{wind_speed} m/s
""".strip()
            
            return result
            
        except KeyError as e:
            raise APIError(f"数据解析失败：缺少字段{str(e)}")
    
    def to_dict(self) -> Dict:
        """转为工具定义"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如'Beijing'、'Shanghai'"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["metric", "imperial"],
                            "description": "温度单位，metric=摄氏度，imperial=华氏度"
                        }
                    },
                    "required": ["city"]
                }
            }
        }

# 演示
def demo_weather_api():
    """演示天气API"""
    
    # 注意：需要替换为真实的API Key
    # 免费注册：https://openweathermap.org/api
    api_key = "YOUR_API_KEY_HERE"
    
    if api_key == "YOUR_API_KEY_HERE":
        print("请先设置API Key")
        print("注册地址：https://openweathermap.org/api")
        return
    
    weather_tool = WeatherAPITool(api_key)
    
    print("="*60)
    print("天气API工具演示")
    print("="*60)
    
    # 测试查询
    cities = ["Beijing", "Shanghai", "New York"]
    
    for city in cities:
        print(f"\n查询 {city} 的天气：")
        result = weather_tool.run(city)
        print(result)
        time.sleep(1)  # 避免请求过快

# demo_weather_api()
```

---

## 🎯 第三部分：翻译API封装

### 翻译API工具

```python
class TranslateAPITool:
    """翻译API工具"""
    
    def __init__(self, api_key: str = None):
        self.name = "translate"
        self.description = "将文本翻译成指定语言"
        
        self.api_key = api_key
        
        # 这里使用MyMemory免费翻译API（无需Key）
        # 实际项目建议使用Google Translate API或DeepL API
        self.base_url = "https://api.mymemory.translated.net"
        self.client = APIClient(self.base_url)
    
    def run(
        self,
        text: str,
        target_lang: str = "zh",
        source_lang: str = "auto"
    ) -> str:
        """
        翻译文本
        
        Args:
            text: 要翻译的文本
            target_lang: 目标语言（zh=中文，en=英文，etc）
            source_lang: 源语言（auto=自动检测）
        """
        try:
            # 调用API
            result = self._call_translate_api(text, source_lang, target_lang)
            
            # 解析结果
            translated = self._parse_result(result)
            
            return f"翻译结果：{translated}"
            
        except APIError as e:
            return f"翻译失败：{str(e)}"
        except Exception as e:
            return f"错误：{str(e)}"
    
    def _call_translate_api(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Dict:
        """调用翻译API"""
        
        params = {
            "q": text,
            "langpair": f"{source_lang}|{target_lang}"
        }
        
        return self.client.get("get", params=params)
    
    def _parse_result(self, data: Dict) -> str:
        """解析翻译结果"""
        
        try:
            translated = data["responseData"]["translatedText"]
            return translated
        except KeyError:
            raise APIError("翻译结果解析失败")
    
    def to_dict(self) -> Dict:
        """转为工具定义"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "要翻译的文本"
                        },
                        "target_lang": {
                            "type": "string",
                            "description": "目标语言代码，如zh(中文)、en(英文)、ja(日文)"
                        },
                        "source_lang": {
                            "type": "string",
                            "description": "源语言代码，auto表示自动检测"
                        }
                    },
                    "required": ["text", "target_lang"]
                }
            }
        }

# 演示
def demo_translate_api():
    """演示翻译API"""
    
    translate_tool = TranslateAPITool()
    
    print("="*60)
    print("翻译API工具演示")
    print("="*60)
    
    # 测试翻译
    test_cases = [
        ("Hello World", "zh", "en"),
        ("人工智能", "en", "zh"),
        ("Bonjour", "zh", "fr")
    ]
    
    for text, target, source in test_cases:
        print(f"\n翻译：{text}")
        print(f"  {source} → {target}")
        result = translate_tool.run(text, target, source)
        print(f"  {result}")
        time.sleep(1)

demo_translate_api()
```

---

## ⚡ 第四部分：通用API工具框架

### 可复用的API工具基类

```python
from abc import ABC, abstractmethod
from functools import wraps
import hashlib
import json

def retry(tries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(tries):
                try:
                    return func(*args, **kwargs)
                except APIError as e:
                    if attempt == tries - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class BaseAPITool(ABC):
    """API工具基类"""
    
    def __init__(
        self,
        name: str,
        description: str,
        api_key: Optional[str] = None
    ):
        self.name = name
        self.description = description
        self.api_key = api_key
        
        # 缓存
        self.cache = {}
        self.cache_enabled = True
        self.cache_ttl = 3600  # 1小时
    
    @abstractmethod
    def _call_api(self, **kwargs) -> Dict:
        """调用API（子类实现）"""
        pass
    
    @abstractmethod
    def _parse_response(self, response: Dict) -> str:
        """解析响应（子类实现）"""
        pass
    
    @retry(tries=3, delay=1)
    def run(self, **kwargs) -> str:
        """执行工具（带缓存和重试）"""
        
        # 检查缓存
        if self.cache_enabled:
            cache_key = self._get_cache_key(kwargs)
            if cache_key in self.cache:
                cached_result, cached_time = self.cache[cache_key]
                if time.time() - cached_time < self.cache_ttl:
                    return cached_result
        
        try:
            # 调用API
            response = self._call_api(**kwargs)
            
            # 解析结果
            result = self._parse_response(response)
            
            # 保存到缓存
            if self.cache_enabled:
                self.cache[cache_key] = (result, time.time())
            
            return result
            
        except Exception as e:
            return f"错误：{str(e)}"
    
    def _get_cache_key(self, params: Dict) -> str:
        """生成缓存键"""
        param_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(param_str.encode()).hexdigest()
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """转为工具定义（子类实现）"""
        pass

# 使用示例
class CustomWeatherTool(BaseAPITool):
    """自定义天气工具（继承基类）"""
    
    def __init__(self, api_key: str):
        super().__init__(
            name="custom_weather",
            description="获取天气信息",
            api_key=api_key
        )
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.client = APIClient(self.base_url)
    
    def _call_api(self, city: str, **kwargs) -> Dict:
        """调用API"""
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        return self.client.get("weather", params=params)
    
    def _parse_response(self, response: Dict) -> str:
        """解析响应"""
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"温度：{temp}°C，{description}"
    
    def to_dict(self) -> Dict:
        """工具定义"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
```

---

## 📝 课后练习

### 练习1：封装更多API
尝试封装GitHub API、新闻API等

### 练习2：添加高级缓存
使用Redis实现分布式缓存

### 练习3：监控和日志
添加完整的API调用监控

---

## 🎓 知识总结

### 核心要点

1. **API封装流程**
   - 了解API文档
   - 实现基础调用
   - 添加错误处理
   - 封装为工具

2. **关键技术**
   - HTTP请求
   - 认证管理
   - 错误处理
   - 重试机制
   - 缓存策略

3. **最佳实践**
   - 统一接口
   - 完善错误处理
   - API Key安全
   - 性能优化

4. **常见API类型**
   - 天气API
   - 翻译API
   - 地图API
   - 社交媒体API

---

## 🚀 下节预告

下一课：**第80课：自定义工具开发-数据库操作**

- 数据库连接
- CRUD操作
- SQL查询
- 安全防护

**让Agent操作数据库！** 💾

---

**💪 记住：API封装让Agent连接世界！**

**下一课见！** 🎉

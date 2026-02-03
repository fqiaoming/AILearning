![文档处理流程](./images/document.svg)
*图：文档处理流程*

# 第50课：OCR与图像文档处理

> **本课目标**：掌握OCR技术处理扫描件和图像文档，让RAG系统支持图像型PDF
> 
> **核心技能**：Tesseract OCR、PaddleOCR、图像预处理、PDF图像提取
> 
> **实战案例**：构建支持扫描件的智能文档处理系统
> 
> **学习时长**：70分钟

---

## 📖 口播文案（3分钟）

### 🎯 前言

"你有没有遇到过这种情况：公司有几千份扫描的历史文档，都是图片格式的PDF，想搜索里面的内容，结果什么都搜不到？

我见过一个真实案例：一家企业花了20万买了个文档管理系统，结果发现70%的历史文档都是扫描件，系统完全无法识别！相当于这些文档都是'死'的，无法检索，无法利用！

**这就是图像文档的痛点！**

在企业里，大量的文档都是扫描件：合同、报告、证书、表格……这些都是宝贵的知识资产，但如果无法被RAG系统识别，就等于白白浪费！

今天这一课，我要教你如何让RAG系统'看懂'图像文档！

- 如何用OCR技术提取图像中的文字？
- 如何处理低质量的扫描件？
- 如何识别中英文混合的文档？
- 如何处理图片型PDF？

学完这一课，你的RAG系统将支持90%以上的企业文档类型！

让我们开始！"

---

### 💡 核心知识点

大家好！今天我们学习RAG系统的重要能力：**OCR与图像文档处理**。

#### 什么是OCR？

OCR（Optical Character Recognition），光学字符识别，就是让计算机"读懂"图片中的文字。

```
传统PDF（文本型）：
- 文字是可选中、可复制的
- 可以直接提取文字
- PyPDFLoader就能处理

图像PDF（扫描件）：
- 文字是图片的一部分
- 无法直接选中和复制
- 需要OCR识别
```

#### 为什么需要OCR？

**企业场景1：历史文档数字化**
```
公司有10年的纸质文档
- 合同、报告、会议记录
- 全部扫描成PDF
- 需要OCR才能检索
```

**企业场景2：手写文档识别**
```
手写的会议记录
手写的审批单
需要OCR识别手写字
```

**企业场景3：多语言文档**
```
中英文混合的技术文档
需要OCR支持多语言
```

#### OCR技术选型

**1. Tesseract OCR**
- 优点：开源免费，支持100+语言
- 缺点：中文识别效果一般
- 适合：英文文档、简单场景

**2. PaddleOCR**
- 优点：中文识别准确率高，轻量级
- 缺点：需要安装依赖
- 适合：中文文档、生产环境（推荐）

**3. 商业OCR**
- 百度OCR、腾讯OCR、阿里OCR
- 优点：识别准确率最高
- 缺点：收费，依赖网络
- 适合：高精度要求

#### 今天的学习路线

1. **OCR基础**：Tesseract和PaddleOCR使用
2. **图像预处理**：提升OCR识别率
3. **PDF图像处理**：处理扫描型PDF
4. **质量优化**：识别率提升技巧
5. **实战项目**：扫描件文档处理系统

---

### 🔥 痛点与解决方案

**痛点1：扫描件无法检索**
- ❌ 问题：图片型PDF，搜索不到内容
- ✅ 解决：OCR提取文字，建立索引

**痛点2：OCR识别率低**
- ❌ 问题：识别出来的文字错误百出
- ✅ 解决：图像预处理（去噪、二值化、倾斜校正）

**痛点3：中文识别效果差**
- ❌ 问题：Tesseract中文识别率只有60%
- ✅ 解决：使用PaddleOCR，识别率95%+

**痛点4：表格和复杂布局识别困难**
- ❌ 问题：表格内容乱序
- ✅ 解决：使用布局分析 + OCR

---

## 📚 知识讲解

### 一、Tesseract OCR基础

#
![OCR图像处理](./images/ocr.svg)
*图：OCR图像处理*

### 1.1 安装Tesseract

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# 安装中文语言包
# macOS
brew install tesseract-lang

# Ubuntu
sudo apt-get install tesseract-ocr-chi-sim  # 简体中文
sudo apt-get install tesseract-ocr-chi-tra  # 繁体中文

# 安装Python包
pip install pytesseract pillow pdf2image
```

#### 1.2 基础使用

```python
import pytesseract
from PIL import Image

# 1. 读取图像
image = Image.open("document.png")

# 2. OCR识别（英文）
text = pytesseract.image_to_string(image, lang='eng')
print(text)

# 3. OCR识别（中文）
text = pytesseract.image_to_string(image, lang='chi_sim')
print(text)

# 4. OCR识别（中英文混合）
text = pytesseract.image_to_string(image, lang='chi_sim+eng')
print(text)
```

#### 1.3 高级配置

```python
# 自定义配置
custom_config = r'--oem 3 --psm 6'
# OEM (OCR Engine Mode):
#   0 = Legacy engine
#   1 = Neural nets LSTM engine
#   2 = Legacy + LSTM engines
#   3 = Default (based on what is available)

# PSM (Page Segmentation Mode):
#   0 = Orientation and script detection (OSD) only
#   1 = Automatic page segmentation with OSD
#   6 = Assume a single uniform block of text (推荐)
#   11 = Sparse text. Find as much text as possible

text = pytesseract.image_to_string(
    image,
    lang='chi_sim+eng',
    config=custom_config
)
```

#### 1.4 获取详细信息

```python
# 获取边界框和置信度
data = pytesseract.image_to_data(image, lang='chi_sim', output_type=pytesseract.Output.DICT)

# data包含：
# - text: 识别的文字
# - conf: 置信度（0-100）
# - left, top, width, height: 边界框坐标

# 过滤低置信度的结果
for i, conf in enumerate(data['conf']):
    if int(conf) > 60:  # 置信度大于60
        text = data['text'][i]
        print(f"{text} (置信度: {conf})")
```

---

### 二、PaddleOCR实战（推荐）

#### 2.1 安装PaddleOCR

```bash
# 安装PaddleOCR
pip install paddleocr paddlepaddle

# 如果有GPU（可选）
pip install paddlepaddle-gpu
```

#### 2.2 基础使用

```python
from paddleocr import PaddleOCR

# 1. 初始化OCR
ocr = PaddleOCR(
    use_angle_cls=True,  # 使用方向分类器
    lang='ch',           # 中文
    use_gpu=False        # 不使用GPU
)

# 2. 识别图像
result = ocr.ocr('document.png', cls=True)

# 3. 解析结果
for line in result[0]:
    # line[0]: 边界框坐标
    # line[1]: (文字, 置信度)
    text = line[1][0]
    confidence = line[1][1]
    print(f"{text} (置信度: {confidence:.2f})")

# 4. 提取纯文本
full_text = '\n'.join([line[1][0] for line in result[0]])
print(full_text)
```

#### 2.3 批量处理

```python
from paddleocr import PaddleOCR
from pathlib import Path

class BatchOCR:
    """批量OCR处理器"""
    
    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            use_gpu=False,
            show_log=False  # 不显示日志
        )
    
    def process_image(self, image_path):
        """处理单个图像"""
        result = self.ocr.ocr(image_path, cls=True)
        
        if not result or not result[0]:
            return ""
        
        # 提取文字
        texts = [line[1][0] for line in result[0]]
        return '\n'.join(texts)
    
    def process_directory(self, directory):
        """批量处理目录"""
        results = {}
        
        for img_path in Path(directory).glob("*.png"):
            print(f"处理: {img_path.name}")
            text = self.process_image(str(img_path))
            results[img_path.name] = text
        
        return results

# 使用
batch_ocr = BatchOCR()
results = batch_ocr.process_directory("scanned_docs/")

for filename, text in results.items():
    print(f"\n{'='*50}")
    print(f"文件: {filename}")
    print(f"内容: {text[:200]}...")
```

#### 2.4 支持多语言

```python
# 英文
ocr_en = PaddleOCR(lang='en')

# 日文
ocr_ja = PaddleOCR(lang='japan')

# 韩文
ocr_ko = PaddleOCR(lang='korean')

# 自动检测语言（推荐）
ocr_auto = PaddleOCR(lang='ch')  # 会自动识别中英文混合
```

---

### 三、图像预处理（提升识别率）

#### 3.1 为什么需要预处理？

```
原始扫描件的问题：
- 倾斜歪曲
- 噪点太多
- 对比度低
- 分辨率不够

预处理可以提升识别率20%-50%！
```

#### 3.2 图像预处理流程

```python
import cv2
import numpy as np
from PIL import Image

class ImagePreprocessor:
    """图像预处理器"""
    
    def preprocess(self, image_path, output_path=None):
        """完整的预处理流程"""
        # 1. 读取图像
        img = cv2.imread(image_path)
        
        # 2. 灰度化
        gray = self.to_grayscale(img)
        
        # 3. 去噪
        denoised = self.denoise(gray)
        
        # 4. 二值化
        binary = self.binarize(denoised)
        
        # 5. 倾斜校正
        corrected = self.deskew(binary)
        
        # 6. 保存
        if output_path:
            cv2.imwrite(output_path, corrected)
        
        return corrected
    
    def to_grayscale(self, img):
        """灰度化"""
        if len(img.shape) == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img
    
    def denoise(self, img):
        """去噪"""
        # 使用双边滤波去噪，保留边缘
        return cv2.bilateralFilter(img, 9, 75, 75)
    
    def binarize(self, img):
        """二值化（黑白化）"""
        # 自适应阈值二值化
        return cv2.adaptiveThreshold(
            img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
    
    def deskew(self, img):
        """倾斜校正"""
        # 检测倾斜角度
        coords = np.column_stack(np.where(img > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        # 角度修正
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # 旋转图像
        if abs(angle) > 0.5:  # 只有角度大于0.5度才校正
            (h, w) = img.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            img = cv2.warpAffine(
                img, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
        
        return img
    
    def resize_if_needed(self, img, min_width=1000):
        """调整分辨率（如果太小）"""
        height, width = img.shape[:2]
        
        if width < min_width:
            scale = min_width / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        return img

# 使用
preprocessor = ImagePreprocessor()
processed_img = preprocessor.preprocess("scan.png", "scan_processed.png")

# 对比OCR效果
from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='ch')

# 原始图像
result_original = ocr.ocr("scan.png")
text_original = '\n'.join([line[1][0] for line in result_original[0]])

# 预处理后
result_processed = ocr.ocr("scan_processed.png")
text_processed = '\n'.join([line[1][0] for line in result_processed[0]])

print("原始识别:")
print(text_original)
print("\n预处理后:")
print(text_processed)
```

#### 3.3 高级预处理技巧

```python
class AdvancedPreprocessor(ImagePreprocessor):
    """高级预处理"""
    
    def remove_borders(self, img):
        """去除边框"""
        # 查找轮廓
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 找到最大轮廓（通常是文档边界）
        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            img = img[y:y+h, x:x+w]
        
        return img
    
    def enhance_contrast(self, img):
        """增强对比度"""
        # CLAHE (对比度受限自适应直方图均衡化)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        return clahe.apply(img)
    
    def sharpen(self, img):
        """锐化"""
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        return cv2.filter2D(img, -1, kernel)
```

---

### 四、处理图像型PDF

#### 4.1 提取PDF中的图像

```python
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
from pathlib import Path

class PDFImageProcessor:
    """PDF图像处理器"""
    
    def __init__(self):
        self.ocr = PaddleOCR(lang='ch', use_gpu=False, show_log=False)
    
    def is_image_pdf(self, pdf_path):
        """判断PDF是否为图像型（扫描件）"""
        # 简单判断：尝试用PyPDF提取文字
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            
            # 提取前几页的文字
            text = ""
            for page in reader.pages[:3]:
                text += page.extract_text()
            
            # 如果文字很少（<100字），认为是图像PDF
            return len(text.strip()) < 100
        except:
            return True
    
    def pdf_to_images(self, pdf_path, output_folder='temp_images', dpi=300):
        """将PDF转为图像"""
        print(f"📄 转换PDF为图像: {pdf_path}")
        
        # 创建输出目录
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        # 转换（每页一张图）
        images = convert_from_path(
            pdf_path,
            dpi=dpi,  # 分辨率，越高越清晰，但越慢
            output_folder=output_folder,
            fmt='png'
        )
        
        print(f"   ✅ 转换完成: {len(images)} 页")
        
        return images
    
    def ocr_images(self, images):
        """OCR识别图像列表"""
        results = []
        
        for i, image in enumerate(images):
            print(f"   🔍 OCR识别第 {i+1} 页...")
            
            # 保存临时文件
            temp_path = f"temp_page_{i}.png"
            image.save(temp_path)
            
            # OCR识别
            result = self.ocr.ocr(temp_path, cls=True)
            
            if result and result[0]:
                text = '\n'.join([line[1][0] for line in result[0]])
                results.append({
                    "page": i + 1,
                    "text": text,
                    "image": image
                })
            
            # 删除临时文件
            Path(temp_path).unlink()
        
        return results
    
    def process_pdf(self, pdf_path, output_text_file=None):
        """处理图像型PDF"""
        print(f"🚀 开始处理图像PDF: {pdf_path}")
        print("=" * 50)
        
        # 1. 判断是否为图像PDF
        if not self.is_image_pdf(pdf_path):
            print("⚠️  这不是图像PDF，可以直接提取文字")
            return None
        
        # 2. 转换为图像
        images = self.pdf_to_images(pdf_path)
        
        # 3. OCR识别
        results = self.ocr_images(images)
        
        # 4. 合并文本
        full_text = ""
        for result in results:
            full_text += f"\n{'='*50}\n"
            full_text += f"第 {result['page']} 页\n"
            full_text += f"{'='*50}\n"
            full_text += result['text']
            full_text += "\n"
        
        # 5. 保存
        if output_text_file:
            with open(output_text_file, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"\n💾 文本已保存: {output_text_file}")
        
        print(f"\n✅ 处理完成!")
        print(f"   总页数: {len(results)}")
        print(f"   总字数: {len(full_text)}")
        
        return full_text

# 使用
processor = PDFImageProcessor()
text = processor.process_pdf(
    "scanned_document.pdf",
    output_text_file="extracted_text.txt"
)

print("\n提取的文本预览:")
print(text[:500])
```

#### 4.2 集成到LangChain

```python
from langchain.document_loaders.base import BaseLoader
from langchain.docstore.document import Document
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from pathlib import Path
import tempfile

class OCRPDFLoader(BaseLoader):
    """支持OCR的PDF加载器"""
    
    def __init__(self, file_path, use_ocr=True, dpi=300):
        self.file_path = file_path
        self.use_ocr = use_ocr
        self.dpi = dpi
        self.ocr = PaddleOCR(lang='ch', use_gpu=False, show_log=False) if use_ocr else None
    
    def load(self):
        """加载PDF"""
        # 1. 尝试常规加载
        try:
            from langchain.document_loaders import PyPDFLoader
            loader = PyPDFLoader(self.file_path)
            docs = loader.load()
            
            # 检查是否有足够的文字
            total_text = ''.join([doc.page_content for doc in docs])
            
            if len(total_text.strip()) > 100:
                # 文字足够，直接返回
                return docs
        except:
            pass
        
        # 2. 使用OCR
        if self.use_ocr:
            return self._load_with_ocr()
        
        return []
    
    def _load_with_ocr(self):
        """使用OCR加载"""
        documents = []
        
        # 转换PDF为图像
        with tempfile.TemporaryDirectory() as temp_dir:
            images = convert_from_path(
                self.file_path,
                dpi=self.dpi,
                output_folder=temp_dir
            )
            
            # OCR每一页
            for page_num, image in enumerate(images):
                temp_image_path = f"{temp_dir}/page_{page_num}.png"
                image.save(temp_image_path)
                
                # OCR识别
                result = self.ocr.ocr(temp_image_path, cls=True)
                
                if result and result[0]:
                    text = '\n'.join([line[1][0] for line in result[0]])
                    
                    # 创建Document
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": self.file_path,
                            "page": page_num + 1,
                            "ocr": True,
                        }
                    )
                    documents.append(doc)
        
        return documents

# 使用
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 加载OCR PDF
loader = OCRPDFLoader("scanned_report.pdf")
documents = loader.load()

print(f"加载了 {len(documents)} 页")

# 2. 分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

print(f"分块后: {len(chunks)} 个块")

# 3. 向量化存储
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. 检索测试
results = vectorstore.similarity_search("关键信息", k=3)
for doc in results:
    print(f"\n页码: {doc.metadata['page']}")
    print(f"内容: {doc.page_content[:200]}...")
```

---

## 💻 完整实战案例

### 案例：智能扫描件处理系统

**需求**：
- 自动识别PDF类型（文本型/图像型）
- 图像型自动OCR处理
- 图像预处理提升识别率
- 统一的文档加载接口
- 处理进度展示

**完整代码**：

```python
from pathlib import Path
from typing import List
import tempfile
from tqdm import tqdm

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.base import BaseLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

from paddleocr import PaddleOCR
from pdf2image import convert_from_path
import cv2
import numpy as np

class SmartDocumentProcessor:
    """智能文档处理系统"""
    
    def __init__(self, use_preprocessing=True):
        self.ocr = PaddleOCR(lang='ch', use_gpu=False, show_log=False)
        self.use_preprocessing = use_preprocessing
        self.stats = {
            "total_files": 0,
            "text_pdfs": 0,
            "image_pdfs": 0,
            "ocr_pages": 0,
            "total_chunks": 0,
        }
    
    def is_text_pdf(self, pdf_path):
        """判断是否为文本型PDF"""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            
            # 提取前3页文字
            text = ""
            for page in reader.pages[:min(3, len(reader.pages))]:
                text += page.extract_text()
            
            # 如果文字较多，认为是文本PDF
            return len(text.strip()) > 100
        except:
            return False
    
    def preprocess_image(self, image_array):
        """图像预处理"""
        if not self.use_preprocessing:
            return image_array
        
        # 灰度化
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array
        
        # 去噪
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 二值化
        binary = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 转回RGB（PaddleOCR需要）
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    
    def load_text_pdf(self, pdf_path):
        """加载文本型PDF"""
        loader = PyPDFLoader(pdf_path)
        return loader.load()
    
    def load_image_pdf(self, pdf_path, dpi=300):
        """加载图像型PDF（OCR）"""
        documents = []
        
        print(f"   📸 转换PDF为图像...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # 转换为图像
            images = convert_from_path(pdf_path, dpi=dpi, output_folder=temp_dir)
            
            self.stats["ocr_pages"] += len(images)
            
            print(f"   🔍 OCR识别 {len(images)} 页...")
            
            # OCR每一页
            for page_num in tqdm(range(len(images)), desc="   OCR进度"):
                image = images[page_num]
                
                # 保存临时文件
                temp_path = f"{temp_dir}/page_{page_num}.png"
                image.save(temp_path)
                
                # 图像预处理
                if self.use_preprocessing:
                    img_array = cv2.imread(temp_path)
                    processed = self.preprocess_image(img_array)
                    cv2.imwrite(temp_path, processed)
                
                # OCR识别
                result = self.ocr.ocr(temp_path, cls=True)
                
                if result and result[0]:
                    # 提取文字
                    text = '\n'.join([line[1][0] for line in result[0]])
                    
                    # 创建Document
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": Path(pdf_path).name,
                            "file_path": str(pdf_path),
                            "page": page_num + 1,
                            "total_pages": len(images),
                            "ocr": True,
                            "preprocessed": self.use_preprocessing,
                        }
                    )
                    documents.append(doc)
        
        return documents
    
    def process_pdf(self, pdf_path):
        """智能处理PDF"""
        print(f"\n{'='*60}")
        print(f"📄 处理文件: {Path(pdf_path).name}")
        print(f"{'='*60}")
        
        self.stats["total_files"] += 1
        
        # 1. 判断PDF类型
        if self.is_text_pdf(pdf_path):
            print("   ✅ 检测到文本型PDF，直接提取")
            self.stats["text_pdfs"] += 1
            documents = self.load_text_pdf(pdf_path)
        else:
            print("   📷 检测到图像型PDF，使用OCR")
            self.stats["image_pdfs"] += 1
            documents = self.load_image_pdf(pdf_path)
        
        print(f"   ✅ 加载完成: {len(documents)} 页")
        
        return documents
    
    def process_directory(self, directory, recursive=True):
        """批量处理目录"""
        print("🚀 开始批量处理文档")
        print(f"📂 目录: {directory}")
        print(f"🔄 递归: {'是' if recursive else '否'}")
        print("=" * 60)
        
        all_documents = []
        
        # 查找所有PDF
        pattern = "**/*.pdf" if recursive else "*.pdf"
        pdf_files = list(Path(directory).glob(pattern))
        
        print(f"📋 找到 {len(pdf_files)} 个PDF文件\n")
        
        # 处理每个PDF
        for pdf_path in pdf_files:
            try:
                documents = self.process_pdf(str(pdf_path))
                all_documents.extend(documents)
            except Exception as e:
                print(f"   ❌ 处理失败: {e}")
        
        return all_documents
    
    def build_knowledge_base(self, documents, chunk_size=1000, chunk_overlap=200):
        """构建知识库"""
        print(f"\n{'='*60}")
        print("🔨 构建知识库")
        print(f"{'='*60}")
        
        # 1. 分块
        print("   ✂️  文档分块...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_documents(documents)
        
        self.stats["total_chunks"] = len(chunks)
        
        print(f"   ✅ 分块完成: {len(chunks)} 个块")
        
        # 2. 向量化
        print("   🔢 向量化...")
        embeddings = HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
        
        print("   💾 构建向量库...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db_ocr"
        )
        
        print("   ✅ 知识库构建完成")
        
        return vectorstore
    
    def print_stats(self):
        """打印统计信息"""
        print(f"\n{'='*60}")
        print("📊 处理统计")
        print(f"{'='*60}")
        print(f"总文件数: {self.stats['total_files']}")
        print(f"  - 文本型PDF: {self.stats['text_pdfs']}")
        print(f"  - 图像型PDF: {self.stats['image_pdfs']}")
        print(f"OCR处理页数: {self.stats['ocr_pages']}")
        print(f"总文档块数: {self.stats['total_chunks']}")
        print(f"{'='*60}")

# ============= 使用示例 =============

if __name__ == "__main__":
    # 1. 创建处理器
    processor = SmartDocumentProcessor(use_preprocessing=True)
    
    # 2. 处理单个文件
    # documents = processor.process_pdf("scanned_report.pdf")
    
    # 3. 批量处理目录
    documents = processor.process_directory("data/pdfs", recursive=True)
    
    # 4. 构建知识库
    vectorstore = processor.build_knowledge_base(documents)
    
    # 5. 打印统计
    processor.print_stats()
    
    # 6. 检索测试
    print(f"\n{'='*60}")
    print("🔍 检索测试")
    print(f"{'='*60}")
    
    query = "销售数据"
    results = vectorstore.similarity_search(query, k=3)
    
    for i, doc in enumerate(results):
        print(f"\n--- 结果 {i+1} ---")
        print(f"来源: {doc.metadata.get('source')}")
        print(f"页码: {doc.metadata.get('page')}")
        print(f"OCR: {'是' if doc.metadata.get('ocr') else '否'}")
        print(f"内容: {doc.page_content[:150]}...")
```

---

## 📝 课后练习

### 练习1：表格OCR

实现表格识别和提取功能

### 练习2：手写文字识别

使用PaddleOCR的手写文字识别模型

### 练习3：多语言混合识别

处理中英日韩混合的文档

---

## 🎓 知识总结

### 核心要点

1. **OCR技术选型**
   - Tesseract：开源免费，英文好
   - PaddleOCR：中文识别准确率高（推荐）
   - 商业OCR：最高精度

2. **图像预处理**
   - 灰度化、去噪、二值化
   - 倾斜校正、分辨率调整
   - 可提升识别率20%-50%

3. **PDF处理**
   - 判断文本型/图像型
   - pdf2image转换
   - 逐页OCR识别

4. **集成RAG**
   - 自定义Loader
   - 统一文档接口
   - 元数据标记OCR来源

### 最佳实践

✅ 优先判断PDF类型
✅ 图像预处理提升识别率
✅ 使用PaddleOCR处理中文
✅ 合理设置DPI（300推荐）
✅ 批量处理显示进度

---

## 🚀 下节预告

下一课：**第51课：批量处理：高效处理海量文档**

- 如何并发处理文档？
- 如何处理大文件？
- 如何实现断点续传？
- 实战：每秒处理100+文档

**让你的文档处理速度提升10倍！** ⚡

---

**💪 记住：OCR让RAG系统支持90%以上的企业文档，掌握OCR是必备技能！**

**下一课见！** 🎉
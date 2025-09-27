# PDF章节切分工具

一个功能强大的PDF章节切分工具，支持多种切分方式，可以将PDF文件按章节自动切分成多个独立的PDF文件。

## 功能特点

- 🔖 **基于书签切分**: 使用PDF内置书签自动识别章节
- 🔤 **基于字体切分**: 根据字体大小和样式检测章节标题
- 🔍 **基于关键词切分**: 通过自定义关键词匹配章节
- 📄 **手动页码切分**: 手动指定页码范围进行切分
- 🖥️ **图形界面**: 提供简单易用的GUI界面
- 💻 **命令行支持**: 支持命令行批量处理
- 📊 **PDF信息查看**: 显示PDF基本信息和书签结构

## 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖包说明

- `PyPDF2`: PDF文件处理
- `pymupdf`: 高性能PDF处理库
- `fitz`: PyMuPDF的Python绑定
- `tkinter-dnd2`: GUI拖拽支持（可选）

## 使用方法

### 1. 图形界面使用

启动GUI界面：

```bash
python pdf_splitter_gui.py
```

操作步骤：
1. 点击"浏览"选择要切分的PDF文件
2. 选择输出目录（可选，默认为原文件名_chapters）
3. 选择切分方法：
   - **基于书签**: 适用于有完整书签结构的PDF
   - **基于字体大小**: 通过字体大小检测标题
   - **基于关键词**: 通过关键词匹配章节标题
   - **手动指定页码**: 精确控制切分范围
4. 点击"查看PDF信息"了解文件结构（可选）
5. 点击"开始切分"执行切分操作

### 2. 命令行使用

#### 基本用法

```bash
# 使用书签切分（推荐）
python pdf_splitter.py example.pdf

# 指定输出目录
python pdf_splitter.py example.pdf -o output_folder

# 查看PDF信息
python pdf_splitter.py example.pdf --info
```

#### 不同切分方法

```bash
# 基于字体大小切分
python pdf_splitter.py example.pdf -m font --font-size 16

# 基于关键词切分
python pdf_splitter.py example.pdf -m keywords --keywords 第 章 Chapter

# 手动指定页码范围
python pdf_splitter.py example.pdf -m pages --pages 1-10,11-25,26-40
```

#### 命令行参数说明

- `-m, --method`: 切分方法 (bookmarks/font/keywords/pages)
- `-o, --output`: 输出目录
- `--font-size`: 最小字体大小阈值（用于font方法）
- `--keywords`: 章节关键词列表（用于keywords方法）
- `--pages`: 页码范围（用于pages方法）
- `--info`: 显示PDF信息

## 使用示例

### 示例1：学术论文切分

```bash
# 查看论文结构
python pdf_splitter.py research_paper.pdf --info

# 基于书签切分
python pdf_splitter.py research_paper.pdf -m bookmarks -o paper_chapters
```

### 示例2：教材切分

```bash
# 基于字体大小切分教材
python pdf_splitter.py textbook.pdf -m font --font-size 18 -o textbook_chapters
```

### 示例3：技术文档切分

```bash
# 基于关键词切分
python pdf_splitter.py manual.pdf -m keywords --keywords "第" "章节" "Section" -o manual_sections
```

### 示例4：精确页码切分

```bash
# 手动指定页码范围
python pdf_splitter.py document.pdf -m pages --pages 1-15,16-30,31-45 -o doc_parts
```

## 代码示例

### Python API使用

```python
from pdf_splitter import PDFSplitter

# 使用上下文管理器
with PDFSplitter('example.pdf') as splitter:
    # 查看PDF信息
    info = splitter.get_pdf_info()
    print(f"总页数: {info['total_pages']}")
    print(f"书签数: {info['bookmarks_count']}")
    
    # 基于书签切分
    files = splitter.split_by_bookmarks()
    print(f"生成了 {len(files)} 个文件")
    
    # 基于字体切分
    files = splitter.split_by_auto_detection('font', min_font_size=14)
    
    # 手动页码切分
    page_ranges = [(0, 9), (10, 19), (20, 29)]  # 页码从0开始
    chapter_names = ['前言', '第一章', '第二章']
    files = splitter.split_by_pages(page_ranges, chapter_names)
```

## 输出文件命名规则

生成的文件按以下规则命名：
- 格式：`序号_章节标题.pdf`
- 序号：两位数字，从01开始
- 标题：自动清理非法字符，限制长度
- 示例：`01_第一章_绪论.pdf`

## 注意事项

1. **PDF质量**: 扫描版PDF可能识别效果较差，建议使用文本版PDF
2. **书签结构**: 使用书签切分时，需要PDF包含完整的书签结构
3. **字体检测**: 字体方法适用于标题字体明显大于正文的PDF
4. **关键词匹配**: 关键词方法需要章节标题包含明确的关键词
5. **文件权限**: 确保对输出目录有写入权限
6. **内存使用**: 处理大型PDF时可能消耗较多内存

## 故障排除

### 常见问题

**Q: 提示"未找到书签"**
A: PDF文件没有书签结构，请尝试其他切分方法

**Q: 字体方法检测不到章节**
A: 尝试调整字体大小阈值，或检查PDF是否为扫描版

**Q: 关键词方法匹配过多内容**
A: 使用更具体的关键词，或结合字体大小进行过滤

**Q: 生成的文件名乱码**
A: 可能是编码问题，程序会自动清理并使用默认名称

### 错误处理

程序包含完善的错误处理机制：
- 文件不存在检查
- PDF格式验证
- 输出目录权限检查
- 页码范围验证
- 异常信息详细记录

## 开发说明

### 项目结构

```
pdfsplitter/
├── pdf_splitter.py      # 核心切分功能
├── pdf_splitter_gui.py  # 图形界面
├── requirements.txt     # 依赖包列表
└── README.md           # 使用说明
```

### 扩展开发

可以基于`PDFSplitter`类进行功能扩展：
- 添加新的章节检测算法
- 支持更多输出格式
- 集成OCR功能
- 批量处理支持

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持4种切分方法
- 提供GUI和命令行界面
- 完整的错误处理和日志记录

# PDF章节切分工具 - 安装指南

## 快速安装

### 方法1：自动安装（推荐）
```bash
python install.py
```

### 方法2：使用pip
```bash
pip install PyMuPDF PyPDF2
```

### 方法3：使用conda
```bash
conda install -c conda-forge pymupdf pypdf2
```

## 常见安装问题及解决方案

### 问题1：pip安装失败
**错误信息**: `ERROR: Could not find a version that satisfies the requirement...`

**解决方案**:
1. 升级pip:
   ```bash
   python -m pip install --upgrade pip
   ```

2. 使用国内镜像源:
   ```bash
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyMuPDF PyPDF2
   ```

3. 或者使用阿里云镜像:
   ```bash
   pip install -i https://mirrors.aliyun.com/pypi/simple/ PyMuPDF PyPDF2
   ```

### 问题2：网络连接问题
**错误信息**: `TimeoutError` 或 `Connection error`

**解决方案**:
1. 检查网络连接
2. 使用代理（如果需要）:
   ```bash
   pip install --proxy http://proxy.company.com:port PyMuPDF PyPDF2
   ```

3. 离线安装:
   - 下载wheel文件到本地
   - 使用 `pip install *.whl` 安装

### 问题3：权限问题
**错误信息**: `Permission denied` 或 `Access is denied`

**解决方案**:
1. Windows用户：以管理员身份运行命令提示符
2. Linux/Mac用户：使用sudo（不推荐）或用户安装:
   ```bash
   pip install --user PyMuPDF PyPDF2
   ```

### 问题4：Python版本不兼容
**错误信息**: `Requires Python >=3.7`

**解决方案**:
1. 检查Python版本:
   ```bash
   python --version
   ```

2. 升级Python到3.7或更高版本
3. 或使用较低版本的包:
   ```bash
   pip install PyMuPDF==1.20.0 PyPDF2==2.12.1
   ```

### 问题5：tkinter缺失（Linux系统）
**错误信息**: `No module named '_tkinter'`

**解决方案**:
- Ubuntu/Debian:
  ```bash
  sudo apt-get install python3-tk
  ```

- CentOS/RHEL:
  ```bash
  sudo yum install tkinter
  # 或者新版本使用
  sudo dnf install python3-tkinter
  ```

- Arch Linux:
  ```bash
  sudo pacman -S tk
  ```

### 问题6：编译错误（源码安装时）
**错误信息**: `Microsoft Visual C++ 14.0 is required`

**解决方案**:
1. Windows用户安装Visual Studio Build Tools
2. 或者使用预编译的wheel包:
   ```bash
   pip install --only-binary=all PyMuPDF
   ```

## 验证安装

运行以下命令验证安装是否成功:

```python
python -c "import fitz; print('PyMuPDF安装成功')"
python -c "import PyPDF2; print('PyPDF2安装成功')"
python -c "import tkinter; print('tkinter可用')"
```

或者运行测试脚本:
```bash
python install.py
```

## 替代安装方法

### 使用Anaconda/Miniconda
```bash
conda create -n pdfsplitter python=3.8
conda activate pdfsplitter
conda install -c conda-forge pymupdf pypdf2
```

### 使用pipenv
```bash
pipenv install PyMuPDF PyPDF2
pipenv shell
```

### 使用poetry
```bash
poetry add PyMuPDF PyPDF2
poetry shell
```

## 最小依赖版本

如果遇到兼容性问题，可以尝试安装最小依赖版本:

```bash
pip install PyMuPDF>=1.18.0 PyPDF2>=2.0.0
```

## 开发环境设置

如果你想修改代码，建议创建虚拟环境:

```bash
# 创建虚拟环境
python -m venv pdf_splitter_env

# 激活虚拟环境
# Windows:
pdf_splitter_env\Scripts\activate
# Linux/Mac:
source pdf_splitter_env/bin/activate

# 安装依赖
pip install PyMuPDF PyPDF2
```

## 故障排除步骤

1. **检查Python版本**: `python --version`
2. **检查pip版本**: `pip --version`
3. **升级pip**: `python -m pip install --upgrade pip`
4. **清除缓存**: `pip cache purge`
5. **尝试不同镜像源**
6. **检查网络连接**
7. **运行自动安装脚本**: `python install.py`

## 获取帮助

如果以上方法都无法解决问题，请提供以下信息:

1. 操作系统版本
2. Python版本
3. 完整的错误信息
4. 已尝试的解决方案

## 无需安装的替代方案

如果实在无法安装依赖，可以考虑:

1. 使用在线PDF处理工具
2. 使用Docker容器运行
3. 在其他已安装依赖的环境中运行

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF章节切分工具依赖安装脚本
自动检测和安装所需的依赖包
"""

import subprocess
import sys
import os


def run_command(command):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("警告: 建议使用Python 3.7或更高版本")
        return False
    return True


def install_package(package_name, alternative_name=None):
    """安装单个包"""
    print(f"正在安装 {package_name}...")
    
    # 首先尝试安装主包
    success, stdout, stderr = run_command(f"pip install {package_name}")
    
    if success:
        print(f"✓ {package_name} 安装成功")
        return True
    else:
        print(f"✗ {package_name} 安装失败: {stderr}")
        
        # 如果有备选包名，尝试安装
        if alternative_name:
            print(f"尝试安装备选包 {alternative_name}...")
            success, stdout, stderr = run_command(f"pip install {alternative_name}")
            
            if success:
                print(f"✓ {alternative_name} 安装成功")
                return True
            else:
                print(f"✗ {alternative_name} 也安装失败: {stderr}")
        
        return False


def install_dependencies():
    """安装所有依赖"""
    print("开始安装PDF切分工具依赖包...")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        print("建议升级Python版本")
    
    # 升级pip
    print("\n正在升级pip...")
    run_command("python -m pip install --upgrade pip")
    
    # 要安装的包列表
    packages = [
        ("PyMuPDF", "pymupdf"),  # PDF处理的主要库
        ("PyPDF2", None),        # PDF处理备选库
    ]
    
    success_count = 0
    total_count = len(packages)
    
    print("\n开始安装依赖包:")
    print("-" * 30)
    
    for package, alternative in packages:
        if install_package(package, alternative):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"安装完成: {success_count}/{total_count} 个包安装成功")
    
    # 检查tkinter（通常是Python内置的）
    try:
        import tkinter
        print("✓ tkinter 可用（图形界面支持）")
    except ImportError:
        print("✗ tkinter 不可用，图形界面可能无法使用")
        print("  在Ubuntu/Debian上运行: sudo apt-get install python3-tk")
        print("  在CentOS/RHEL上运行: sudo yum install tkinter")
    
    return success_count == total_count


def test_imports():
    """测试导入"""
    print("\n测试依赖包导入:")
    print("-" * 20)
    
    packages_to_test = [
        ("fitz", "PyMuPDF"),
        ("PyPDF2", "PyPDF2"),
        ("tkinter", "tkinter"),
    ]
    
    all_good = True
    
    for module_name, display_name in packages_to_test:
        try:
            if module_name == "fitz":
                import fitz
            elif module_name == "PyPDF2":
                import PyPDF2
            elif module_name == "tkinter":
                import tkinter
            
            print(f"✓ {display_name} 导入成功")
        except ImportError as e:
            print(f"✗ {display_name} 导入失败: {e}")
            all_good = False
    
    return all_good


def main():
    """主函数"""
    print("PDF章节切分工具 - 依赖安装程序")
    print("=" * 50)
    
    # 安装依赖
    install_success = install_dependencies()
    
    if install_success:
        print("\n🎉 所有依赖安装成功！")
    else:
        print("\n⚠️ 部分依赖安装失败，但可能仍然可以使用")
    
    # 测试导入
    if test_imports():
        print("\n✅ 所有依赖都可以正常导入")
        print("\n现在你可以运行以下命令:")
        print("  python run.py              # 启动选择菜单")
        print("  python pdf_splitter_gui.py # 直接启动图形界面")
        print("  python pdf_splitter.py -h  # 查看命令行帮助")
    else:
        print("\n❌ 部分依赖导入失败")
        print("\n可能的解决方案:")
        print("1. 重新运行此安装脚本")
        print("2. 手动安装: pip install PyMuPDF PyPDF2")
        print("3. 使用conda: conda install -c conda-forge pymupdf pypdf2")
        print("4. 检查网络连接和防火墙设置")
    
    input("\n按回车键退出...")


if __name__ == '__main__':
    main()

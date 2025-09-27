#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF章节切分工具启动脚本
提供简单的选择界面来启动不同的功能
"""

import sys
import os
import subprocess


def check_dependencies():
    """检查依赖包是否安装"""
    missing_packages = []
    
    try:
        import fitz
    except ImportError:
        missing_packages.append("PyMuPDF (fitz)")
    
    try:
        import tkinter
    except ImportError:
        missing_packages.append("tkinter")
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        print("\n推荐的安装方法:")
        print("1. 运行自动安装脚本: python install.py")
        print("2. 手动安装: pip install PyMuPDF PyPDF2")
        print("3. 使用conda: conda install -c conda-forge pymupdf pypdf2")
        
        choice = input("\n是否现在运行自动安装脚本? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            try:
                import subprocess
                subprocess.run([sys.executable, 'install.py'])
                return check_dependencies()  # 重新检查
            except Exception as e:
                print(f"自动安装失败: {e}")
                return False
        else:
            return False
    
    return True


def main():
    """主函数"""
    print("PDF章节切分工具")
    print("=" * 30)
    
    if not check_dependencies():
        return
    
    print("请选择启动方式:")
    print("1. 图形界面 (推荐)")
    print("2. 命令行帮助")
    print("3. 查看使用示例")
    print("4. 退出")
    
    while True:
        try:
            choice = input("\n请输入选择 (1-4): ").strip()
            
            if choice == '1':
                print("启动图形界面...")
                try:
                    subprocess.run([sys.executable, 'pdf_splitter_gui.py'])
                except Exception as e:
                    print(f"启动图形界面失败: {e}")
                break
                
            elif choice == '2':
                print("\n命令行使用帮助:")
                subprocess.run([sys.executable, 'pdf_splitter.py', '--help'])
                break
                
            elif choice == '3':
                print("运行使用示例...")
                subprocess.run([sys.executable, 'example.py'])
                break
                
            elif choice == '4':
                print("退出程序")
                break
                
            else:
                print("无效选择，请输入 1-4")
                
        except KeyboardInterrupt:
            print("\n\n程序被中断")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == '__main__':
    main()

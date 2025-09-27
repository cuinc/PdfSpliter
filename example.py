#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF章节切分工具使用示例
演示如何使用PDFSplitter类进行各种切分操作
"""

from pdf_splitter import PDFSplitter
import os


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 替换为你的PDF文件路径
    pdf_file = "example.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"请将示例PDF文件命名为 {pdf_file} 并放在当前目录下")
        return
    
    try:
        with PDFSplitter(pdf_file) as splitter:
            # 查看PDF基本信息
            info = splitter.get_pdf_info()
            print(f"文件名: {info['filename']}")
            print(f"总页数: {info['total_pages']}")
            print(f"书签数量: {info['bookmarks_count']}")
            
            if info['bookmarks']:
                print("前几个书签:")
                for bookmark in info['bookmarks'][:5]:
                    print(f"  - {bookmark['title']} (第{bookmark['page']+1}页)")
            
    except Exception as e:
        print(f"错误: {e}")


def example_bookmark_split():
    """基于书签切分示例"""
    print("\n=== 基于书签切分示例 ===")
    
    pdf_file = "example.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"请提供PDF文件: {pdf_file}")
        return
    
    try:
        with PDFSplitter(pdf_file) as splitter:
            # 基于书签切分
            files = splitter.split_by_bookmarks()
            
            if files:
                print(f"成功切分为 {len(files)} 个文件:")
                for file_path in files:
                    print(f"  - {os.path.basename(file_path)}")
            else:
                print("未找到书签或切分失败")
                
    except Exception as e:
        print(f"错误: {e}")


def example_font_split():
    """基于字体切分示例"""
    print("\n=== 基于字体切分示例 ===")
    
    pdf_file = "example.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"请提供PDF文件: {pdf_file}")
        return
    
    try:
        with PDFSplitter(pdf_file) as splitter:
            # 先检测可能的章节
            chapters = splitter.detect_chapters_by_font(min_font_size=14)
            print(f"检测到 {len(chapters)} 个可能的章节:")
            for chapter in chapters[:10]:  # 只显示前10个
                print(f"  - 第{chapter['page']+1}页: {chapter['title']} (字体大小: {chapter['font_size']})")
            
            if chapters:
                # 执行切分
                files = splitter.split_by_auto_detection('font', min_font_size=14)
                print(f"\n切分结果: {len(files)} 个文件")
                
    except Exception as e:
        print(f"错误: {e}")


def example_keyword_split():
    """基于关键词切分示例"""
    print("\n=== 基于关键词切分示例 ===")
    
    pdf_file = "example.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"请提供PDF文件: {pdf_file}")
        return
    
    try:
        with PDFSplitter(pdf_file) as splitter:
            # 使用中文关键词
            keywords = ['第', '章', '节']
            chapters = splitter.detect_chapters_by_keywords(keywords)
            print(f"使用关键词 {keywords} 检测到 {len(chapters)} 个章节:")
            for chapter in chapters[:10]:  # 只显示前10个
                print(f"  - 第{chapter['page']+1}页: {chapter['title']}")
            
            if chapters:
                files = splitter.split_by_auto_detection('keywords', keywords=keywords)
                print(f"\n切分结果: {len(files)} 个文件")
                
    except Exception as e:
        print(f"错误: {e}")


def example_manual_split():
    """手动页码切分示例"""
    print("\n=== 手动页码切分示例 ===")
    
    pdf_file = "example.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"请提供PDF文件: {pdf_file}")
        return
    
    try:
        with PDFSplitter(pdf_file) as splitter:
            total_pages = splitter.total_pages
            print(f"PDF总页数: {total_pages}")
            
            # 手动定义页码范围（页码从0开始）
            if total_pages >= 20:
                page_ranges = [
                    (0, 9),    # 第1-10页
                    (10, 19),  # 第11-20页
                ]
                chapter_names = ['前言部分', '主要内容']
            else:
                # 如果页数较少，按一半切分
                mid = total_pages // 2
                page_ranges = [
                    (0, mid-1),
                    (mid, total_pages-1)
                ]
                chapter_names = ['前半部分', '后半部分']
            
            files = splitter.split_by_pages(page_ranges, chapter_names)
            print(f"手动切分为 {len(files)} 个文件:")
            for i, file_path in enumerate(files):
                start_page, end_page = page_ranges[i]
                print(f"  - {os.path.basename(file_path)} (第{start_page+1}-{end_page+1}页)")
                
    except Exception as e:
        print(f"错误: {e}")


def example_custom_output_dir():
    """自定义输出目录示例"""
    print("\n=== 自定义输出目录示例 ===")
    
    pdf_file = "example.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"请提供PDF文件: {pdf_file}")
        return
    
    try:
        # 创建自定义输出目录
        custom_output = "my_pdf_chapters"
        
        with PDFSplitter(pdf_file) as splitter:
            files = splitter.split_by_bookmarks(output_dir=custom_output)
            
            if files:
                print(f"文件保存到: {custom_output}")
                print(f"生成文件数: {len(files)}")
            else:
                print("切分失败或未找到章节")
                
    except Exception as e:
        print(f"错误: {e}")


def main():
    """主函数"""
    print("PDF章节切分工具使用示例")
    print("=" * 50)
    
    # 运行各种示例
    example_basic_usage()
    example_bookmark_split()
    example_font_split()
    example_keyword_split()
    example_manual_split()
    example_custom_output_dir()
    
    print("\n" + "=" * 50)
    print("示例结束")
    print("\n使用说明:")
    print("1. 将要切分的PDF文件重命名为 'example.pdf' 并放在当前目录")
    print("2. 运行此脚本查看各种切分方法的效果")
    print("3. 根据PDF特点选择最适合的切分方法")
    print("\n启动GUI界面: python pdf_splitter_gui.py")
    print("命令行使用: python pdf_splitter.py your_file.pdf")


if __name__ == '__main__':
    main()

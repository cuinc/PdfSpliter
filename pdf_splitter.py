#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF章节切分工具
支持多种章节检测方式：
1. 基于标题文本的检测
2. 基于页码范围的手动切分
3. 基于书签的自动切分
4. 基于字体大小和样式的智能检测
"""

import os
import re
import fitz  # PyMuPDF
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class PDFSplitter:
    """PDF章节切分器"""
    
    def __init__(self, pdf_path: str):
        """
        初始化PDF切分器
        
        Args:
            pdf_path: PDF文件路径
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        self.doc = fitz.open(str(self.pdf_path))
        self.total_pages = len(self.doc)
        self.output_dir = self.pdf_path.parent / f"{self.pdf_path.stem}_chapters"
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'doc') and self.doc:
            self.doc.close()
    
    def get_bookmarks(self) -> List[Dict]:
        """
        获取PDF书签信息
        
        Returns:
            书签列表，每个书签包含标题和页码信息
        """
        bookmarks = []
        toc = self.doc.get_toc()
        
        for item in toc:
            level, title, page = item
            if level == 1:  # 只取一级标题作为章节
                bookmarks.append({
                    'title': title.strip(),
                    'page': page - 1,  # PyMuPDF页码从0开始
                    'level': level
                })
        
        return bookmarks
    
    def detect_chapters_by_font(self, min_font_size: float = 14) -> List[Dict]:
        """
        基于字体大小检测章节标题
        
        Args:
            min_font_size: 最小字体大小阈值
            
        Returns:
            检测到的章节信息列表
        """
        chapters = []
        chapter_patterns = [
            r'第[一二三四五六七八九十\d]+章',
            r'Chapter\s+\d+',
            r'CHAPTER\s+\d+',
            r'第\d+章',
            r'^\d+\.',
            r'^\d+\s+',
        ]
        
        for page_num in range(self.total_pages):
            page = self.doc[page_num]
            blocks = page.get_text("dict")
            
            for block in blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            font_size = span["size"]
                            
                            # 检查字体大小和文本模式
                            if font_size >= min_font_size and text:
                                for pattern in chapter_patterns:
                                    if re.search(pattern, text, re.IGNORECASE):
                                        chapters.append({
                                            'title': text,
                                            'page': page_num,
                                            'font_size': font_size
                                        })
                                        break
        
        return chapters
    
    def detect_chapters_by_keywords(self, keywords: List[str]) -> List[Dict]:
        """
        基于关键词检测章节
        
        Args:
            keywords: 章节关键词列表
            
        Returns:
            检测到的章节信息列表
        """
        chapters = []
        
        for page_num in range(self.total_pages):
            page = self.doc[page_num]
            text = page.get_text()
            lines = text.split('\n')
            
            for line_num, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        chapters.append({
                            'title': line,
                            'page': page_num,
                            'line': line_num
                        })
                        break
        
        return chapters
    
    def split_by_bookmarks(self, output_dir: Optional[str] = None) -> List[str]:
        """
        根据书签切分PDF
        
        Args:
            output_dir: 输出目录，默认为原文件名_chapters
            
        Returns:
            生成的文件路径列表
        """
        bookmarks = self.get_bookmarks()
        if not bookmarks:
            print("未找到书签，无法按书签切分")
            return []
        
        return self._split_pdf(bookmarks, output_dir)
    
    def split_by_pages(self, page_ranges: List[Tuple[int, int]], 
                      chapter_names: Optional[List[str]] = None,
                      output_dir: Optional[str] = None) -> List[str]:
        """
        根据页码范围切分PDF
        
        Args:
            page_ranges: 页码范围列表，格式为[(起始页, 结束页), ...]
            chapter_names: 章节名称列表，可选
            output_dir: 输出目录
            
        Returns:
            生成的文件路径列表
        """
        chapters = []
        for i, (start_page, end_page) in enumerate(page_ranges):
            title = f"Chapter_{i+1}"
            if chapter_names and i < len(chapter_names):
                title = chapter_names[i]
            
            chapters.append({
                'title': title,
                'page': start_page,
                'end_page': end_page
            })
        
        return self._split_pdf(chapters, output_dir, use_end_page=True)
    
    def split_by_auto_detection(self, method: str = 'font', 
                               output_dir: Optional[str] = None,
                               **kwargs) -> List[str]:
        """
        自动检测章节并切分PDF
        
        Args:
            method: 检测方法 ('font', 'keywords', 'bookmarks')
            output_dir: 输出目录
            **kwargs: 其他参数
            
        Returns:
            生成的文件路径列表
        """
        if method == 'bookmarks':
            return self.split_by_bookmarks(output_dir)
        elif method == 'font':
            min_font_size = kwargs.get('min_font_size', 14)
            chapters = self.detect_chapters_by_font(min_font_size)
        elif method == 'keywords':
            keywords = kwargs.get('keywords', ['第', '章', 'Chapter', 'CHAPTER'])
            chapters = self.detect_chapters_by_keywords(keywords)
        else:
            raise ValueError(f"不支持的检测方法: {method}")
        
        if not chapters:
            print(f"使用{method}方法未检测到章节")
            return []
        
        return self._split_pdf(chapters, output_dir)
    
    def _split_pdf(self, chapters: List[Dict], output_dir: Optional[str] = None,
                  use_end_page: bool = False) -> List[str]:
        """
        执行PDF切分
        
        Args:
            chapters: 章节信息列表
            output_dir: 输出目录
            use_end_page: 是否使用end_page字段
            
        Returns:
            生成的文件路径列表
        """
        if output_dir:
            self.output_dir = Path(output_dir)
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        
        generated_files = []
        
        # 按页码排序
        chapters.sort(key=lambda x: x['page'])
        
        for i, chapter in enumerate(chapters):
            start_page = chapter['page']
            
            if use_end_page and 'end_page' in chapter:
                end_page = chapter['end_page']
            else:
                # 计算结束页码
                if i < len(chapters) - 1:
                    end_page = chapters[i + 1]['page'] - 1
                else:
                    end_page = self.total_pages - 1
            
            # 清理文件名
            title = self._clean_filename(chapter['title'])
            output_filename = f"{i+1:02d}_{title}.pdf"
            output_path = self.output_dir / output_filename
            
            # 创建新的PDF文档
            new_doc = fitz.open()
            
            # 复制页面
            for page_num in range(start_page, end_page + 1):
                if page_num < self.total_pages:
                    new_doc.insert_pdf(self.doc, from_page=page_num, to_page=page_num)
            
            # 保存文件
            new_doc.save(str(output_path))
            new_doc.close()
            
            generated_files.append(str(output_path))
            print(f"生成章节: {output_filename} (页码 {start_page+1}-{end_page+1})")
        
        return generated_files
    
    def _clean_filename(self, filename: str) -> str:
        """
        清理文件名，移除不合法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        import unicodedata
        
        # 移除或替换不合法字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # 移除不可打印字符和特殊Unicode字符
        filename = ''.join(char for char in filename if unicodedata.category(char)[0] != 'C')
        
        # 替换可能有问题的字符
        filename = re.sub(r'[^\w\s\-_\.\u4e00-\u9fff\u3400-\u4dbf]', '_', filename)
        
        filename = filename.strip()
        
        # 限制长度
        if len(filename) > 50:
            filename = filename[:50]
        
        return filename or "unnamed_chapter"
    
    def get_pdf_info(self) -> Dict:
        """
        获取PDF基本信息
        
        Returns:
            PDF信息字典
        """
        metadata = self.doc.metadata
        bookmarks = self.get_bookmarks()
        
        return {
            'filename': self.pdf_path.name,
            'total_pages': self.total_pages,
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'bookmarks_count': len(bookmarks),
            'bookmarks': bookmarks[:10]  # 只显示前10个书签
        }


def main():
    """主函数，提供命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PDF章节切分工具')
    parser.add_argument('pdf_file', help='PDF文件路径')
    parser.add_argument('-m', '--method', choices=['bookmarks', 'font', 'keywords', 'pages'], 
                       default='bookmarks', help='切分方法')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('--font-size', type=float, default=14, help='最小字体大小阈值')
    parser.add_argument('--keywords', nargs='+', default=['第', '章', 'Chapter'], 
                       help='章节关键词')
    parser.add_argument('--pages', help='页码范围，格式: 1-10,11-20,21-30')
    parser.add_argument('--info', action='store_true', help='显示PDF信息')
    
    args = parser.parse_args()
    
    try:
        with PDFSplitter(args.pdf_file) as splitter:
            if args.info:
                info = splitter.get_pdf_info()
                print("PDF信息:")
                print(f"文件名: {info['filename']}")
                print(f"总页数: {info['total_pages']}")
                print(f"标题: {info['title']}")
                print(f"作者: {info['author']}")
                print(f"书签数量: {info['bookmarks_count']}")
                if info['bookmarks']:
                    print("书签列表:")
                    for bookmark in info['bookmarks']:
                        print(f"  - {bookmark['title']} (第{bookmark['page']+1}页)")
                return
            
            if args.method == 'pages':
                if not args.pages:
                    print("使用pages方法时必须指定--pages参数")
                    return
                
                page_ranges = []
                for page_range in args.pages.split(','):
                    start, end = map(int, page_range.split('-'))
                    page_ranges.append((start-1, end-1))  # 转换为0基索引
                
                files = splitter.split_by_pages(page_ranges, output_dir=args.output)
            else:
                kwargs = {}
                if args.method == 'font':
                    kwargs['min_font_size'] = args.font_size
                elif args.method == 'keywords':
                    kwargs['keywords'] = args.keywords
                
                files = splitter.split_by_auto_detection(args.method, args.output, **kwargs)
            
            print(f"\n切分完成！生成了 {len(files)} 个文件:")
            for file_path in files:
                print(f"  - {file_path}")
                
    except Exception as e:
        print(f"错误: {e}")


if __name__ == '__main__':
    main()

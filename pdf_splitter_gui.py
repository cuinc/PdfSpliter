#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF章节切分工具 - 图形用户界面
提供简单易用的GUI界面来切分PDF文件
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from pdf_splitter import PDFSplitter


class PDFSplitterGUI:
    """PDF切分工具图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF章节切分工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.method = tk.StringVar(value="bookmarks")
        self.font_size = tk.DoubleVar(value=14.0)
        self.keywords = tk.StringVar(value="第,章,Chapter")
        self.page_ranges = tk.StringVar()
        self.bookmark_level = tk.IntVar(value=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # PDF文件选择
        ttk.Label(main_frame, text="PDF文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        pdf_frame = ttk.Frame(main_frame)
        pdf_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        pdf_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(pdf_frame, textvariable=self.pdf_path, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(pdf_frame, text="浏览", command=self.browse_pdf).grid(row=0, column=1)
        
        # 输出目录选择
        ttk.Label(main_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="浏览", command=self.browse_output_dir).grid(row=0, column=1)
        
        # 切分方法选择
        method_frame = ttk.LabelFrame(main_frame, text="切分方法", padding="10")
        method_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        method_frame.columnconfigure(1, weight=1)
        
        # 书签方法
        ttk.Radiobutton(method_frame, text="基于书签", variable=self.method, 
                       value="bookmarks").grid(row=0, column=0, sticky=tk.W, pady=2)
        bookmark_frame = ttk.Frame(method_frame)
        bookmark_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        ttk.Label(bookmark_frame, text="使用PDF内置书签自动切分章节，书签级别:").pack(side=tk.LEFT)
        ttk.Spinbox(bookmark_frame, from_=1, to=5, width=5, textvariable=self.bookmark_level).pack(side=tk.LEFT, padx=(5, 0))
        
        # 字体方法
        ttk.Radiobutton(method_frame, text="基于字体大小", variable=self.method, 
                       value="font").grid(row=1, column=0, sticky=tk.W, pady=2)
        font_frame = ttk.Frame(method_frame)
        font_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        ttk.Label(font_frame, text="最小字体大小:").pack(side=tk.LEFT)
        ttk.Spinbox(font_frame, from_=8, to=24, width=5, textvariable=self.font_size).pack(side=tk.LEFT, padx=(5, 0))
        
        # 关键词方法
        ttk.Radiobutton(method_frame, text="基于关键词", variable=self.method, 
                       value="keywords").grid(row=2, column=0, sticky=tk.W, pady=2)
        keyword_frame = ttk.Frame(method_frame)
        keyword_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        keyword_frame.columnconfigure(1, weight=1)
        ttk.Label(keyword_frame, text="关键词(逗号分隔):").pack(side=tk.LEFT)
        ttk.Entry(keyword_frame, textvariable=self.keywords, width=30).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # 页码范围方法
        ttk.Radiobutton(method_frame, text="手动指定页码", variable=self.method, 
                       value="pages").grid(row=3, column=0, sticky=tk.W, pady=2)
        page_frame = ttk.Frame(method_frame)
        page_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        page_frame.columnconfigure(1, weight=1)
        ttk.Label(page_frame, text="页码范围(如: 1-10,11-20):").pack(side=tk.LEFT)
        ttk.Entry(page_frame, textvariable=self.page_ranges, width=30).pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="查看PDF信息", command=self.show_pdf_info).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="开始切分", command=self.start_split).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空日志", command=self.clear_log).pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 日志输出
        log_frame = ttk.LabelFrame(main_frame, text="输出日志", padding="5")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def browse_pdf(self):
        """浏览选择PDF文件"""
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
            # 自动设置输出目录
            if not self.output_dir.get():
                pdf_path = Path(filename)
                output_path = pdf_path.parent / f"{pdf_path.stem}_chapters"
                self.output_dir.set(str(output_path))
    
    def browse_output_dir(self):
        """浏览选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)
    
    def log(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
    
    def show_pdf_info(self):
        """显示PDF信息"""
        if not self.pdf_path.get():
            messagebox.showerror("错误", "请先选择PDF文件")
            return
        
        try:
            with PDFSplitter(self.pdf_path.get()) as splitter:
                info = splitter.get_pdf_info()
                
                self.log("=== PDF信息 ===")
                self.log(f"文件名: {info['filename']}")
                self.log(f"总页数: {info['total_pages']}")
                self.log(f"标题: {info['title']}")
                self.log(f"作者: {info['author']}")
                self.log(f"主题: {info['subject']}")
                
                # 获取当前配置级别的书签
                current_level_bookmarks = splitter.get_bookmarks(self.bookmark_level.get())
                self.log(f"书签数量(全部): {info['bookmarks_count']}")
                self.log(f"书签数量(第{self.bookmark_level.get()}级): {len(current_level_bookmarks)}")
                
                if current_level_bookmarks:
                    self.log(f"第{self.bookmark_level.get()}级书签列表:")
                    for bookmark in current_level_bookmarks[:10]:  # 只显示前10个
                        self.log(f"  - {bookmark['title']} (第{bookmark['page']+1}页)")
                    if len(current_level_bookmarks) > 10:
                        self.log(f"  ... 还有{len(current_level_bookmarks)-10}个书签")
                else:
                    self.log(f"未找到第{self.bookmark_level.get()}级书签")
                
                self.log("=" * 30)
                
        except Exception as e:
            messagebox.showerror("错误", f"读取PDF信息失败: {str(e)}")
            self.log(f"错误: {str(e)}")
    
    def start_split(self):
        """开始切分PDF"""
        if not self.pdf_path.get():
            messagebox.showerror("错误", "请先选择PDF文件")
            return
        
        if not os.path.exists(self.pdf_path.get()):
            messagebox.showerror("错误", "PDF文件不存在")
            return
        
        # 在后台线程中执行切分
        self.progress.start()
        thread = threading.Thread(target=self._split_worker)
        thread.daemon = True
        thread.start()
    
    def _split_worker(self):
        """切分工作线程"""
        try:
            self.log(f"开始切分PDF: {self.pdf_path.get()}")
            self.log(f"切分方法: {self.method.get()}")
            
            with PDFSplitter(self.pdf_path.get()) as splitter:
                method = self.method.get()
                output_dir = self.output_dir.get() if self.output_dir.get() else None
                
                if method == "bookmarks":
                    files = splitter.split_by_bookmarks(output_dir, self.bookmark_level.get())
                elif method == "font":
                    files = splitter.split_by_auto_detection(
                        'font', output_dir, min_font_size=self.font_size.get()
                    )
                elif method == "keywords":
                    keywords = [k.strip() for k in self.keywords.get().split(',') if k.strip()]
                    files = splitter.split_by_auto_detection(
                        'keywords', output_dir, keywords=keywords
                    )
                elif method == "pages":
                    if not self.page_ranges.get():
                        self.log("错误: 请输入页码范围")
                        return
                    
                    try:
                        page_ranges = []
                        for page_range in self.page_ranges.get().split(','):
                            start, end = map(int, page_range.strip().split('-'))
                            page_ranges.append((start-1, end-1))  # 转换为0基索引
                        
                        files = splitter.split_by_pages(page_ranges, output_dir=output_dir)
                    except ValueError as e:
                        self.log(f"错误: 页码范围格式不正确: {e}")
                        return
                else:
                    self.log(f"错误: 不支持的切分方法: {method}")
                    return
                
                if files:
                    self.log(f"\n切分完成！生成了 {len(files)} 个文件:")
                    for file_path in files:
                        self.log(f"  - {os.path.basename(file_path)}")
                    
                    self.log(f"\n输出目录: {os.path.dirname(files[0])}")
                    messagebox.showinfo("成功", f"PDF切分完成！\n生成了 {len(files)} 个文件")
                else:
                    self.log("未能检测到章节或切分失败")
                    messagebox.showwarning("警告", "未能检测到章节，请尝试其他方法")
                    
        except Exception as e:
            error_msg = f"切分失败: {str(e)}"
            self.log(f"错误: {error_msg}")
            messagebox.showerror("错误", error_msg)
        finally:
            self.progress.stop()


def main():
    """主函数"""
    root = tk.Tk()
    app = PDFSplitterGUI(root)
    
    # 设置窗口图标（如果有的话）
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    root.mainloop()


if __name__ == '__main__':
    main()

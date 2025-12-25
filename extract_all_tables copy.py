"""
提取PDF文件中所有表格的脚本
使用pdfplumber库提取所有表格并保存为CSV和Excel文件

功能：
1. 提取PDF中的所有表格
2. 将每个表格保存为独立的CSV文件
3. 生成整合Excel文件（all_tables_combined.xlsx），包含所有表格，每个表格一个sheet页
4. 生成汇总Excel文件（tables_summary.xlsx），包含所有表格的索引信息
"""
import pdfplumber
import pandas as pd
import os
from datetime import datetime
from pathlib import Path


def extract_all_tables_from_pdf(pdf_path, output_dir="extracted_tables"):
    """
    从PDF文件中提取所有表格
    
    参数:
        pdf_path: PDF文件路径
        output_dir: 输出目录
    """
    if not os.path.exists(pdf_path):
        print(f"错误: 文件不存在: {pdf_path}")
        return
    
    # 创建输出目录
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = Path(output_dir) / f"tables_{timestamp}"
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("开始提取PDF中的所有表格")
    print("=" * 60)
    print(f"PDF文件: {pdf_path}")
    print(f"文件大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
    print(f"输出目录: {output_path}")
    print("=" * 60)
    
    all_tables_data = []
    total_tables = 0
    total_pages = 0
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"\nPDF总页数: {total_pages}")
            print("\n正在处理页面...")
            
            for page_num, page in enumerate(pdf.pages, start=1):
                # 提取当前页面的所有表格
                tables = page.extract_tables()
                
                if tables:
                    print(f"  第 {page_num} 页: 找到 {len(tables)} 个表格")
                    
                    for table_num, table in enumerate(tables, start=1):
                        if table and len(table) > 0:
                            total_tables += 1
                            
                            # 将表格转换为DataFrame
                            try:
                                # 使用第一行作为表头（如果存在）
                                if len(table) > 1:
                                    df = pd.DataFrame(table[1:], columns=table[0])
                                else:
                                    df = pd.DataFrame(table)
                                
                                # 清理数据：移除空行和空列
                                df = df.dropna(how='all').dropna(axis=1, how='all')
                                
                                # 保存为CSV
                                csv_filename = f"page_{page_num:04d}_table_{table_num:02d}.csv"
                                csv_path = output_path / csv_filename
                                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                                
                                # 保存表格信息
                                all_tables_data.append({
                                    'page': page_num,
                                    'table_num': table_num,
                                    'rows': len(df),
                                    'columns': len(df.columns),
                                    'csv_file': csv_filename,
                                    'preview': df.head(3).to_dict('records') if len(df) > 0 else []
                                })
                                
                            except Exception as e:
                                print(f"    警告: 处理第 {page_num} 页第 {table_num} 个表格时出错: {str(e)}")
                                # 即使转换失败，也保存原始数据
                                raw_filename = f"page_{page_num:04d}_table_{table_num:02d}_raw.txt"
                                raw_path = output_path / raw_filename
                                with open(raw_path, 'w', encoding='utf-8') as f:
                                    for row in table:
                                        f.write(str(row) + '\n')
                
                # 每处理10页显示一次进度
                if page_num % 10 == 0:
                    print(f"  已处理 {page_num}/{total_pages} 页，找到 {total_tables} 个表格")
            
            # 保存汇总信息到Excel，并整合所有表格到一个Excel文件
            if all_tables_data:
                print(f"\n正在生成整合的Excel文件...")
                print(f"  将整合 {total_tables} 个表格到Excel文件中")
                
                summary_df = pd.DataFrame([
                    {
                        '页码': item['page'],
                        '表格编号': item['table_num'],
                        '行数': item['rows'],
                        '列数': item['columns'],
                        'CSV文件名': item['csv_file'],
                        'Sheet名称': f"P{item['page']}_T{item['table_num']}"
                    }
                    for item in all_tables_data
                ])
                
                # 生成整合所有表格的Excel文件
                excel_path = output_path / "all_tables_combined.xlsx"
                print(f"  正在创建Excel文件: {excel_path}")
                
                # Excel工作表名称限制和特殊字符处理
                def clean_sheet_name(name):
                    """清理工作表名称，确保符合Excel要求"""
                    # Excel工作表名称不能包含: \ / ? * [ ]
                    invalid_chars = ['\\', '/', '?', '*', '[', ']', ':']
                    for char in invalid_chars:
                        name = name.replace(char, '_')
                    # 限制长度为31个字符
                    if len(name) > 31:
                        name = name[:31]
                    return name
                
                try:
                    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                        # 先添加汇总表
                        summary_df.to_excel(writer, sheet_name='表格汇总', index=False)
                        print(f"  [OK] 已添加汇总表")
                        
                        # 为每个表格创建一个工作表
                        added_count = 0
                        skipped_count = 0
                        used_sheet_names = {'表格汇总'}  # 记录已使用的工作表名称
                        
                        for idx, item in enumerate(all_tables_data, start=1):
                            try:
                                csv_path = output_path / item['csv_file']
                                if csv_path.exists():
                                    df = pd.read_csv(csv_path, encoding='utf-8-sig')
                                    
                                    # 生成工作表名称
                                    sheet_name = f"P{item['page']}_T{item['table_num']}"
                                    sheet_name = clean_sheet_name(sheet_name)
                                    
                                    # 检查工作表名称是否已存在（处理重复情况）
                                    original_sheet_name = sheet_name
                                    counter = 1
                                    while sheet_name in used_sheet_names:
                                        sheet_name = f"{original_sheet_name[:28]}_{counter}"
                                        counter += 1
                                    
                                    used_sheet_names.add(sheet_name)
                                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                                    added_count += 1
                                    
                                    # 每处理50个表格显示一次进度
                                    if idx % 50 == 0:
                                        print(f"  已处理 {idx}/{total_tables} 个表格...")
                                    
                            except Exception as e:
                                skipped_count += 1
                                if skipped_count <= 5:  # 只显示前5个错误
                                    print(f"  警告: 无法添加表格 {item['csv_file']}: {str(e)}")
                                elif skipped_count == 6:
                                    print(f"  ... (更多错误已忽略)")
                        
                        print(f"  [OK] 成功添加 {added_count} 个表格到Excel")
                        if skipped_count > 0:
                            print(f"  [WARN] 跳过 {skipped_count} 个表格")
                    
                    print(f"\n整合Excel文件已保存到: {excel_path}")
                    
                    # 同时生成一个轻量级的汇总文件（只包含汇总表）
                    summary_excel_path = output_path / "tables_summary.xlsx"
                    summary_df.to_excel(summary_excel_path, sheet_name='表格汇总', index=False)
                    print(f"汇总文件已保存到: {summary_excel_path}")
                    
                except Exception as e:
                    print(f"\n错误: 生成整合Excel文件时出错: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    # 如果整合文件失败，至少保存汇总文件
                    summary_excel_path = output_path / "tables_summary.xlsx"
                    summary_df.to_excel(summary_excel_path, sheet_name='表格汇总', index=False)
                    print(f"已保存汇总文件: {summary_excel_path}")
            
            # 打印统计信息
            print("\n" + "=" * 60)
            print("提取完成！")
            print("=" * 60)
            print(f"总页数: {total_pages}")
            print(f"找到表格: {total_tables} 个")
            print(f"输出目录: {output_path}")
            print(f"CSV文件: {total_tables} 个")
            if all_tables_data:
                print(f"整合Excel文件: all_tables_combined.xlsx (包含所有表格)")
                print(f"汇总文件: tables_summary.xlsx (仅包含汇总表)")
            print("=" * 60)
            
            return {
                'total_pages': total_pages,
                'total_tables': total_tables,
                'output_dir': str(output_path),
                'tables_data': all_tables_data
            }
    
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    pdf_path = r"c:\Users\Z2200\Desktop\Safety Assessment\safety-assessment.pdf"
    
    result = extract_all_tables_from_pdf(pdf_path)
    
    if result:
        print(f"\n成功提取 {result['total_tables']} 个表格")
        print(f"所有文件保存在: {result['output_dir']}")


if __name__ == "__main__":
    main()

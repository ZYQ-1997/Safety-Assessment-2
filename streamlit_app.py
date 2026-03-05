"""
PDF 表格提取工具 - Streamlit 入口（用于 Streamlit Cloud 部署）
运行命令: streamlit run streamlit_app.py
"""
import os
import sys
import tempfile
from pathlib import Path

import streamlit as st

# 确保项目根目录在路径中
_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from extract_all_tables import (
    get_all_tables_info,
    filter_tables_for_display,
    extract_all_tables_from_pdf,
)

st.set_page_config(
    page_title="PDF表格提取工具",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("📄 PDF 表格提取工具")
st.caption("上传 PDF，识别表格并导出为新的 PDF")

uploaded_file = st.file_uploader("上传 PDF 文件", type=["pdf"], help="支持大文件，最大约 500MB")

if uploaded_file is None:
    st.info("请先上传一个 PDF 文件。")
    st.stop()

# 保存上传文件到临时目录（Streamlit Cloud 兼容）
with tempfile.TemporaryDirectory() as tmpdir:
    pdf_path = os.path.join(tmpdir, uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    try:
        with st.spinner("正在识别 PDF 中的表格…"):
            all_tables = get_all_tables_info(pdf_path)
            display_tables = filter_tables_for_display(all_tables)
    except Exception as e:
        st.error(f"识别表格失败：{e}")
        st.stop()

    if not display_tables:
        st.warning("未在该 PDF 中发现可显示的表格。")
        st.stop()

    st.success(f"共识别到 **{len(display_tables)}** 个表格（共 {len(all_tables)} 个区域）。")

    # 表格选择
    options = [f"{t.get('name', t.get('id', ''))}（第{t.get('page', '?')}页）" for t in display_tables]
    id_to_option = {t["id"]: opt for t, opt in zip(display_tables, options)}
    option_to_id = {opt: tid for tid, opt in id_to_option.items()}

    selected_options = st.multiselect(
        "选择要提取的表格（不选则提取全部）",
        options=options,
        default=[],
        help="可多选；不选则导出所有表格。",
    )
    selected_ids = [option_to_id[opt] for opt in selected_options] if selected_options else None

    if st.button("提取并生成 PDF", type="primary"):
        out_dir = os.path.join(tmpdir, "output")
        os.makedirs(out_dir, exist_ok=True)
        try:
            with st.spinner("正在提取表格并生成 PDF…"):
                result = extract_all_tables_from_pdf(
                    pdf_path,
                    output_dir=out_dir,
                    selected_table_ids=selected_ids,
                )
            out_pdf = result.get("output_pdf")
            if out_pdf and os.path.isfile(out_pdf):
                with open(out_pdf, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    "下载提取结果 PDF",
                    data=pdf_bytes,
                    file_name=os.path.basename(out_pdf),
                    mime="application/pdf",
                )
                st.success(f"已提取 {result.get('total_tables', 0)} 个表格区域，请点击上方按钮下载。")
            else:
                st.error("生成 PDF 失败，未得到输出文件。")
        except Exception as e:
            st.error(f"提取失败：{e}")

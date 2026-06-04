"""
长文本数据提取平台 - Streamlit 版
"""
import os, sys, tempfile, json, io, uuid, re
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from pathlib import Path

import streamlit as st

_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from extract_all_tables import (
    get_all_tables_info,
    filter_tables_for_display,
    extract_all_tables_from_pdf,
)

# ---- 配置 ----
LOGIN_USER = os.getenv("LOGIN_USERNAME", "admin")
LOGIN_PASS = os.getenv("LOGIN_PASSWORD", "admin123")

st.set_page_config(page_title="长文本数据提取平台", page_icon="📊", layout="centered")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
def do_logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"

def go_workbench():
    st.session_state.page = "workbench"

def go_tool():
    st.session_state.page = "tool"


# ==========================================================================
# 登录页
# ==========================================================================
def show_login():
    st.title("长文本数据提取平台")
    st.caption("请登录以使用系统功能")
    u = st.text_input("用户名", key="login_u")
    p = st.text_input("密码", type="password", key="login_p")

    def try_login():
        if u == LOGIN_USER and p == LOGIN_PASS:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.session_state.page = "workbench"
            st.session_state.err = False
        else:
            st.session_state.err = True

    st.button("登 录", key="login_btn", on_click=try_login)
    if st.session_state.get("err"):
        st.error("用户名或密码错误")


# ==========================================================================
# 工作台
# ==========================================================================
def show_workbench():
    st.subheader("工作台")
    st.caption("选择工具开始处理报告数据")
    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 安评报告智能提取")
        st.caption("上传安全评价报告（PDF/Word），智能识别并提取表格数据")
        if st.button("开始使用", key="btn1", on_click=go_tool):
            pass
    with c2:
        st.markdown("#### 环评报告智能提取")
        st.caption("上传环境影响评价报告，识别提取关键数据表格")
        st.button("开发中", key="btn2", disabled=True)
    with c3:
        st.markdown("#### 总体规划智能提取")
        st.caption("上传总体规划文档，识别提取规划关键信息")
        st.button("开发中", key="btn3", disabled=True)


# ==========================================================================
# 工具页
# ==========================================================================
def show_tool():
    st.subheader("安评报告智能提取")
    st.caption("上传 PDF 或 Word 文件，提取表格导出为 Word")

    mode = st.radio("处理方式", ["本地处理", "后端 API"], horizontal=True, key="mode")
    api_url = ""
    if mode == "后端 API":
        api_url = st.text_input("后端地址", "http://localhost:5000", key="api_url")

    f = st.file_uploader("选择文件", type=["pdf", "docx"], key="upfile")
    if f is None:
        return

    if mode == "本地处理":
        local_handle(f)
    else:
        api_handle(f, api_url)


# ==========================================================================
# 本地处理
# ==========================================================================
def local_handle(uploaded_file):
    fname = uploaded_file.name or "upload"
    ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
    data = uploaded_file.getvalue()
    file_id = uploaded_file.file_id

    if ext == "docx":
        handle_docx_local(fname, data, file_id)
    elif ext == "pdf":
        handle_pdf_local(fname, data, file_id)
    else:
        st.error("仅支持 PDF 或 DOCX")


def handle_docx_local(fname, data, file_id):
    cache_key = f"docx_groups_{file_id}"
    if st.session_state.get(cache_key):
        groups = st.session_state[cache_key]
    else:
        with tempfile.TemporaryDirectory() as td:
            inpath = os.path.join(td, fname)
            with open(inpath, "wb") as fh:
                fh.write(data)
            with st.spinner("分析 Word 表格..."):
                groups, _ = get_docx_table_groups(inpath)
            st.session_state[cache_key] = groups
            st.session_state["docx_path"] = inpath

    if not groups:
        st.warning("未发现表格")
        return
    st.success(f"识别到 {len(groups)} 个表格组")
    opts, idmap = [], {}
    for g in groups:
        nm = g.get("name", "表格")
        cnt = g.get("count", 1)
        lb = f"{nm}（{cnt}个）" if cnt > 1 else nm
        opts.append(lb)
        idmap[lb] = g["id"]
    sel = st.multiselect("选择表格（不选=全部）", opts, default=opts, key="docx_sel")
    sids = [idmap[o] for o in sel] if sel else None
    st.button("生成结果", key="docx_gen", on_click=lambda: st.session_state.__setitem__("do_docx_process", True))

    if st.session_state.get("do_docx_process"):
        with st.spinner("正在生成 Word..."):
            do_docx_process(data, fname, sids, file_id)
        st.session_state.do_docx_process = False
        st.rerun()

    if st.session_state.get(f"download_docx_{file_id}"):
        buf = st.session_state.get(f"download_docx_{file_id}")
        st.download_button("下载 Word", buf,
                           file_name=f"{Path(fname).stem}_提取结果.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           key="docx_dl")
        st.success(f"完成，保留 {st.session_state.get(f'docx_count_{file_id}', 0)} 个表格")


def do_docx_process(data, fname, sids, file_id):
    try:
        tmpd = tempfile.mkdtemp()
        inpath = os.path.join(tmpd, fname)
        with open(inpath, "wb") as fh:
            fh.write(data)
        out = os.path.join(tmpd, f"{uuid.uuid4().hex}.docx")
        n = word_remove_non_table(inpath, out, sids)
        with open(out, "rb") as fh:
            st.session_state[f"download_docx_{file_id}"] = fh.read()
        st.session_state[f"docx_count_{file_id}"] = n
    except Exception as e:
        st.session_state.docx_error = str(e)


def handle_pdf_local(fname, data, file_id):
    cache_key = f"pdf_tables_{file_id}"
    if st.session_state.get(cache_key):
        disp = st.session_state[cache_key]
    else:
        with tempfile.TemporaryDirectory() as td:
            pp = os.path.join(td, fname)
            with open(pp, "wb") as fh:
                fh.write(data)
            with st.spinner("识别 PDF 表格..."):
                allt = get_all_tables_info(pp)
                disp = filter_tables_for_display(allt)
            st.session_state[cache_key] = disp
            st.session_state["pdf_path"] = pp

    if not disp:
        st.warning("未发现表格")
        return
    st.success(f"识别到 {len(disp)} 个表格")
    ol = [f"{t.get('name','')}（第{t.get('page','?')}页）" for t in disp]
    o2i = {o: t["id"] for o, t in zip(ol, disp)}
    sel = st.multiselect("选择表格（不选=全部）", ol, default=[], key="pdf_sel")
    sids = [o2i[o] for o in sel] if sel else None
    st.button("生成结果", key="pdf_gen", on_click=lambda: st.session_state.__setitem__("do_pdf_process", True))

    if st.session_state.get("do_pdf_process"):
        with st.spinner("正在提取表格并生成 Word..."):
            do_pdf_process(data, fname, sids, file_id)
        st.session_state.do_pdf_process = False
        st.rerun()

    if st.session_state.get(f"download_pdf_{file_id}"):
        buf = st.session_state.get(f"download_pdf_{file_id}")
        st.download_button("下载 Word", buf,
                           file_name=f"{Path(fname).stem}_提取结果.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           key="pdf_dl")
        st.success(f"完成，{st.session_state.get(f'pdf_count_{file_id}', 0)} 个表格")


def do_pdf_process(data, fname, sids, file_id):
    try:
        tmpd = tempfile.mkdtemp()
        pp = os.path.join(tmpd, fname)
        with open(pp, "wb") as fh:
            fh.write(data)
        od = os.path.join(tmpd, "out")
        os.makedirs(od, exist_ok=True)
        r = extract_all_tables_from_pdf(pp, od, sids, output_format="docx")
        td2 = r.get("tables_data", []) if isinstance(r, dict) else []
        if not td2:
            st.session_state.pdf_error = "未提取到表格"
            return
        buf = build_docx(td2)
        st.session_state[f"download_pdf_{file_id}"] = buf
        st.session_state[f"pdf_count_{file_id}"] = len(td2)
    except Exception as e:
        st.session_state.pdf_error = str(e)


# ==========================================================================
# API 处理
# ==========================================================================
def api_handle(uploaded_file, base_url):
    base = base_url.strip().rstrip("/")
    if not base:
        st.error("请输入后端地址")
        return
    fname = uploaded_file.name
    data = uploaded_file.getvalue()

    try:
        with st.spinner("连接后端..."):
            h = http_json("GET", f"{base}/api/health")
            if h.get("status") != "ok":
                st.warning(f"后端异常: {h}")
    except Exception as e:
        st.error(f"无法连接: {e}")
        return
    try:
        with st.spinner("上传中..."):
            up = http_upload(f"{base}/api/upload", "file", fname, data)
        bfn = up.get("filename")
        if not bfn:
            st.error(f"上传失败: {up}")
            return
    except Exception as e:
        st.error(f"上传失败: {e}")
        return
    try:
        with st.spinner("获取表格列表..."):
            r = http_json("POST", f"{base}/api/tables", {"filename": bfn})
        tabs = r.get("tables", [])
        if not tabs:
            st.warning("未获取到表格")
            return
    except Exception as e:
        st.error(f"获取失败: {e}")
        return
    st.success(f"{len(tabs)} 个表格")
    ol = [f"{t.get('name','')}（第{t.get('page','?')}页）" for t in tabs]
    o2i = {o: t["id"] for o, t in zip(ol, tabs)}
    sel = st.multiselect("选择表格（不选=全部）", ol, default=[], key="api_sel")
    sids = [o2i[o] for o in sel] if sel else None
    st.button("提取", key="api_gen", on_click=lambda: st.session_state.__setitem__("do_api_process", True))

    if st.session_state.get("do_api_process"):
        with st.spinner("正在提取..."):
            do_api_process(base, bfn, sids)
        st.session_state.do_api_process = False
        st.rerun()

    if st.session_state.get("download_api"):
        out = st.session_state.get("download_api")
        oname = st.session_state.get("download_api_name", "result.docx")
        st.download_button("下载结果", out, file_name=oname,
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           key="api_dl")
        st.success(f"完成，{st.session_state.get('api_table_count','?')} 个表格")
    if st.session_state.get("api_error"):
        st.error(st.session_state.api_error)
        st.session_state.api_error = None


def do_api_process(base, bfn, sids):
    try:
        pld = {"filename": bfn}
        if sids is not None:
            pld["selected_table_ids"] = sids
        r2 = http_json("POST", f"{base}/api/extract", pld)
        dl = r2.get("download_url")
        oname = r2.get("output_filename", "result.docx")
        if not dl:
            st.session_state.api_error = f"提取失败: {r2}"
            return
        out = http_get(f"{base}{dl}")
        st.session_state.download_api = out
        st.session_state.download_api_name = oname
        st.session_state.api_table_count = r2.get("total_tables", "?")
    except Exception as e:
        st.session_state.api_error = str(e)


# ==========================================================================
# 工具函数
# ==========================================================================
def http_json(method, url, payload=None, timeout=60):
    d = None
    hd = {"Accept": "application/json"}
    if payload:
        d = json.dumps(payload, ensure_ascii=False).encode()
        hd["Content-Type"] = "application/json; charset=utf-8"
    with urlopen(Request(url, data=d, headers=hd, method=method.upper()), timeout=timeout) as resp:
        raw = resp.read()
    return json.loads(raw.decode()) if raw else {}

def http_upload(url, field, fname, content, timeout=120):
    b = uuid.uuid4().hex
    body = io.BytesIO()
    body.write(f"--{b}\r\n".encode())
    body.write(f'Content-Disposition: form-data; name="{field}"; filename="{fname}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode())
    body.write(content)
    body.write(b"\r\n")
    body.write(f"--{b}--\r\n".encode())
    ct = f"multipart/form-data; boundary={b}"
    req = Request(url, data=body.getvalue(), headers={"Content-Type": ct, "Accept": "application/json"}, method="POST")
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return json.loads(raw.decode()) if raw else {}

def http_get(url, timeout=120):
    with urlopen(Request(url, method="GET"), timeout=timeout) as resp:
        return resp.read()

def clean_text(text):
    if not text or not isinstance(text, str):
        return ""
    s = text.replace("\r\n", "\n").replace("\r", "\n").replace("\a", "\n")
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", s).strip()

def norm_title(pt):
    if not pt or not isinstance(pt, str):
        return None
    s = pt.strip()
    if not s:
        return None
    if "评价报告摘要" in s:
        return "评价报告摘要"
    m = re.match(r"^表\s*\d+\s*[-－–]\s*\d+\s+.+", s)
    return s if m else None

def clean_title_line(pt):
    if not pt or not isinstance(pt, str):
        return None
    s = clean_text(pt)
    if not s:
        return None
    for line in s.split("\n"):
        t = re.sub(r"\s+", " ", line.strip())
        if t:
            return t
    return None

def dedupe_title(title):
    if not title or not isinstance(title, str):
        return ""
    s = re.sub(r"\s+", " ", title).strip()
    m = re.match(r"^(.+?)(?:\s+\1)+$", s)
    if m:
        s = m.group(1).strip()
    tokens = s.split(" ")
    out, prev = [], None
    for tok in tokens:
        if tok and tok != prev:
            out.append(tok)
        prev = tok
    if len(out) % 2 == 0 and out[:len(out)//2] == out[len(out)//2:]:
        out = out[:len(out)//2]
    return " ".join(out).strip()

def get_docx_table_groups(docx_path):
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(docx_path)
    body = doc.element.body
    pT, tblT = qn("w:p"), qn("w:tbl")
    last, gmap, glist, ti = None, {}, [], 0
    for ch in body:
        if ch.tag == pT:
            try:
                t = "".join((n.text or "") for n in ch.iter() if hasattr(n, "text"))
                if t and t.strip():
                    last = t.strip()
            except Exception:
                pass
            continue
        if ch.tag != tblT:
            continue
        tid = f"table_{ti}"
        raw = clean_title_line(last)
        n = norm_title(raw) if raw else None
        nm = dedupe_title(n or raw or f"表格{ti+1}")
        if nm not in gmap:
            g = {"id": tid, "name": nm, "page": ti+1, "table_num": len(glist)+1, "table_ids": [tid], "count": 1}
            gmap[nm] = g
            glist.append(g)
        else:
            g = gmap[nm]
            g["table_ids"].append(tid)
            g["count"] += 1
        ti += 1
    imap = {}
    for g in glist:
        for tid in g["table_ids"]:
            imap[tid] = g["table_ids"]
        imap[g["id"]] = g["table_ids"]
    return glist, imap

def word_remove_non_table(docx_path, out_path, selected_ids=None):
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(docx_path)
    body = doc.element.body
    tblT, pT = qn("w:tbl"), qn("w:p")
    children = list(body)
    keep, ti = set(), 0
    for i, ch in enumerate(children):
        if ch.tag == tblT:
            if selected_ids is None or f"table_{ti}" in selected_ids:
                keep.add(i)
                if i > 0 and children[i-1].tag == pT:
                    keep.add(i-1)
            ti += 1
    for i in range(len(children)-1, -1, -1):
        if i not in keep:
            body.remove(children[i])
    doc.save(out_path)
    return sum(1 for i in keep if children[i].tag == tblT)

def build_docx(tables_data):
    from docx import Document
    from docx.shared import Pt
    from docx.oxml.ns import qn
    from docx.enum.table import WD_TABLE_ALIGNMENT
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "等线"
    style.font.size = Pt(9)
    try:
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "等线")
    except Exception:
        pass
    for t in tables_data:
        title = (t.get("title") or t.get("name") or "").strip()
        if title:
            p = doc.add_paragraph()
            r = p.add_run(title)
            r.bold = True
            r.font.size = Pt(10.5)
        rows = t.get("data") or []
        if not rows:
            continue
        ncols = max((len(row) for row in rows), default=0)
        if ncols <= 0:
            continue
        norm = [list(r)[:ncols] for r in rows]
        for r in norm:
            while len(r) < ncols:
                r.append("")
        tbl = doc.add_table(rows=len(norm), cols=ncols, style="Table Grid")
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for ri, row in enumerate(norm):
            for ci, val in enumerate(row):
                tbl.cell(ri, ci).text = "" if val is None else str(val)
        doc.add_paragraph("")
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


# ==========================================================================
# 主入口
# ==========================================================================
if not st.session_state.logged_in:
    show_login()
else:
    # 顶部栏
    c_top_l, c_top_r = st.columns([8, 1])
    with c_top_l:
        st.caption(f"长文本数据提取平台  |  当前用户: {st.session_state.get('username', 'admin')}")
    with c_top_r:
        st.button("退出", key="top_logout", on_click=do_logout)

    if st.session_state.page == "tool":
        st.button("← 工作台", key="top_back", on_click=go_workbench)
        show_tool()
    else:
        show_workbench()

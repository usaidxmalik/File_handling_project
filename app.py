"""
File Manager — minimalist dark Streamlit UI over basic file operations
(create / read / write (rename, append, overwrite) / delete).

All operations are sandboxed to a local `workspace/` folder next to this
file, and file names are validated to prevent path traversal.
"""

from pathlib import Path

import streamlit as st

# --------------------------------------------------------------------------
# Setup & safety
# --------------------------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
WORKSPACE = (APP_DIR / "workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)


def safe_path(filename: str) -> Path:
    filename = (filename or "").strip()
    if not filename:
        raise ValueError("Enter a file name.")
    if any(sep in filename for sep in ("/", "\\")) or filename in (".", ".."):
        raise ValueError("File name can't contain a path — just a plain file name.")
    candidate = (WORKSPACE / filename).resolve()
    if candidate.parent != WORKSPACE:
        raise ValueError("That file name isn't allowed.")
    return candidate


# --------------------------------------------------------------------------
# Page config + minimal styling
# --------------------------------------------------------------------------

st.set_page_config(page_title="File Manager", page_icon="🗂️", layout="centered")

st.markdown(
    """
    <style>
    .block-container { padding-top: 3.5rem; max-width: 640px; }
    h1 { text-align: center; font-weight: 600; }
    .muted { color: #9A9CA3; text-align: center; margin-top: -0.8rem; margin-bottom: 2rem; }

    button[kind="primary"], button[kind="secondary"] {
        border-radius: 999px !important;
        font-weight: 500 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        padding: 0.5rem 0.25rem;
    }

    .file-contents {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.88rem;
        white-space: pre-wrap;
        word-break: break-word;
        background-color: #17181B;
        border: 1px solid #2A2B2E;
        border-left: 3px solid #5C7CFA;
        padding: 1rem;
        border-radius: 8px;
        max-height: 380px;
        overflow-y: auto;
        margin-top: 0.75rem;
    }

    .status-ok, .status-err {
        padding: 0.5rem 0.9rem;
        border-radius: 6px;
        font-size: 0.92rem;
        margin-top: 0.75rem;
    }
    .status-ok  { background-color: rgba(52, 211, 153, 0.12); color: #34D399; }
    .status-err { background-color: rgba(248, 113, 113, 0.12); color: #F87171; }
    </style>
    """,
    unsafe_allow_html=True,
)


def ok(msg: str) -> None:
    st.markdown(f'<div class="status-ok">{msg}</div>', unsafe_allow_html=True)


def err(msg: str) -> None:
    st.markdown(f'<div class="status-err">{msg}</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Header + centered nav
# --------------------------------------------------------------------------

st.title("File Manager")
st.markdown('<p class="muted">workspace/ · sandboxed</p>', unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Create"

labels = ["Create", "Read", "Write", "Delete"]
cols = st.columns(len(labels))
for col, label in zip(cols, labels):
    with col:
        active = st.session_state.page == label
        if st.button(
            label,
            key=f"nav_{label}",
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state.page = label

page = st.session_state.page
st.write("")

# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

if page == "Create":
    with st.container(border=True):
        st.caption("Make a new file in the workspace.")
        name = st.text_input("File name")
        content = st.text_area("Contents", height=150)
        if st.button("Create file"):
            try:
                path = safe_path(name)
                if path.exists():
                    err("A file with that name already exists.")
                else:
                    path.write_text(content, encoding="utf-8")
                    ok(f"Created {path.name}.")
            except ValueError as e:
                err(str(e))
            except OSError as e:
                err(f"Couldn't create the file: {e}")

elif page == "Read":
    with st.container(border=True):
        st.caption("View the contents of a file.")
        name = st.text_input("File name")
        if st.button("Read file"):
            try:
                path = safe_path(name)
                if not path.exists():
                    err("That file doesn't exist.")
                else:
                    data = path.read_text(encoding="utf-8")
                    st.markdown(
                        f'<div class="file-contents">{data or "(empty file)"}</div>',
                        unsafe_allow_html=True,
                    )
            except ValueError as e:
                err(str(e))
            except UnicodeDecodeError:
                err("That file isn't plain text — can't display it here.")
            except OSError as e:
                err(f"Couldn't read the file: {e}")

elif page == "Write":
    with st.container(border=True):
        st.caption("Rename, append to, or overwrite an existing file.")
        name = st.text_input("File name")
        target_path = None
        if name.strip():
            try:
                target_path = safe_path(name)
            except ValueError as e:
                err(str(e))

        if target_path is not None:
            if not target_path.exists():
                err("That file doesn't exist.")
            else:
                op = st.radio("Operation", ["Rename", "Append", "Overwrite"], horizontal=True)

                if op == "Rename":
                    new_name = st.text_input("New file name")
                    if st.button("Rename"):
                        try:
                            new_path = safe_path(new_name)
                            if new_path.exists():
                                err("A file with that name already exists.")
                            else:
                                target_path.rename(new_path)
                                ok(f"Renamed to {new_path.name}.")
                        except ValueError as e:
                            err(str(e))
                        except OSError as e:
                            err(f"Couldn't rename the file: {e}")

                elif op == "Append":
                    data = st.text_area("Data to append", height=120)
                    if st.button("Append"):
                        try:
                            with open(target_path, "a", encoding="utf-8") as f:
                                f.write("\n" + data)
                            ok("Appended.")
                        except OSError as e:
                            err(f"Couldn't append: {e}")

                elif op == "Overwrite":
                    data = st.text_area("New contents", height=150)
                    if st.button("Overwrite"):
                        try:
                            target_path.write_text(data, encoding="utf-8")
                            ok("Overwritten.")
                        except OSError as e:
                            err(f"Couldn't overwrite: {e}")

elif page == "Delete":
    with st.container(border=True):
        st.caption("Permanently remove a file from the workspace.")
        name = st.text_input("File name")
        confirm = st.checkbox("I understand this can't be undone.")
        if st.button("Delete file", disabled=not confirm):
            try:
                path = safe_path(name)
                if not path.exists():
                    err("That file doesn't exist.")
                else:
                    path.unlink()
                    ok(f"Deleted {path.name}.")
            except ValueError as e:
                err(str(e))
            except OSError as e:
                err(f"Couldn't delete the file: {e}")
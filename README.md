# File Manager

A minimalist Streamlit UI for basic file operations — create, read,
write (rename / append / overwrite), and delete. All operations are
sandboxed to a local `workspace/` folder, with filenames validated to
prevent path traversal.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. `workspace/` is created
automatically on first run.

## Notes

- Only plain filenames are accepted (no subfolders, no `..`) — this is
  what keeps every operation locked inside `workspace/`.
- UI built with AI assistance (Claude); the file-handling logic is
  original.
- Not meant for multi-user hosting: on Streamlit Community Cloud,
  storage is ephemeral and shared across every visitor, with no
  per-user isolation.

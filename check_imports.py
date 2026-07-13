import importlib
mods=['dotenv','groq','flask','werkzeug','click']
res={m: bool(importlib.util.find_spec(m)) for m in mods}
print(res)

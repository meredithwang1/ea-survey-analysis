import importlib.util
spec=importlib.util.spec_from_file_location('ea','ea_forum_streamlit.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
threads=[
    {'title':'bug fix not working'},
    {'title':'patch update is horrible'},
    {'title':'cheating in game'},
    {'title':'crash on startup'},
    {'title':'bug fix still happening'},
    {'title':'patch update issue'},
    {'title':'crash and bug'}
]
print(mod.most_common_phrases(threads, top_n=12))

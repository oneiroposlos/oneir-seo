from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from .prompt import *

prompts_file = str(Path('./prompts').resolve())
print(f"Load pdf understanding prompts from: {prompts_file}")

prompts_tpl = Environment(
    loader=FileSystemLoader(prompts_file),
    autoescape=select_autoescape(['html', 'xml'])
)

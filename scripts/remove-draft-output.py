"""Remove only the two withdrawn notes' generated HTML after Quarto renders.

Quarto's draft-mode: gone strips their contents but leaves reachable empty
files. The sources remain intact. Stop removing a note if it is undrafted.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
targets = (
    (root / 'notes/probability-paths.qmd', root / '_site/notes/probability-paths.html'),
    (root / 'notes/evaluation-under-budget.qmd', root / '_site/notes/evaluation-under-budget.html'),
)

for source, output in targets:
    text = source.read_text(encoding='utf-8')
    frontmatter = text.split('---', 2)[1] if text.startswith('---\n') else ''
    if not re.search(r'^draft:\s*true\s*$', frontmatter, re.MULTILINE):
        continue
    if output.is_symlink():
        raise RuntimeError(f'Refusing to follow a symlink: {output}')
    if output.exists():
        if not output.is_file():
            raise RuntimeError(f'Expected a generated file: {output}')
        output.unlink()
        print(f'Removed generated draft output: {output.relative_to(root)}')

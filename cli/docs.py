"""Documentation generator CLI tool for Python modules.

python -m cli.docs <module_path> [-o <output_file>] [-v]

Arguments:
    module_path: The dotted path to the module for which documentation is to be \
        generated.

Options:
    -o, --output: Optional file path to write the markdown documentation.
    -v, --verbose: Renders the markdown content to the console.

Example:
    python -m cli.docs cli.docs -o cli.md -v

This will generate markdown documentation for the `cli.docs` module and write it to \
    `cli.md`:

    # Documentation for `cli.docs`

    ### Function `cli(module_path, output, verbose)`
    **Docstring**:
    CLI tool to generate markdown documentation for a given Python module path.

    ### Function `MDGenerator(module_path)`
    **Docstring**:
    Initializes the generator with the module path.

    (...)

    ---

    Generated using `docs.py` on `cli/docs.py`. | 2024-11-01 12:00:00
"""

import ast
import datetime
import importlib.util
import os

import click
import django
from rich.console import Console
from rich.markdown import Markdown

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_PATH = os.environ.get("DOC_PATH", os.path.join(_root_path, "docs", "md"))

ASTNode = ast.AsyncFunctionDef | ast.FunctionDef | ast.ClassDef | ast.Module

console = Console()


class MDGenerator:
    """Markdown file generator."""

    console: Console
    module_path: str
    _module_file_path: str
    _content: str

    def __init__(self, module_path: str) -> None:
        """Initializes the generator with the module path."""
        self.module_path = module_path
        self.console = Console()

    def set_module_file_path(self) -> str:
        """Returns the file path of a module given its dotted path."""
        spec = importlib.util.find_spec(self.module_path)
        if spec and spec.origin:
            self._module_file_path = spec.origin
            return spec.origin

        raise ImportError(f"Module '{self.module_path}' not found.")

    def extract_docstring(self, node: ASTNode) -> str:
        """Extracts the docstring from a node if available."""
        if docstring := ast.get_docstring(node):
            summary, *details = docstring.split("\n\n")
            return f"{summary}\n\n" + "\n".join(f"\t{line}" for line in details)
        else:
            return "No docstring available."

    def process_function(self, node: ASTNode) -> str:
        """Processes a function node and returns markdown-formatted information."""
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            raise ValueError("Node must be a function definition.")

        func_name = node.name
        args = [arg.arg for arg in node.args.args]
        docstring = self.extract_docstring(node)
        args_str = ", ".join(args)

        return (
            f"### Function `{func_name}({args_str})`\n\n**Docstring**:\n\n{docstring}\n"
        )

    def process_class(self, node: ASTNode) -> str:
        """Processes a class node and returns markdown-formatted information."""
        if not isinstance(node, ast.ClassDef):
            raise ValueError("Node must be a class definition.")

        class_name = node.name
        docstring = self.extract_docstring(node)

        methods_md = ""
        for sub_node in node.body:
            if isinstance(sub_node, ast.FunctionDef):
                methods_md += self.process_function(sub_node)

        attrs_md: str | None = None

        if attrs := self._process_class_attrs(node):
            attrs_md = "\n".join(f"- `{attr}`" for attr in attrs) + "\n"

        content = f"## Class `{class_name}`\n\n"
        content += f"**Docstring**:{docstring}\n\n"
        content += f"**Attributes**:\n\n{attrs_md}\n" if attrs_md else ""
        content += methods_md

        return content

    def generate_markdown_from_module_path(self) -> None:
        """Generates markdown documentation for a module specified by its path."""
        with open(self._module_file_path, encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=self._module_file_path)

        markdown_content = f"# Documentation for `{self.module_path}`\n\n"

        for node in tree.body:
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markdown_content += self.process_function(node)
            elif isinstance(node, ast.ClassDef):
                markdown_content += self.process_class(node)

        markdown_content += self._footer

        self._content = markdown_content

    @property
    def _footer(self) -> str:
        return (
            "\n---\n"
            f"Generated using `docs.py` on `{self._module_file_path}`. | "
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def _process_class_attrs(self, node: ASTNode) -> list[str] | None:
        attrs = []
        for sub_node in node.body:
            if isinstance(sub_node, ast.Assign):
                for target in sub_node.targets:
                    if isinstance(target, ast.Name):
                        attrs.append(target.id)

        if len(attrs) == 0:
            return None

        return attrs

    def _handle_verbose(self, verbose: bool) -> None:
        if verbose:
            md = Markdown(markup=self._content, justify="left")
            self.console.print(md)
        else:
            self.console.print(self._content)

    def _handle_output(self, output: str | None) -> None:
        if not output:
            self.console.print(self._content)
            return

        dirpath = f"{DOC_PATH}/pydocs"

        if not os.path.exists(dirpath):
            os.makedirs(f"{dirpath}")

        fpath, ext = os.path.splitext(output)
        fpath = os.path.join(dirpath, f"{fpath}.md")

        with open(fpath, "w+", encoding="utf-8") as md_file:
            md_file.write(self._content)
            self.console.print(f"Markdown documentation has been written to {fpath}")

    def __call__(self, output: str | None, verbose: bool) -> None:
        """CLI tool to generate markdown documentation for a given module path."""
        try:
            self.set_module_file_path()
            self.generate_markdown_from_module_path()
            self._handle_output(output)
            self._handle_verbose(verbose)
        except ImportError as e:
            self.console.print(f"Error: {e}", style="bold red")


@click.command()
@click.argument("module_path")
@click.option("--output", "-o", default=None, help="Optional file path.")
@click.option("--verbose", "-v", is_flag=True, help="Renders md to stdout.")
def cli(module_path: str, output: str | None, verbose: bool) -> None:
    """CLI tool to generate markdown documentation for a given Python module path."""
    MDGenerator(module_path).__call__(output, verbose)


if __name__ == "__main__":
    cli()

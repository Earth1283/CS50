from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.box import ROUNDED

console = Console()

def printBox(content: str, title: str = None, subtitle: str = None, color: str = "white", title_color: str = "white", subtitle_color: str = "white"):
    panel_content = Text(content, style=color, justify="center")
    panel = Panel(
        panel_content,
        title=f"[{title_color}]{title}[/]" if title else None,
        subtitle=f"[{subtitle_color}]{subtitle}[/]" if subtitle else None,
        border_style=color,
        width=80,
        box=ROUNDED
    )
    console.print(panel, justify="center")
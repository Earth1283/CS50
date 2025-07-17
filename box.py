from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.box import ROUNDED

console = Console()

# Okay i will depreciate this API because nobdoy will use this as everyone will be using Rich.box or rich.panel before we know it
# We just have to set best practices for this so that they don't make weird windows.
# So Depreciation in some commits

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
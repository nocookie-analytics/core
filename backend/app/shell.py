from IPython.terminal import embed

if __name__ == "__main__":
    terminal = embed.InteractiveShellEmbed()
    terminal.extension_manager.load_extension("autoreload")
    terminal.run_line_magic("autoreload", "2")

    from app.models import *
    from app.api.deps import get_db

    db = next(get_db())
    terminal.mainloop()

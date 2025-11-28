import sqlite3
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box

class DatabaseManager:
    def __init__(self):
        self.db_path = Path.home() / ".phshorts" / "history.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                title TEXT,
                filename TEXT,
                quality TEXT,
                date_downloaded TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_entry(self, url, title, filename, quality):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('INSERT INTO history (url, title, filename, quality, date_downloaded) VALUES (?, ?, ?, ?, ?)',
                      (url, title, str(filename), str(quality), datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:
            # Fail silently to not interrupt the user experience
            pass

    def show_history(self, console: Console, limit=10):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT title, quality, date_downloaded, filename FROM history ORDER BY date_downloaded DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()

        if not rows:
            console.print("[yellow]No download history found.[/]")
            return

        table = Table(title="📜 Download History", box=box.ROUNDED)
        table.add_column("Date", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Quality", style="magenta")
        table.add_column("Filename", style="dim")

        for title, quality, date_str, filename in rows:
            try:
                dt = datetime.fromisoformat(date_str)
                formatted_date = dt.strftime("%Y-%m-%d %H:%M")
            except:
                formatted_date = date_str
            
            table.add_row(formatted_date, title, f"{quality}p", Path(filename).name)

        console.print(table)

    def show_stats(self, console: Console):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Total downloads
        c.execute('SELECT COUNT(*) FROM history')
        total = c.fetchone()[0]
        
        if total == 0:
            console.print("[yellow]No statistics available yet.[/]")
            conn.close()
            return

        # Quality stats
        c.execute('SELECT quality, COUNT(*) FROM history GROUP BY quality')
        quality_stats = c.fetchall()
        
        conn.close()

        console.print(f"\n[bold cyan]📊 Download Statistics[/]")
        console.print(f"Total Downloads: [bold green]{total}[/]\n")
        
        table = Table(title="Quality Distribution", box=box.SIMPLE)
        table.add_column("Quality", style="magenta")
        table.add_column("Count", style="green")
        table.add_column("Percentage", style="yellow")

        for quality, count in quality_stats:
            percentage = (count / total) * 100
            table.add_row(f"{quality}p", str(count), f"{percentage:.1f}%")

        console.print(table)

#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Input, ListView, ListItem, Label, Header, Footer
import subprocess

class PackageItem(ListItem):
    def __init__(self, paket_name: str, anzeige_text: str, status_info: str) -> None:
        super().__init__()
        self.paket_name = paket_name
        self.anzeige_text = anzeige_text
        self.status_info = status_info

    def compose(self) -> ComposeResult:
        yield Label(self.anzeige_text)

class PacmanTui(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    Input {
        dock: top;
        margin: 1;
    }
    ListView {
        height: 1fr;
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("u", "system_update", "System Update"),
        ("r", "remove_package", "Uninstall"),
        ("1", "filter_installed", "Installed"),
        ("2", "filter_not_installed", "Not Installed"),
        ("3", "filter_newest", "Newest"),
        ("4", "filter_oldest", "Oldest"),
        ("0", "filter_clear", "Clear Filter"),
    ]

    def __init__(self):
        super().__init__()
        self.all_items = []
        self.installed_packages = set()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search for packet... (Press Enter to search)")
        yield ListView(id="package-list")
        yield Footer()

    def load_installed_packages(self) -> None:
        res = subprocess.run(["pacman", "-Q", "--color=never"], capture_output=True, text=True)
        self.installed_packages = {line.split(" ")[0].strip() for line in res.stdout.splitlines() if line.strip()}

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        suchbegriff = event.value
        list_view = self.query_one("#package-list", ListView)
        await list_view.clear()
        self.all_items.clear()
            
        if not suchbegriff:
            return

        self.load_installed_packages()

        kommando = ["yay", "-Ss", "--color=never", suchbegriff]
        ausgabe = subprocess.run(kommando, capture_output=True, text=True)
        zeilen = ausgabe.stdout.splitlines()

        for i in range(0, len(zeilen), 2):
            if i + 1 >= len(zeilen):
                break
                
            paket_info = zeilen[i].strip()
            beschreibung = zeilen[i+1].strip()
            
            repo_und_name_liste = paket_info.split(" ")
            if not repo_und_name_liste:
                continue
            full_repo_name = repo_und_name_liste[0]
            reiner_name = full_repo_name.split("/")[-1]
            
            is_installed = reiner_name in self.installed_packages
            status_str = "installed" if is_installed else "not installed"
            
            badge = " [green][Installed][/green]" if is_installed else ""
            anzeige_text = f"[bold]{paket_info}[/bold]{badge}\n   [dim]{beschreibung}[/dim]"
            
            item = PackageItem(reiner_name, anzeige_text, status_str)
            self.all_items.append(item)

        await self.apply_filter_and_sort()
        list_view.focus()

    async def apply_filter_and_sort(self, filter_type: str = "all", sort_type: str = "none") -> None:
        list_view = self.query_one("#package-list", ListView)
        await list_view.clear()
        
        filtered = self.all_items
        if filter_type == "installed":
            filtered = [item for item in self.all_items if item.status_info == "installed"]
        elif filter_type == "not_installed":
            filtered = [item for item in self.all_items if item.status_info == "not_installed"]

        if sort_type == "newest":
            filtered = sorted(filtered, key=lambda x: x.paket_name, reverse=True)
        elif sort_type == "oldest":
            filtered = sorted(filtered, key=lambda x: x.paket_name)

        for item in filtered:
            new_item = PackageItem(item.paket_name, item.anzeige_text, item.status_info)
            await list_view.append(new_item)

    async def action_filter_installed(self) -> None:
        await self.apply_filter_and_sort(filter_type="installed")

    async def action_filter_not_installed(self) -> None:
        await self.apply_filter_and_sort(filter_type="not_installed")

    async def action_filter_newest(self) -> None:
        await self.apply_filter_and_sort(sort_type="newest")

    async def action_filter_oldest(self) -> None:
        await self.apply_filter_and_sort(sort_type="oldest")

    async def action_filter_clear(self) -> None:
        await self.apply_filter_and_sort()

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        paket_name = event.item.paket_name
        with self.suspend():
            print(f"\n=== Start installation of: {paket_name} ===")
            subprocess.run(["yay", "-S", paket_name])
            input("\nPress ENTER to return to the TUI...")

    async def action_remove_package(self) -> None:
        list_view = self.query_one("#package-list", ListView)
        if list_view.highlighted_child is None:
            return
        paket_name = list_view.highlighted_child.paket_name
        with self.suspend():
            print(f"\n=== Remove Package: {paket_name} ===")
            subprocess.run(["sudo", "pacman", "-Rns", paket_name])
            input("\nPress ENTER to return to the TUI...")

    async def action_system_update(self) -> None:
        with self.suspend():
            print("\n=== Start System-Update (yay -Syu) ===")
            subprocess.run(["yay", "-Syu"])
            input("\nPress ENTER to return to the TUI...")
        input_field = self.query_one(Input)
        if input_field.value:
            await self.on_input_submitted(Input.Submitted(input_field, input_field.value))

def main():
    app = PacmanTui()
    app.run()

if __name__ == "__main__":
    main()

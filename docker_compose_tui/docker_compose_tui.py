from datetime import datetime

from rich.align import Align
from rich.table import Table

from textual.app import App
from textual.widget import Widget
import subprocess
import re


class Clock(Widget):
    def on_mount(self):
        self.set_interval(1, self.refresh)
        pass

    def render(self):
        # time = datetime.now().strftime("%c")
        ps = subprocess.check_output("docker-compose --log-level ERROR ps".split())
        ps_lines = ps.split(b"\n")[2:-1]
        table = Table(title="Docker-Compose PS")
        table.add_column("Name")
        table.add_column("Command")
        table.add_column("State")
        table.add_column("Ports")
        for line in ps_lines:
            ls = re.split(b"\s\s+", line)[:-1]
            gg = []
            for i in ls:
                gg.append(i.decode("utf-8"))
            table.add_row(*gg)

        return table


class DockerComposeApp(App):
    def __init__(self, title: str, log: str = None, **kwargs):
        """Docker Compose TUI

        Args:
            title (str): Title of the application.
            log (str, optional): Name of the log file that the app will write to. Defaults to None.
            chicken_mode_enabled (bool, optional): Enable super special chicken mode. Defaults to False.
        """

        super().__init__(title=title, log=log, log_verbosity=1, **kwargs)

        self.current_node = "root"

    async def on_mount(self):
        await self.view.dock(Clock())


def run():
    DockerComposeApp.run(title="Docker Compose TUI")


if __name__ == "__main__":
    DockerComposeApp.run(title="Docker Compose TUI", log="textual.log")

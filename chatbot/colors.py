class Color:
    def __init__(self) -> None:
        self.RESET = "\033[0m"
        self.BOLD = "\033[1m"
        self.COLORS = {
            "red": "\033[91m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "green": "\033[92m",
        }

    def color(self, text: str, color_name: str, bold: bool = False) -> str:
        color_code = self.COLORS.get(color_name.lower(), "")
        bold_code = self.BOLD if bold else ""
        return f"{bold_code}{color_code}{text}{self.RESET}"

    def red(self, text: str, bold: bool = False) -> str:
        return self.color(text, "red", bold)

    def yellow(self, text: str, bold: bool = False) -> str:
        return self.color(text, "yellow", bold)

    def blue(self, text: str, bold: bool = False) -> str:
        return self.color(text, "blue", bold)

    def magenta(self, text: str, bold: bool = False) -> str:
        return self.color(text, "magenta", bold)

    def cyan(self, text: str, bold: bool = False) -> str:
        return self.color(text, "cyan", bold)

    def green(self, text: str, bold: bool = False) -> str:
        return self.color(text, "green", bold)

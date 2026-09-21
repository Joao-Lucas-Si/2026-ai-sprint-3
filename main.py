from io import StringIO
from subprocess import run
import sys
import time
from typing import TextIO

from textual.app import App, ComposeResult
from dotenv import load_dotenv
from src.screens.teste_tela import TesteTela
from src.screens.main_screen import TelaChat



class Aplicativo(App):
    SCREENS={"chat": TelaChat, "teste": TesteTela}
    
    def on_mount(self):
        if len(sys.argv) == 2 and sys.argv[1] == "--teste":
            self.push_screen("teste")
        elif len(sys.argv) > 1:
            raise Exception("parâmetros invalidos")
        else:
            self.push_screen("chat")
        self.theme = "catppuccin-mocha"
    # def compose(self) ->ComposeResult:
    #     yield

def main():
    try:
        app = Aplicativo()
        app.run()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    load_dotenv()
    
    main()
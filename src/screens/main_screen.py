from textual.app import ComposeResult, RenderResult
from textual.containers import (
    Container,
    Horizontal,
    ScrollableContainer,
    Vertical,
    VerticalScroll,
)
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import (
    Button,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    Static,
)

from src.ai.engine.ai_engine import AiEngine
from src.dados import Mensagem, MensagemChat, Papel
from src.ai.client.instancia import instanciarAi


def mensagem_chat(mensagem: MensagemChat):
    return Container(
        Container(
            Markdown(mensagem.conteudo),
            classes="mensagem-container mensagem-container-chat",
        ),
        classes="mensagem-chat",
    )


def mensagem_usuario(mensagem: Mensagem):
    return Container(
        Container(
            Markdown(mensagem.conteudo),
            classes="mensagem-container mensagem-container-usuario",
        ),
        classes="mensagem-usuario",
    )


class ChatMensagens(Widget):
    mensagens = reactive[list[Mensagem]]([])

    def __init__(
        self,
        mensagens: list[Mensagem],
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True
    ) -> None:
        super().__init__(
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )
        self.mensagens = mensagens

    def compose(self) -> ComposeResult:

        with Container():
            yield ScrollableContainer(
                *[
                    (
                        mensagem_chat(mensagem)
                        if isinstance(mensagem, MensagemChat)
                        else mensagem_usuario(mensagem)
                    )
                    for mensagem in self.mensagens
                ],
                id="mensagens-container",
                can_maximize=True,
            )
            with Horizontal(classes="input"):
                yield Input()
                yield Button("enviar")



class TelaChat(Screen):
    TITLE = "chat ai"
    CSS_PATH = "../../assets/css/styles.tcss"

    mensagem = reactive("")
    mensagens = reactive[list[Mensagem]]([])

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(ChatMensagens(self.mensagens), classes="chat-container")

    def on_button_pressed(self, mensagem: Button.Pressed) -> None:

        ai = AiEngine()

        # mensagens =
        # self.mensagens = self.mensagens
        resposta = ai.responder(self.mensagem)
        self.mensagens.append(Mensagem(self.mensagem, Papel.USUARIO))
        # # self.query_one("#debug", Label).content = resposta
        self.mensagens.append(MensagemChat(resposta, ""))
        self.query_one(ChatMensagens).mensagens = self.mensagens
        self.query_one(ChatMensagens).refresh(recompose=True)
        self.mensagem = ""
        self.query_one(Input).value = ""

    def on_input_changed(self, evento: Input.Changed) -> None:
        self.mensagem = evento.value
        # self.query_one("#debug", Label).content = self.mensagem

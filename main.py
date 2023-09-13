import random
import flet as ft
import os


class Message:
    def __init__(self, user: str, user_color: str, text: str, message_type: str):
        self.user_name = user
        self.user_color = user_color
        self.text = text
        self.message_type = message_type


def get_initials(user_name: str):
    return user_name[:1].capitalize()


"""
def get_avatar_color(user_name: str):
    colors_lookup = [
        ft.colors.AMBER,
        ft.colors.BLUE,
        ft.colors.BROWN,
        ft.colors.CYAN,
        ft.colors.GREEN,
        ft.colors.INDIGO,
        ft.colors.LIME,
        ft.colors.ORANGE,
        ft.colors.PINK,
        ft.colors.PURPLE,
        ft.colors.RED,
        ft.colors.TEAL,
        ft.colors.YELLOW,
    ]
    hashes = hash(user_name)
    color = hash(user_name) % len(colors_lookup)
    print(hashes, color, hashes % color)
    return colors_lookup[hash(user_name) % len(colors_lookup)]
"""


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.MainAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=message.user_color
                # bgcolor=get_avatar_color(message.user_name),

            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight=ft.FontWeight.BOLD),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            )
        ]


def main(page: ft.Page):
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    new_message = ft.TextField(
        hint_text="Escribe un mensaje,...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
    )

    def on_message(message: Message):
        m = ''
        if message.message_type == "chat_message":
            m = ChatMessage(message)
            # get_avatar_color(user_name.value)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    # Add new subscription to page, by session_id
    page.pubsub.subscribe(on_message)

    def login(e):
        page.update()
        login_button.visible = False

    def send_click(e):
        page.pubsub.send_all(Message(
            user=page.session.get('user_name'),
            user_color=page.session.get("user_color"),
            text=new_message.value,
            message_type='chat_message'
        ))
        new_message.value = ""
        new_message.focus()
        page.update()

    user_name = ft.TextField(label="Entra tu nombre")

    def join_click(e):
        if not user_name.value:
            user_name.error_text = "Debe aportar un nombre de usuario!"
            user_name.update()
        else:
            random_color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
            user_color = random_color
            page.session.set("user_name", user_name.value)
            page.session.set("user_color", user_color)
            page.dialog.open = False
            page.pubsub.send_all(
                Message(
                    user=user_name.value,
                    user_color=user_color,
                    text=f"{user_name.value} a entrado al chat.",
                    message_type="login_message"
                )
            )
            page.update()  # To init login at first

    login_button = ft.ElevatedButton("Login", on_click=login, autofocus=True)
    send_button = ft.IconButton(icon=ft.icons.SEND_ROUNDED, tooltip="Enviar", on_click=send_click)

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True
        )
        , login_button,
        ft.Row(
            [
                new_message,
                send_button
            ]
        )
    )

    # page.add(ft.Image(src="/assets/favicon.png"))

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Bienvenido!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Entra en el chat", on_click=join_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )


DEFAULT_FLET_PATH = ''  # or 'ui/path'
DEFAULT_FLET_PORT = 8501

if __name__ == "__main__":
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    ft.app(name=flet_path, target=main, view=None, assets_dir="assets", port=flet_port)

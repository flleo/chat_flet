import random
import flet as ft


class Message:
    def __init__(self, user: str, user_color: str, text: str, message_type: str):
        self.user = user
        self.user_color = user_color
        self.text = text
        self.message_type = message_type


def main(page: ft.Page):
    chat = ft.Column()
    new_message = ft.TextField()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            user = ft.TextSpan(message.user, ft.TextStyle(color=message.user_color))
            men = ft.TextSpan(": " + message.text)
            chat.controls.append(ft.Text(spans=[user, men]))
        elif message.message_type == "login_message":
            chat.controls.append(
                ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            )
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
    send_button = ft.ElevatedButton("Enviar", on_click=send_click, autofocus=True)

    page.add(
        chat, login_button, ft.Row([new_message, send_button])
    )

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Bienvenido!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Entra en el chat", on_click=join_click)],
        actions_alignment=ft.MainAxisAlignment.END
    )


ft.app(target=main, view=ft.AppView.WEB_BROWSER)

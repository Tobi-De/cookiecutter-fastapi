from __future__ import annotations


class Null:
    async def send_email(
        self,
        *,
        recipient: tuple[str, str | None],
        sender: tuple[str, str | None],
        subject: str,
        text: str | None = None,
        html: str | None = None,
    ):
        pass

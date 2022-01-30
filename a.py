from textual.app import App
from textual.widgets import ScrollView


class a(App):
    async def on_mount(self, _):
        x = ScrollView("a\nb\nc\n" * 50)
        await self.view.dock(x)

a().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window


class ScrollableText(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Create a ScrollView
        scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)

        # Create a Label with long text
        text = ""
        self.label = Label(
            text=text,
            font_size = 20,
            size_hint_y=None,
            text_size=(Window.width * 0.95, None),
            halign='left',
            valign='top',
            padding=(10, 10)
        )

        # Dynamically update label height based on text size
        self.label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        # Make text wrap dynamically when window resizes
        self.label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))

        # Add label into scrollview
        scroll_view.add_widget(self.label)

        # Add scrollview into main layout
        self.add_widget(scroll_view)


class ScrollTextApp(App):
    def build(self):
        return ScrollableText()


if __name__ == '__main__':
    ScrollTextApp().run()
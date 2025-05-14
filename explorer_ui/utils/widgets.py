from PySide6.QtWidgets import QWidget

class WidgetHandler:
    def __init__(self):
        self.buttons = {}

    def add_widget(self, widget: QWidget, can_replace: bool = False):
        """Adds a widget to the handler."""
        if widget.objectName() in self.buttons and not can_replace:
            raise ValueError('widget with name already exists')
        self.buttons[widget.objectName()] = widget

    def get_widget(self, name: str) -> QWidget:
        """Gets a widget by name."""
        return self.buttons.get(name)

    def remove_widget(self, name: str):
        """Removes a widget by name."""
        if name in self.buttons:
            del self.buttons[name]
        else:
            raise ValueError('widget with name does not exist')

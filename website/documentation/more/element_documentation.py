from nicegui import ui

from ..tools import text_demo


def main_demo() -> None:
    with ui.element('div').classes('p-2 bg-blue-100'):
        ui.label('inside a colored div')


def more() -> None:
    @text_demo('Move elements', '''
        This demo shows how to move elements between or within containers.
    ''')
    def move_elements() -> None:
        with ui.card() as a:
            ui.label('A')
            x = ui.label('X')

        with ui.card() as b:
            ui.label('B')

        ui.button('Move X to A', on_click=lambda: x.move(a))
        ui.button('Move X to B', on_click=lambda: x.move(b))
        ui.button('Move X to top', on_click=lambda: x.move(target_index=0))

    @text_demo('Default props', '''
        You can set default props for all elements of a certain class.
        This way you can avoid repeating the same props over and over again.
        
        Default props only apply to elements created after the default props were set.
        Subclasses inherit the default props of their parent class.
    ''')
    def default_props() -> None:
        ui.button.default_props('rounded outline')
        ui.button('Button A')
        ui.button('Button B')
        # END OF DEMO
        ui.button.default_props(remove='rounded outline')

    @text_demo('Default classes', '''
        You can set default classes for all elements of a certain class.
        This way you can avoid repeating the same classes over and over again.
        
        Default classes only apply to elements created after the default classes were set.
        Subclasses inherit the default classes of their parent class.
    ''')
    def default_classes() -> None:
        ui.label.default_classes('bg-blue-100 p-2')
        ui.label('Label A')
        ui.label('Label B')
        # END OF DEMO
        ui.label.default_classes(remove='bg-blue-100 p-2')

    @text_demo('Default style', '''
        You can set a default style for all elements of a certain class.
        This way you can avoid repeating the same style over and over again.
        
        A default style only applies to elements created after the default style was set.
        Subclasses inherit the default style of their parent class.
    ''')
    def default_style() -> None:
        ui.label.default_style('color: tomato')
        ui.label('Label A')
        ui.label('Label B')
        # END OF DEMO
        ui.label.default_style(remove='color: tomato')

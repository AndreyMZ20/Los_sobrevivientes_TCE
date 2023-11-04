from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.navigationdrawer import NavigationDrawer

class MyApp(App):
    def build(self):
        # Crear el NavigationDrawer
        navigationdrawer = NavigationDrawer()

        # Crear el menú principal
        main_menu = BoxLayout(orientation='vertical')
        modulacion_button = Button(text='Modulación',
                                   size_hint_y=None,
                                   height=40)
        modulacion_button.bind(on_press=self.show_modulacion_options)
        main_menu.add_widget(modulacion_button)
        main_menu.add_widget(Button(text='Demodulación',
                                    on_press=self.toggle_nav_drawer,
                                    size_hint_y=None,
                                    height=40))

        # Crear las opciones de 'Modulación'
        self.modulacion_options = BoxLayout(orientation='vertical', size_hint_y=None)
        self.modulacion_options.add_widget(Button(text='Opción 1',
                                                  size_hint_y=None,
                                                  height=40))
        self.modulacion_options.add_widget(Button(text='Opción 2',
                                                  size_hint_y=None,
                                                  height=40))
        self.modulacion_options.add_widget(Button(text='Opción 3',
                                                  size_hint_y=None,
                                                  height=40))
        self.modulacion_options.height = 0  # Inicialmente oculto

        # Añadir el menú principal y las opciones de 'Modulación' a un BoxLayout
        menu_layout = BoxLayout(orientation='vertical')
        menu_layout.add_widget(main_menu)
        menu_layout.add_widget(self.modulacion_options)

        # Añadir el BoxLayout al NavigationDrawer
        navigationdrawer.add_widget(menu_layout)

        # Crear el área de contenido
        content_area = BoxLayout(orientation='vertical')
        content_area.add_widget(Button(text='Contenido',
                                       on_press=self.toggle_nav_drawer,
                                       size_hint_y=None,
                                       height=40))

        # Añadir el área de contenido al NavigationDrawer
        navigationdrawer.add_widget(content_area)

        # Establecer el área de contenido como el panel principal
        navigationdrawer.anim_type = 'slide_above_anim'

        return navigationdrawer

    def toggle_nav_drawer(self, instance):
        # Alternar la apertura/cierre del NavigationDrawer
        self.root.toggle_state()

    def show_modulacion_options(self, instance):
        # Mostrar/ocultar las opciones de 'Modulación'
        if self.modulacion_options.height == 0:
            self.modulacion_options.height = 80  # Mostrar
        else:
            self.modulacion_options.height = 0  # Ocultar

MyApp().run()

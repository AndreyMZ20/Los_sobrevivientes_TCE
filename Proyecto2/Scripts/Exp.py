from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from matplotlib.figure import Figure
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.button = Button(text='Abrir segunda ventana')
        self.button.bind(on_release=self.change_to_second)
        self.layout.add_widget(self.button)
        self.add_widget(self.layout)

    def change_to_second(self, value):
        self.manager.current = 'second'

class SecondWindow(Screen):
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal')
        
        # Columna izquierda
        self.scrollview_left = ScrollView()
        self.boxlayout_left = BoxLayout(orientation='vertical', size_hint_y=None)
        self.boxlayout_left.bind(minimum_height=self.boxlayout_left.setter('height'))

        # Columna derecha
        self.scrollview_right = ScrollView()
        self.boxlayout_right = BoxLayout(orientation='vertical', size_hint_y=None)
        self.boxlayout_right.bind(minimum_height=self.boxlayout_right.setter('height'))

        # Agregar gráficas de matplotlib a la columna izquierda
        for i in range(2):
            fig, ax = plt.subplots()
            t = np.arange(0.0, 2.0, 0.01)
            s = 1 + np.sin(2 * np.pi * t)
            ax.plot(t, s)

            self.boxlayout_left.add_widget(FigureCanvasKivyAgg(fig))

        # Agregar gráficas de matplotlib a la columna derecha
        for i in range(2):
            fig, ax = plt.subplots()
            t = np.arange(0.0, 2.0, 0.01)
            s = 1 + np.sin(2 * np.pi * t)
            ax.plot(t, s)

            self.boxlayout_right.add_widget(FigureCanvasKivyAgg(fig))

        # Agregar las columnas al layout principal
        self.scrollview_left.add_widget(self.boxlayout_left)
        self.scrollview_right.add_widget(self.boxlayout_right)
        
        self.layout.add_widget(self.scrollview_left)
        self.layout.add_widget(self.scrollview_right)

        self.add_widget(self.layout)

class TestApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainWindow(name="main"))
        screen_manager.add_widget(SecondWindow(name="second"))
        return screen_manager

TestApp().run()

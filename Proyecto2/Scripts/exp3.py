from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from matplotlib.figure import Figure
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FC
from kivy.garden.matplotlib.backend_kivyagg import NavigationToolbar2Kivy as NT

class MyApp(App):
    def build(self):
        box = BoxLayout(orientation='vertical')
        
        # Crea una figura y agrega un subplot
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5])
        
        # Crea un canvas y añádelo a la BoxLayout
        canvas = FC(fig)
        box.add_widget(canvas)
        
        # Crea la barra de herramientas y añádela a la BoxLayout
        toolbar = NT(canvas, pack_toolbar=False)
        box.add_widget(toolbar.actionbar)
        
        return box

MyApp().run()

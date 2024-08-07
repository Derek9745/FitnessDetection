from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase


class Panda3DApp(ShowBase):
    def __init__(self,parent):
        super().__init__()  # This calls the __init__ method of ShowBase

        # Set up Panda3D window properties
        props = WindowProperties()
        props.set_origin(0, 0)
        props.set_size(640, 480)
        props.set_parent_window(parent.winfo_id())

        self.win.request_properties(props)
        self.disable_mouse()    

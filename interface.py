

from __future__ import print_function
from __future__ import division

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui


#update = None


_app = None
_update_timer = None
_ptree = None
_params = None #
_params_target_obj = None

_window_view = None
_window_layout = None
_window_imgs = []
_window_stats_label = None

_windows = []



def screen_size():
    return _app.desktop().screenGeometry()
    
    

def init_app():
    global _app
    print('gui | Initializing QApplication')
    _app = QtGui.QApplication([])

    
    
def process_events():
    if _app != None:
        _app.processEvents()



def toggle_param(p):
    p.setValue( not p.value() )



# reading & writing to pyqtgraph.parametertree seems to be slow,
# so going to cache in an object for direct access

def _add_image_to_layout(layout, row=None, col=None, rowspan=1, colspan=1, title=''):
    i = pg.ImageItem(border='w')
    i.setOpts(axisOrder='row-major')
    
    l = layout.addLayout()
    l.addLabel(title)
    l.nextRow()

    v = l.addViewBox(lockAspect=True, invertY=True, row=row, col=col, rowspan=rowspan, colspan=colspan)
    v.addItem(i)
    return {'img':i, 'view':v, 'layout':l}
    


def init_window(x=0, y=0, w=500, h=300, title='NightfallProject'):
    global _window_view, _window_layout, _window_imgs, _window_stats_label, _windows
    view = pg.GraphicsView()
    layout = pg.GraphicsLayout(border=(100,100,100))
    view.setCentralItem(layout)
    view.setWindowTitle(title)
    view.setGeometry(x, y, w, h)
    view.show()
    
    imgs = []
    imgs.append( _add_image_to_layout(layout, title='DAY') )
    imgs.append( _add_image_to_layout(layout, title='NIGHT') )
    
    layout.nextRow()

    stats_label = pg.LabelItem()
    layout.addItem(stats_label, colspan=3)
    
    _window_view = view
    _window_layout = layout
    _window_imgs = imgs
    _window_stats_label = stats_label
    
    _windows.append(view)
    


def update_image(index, img_data, enabled=True):
    if enabled:
        _window_imgs[index]['img'].setImage(img_data)
    else:
        _window_imgs[index]['img'].clear()
        
        

def close():
    global _app, _update_timer, _windows
    _update_timer = None
    _app.closeAllWindows()
    for w in _windows:
        w.close()

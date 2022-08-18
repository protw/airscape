# Holoviews produces content to be rendered in a web browser and Spyder 
# consoles are not able to display that content at the moment.
# Therefore Maxime Beau designed a snippet to render Holoviews plot in Spyder
# See: "Why doesn't holoviews show histogram in Spyder?"
# https://stackoverflow.com/a/61975403

import matplotlib.pyplot as plt
import bokeh as bk
import holoviews as hv

def mplshow(fig):

    # create a dummy figure and use its
    # manager to display "fig"

    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)

def bkshow(bkfig, title=None, save=0, savePath='~/Downloads'):
    if title is None: title=bkfig.__repr__()
    if save:bk.plotting.output_file(f'{title}.html')
    bk.plotting.show(bkfig)

def hvshow(hvobject, backend='matplotlib', return_mpl=True):
    '''
    Holoview utility which
    - for dynamic display, interaction and data exploration:
        in browser, pops up a holoview object as a bokeh figure
    - for static instanciation, refinement and data exploitation:
        in matplotlib current backend, pops up a holoview object as a matplotlib figure
        and eventually returns it for further tweaking.
    Parameters:
        - hvobject: a Holoviews object e.g. Element, Overlay or Layout.
        - backend: 'bokeh' or 'matplotlib', which backend to use to show figure
        - return_mpl: bool, returns a matplotlib figure
        
    '''
    assert backend in ['bokeh', 'matplotlib']
    if backend=='matplotlib' or return_mpl:
        mplfig=hv.render(hvobject, backend='matplotlib')
    if backend=='bokeh': bkshow(hv.render(hvobject, backend='bokeh'))
    elif backend=='matplotlib': mplshow(mplfig)
    if return_mpl: return mplfig
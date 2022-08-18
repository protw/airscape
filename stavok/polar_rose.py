# # Будуємо "полярну розу"
# 
# Спочатку імпортуємо та ініціалізуємо потрібні модулі:

import numpy as np, holoviews as hv, panel as pn
from holoviews import opts

hv.extension('matplotlib')
pn.extension()

# Формуємо дані за формулою полярної рози: $r(\phi) = a \cos (k \phi + \theta_0)$, де $k$ — кількіст пелюстків (див. [статтю](https://uk.wikipedia.org/wiki/Полярна_система_координат#Полярна_роза)).

phi = np.linspace(0, np.pi*2, 400)

def polar_rose(phi, a=1, k=6, theta0=np.pi/6):
    return a*np.cos(k*phi + theta0)

# Створюємо слайдер параметру $k$:

k_slider = pn.widgets.FloatSlider(name='K slider', start=1, end=8, step=0.1, value=6)

# Компонуємо інтерактивну візуалізацію

@pn.depends(k_slider.param.value)
def rose_viz(k):
    r = polar_rose(phi, k=k)
    rose = hv.Curve((phi, r),'$\phi$','r').opts(projection='polar', show_grid=True)
    return rose

# Будуємо інтерактивне відображення 

hv.extension('matplotlib') # Цей рядок потрібен для відображення у Colab

pn.Column(k_slider,rose_viz)





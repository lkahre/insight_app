def make_plot(probs):
    import matplotlib.pyplot as plt
    import numpy as np
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components
    from io import StringIO
    import base64
    
    plot = figure(x_range=probs['Month'], y_range=(0,100))
    plot.xaxis.axis_label = 'Month'
    plot.yaxis.axis_label = '% Chance of Acceptance'
    plot.line(probs['Month'], probs['Probability'])
    script, div = components(plot)
    print(script)
    print(div)
    return script, div
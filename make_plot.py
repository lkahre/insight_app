def make_plot(probs):
    import matplotlib.pyplot as plt
    import numpy as np
    import datetime as dt
    import pandas as pd
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components
    from io import StringIO
    import base64
    
    months_list = []
    for i in range(1, 13):
        months_list.append(dt.date(2008, i, 1).strftime('%b'))

    month_df = pd.DataFrame({'Month': months_list})
    print(month_df)
    
    plot = figure(x_range=month_df['Month'], y_range=(0,105))
    plot.xaxis.axis_label = 'Month'
    plot.xaxis.axis_label_text_font = 'helvetica'
    plot.xaxis.axis_label_text_font_size = '14pt'
    plot.xaxis.axis_label_text_font_style = 'bold'
    plot.xaxis.major_label_text_font_size = '14pt'
    plot.xgrid.grid_line_color = 'LightGrey'
    plot.yaxis.axis_label = '% Chance of Acceptance'
    plot.yaxis.axis_label_text_font = 'helvetica'
    plot.yaxis.axis_label_text_font_size = '14pt'
    plot.yaxis.axis_label_text_font_style = 'bold'
    plot.yaxis.major_label_text_font_size = '14pt'
    plot.ygrid.grid_line_color = 'LightGrey'
    #plot.plot_width=500 
    plot.plot_height=400
    plot.line(month_df['Month'], probs['Percent Chance'], line_width=3, line_cap='round')
    script, div = components(plot)
    print(script)
    print(div)
    return script, div
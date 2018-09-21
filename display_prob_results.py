def display_prob_results(prob_results):
    import numpy as np
    import pandas as pd
    import math
    import matplotlib.pyplot as plt
    from IPython.display import display, HTML
    %matplotlib inline 
    
    months_list = []
    for i in range(1, 13):
        months_list.append(datetime.date(2008, i, 1).strftime('%b'))

    prob_accept_percent = np.around(prob_accept*100, decimals=2)

    result_df = pd.DataFrame({'Month': months_list, 'Probability': prob_accept_percent})

    display(result_df.nlargest(3, 'Probability'))

    fig = plt.figure(figsize=(9.8,5), dpi=100)
    xaxis_loc = np.arange(12)
    fig.patch.set_facecolor('w')
    plt.plot(xaxis_loc, prob_accept_percent)
    plt.ylim([0, 100])
    plt.xticks(xaxis_loc, months_list)
    plt.xlabel('Month')
    plt.ylabel('% Chance of Acceptance')
    plt.title('Visa Chance of Acceptance by Month')
    plt.savefig('Prob_Accept_bymonth')
    plt.show()
    return
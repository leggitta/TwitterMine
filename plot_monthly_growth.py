from matplotlib import rcParams
rcParams['font.family'] = 'monospace'
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle


def plot_growth(tweets):
    # compute time and user
    tweets['created_at'] = pd.to_datetime(tweets['created_at'])
    tweets['year'] = tweets.created_at.dt.year
    tweets['month'] = tweets.created_at.dt.month
    tweets['user_id'] = tweets['user'].apply(lambda x: x['id'])

    # create figure
    fig, ax = plt.subplots(figsize=(20, 7))
    alpha = 0.4
    
    # group data by year and month
    monthly_activity = []
    for (y, m), data in tweets.groupby(('year', 'month')):
        t = y + m / 12.
        w = 1./12
        favorites_ = ax.bar(t, data.favorite_count.sum(), w, color='r', alpha=alpha)
        tweets_ = ax.bar(t, len(data), w, color='b', alpha=alpha)
        retweets_ = ax.bar(t, data.retweet_count.sum(), w, color='g', alpha=alpha)
        users_ = ax.bar(t, len(data.user_id.unique()), w, color='k', alpha=alpha)

        monthly_activity.append({
            't': t, 'favorites': data.favorite_count.sum(), 'tweets': len(data),
            'retweets': data.retweet_count.sum(), 'users': len(data.user_id.unique())
        })
    # convert to data frame
    monthly_activity = pd.DataFrame(monthly_activity)    

    # normalize time for curve fitting
    x = monthly_activity.index.values
    t = monthly_activity['t'].values
    dt = np.diff(t)[0]
    tnorm = np.r_[0, t - (t.min() - dt)]

    # plot growth curves
    handles, labels = [], []
    colors = ['r', 'b', 'g', 'k']
    for i, k in enumerate(('favorites', 'tweets', 'retweets', 'users')):
        y = monthly_activity[k].values

        m = np.linalg.lstsq(tnorm[:, None], np.r_[0, y][:, None], rcond=None)[0][0][0]
        yfit = tnorm[1:] * m

        line, = ax.plot(t, yfit, '-', lw=4, color=colors[i])
        handles.append(line)

        xnorm = np.r_[0, x]
        growth = np.linalg.lstsq(xnorm[:, None], np.r_[0, y][:, None], rcond=None)[0][0][0]

        label = '%s +%d/mo' % (k, growth)
        n_pad = 20 - len(label)
        label = label.split(' ')[0] + '.'*n_pad + label.split(' ')[-1]
        labels.append(label)

    ax.legend(handles, labels, fontsize=15, loc=4)
    ax.tick_params(labelsize=15)
    ax.set_title('Monthly Growth', fontsize=20)
    ax.set_xlim(t.min()-dt, t.max()+dt)

    plt.yscale('log')
    ax.set_yticks([10, 100, 1000])
    ax.set_yticklabels([10, 100, 1000])
    fig.savefig('monthly_growth.png')


if __name__ == "__main__":
    with open('shipwreck_cleaned.pkl', 'rb') as fid:
        tweets = pickle.load(fid)
    plot_growth(tweets)
    plt.show()
    plt.close('all')
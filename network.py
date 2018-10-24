import networkx as nx
import pickle


def gen_tag_network(tweets, outfile='tag_network.pkl'):
    G = nx.Graph()  # undirected graph to store tags
    
    # extract tags
    tweets['tags'] = tweets['entities'].apply(lambda x: [t['text'].lower() for t in x['hashtags']])
    
    # loop through tweets
    for i, tweet in tweets.iterrows():
        tags = tweet['tags']
        n_tags = len(tags)

        # update tag counts
        for tag in tags:
            if not tag in G.nodes:
                G.add_node(tag, weight=1)
            else:
                G.node[tag]['weight'] += 1

        # update edges
        for i in range(n_tags):
            t1 = tags[i]
            for j in range(i+1, n_tags):
                t2 = tags[j]
                if G.has_edge(t1, t2):
                    G[t1][t2]['weight'] += 1
                else:
                    G.add_edge(t1, t2, weight=1)
    # save
    with open(outfile, 'wb') as fout:
        pickle.dump(G, fout)
    return G

def gen_word_network(tweets, outfile='word_network.pkl'):
    H = nx.Graph()  # undirected graph to store words
    for i, tweet in tweets.iterrows():
        if type(tweet['extended_tweet']) != dict:
            text = tweet['text']
        else:
            text = tweet['extended_tweet']['full_text']

        words = text.split(' ')
        words = [w.rstrip('.').rstrip(',').rstrip('?').rstrip('!').rstrip(':').lower() for w in words]
        n_words = len(words)

        # update word counts
        for word in words:
            if not word in H.nodes:
                H.add_node(word, weight=1)
            else:
                H.node[word]['weight'] += 1

        # update edges
        for i in range(n_words):
            w1 = words[i]
            for j in range(i+1, n_words):
                w2 = words[j]
                if H.has_edge(w1, w2):
                    H[w1][w2]['weight'] += 1
                else:
                    H.add_edge(w1, w2, weight=1)

    # save
    with open(outfile, 'wb') as fout:
        pickle.dump(H, fout)
    return H


if __name__ == "__main__":
    with open('shipwreck_cleaned.pkl', 'rb') as fid:
        tweets = pickle.load(fid)
    tag_network = gen_tag_network(tweets)
    word_network = gen_word_network(tweets)
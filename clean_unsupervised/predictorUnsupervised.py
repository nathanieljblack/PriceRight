import pandas as pd
import re
from unicodedata import category as cat
from nltk.corpus import stopwords
from gensim import corpora, models
import operator
from collections import OrderedDict
import scipy
from scipy.cluster.vq import kmeans, vq


class Predictor(): # Note: This predictor trains the model and runs the model on the same data set

    def __init__(self, list):
        """
        :param list: a list of dictionaries as read in from a json file
        """
        self.data = pd.DataFrame(list)

    def regularize_training_corpus(self):

        def clean_titles(title):
            if re.search('(wtb|wanted|want|purchase|repair|buy|need|trade|replacement| \
                           looking|fix|cash|me|pawn|wtt|trading)', title, re.IGNORECASE):
                out = "exclude" # common non-sales words

            elif re.search('(ipad|ipod)', title, re.IGNORECASE):
                out = "exclude" # common iPhone related items for sale

            else:
                out = "OK"

            return out

        print "\nRegularizing titles ..."
        self.data['status'] = self.data.title.apply(clean_titles)
        self.data = self.data[self.data.status != 'exclude']

        return self.data

    def tokenize_training_corpus(self):

        stoplist = stopwords.words('english')

        sales_words = ['like', 'new', 'brand', 'excellent', 'condition', 'pristine', 'never', 'used', 'clean',
                       'perfect', 'great', 'sale', 'sell', 'selling', 'good', 'obo', 'warranty', 'cl', 'color',
                       'works', 'extras', 'open', 'flawless', 'bad', 'guaranteed', 'working', 'unopened'
                       ] # common sales words

        iphone_words = ['iphone', 'apple', 'icloud', 'contract', 'iphones',
                        'carrier', 'verizon', 'tmobile', 'att', 'metropcs', 'sprint', 'cricket',
                        'wireless', 'mobile', 'phone', 'smartphone', 'unlocked', 'unlock', 'locked', 'lock', 'factory',
                        'box', 'sealed', 'gsm', 'esn', '4g', 'imei', 'international', 'cracked', 'screen', 'charger',
                        '8', '16', '32', '64', '128',
                        'g', '8g', '16g', '32g', '64g', '128g',
                        'gb', '8gb', '16gb', '32gb', '64gb', '128gb',
                        'gig', '8gig', '16gig', '32gig', '64gig','128gig',
                        'gigs', '8gigs', '16gigs', '32gigs', '64gigs','128gigs',
                        'white', 'black', 'gray', 'grey', 'spacegray', 'spacegrey', 'space', 'pink', 'mint',
                        'gold', 'silver', 'blue', 'yellow', 'green', 'pink', 'whitesilver', 'blackgray', 'slate',
                        'whitegold'
                        ] # words that will appear across all iphone brands (4, 4s, 5, 5c, 5s, 6, 6+)

        custom_stoplist = sales_words + iphone_words

        # Tokenize titles
        def create_tokens(title):
            out = []
            for word in title.lower().split():
                out.append(word)
            return out

        # Remove punctuation
        def strip_punctuation(token):
            out = []
            for word in token:
                if __name__ == "__main__":
                    new_word = "".join(char for char in word if not cat(char).startswith('P'))
                else:
                    new_word = "".join(char for char in word.decode('utf-8') if not cat(char).startswith('P'))
                out.append(new_word)
            return out

        # Remove common words
        def remove_common_words(token):
            out = []
            for word in token:
                if word not in stoplist and word not in custom_stoplist and word != '':
                    out.append(word)
            return out

        # Remove words that appear only once
        def remove_once_words(token):
            out = []
            for word in token:
                if word not in tokens_once:
                    out.append(word)
            return out

        # Exclude postings whose tokens are empty
        def remove_empty_tokens(token):
            if token:
                out = "OK"
            else:
                out = "exclude"
            return out

        def cheat_replace(title):
            newtitle = title.replace('6 plus', '6+') # Cheat
            newtitle = newtitle.replace('6 Plus', '6+') # Cheat
            newtitle = newtitle.replace('6 PLUS', '6+') # Cheat
            newtitle = newtitle.replace('6plus', '6+')  # Cheat
            newtitle = newtitle.replace('6Plus', '6+')  # Cheat
            newtitle = newtitle.replace('6PLUS', '6+')  # Cheat

            return newtitle

        print "Preparing Training Corpus ..."

        print "     Cheating ..."
        self.data.title = self.data.title.apply(cheat_replace)

        print "     Creating tokens ..."
        self.data['tokens'] = self.data.title.apply(create_tokens)

        print "     Removing punctuation ..."
        self.data.tokens = self.data.tokens.apply(strip_punctuation)

        print "     Removing common words ..."
        self.data.tokens = self.data.tokens.apply(remove_common_words)

        print "     Removing words that appear only once ..."
        all_tokens = sum(self.data.tokens, [])
        tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
        self.data.tokens = self.data.tokens.apply(remove_once_words)

        print "     Removing empty tokens ..."
        self.data.status = self.data.tokens.apply(remove_empty_tokens)
        self.data = self.data[self.data.status != 'exclude']

        return self.data

    def train_model(self, numTopics):

        # Create training dictionary
        def create_dictionary(training_data):
            dictionary = corpora.Dictionary(training_data)
            dictionary.save('training_dictionary.dict')  # store to disk, for later use
            return 'training_dictionary.dict'

        # Turn training corpus into sparse Bag of Words vectors
        def corpus_to_bag_of_words(training_dict, training_data):
            training_corpus_bow = [training_dict.doc2bow(token) for token in training_data]
            corpora.MmCorpus.serialize('training_corpus.mm', training_corpus_bow)  # store to disk, for later use
            return 'training_corpus.mm'

        # Train TF-IDF model
        def corpus_to_tfidf(training_corp):
            tfidf_model = models.TfidfModel(training_corp)
            corpus_tfidf = tfidf_model[training_corp]
            return corpus_tfidf, tfidf_model

        # Train LSI model
        def corpus_to_lsi(dict, corpus, topics):
            lsi_model = models.LsiModel(corpus, id2word=dict, num_topics=topics) # initialize an LSI transformation
            topicWordProbMat = lsi_model.print_topics(topics)
            return lsi_model, topicWordProbMat

        def create_topic_dict(topic_words):

            def create_tokens(topic):
                out = []
                for word in topic.lower().split():
                    out.append(word)
                return out

            topics_list = []
            for topic in topic_words:
                topic_wds = []
                topic = topic.replace(' + ', ' ')
                topic = topic.replace('*', ' ')
                topic = topic.replace('"', '')
                topic_tokens = create_tokens(topic)
                for i in range(1, len(topic_tokens)/2):
                    pair = (float(topic_tokens[2*i-2]), topic_tokens[2*i-1],)
                    topic_wds.append(pair)
                topics_list.append(topic_wds)

            for i in range(len(topics_list)):
                topics_list[i] = sorted(topics_list[i], key=operator.itemgetter(0))

            topics_dict = OrderedDict()
            i = 0
            for topic in topics_list:
                topics_dict[i] = dict(enumerate(topic))
                i += 1

            return topics_dict

        print "Training model ..."

        print "     Creating training dictionary ..."
        training_dictionary_file = create_dictionary(self.data.tokens)

        training_dictionary = corpora.Dictionary.load(training_dictionary_file)

        print "     Transforming training corpus into bag-of-words vectors..."
        training_corpus_file = corpus_to_bag_of_words(training_dictionary, self.data.tokens)

        training_corpus = corpora.MmCorpus(training_corpus_file)

        print "     Creating TF-IDF vectors ..."
        corpus_tfidf, tfidf_model = corpus_to_tfidf (training_corpus)

        print "     Training LSI model using " + str(numTopics) + " topics ..."
        lsi_model, topic_words = corpus_to_lsi(training_dictionary, corpus_tfidf, numTopics)

        print "     Creating topic dictionary ..."
        topics_dict = create_topic_dict(topic_words)

        return self.data, training_dictionary, tfidf_model, lsi_model, topics_dict

    def run_model(self, training_dictionary, tfidf_model, lsi_model, num_topics, num_clusters):

        # Create LSI vectors for Clustering
        def create_lsi_vectors(token, dict, tfidf_model, lsi_model):
            vec_bow = dict.doc2bow(token)
            vec_tfidf = tfidf_model[vec_bow] # convert the token to TF-IDF space
            vec_lsi = lsi_model[vec_tfidf]   # convert the token to LSI space
            return vec_lsi

        # Clean LSI vectors
        def clean_lsi_vectors(lsi_vectors, tops):

            # Remove vectors if they have less than numTopics elements
            def remove_short_vectors(vec):
                if len(vec) < tops:
                    out = "exclude"
                else:
                    out = "OK"
                return out

            # Check that LSI model created vectors of proper length
            print "          Checking for short LSI vectors ..."

            minLength = tops + 100
            maxLength = 0
            numTooSmall = 0

            for vector in lsi_vectors:
                if len(vector) < minLength:
                    minLength = len(vector)
                if len(vector) > maxLength:
                    maxLength = len(vector)
                if len(vector) < tops:
                    numTooSmall +=1

            print ("               MinLength = " + str(minLength) +"\n               MaxLength = " + str(maxLength))

            if numTooSmall > 0:  # if lsi model fails, remove short vectors
                print "               After running the LSI model, " + str(numTooSmall) + " vectors were too short."
                print "          Removing short LSI vectors ..."
                self.data.status = self.data.lsiVectors.apply(remove_short_vectors)
                self.data = self.data[self.data.status != 'exclude']

            return self.data

        def cluster(numClusters):

            # Prep LSI vectors for clustering
            self.data.clusterVectors = [[x[1] for x in vector] for vector in self.data.lsiVectors]
            self.data.lsiArray = scipy.array(self.data.clusterVectors)

            # Compute K-Means
            print "          Running K-Means clustering with " + str(numClusters) + " clusters ..."
            centroids, _ = kmeans(self.data.lsiArray, numClusters)

            # Assign each title to a cluster
            print "          Assigning postings to their clusters ..."
            self.data['pred_bin'], _ = vq(self.data.lsiArray,centroids)

            # Save centroids
            print "          Saving centroids ..."
            centroids_list = centroids.tolist()

            centroids_dict = OrderedDict()
            i = 0
            for centroid in centroids_list:
                centroids_dict[i] = dict(enumerate(centroid))
                i += 1

            for i in range(len(centroids_list)):
                centroids_dict[i] = sorted(centroids_dict[i].items(), key=operator.itemgetter(1))

            return self.data, centroids_dict

        print"Running model ..."

        print "     Creating LSI vectors for clustering ..."
        self.data['lsiVectors'] = self.data.tokens.apply(create_lsi_vectors,
                                                         args=(training_dictionary, tfidf_model, lsi_model))
        print "     Cleaning LSI vectors ..."
        self.data = clean_lsi_vectors(self.data.lsiVectors, num_topics)

        print"     Clustering postings ..."
        self.data, centroids = cluster(num_clusters)

        return self.data, centroids

    # Create predictions based on the model
    def predict(self, numTopics, numClusters):
        self.data = self.regularize_training_corpus()
        self.data = self.tokenize_training_corpus()
        self.data, training_dictionary, tfidf_model, lsi_model, topics_dict = self.train_model(numTopics)
        self.data, centroids = self.run_model(training_dictionary, tfidf_model, lsi_model, numTopics, numClusters)
        self.data = self.data.drop(['status', 'lsiVectors'], axis=1) # keep tokens for now

        return self.data, topics_dict, centroids
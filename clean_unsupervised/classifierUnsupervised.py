from collections import OrderedDict


class Classifier():
    """ Use topics and centroids to classify postings """

    def get_topics(self, topics_dict):
        # Get the words out of the topics dictionary

        topics = OrderedDict()
        for key, value in topics_dict.iteritems():
            if abs(value[0][0]) > abs(value[8][0]):
                topics[key] = value[0][1]
            else:
                topics[key] = value[8][1]

        return topics

    def get_centroids_topics(self, centroids_dict):
        # Get the topics from the centroid dictionary

        centroid_topics = OrderedDict()
        for key, value in centroids_dict.iteritems():
            if abs(value[0][1]) > abs(value[-1][1]):
                centroid_topics[key] = value[0][0]
            else:
                centroid_topics[key] = value[-1][0]
        return centroid_topics

    def get_centroid_word(self, cluster, topics_final, centroid_topics_final):
        # Match the topic words to the centroids topic

        cluster_topic_num = centroid_topics_final[cluster]
        cluster_topic = topics_final[cluster_topic_num]
        predicted_class = cluster_topic

        return predicted_class

    def clean_pred_class(self, pclass):
        # Clean out items whose predicted class does not fall in 4/4s/5/5c/5s/6/6+

        if pclass == '4':
            out = "OK"
        elif pclass == '4s':
            out = "OK"
        elif pclass == '5':
            out = "OK"
        elif pclass == '5c':
            out = "OK"
        elif pclass == '5s':
            out = "OK"
        elif pclass == '6':
            out = "OK"
        elif pclass == '6+':
            out = "OK"
        else:
            out = "exclude"
        return out

    def classify(self, dataframe, topics, centroids):

        def cheat_replace(pclass, tokens_list):
            if pclass == '4' and not (u'4' in tokens_list):
                out = "exclude"
            elif pclass == '4s' and not (u'4s' in tokens_list):
                out = "exclude"
            elif pclass == '5' and not (u'5' in tokens_list):
                out = "exclude"
            elif pclass == '5c' and not (u'5c' in tokens_list):
                out = "exclude"
            elif pclass == '5s' and not (u'5s' in tokens_list):
                out = "exclude"
            elif pclass == '6' and not (u'6' in tokens_list):
                out = "exclude"
            elif pclass == '6+' and not (u'6+' in tokens_list):
                out = "exclude"
            else:
                out = "OK"
            return out

        topics_final = self.get_topics(topics)
        centroid_topics_final = self.get_centroids_topics(centroids)
        dataframe['pred_class'] = dataframe.pred_bin.apply(self.get_centroid_word, args=(topics_final,
                                                                                        centroid_topics_final))
        dataframe['status'] = dataframe.pred_class.apply(self.clean_pred_class)
        dataframe = dataframe[dataframe.status != 'exclude']
        dataframe = dataframe.drop(['status'], axis=1)

        print "     Cheating again ..."
        dataframe["status"] = dataframe.apply(lambda row: cheat_replace(row["pred_class"], row["tokens"]), axis=1)
        dataframe = dataframe[dataframe['status'] != 'exclude']

        return dataframe.drop(["tokens", "status"], axis=1)
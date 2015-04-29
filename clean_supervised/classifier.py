import pandas as pd
import string
import re

class Classifier():
    """use regular expressions to classify the iphones categories """

    def classify(self, df):
        """
        :param: data frame to be categorized
        :return: data frame with the classification
        """

        #strip out the punctuation
        df['stripped_title'] = df['title'].apply(func = self.strip_punc)

        #strip out the stop words
        df['stripped_title'] = df['stripped_title'].apply(func = self.remove_memwords)
        

        #regular expression matching
        df['pred_class'] = df['stripped_title'].apply(func = self.cat_match)
        df['pred_class'].where(df['pred_bin'] == 1, df['pred_bin'], inplace = True)
        df['pred_class'] = df['pred_class'].astype(str)
        df = df[df.pred_class != '-1']
        df.drop('stripped_title', 1, inplace=True)
        return df

    def cat_match(self, text):
        if re.search('(WTB|want|repair|fix|buy|need|otterbox|lifeproof|trad|case|otter|replacement|reparacion|olloclip|mophie|booster|compatible)', text, re.IGNORECASE):
            out = '-1'
        elif re.search('(plus|6\+|6.\+)', text, re.IGNORECASE):
            out = '6+'
        elif re.search('(six|6)', text, re.IGNORECASE):
            out =  '6'
        elif re.search('(five|5)', text, re.IGNORECASE):
            if re.search('(5c|5.c|five.c)', text, re.IGNORECASE):
                out = '5c'
            elif re.search('(5s|5.s|five.s)', text, re.IGNORECASE):
                out = '5s'
            else:
                out = '5'
        elif re.search('(four|4)', text, re.IGNORECASE):
            if re.search('(4s|4.s|four.s)', text, re.IGNORECASE):
                out = '4s'
            else:
                out = '4'
        elif re.search('(three|3)', text, re.IGNORECASE):
            if re.search('(threeg|3g)', text, re.IGNORECASE):
                out = '3g'
            else:
                out = '3'
        elif re.search('(first|1st)', text, re.IGNORECASE):
            out = '1'
        else:
            out = '0'
        return out

    def strip_punc(self, text):
        return text.translate(string.maketrans("",""), string.punctuation)

    def remove_memwords(self, text):
        text = re.sub('\d\d+|8', '', text)

        stop_words = [
            'eight',
            'sixteen',
            'thirty two',
            'sixty four',
            'one twenty eight'
        ]

        text = ' '.join([word for word in text.lower().split() if word not in stop_words])
        return text

if __name__ == "__main__":
    c = Classifier()
    text = "iphone 5s 16gb"
    text = c.remove_memwords(text)
    text = 'brand new att iphone 5c blue 16gb clean imei'
    text = c.remove_memwords(text)

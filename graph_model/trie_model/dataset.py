import pandas as pd
import string

class Dataset:
        
    def __init__(self):
        self.df = self.read_data()
        self.preprocess()


    def read_data(self):
        df = pd.read_csv('./temp/data/item_master.csv.gz', compression='gzip')
        return df['PRODUCT_NAME'].values


    def preprocess(self):
        # remove unconsider characters from words in the sequence
        data = []    
        for word in self.df:
            if type(word) == str:
                temp = word.replace('\n', '')
                temp = word.replace(u"\u2122", '')  # remove trademark symbol
                temp = temp.translate(str.maketrans('', '', string.punctuation))
                data.append( temp.lower())

        self.df = data


    def save(self):
        out_file = open("./temp/data/pre_proceed_data.txt", "w")
        for prod_name in self.df:
            out_file.write(" ".join(prod_name.split()) + '\n')
        out_file.close()

    

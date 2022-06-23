import pandas as pd
import string

# for item_master.csv.gz
def data_preprocess():
    df = pd.read_csv('./temp/data/item_master.csv.gz', compression='gzip')
    data = remove_punctuation(df['PRODUCT_NAME'].values)
    out_file = open("./temp/data/pre_proceed_data.txt", "w")
    for prod_name in data:
        # remove trademark symbol
        temp = prod_name.replace(u"\u2122", '')
        out_file.write(" ".join(temp.split()) + '\n')
    out_file.close()
    return data

# remove unconsider characters from words in the sequence
def remove_punctuation(word_sequences):
    sequence_labels = []    
    for word in word_sequences:
        if type(word) == str:
            temp = word.replace('\n', '')
            temp = temp.translate(str.maketrans('', '', string.punctuation))
            sequence_labels.append( temp.lower())
    return sequence_labels

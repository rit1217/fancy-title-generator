import pandas as pd
import string

# for item_master.csv.gz
def data_preprocess():
    df = pd.read_csv('./temp/data/item_master.csv.gz', compression='gzip')
    print(f"Data has {len(df)} rows")
    print(df['PRODUCT_NAME'].values[:10])
    return remove_punctuation(df['PRODUCT_NAME'].values)

# remove unconsider characters from words in the sequence
def remove_punctuation(word_sequences):
    sequence_labels = []    
    count = 0
    for word in word_sequences:
        if type(word) == str:
            temp = word.replace('\n', '')
            temp = temp.translate(str.maketrans('', '', string.punctuation))
            sequence_labels.append( temp.lower())
    print( 'Total NaN', count)
    return sequence_labels

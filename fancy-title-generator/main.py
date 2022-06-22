import model.data_prep as data_prep
import model.model as model
from trie_model.trie import Trie

data2 = data_prep.data2_preparation('data/fashionData2.csv')
res = data_prep.word_sequence_preparation('data/fashionProducts.csv')
print(f"Data 1 has {len(res)} rows")

t = Trie()
t.add_data(res)
t.add_data(data2)
# r = t.search(['solid'])
while(1):
    in_str = input("enter string: ")
    prepared_in_str = data_prep.input_split(in_str)
    print( "\nNext word suggestion: ")
    print(t.search(prepared_in_str), "\n")
    print( "Complete title suggestion: ")
    r = t.autocomplete(prepared_in_str)
    for i in r[:20]:
        print(i)


    
# print(res[:10])

# res = model.train('data/fashionProducts.csv')

# print(res)    
# train_features, train_labels, test_features, test_labels, label_one_hot = data_preparation.prepare_data('data/fashionMNIST.csv')
# print(train_features[:10])
# print(train_labels[:10])
# print(test_features[:10])
# print(test_labels[:10])
# print(label_one_hot[:5])

# for i in train_features[:10]:
#     print(len(i))
# for i in data[6040:6050]:
#     print(i)
# data_frame = pd.DataFrame(data)
# msk = random.sample(range(len(data_frame)), floor(len(data_frame) * 0.2))

# print(len(data_frame[msk]))
# train = data_frame[~msk]
# test = data_frame[msk]
# print(len(train))
# print(len(test))
from model.data_prep import prepare_data 

train_features, train_labels, test_features, test_labels, label_one_hot = prepare_data('data/fashionMNIST.csv')
print(train_features[:10])
print(train_labels[:10])
print(test_features[:10])
print(test_labels[:10])
print(label_one_hot[:5])
# for i in data[6040:6050]:
#     print(i)
# data_frame = pd.DataFrame(data)
# msk = random.sample(range(len(data_frame)), floor(len(data_frame) * 0.2))

# print(len(data_frame[msk]))
# train = data_frame[~msk]
# test = data_frame[msk]
# print(len(train))
# print(len(test))
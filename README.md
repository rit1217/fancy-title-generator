# Fancy Fashion Product Title Generator

Fancy title generator is a web application that can help you to generate a title for your fashion products.

## Prerequisites

Before you get started, make sure you met the [REQUIREMENTS](.tool-versions).

## Installation

Install the packages for recommendation service and web frontend.
```bash
make install
```

## Usage

Preprocessing the data, train and save the graph-based model.
```bash
make train/trie
```

Start the web application and the API locally on port 3000.
```bash
make api
```

## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Acknowledgement

My sincere thanks go to Kirill for guiding this work.
* [Design Autocomplete in Python](https://medium.com/hackernoon/design-auto-complete-system-in-python-8fab1470cd92)
* [Great Article for Autosuggestion](https://medium.com/related-works-inc/autosuggest-retrieval-data-structures-algorithms-3a902c74ffc8)
* [RNN and Data-preparation for Autosuggestion](https://towardsdatascience.com/recurrent-neural-networks-by-example-in-python-ffd204f99470)

### License

Distributed under the [MIT License](LICENSE.md).

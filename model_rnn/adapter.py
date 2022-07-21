import torch
from .rnn import RNN
from .vectorize import make_input_vect
from .config import FILEPATHS
from .preprocessor import preprocess_text, IX_TO_CHAR, EOS


class ModelAdapter:
    def load(self):
        model_state = torch.load(FILEPATHS['model'], map_location=torch.device('cpu'))
        self.rnn = RNN(len(IX_TO_CHAR), len(IX_TO_CHAR))
        if torch.cuda.is_available():
            self.rnn.cuda()
        self.rnn.load_state_dict(model_state)
        self.rnn.eval()
        return self

    def predict(self, prefix:str='', top_n:int=10, max_length:int=100) -> list:
        title = preprocess_text(prefix)[:-1]
        result = self._predict_helper(title, top_n, max_length)
        result.sort(key=lambda item: item['score'], reverse=True)
        return result

    def _predict_helper(self, title:str, top_n:int=10, max_length:int=100, result_list:list=[], prefix_score:float=0) -> list:
        score = prefix_score
        with torch.no_grad():
            X = make_input_vect(title)
            hidden = None
            for i in range(len(title) - 1):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
            for i in range(max_length - len(title)):
                output, hidden = self.rnn.predict(X[-1].reshape(1, 1, -1), hidden)
                topv, topi = output.reshape(-1).topk(2)
                top_char = IX_TO_CHAR[topi[0].item()]
                top_2_char = IX_TO_CHAR[topi[1].item()]
                if top_char == EOS:
                    score += topv[0].item()
                    break
                elif len(result_list) < top_n - 1 and top_2_char != EOS:
                    for result in self._predict_helper(title + top_2_char, top_n, max_length, result_list, score + topv[1].item()):
                        if result not in result_list:
                            #Replace lowest score title with the new result
                            if result['score'] > min(result_list, key=lambda item: item['score'])['score']:
                                result_list[result_list.index( min(result_list, key=lambda item: item['score']))] = result
                            else:
                                result_list.append(result)
                score += topv[0].item()
                title += top_char
                X = make_input_vect(title)
            result = {'title':title[1:], 'score':score}
            if len(result_list) < top_n :
                result_list.append(result)
            #Replace lowest score title with the new result
            elif score > min(result_list, key=lambda item: item['score'])['score']:
                min_ix = result_list.index( min(result_list, key=lambda item: item['score']))
                result_list[min_ix] = result
                
            return result_list

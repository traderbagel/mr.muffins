import os 
import random
import pandas as pd 
from collections import defaultdict
from pypinyin import lazy_pinyin

dir_path = os.path.dirname(os.path.realpath(__file__))

class Solitaire():
    def __init__(self):
        csv_path = f'{dir_path}/idioms.csv'
        self.idiom_dict = pd.read_csv(csv_path)
        self.quick_search = defaultdict(list)
        for index, row in self.idiom_dict.iterrows():
            self.quick_search[self._char_to_pinyin(row["成語"][0])].append(index)
        self.quick_search_random = list(self.quick_search.keys())
        
        # random.choice(list(d.keys()))

    def _char_to_pinyin(self, c):
        return lazy_pinyin(c)[0]

    def _string_row(self, row):
        return  row["成語"] , row["釋義"]


    def get_next(self, idiom):
        last_char = self._char_to_pinyin(idiom[-1])
        if last_char in self.quick_search:
            rnd_idx = random.choice(self.quick_search[last_char])
            return self._string_row(self.idiom_dict.loc[rnd_idx])
        else:
            return "找不到"

    def start(self):
        rnd_pre = random.choice(self.quick_search_random)
        rnd_idx = random.choice(self.quick_search[rnd_pre])
        return self._string_row(self.idiom_dict.loc[rnd_idx])
    

solitaire = Solitaire()
# ans, meaning = solitaire.start()
# print(ans)
# ans, meaning = solitaire.get_next(ans)
# print(ans)

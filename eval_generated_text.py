import textstat
import configparser
import csv
from threading import Lock
from googletrans import Translator


CONFIG_FILE = "./config.ini"

class ConfigUtil:
    _instance = None
    _lock = Lock() 

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls.__internal_new__()
                    cls._instance.config = configparser.ConfigParser()
                    cls._instance.config.read(CONFIG_FILE)
        return cls._instance


def create_csv(config):
    csv_path = config.get('Paths','CsvPath')
    result_path = config.get('Paths','ResultPath')
    csv_name = config.get('Paths', 'CsvName')
    result_list = [] # タプル: (読み込んだcsvの行番号, 生成された文のARI, 生成された文, 生成された文の日本語訳)
    csv_title = ("読み込んだcsvの行番号", "word1", "word2", "FN", "word1 FE","word2 FE","生成された文のARI", "生成された文", "生成された文の日本語訳")
    words = csv_name.split("_") # ['water','pen.csv']
    word1 = words[0] # 'water'
    word2 = words[1].split(".")[0] # 'pen'

    with open(csv_path, 'r') as f:
        for i, row in enumerate(csv.reader(f)):
            current_row_generated_sentences = row[2].split('\n')
            fn = row[3]
            word1_fe = row[4]
            word2_fe = row[5]
            for sentence  in current_row_generated_sentences:
                if len(sentence) != 0:
                    result_list.append(
                        #(i,textstat.automated_readability_index(sentence),sentence, Translator().translate(sentence, dest = 'ja').text)
                        (i, word1, word2, fn, word1_fe, word2_fe, textstat.automated_readability_index(sentence),sentence, "リクエスト制限")
                    )
            print(i)
    del result_list[0]
    result_list.sort(key=lambda tup: tup[6]) # ARIでソート
    
    with open(result_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(csv_title)
        for row in result_list:
            writer.writerow(row)



if __name__ == '__main__':
    config = ConfigUtil.get_instance().config    
    create_csv(config)


import json
import numpy as np
from bs4 import BeautifulSoup



# input the pred_data as dic, cause_id as keys and list of predicted spans as values

class CausalityEvaluator():
    def __init__(self, event_type = None, data_type = None, data_path=None, gold_examples=None):
        self.data_path = data_path
        self.event_type = event_type
        self.data_type = data_type
        self.gold_examples = gold_examples

    def model_performance(self, pred_data):
        num_sample = 0
        p_list,r_list,f_list = [],[],[]
        if (not self.gold_examples):
            self.gold_examples = self._read_gold_example()
        for cas_id, anss in self.gold_examples.items():
            num_sample +=1
            if cas_id in pred_data:
                pre_anss = pred_data[cas_id]
                p,r,f = self.compute_prf(anss,pre_anss)
            else:
                p,r,f = 0, 0, 0
            p_list.append(p)
            r_list.append(r)
            f_list.append(f)

        macro_p = np.mean(p_list)
        macro_r = np.mean(r_list)
        macro_f = 2 * macro_p * macro_r / (macro_p + macro_r)
        return macro_p,macro_r,macro_f

    def compute_prf(self, anss, pre_anss):
        if len(anss[0]) == 0 or len(pre_anss[0]) == 0:
            precision, recall, f1 = int(anss[0] == pre_anss[0]), int(anss[0] == pre_anss[0]), int(anss[0] == pre_anss[0])
        else:
            gold_string_len, pred_string_len, correct_string_len = 0.0,0.0,0.0

            for ans in anss:
                gold_answer = ans.split('|')[0]
                gold_start = int(ans.split('|')[1])
                gold_end = int(ans.split('|')[2])
                gold_string_len+=len(gold_answer)

                for pre_ans in pre_anss:
                    pre_ans = pre_ans.replace(" ", '')
                    pre_answer = pre_ans.split('|')[0]
                    pre_start = int(pre_ans.split('|')[1])
                    pre_end = int(pre_ans.split('|')[2])
                    pred_string_len += len(pre_answer)

                    if not( pre_start > gold_end or gold_start > pre_end):
                        comm_substr, max_overlap = self._get_common_substr(gold_answer, pre_answer)
                        correct_string_len+=float(max_overlap)

            precision = (1.0 * correct_string_len / pred_string_len+0.0000000001)
            recall = (1.0 * correct_string_len / gold_string_len+0.0000000001)
            f1 = (2 * precision * recall) / (precision + recall+0.0000000001)

        return precision, recall, f1



    def _get_id(self):
        f = open(self.data_path + self.event_type + '_id_list.json', 'r')
        if self.data_type == 'dev':
            return json.load(f)['dev']
        elif self.data_type == 'test':
            return json.load(f)['test']


    def _read_gold_example(self):
        soup_argu = BeautifulSoup(open(self.data_path + self.event_type + "_all.xml", encoding='UTF-8'), "lxml")
        documents = soup_argu.find_all("causality")
        examples = {}
        id_list = self._get_id()
        for doc in documents:
            doc_id = doc['id']
            if doc_id not in id_list:
                continue
            doc_content_text = doc.content.get_text().strip()
            doc_tokens = [i for i in doc_content_text]
            events = doc.find_all("event")[0].find_all()
            cause_mention = doc.find_all("reason")[0]

            for evnt in events:
                evnt_dic = eval(evnt.string)
                cause_name = 'cause' + evnt.name[-1]  # one event with multiple reasons
                this_cause = cause_mention.find_all(cause_name)
                cas_id = doc_id + "_" + evnt.name[-1]
                examples[cas_id] = []
                if this_cause:

                    for cause_index, cause in enumerate(this_cause):
                        orig_answer_text = cause.get_text().strip()
                        start_index = cause['start']
                        end_index = cause['end']
                        if orig_answer_text in doc_content_text:
                            examples[cas_id].append(orig_answer_text+'|'+start_index+'|'+end_index)
                        else:
                            print("Reason not found!")

                else:

                    examples[cas_id].append("")

        return examples

    def _get_common_substr(self, str1, str2):

        lstr1 = len(str1)
        lstr2 = len(str2)
        record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # remember to add 1 
        maxNum = 0  #  match the max length
        p = 0  # match the start

        for i in range(lstr1):
            for j in range(lstr2):
                if str1[i] == str2[j]:
                    # augment if the same
                    record[i + 1][j + 1] = record[i][j] + 1
                    if record[i + 1][j + 1] > maxNum:
                        # get the max mathing length
                        maxNum = record[i + 1][j + 1]
                        # recored end position of the max matching length
                        p = i + 1
        return str1[p - maxNum:p], maxNum


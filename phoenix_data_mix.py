import csv
import copy
import os
from pathlib import Path

class PhoenixDataMix:
    # no class variables

    def __init__(self, data_root, result_root):
        self.DATA_ROOT=data_root
        self.RESULT_ROOT=result_root

        self.TRAIN_CORPUS_CSV  = self.DATA_ROOT+"/annotations/manual/train.corpus.csv"
        self.TRAIN_ALIGNMENT   = self.DATA_ROOT+"/annotations/automatic/train.alignment"
        self.TRAINCLASSES_TXT  = self.DATA_ROOT+"/annotations/automatic/trainingClasses.txt"

        self.TRAIN_DATA        = self.DATA_ROOT+"/features/fullFrame-256x256px/train"

        self.train_corpus_dict = {}
        self.glossClass_dict = {}
        self.reversed_glossClass_dict = {}
        self.master_dict = {}

        if len(self.train_corpus_dict) == 0:
            print("Initializing.....\n creating self.train_corpus_dict")
            self.make_train_corpus()
        if len(self.reversed_glossClass_dict) == 0:
            print("Initializing.....\n creating self.glossClass_dict")
            self.make_glossClass()

        self.make_master_dict()

        for key in self.master_dict:
            #print(self.master_dict[key]['annotation'])
            self.insert_annotation_index(self.master_dict[key]['annotation'], self.master_dict[key]['files'])

    def get_partial_list(self, id, index):
        data = self.master_dict[id]['files']
        filtered_data = [item for item in data if item[-1] == index]
        return filtered_data

    def get_filename_id(self, id):
        print(self.master_dict[id]['files'][0][0])

    # all filenames end with -0.png
    # all filenames have _pid0_fn followed by a 6-digit sequence number
    # It will return filename followed by .avi
    def get_filename_first_part(self, id):
        filename = self.master_dict[id]['files'][0][0]
        parts=filename.split('_pid0_fn')

        return parts[0]

    def get_master_dict(self):
        if len(self.master_dict) != 0:
            return self.master_dict
        else:
            print("wth")

    def make_mixed_list(self, s_id, s_idx, t_id, t_idx):
        first_list = copy.deepcopy(self.master_dict[s_id]['files'])
        second_list = copy.deepcopy(self.get_partial_list(t_id, t_idx))

        index_to_insert = next((i for i, item in enumerate(first_list) if item[-1] == s_idx), len(first_list))

        # 첫 번째 리스트에서 해당 위치 이전의 항목들을 가져옵니다.
        result = first_list[:index_to_insert]

        # add source directory flag at the end of list
        for row in first_list:
            row.append('s')
        # 두 번째 리스트를 추가합니다.
        # python 문제점 변수 타입이 pointer 인지 value인지 많이 헷갈리게 한다.
        for row in second_list:
            row[-1] = s_idx
            # add target directory flag at the end of list
            row.append('t')
        #tmp = [row[:-1] + [s_idx] for row in second_list]
        result.extend(second_list)

        # 첫 번째 리스트에서 해당 위치 이후의 항목들을 가져와서 '3'인 항목들을 제외하고 추가합니다.
        result.extend(item for item in first_list[index_to_insert:] if item[-2] != s_idx)

        return result

    def check_dir_exists(self, dir_name):
        if Path(dir_name).exists():
            print(f"{dir_name} exists")
            return True
        else:
            print(f"{dir_name} doesn't exist")
            return False

    def mix(self, dir_name, s_id, s_idx, s_gloss, t_id, t_idx, t_gloss):
        print("creating directory : " + dir_name)
        result_file_dir = self.RESULT_ROOT+ "/" + dir_name

        try:
            Path(result_file_dir).mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print(f"{result_file_dir} already exists!")
            return False

        filename = self.get_filename_first_part(s_id) # need to add "_pid0_fn000000-0.png"

        source_dir = self.TRAIN_DATA + "/" + s_id
        target_dir = self.TRAIN_DATA + "/" + t_id

        if self.check_dir_exists(source_dir) and self.check_dir_exists(target_dir):
            print(f"mix {source_dir} and {target_dir}")
        else:
            return False

        s_ann_list = self.get_annotation_list(s_id)
        t_ann_list = self.get_annotation_list(t_id)
        if s_ann_list[s_idx] != s_gloss:
            print(f"s_gloss : {s_gloss} is not index {s_idx}")
            return False
        if t_ann_list[t_idx] != t_gloss:
            print(f"t_gloss : {t_gloss} is not index {t_idx}")
            return False

        result = self.make_mixed_list(s_id, s_idx, t_id, t_idx)

        for i, row in enumerate(result):
            formatted_i = "_pid0_fn{:06}-0.png".format(i)
            symbolic_file = filename+formatted_i
            row.append(symbolic_file)
            source_file = source_dir + "/1/" + row[0]
            target_file = target_dir + "/1/" + row[0]

            if row[4] == 's':
                final_src_file = source_file
            else:
                final_src_file = target_file

            src_link = Path(final_src_file)
            dst_link = Path(result_file_dir+"/"+row[5])

            if Path(final_src_file).exists():
                #print("good")
                if dst_link.exists():
                    dst_link.unlink()
                dst_link.symlink_to(src_link)
                #print(i, row)
            else:
                print(f"{final_src_file} doesn't exist")
                print(i, row)
                return False

        #self.print_mix_result(result, dir_name, s_id, s_idx, s_gloss, t_id, t_idx, t_gloss)
        self.write_mix_result(result, dir_name, s_id, s_idx, s_gloss, t_id, t_idx, t_gloss)

        return True

    def print_mix_result(self, result, dir_name, s_id, s_idx, s_gloss, t_id, t_idx, t_gloss):
        print(f" Directory : {dir_name}\n S ID : {s_id}\n S Index : {s_idx}\n")
        print(f" T ID : {t_id}\n T Index : {t_idx}\n")
        for row in result:
            print(row)

    def write_mix_result(self, result, dir_name, s_id, s_idx, s_gloss, t_id, t_idx, t_gloss):
        logfile=self.RESULT_ROOT+"/"+dir_name+".txt"
        with open(logfile, 'w') as wfile:
            wfile.write(f"Directory : {dir_name}\nS ID : {s_id}\nS Index : {s_idx}\n")
            wfile.write(f"T ID : {t_id}\nT Index : {t_idx}\n")
            for row in result:
                wfile.write(' '.join(str(e) for e in row)+'\n')

    def print_id_files(self, id):
        #print(len(self.master_dict[id]['files']))
        print("id is : " + id)
        for i, row in enumerate(self.master_dict[id]['files']):
            print(i, row)

    def make_report_train_alignment(self):
        with open("jwkim_train.alignment", 'w') as wfile:
            for key in self.master_dict:
                for item in self.master_dict[key]['files']:
                    aline = f"features/fullFrame-256x256px/train/{key}/1/"
                    files_str = ' '.join(str(i) for i in item)
                    wfile.write(aline+files_str+"\n")


    # train.corpus.csv
    #
    # "id|folder|signer|annotation"
    #"01April_2010_Thursday_heute_default-0|01April_2010_Thursday_heute_default-0/1/*.png|Signer04|__ON__ LIEB ZUSCHAUER ABEND WINTER GESTERN loc-NORD SCHOTTLAND loc-REGION UEBERSCHWEMMUNG AMERIKA IX"
    #
    # self.train_corpus_dict = {}
    def make_train_corpus(self):
        # Open the CSV file
        with open(self.TRAIN_CORPUS_CSV, 'r') as file:
            #reader = csv.reader(file, delimiter='|', quotechar='"')
            reader = csv.reader(file, delimiter='|')
            # Skip the header
            next(reader)

            # Loop through each row in the CSV
            for row in reader:
                #parts = row[0].split('|') # data has "contents"
                parts=row

                if len(parts) == 4:
                    annotation_list = parts[3].split()
                    self.train_corpus_dict[parts[0]] = { 
                        'signer' : parts[2], 
                        'annotation_string' : parts[3],
                        'annotation_list' : annotation_list }
                else:
                    print("Something wrong!!")
                    break

        #print(self.train_corpus_dict['id'])
    def get_annotation_list(self, id):
        return self.train_corpus_dict[id]['annotation_list']

    # trainingClasses.txt
    #
    # 
    #signstate classlabel
    #A0 0
    #A1 1
    #A2 2
    #AACHEN0 3
    #AACHEN1 4
    #AACHEN2 5
    #
    # Total 3694 classes in the trainingClasses.txt
    #
    # glossClass_dict = { 'A' : [ 0, 1, 2 ], 'AACHEN' : [3, 4, 5],.....}

    def make_glossClass(self):
        with open(self.TRAINCLASSES_TXT, 'r') as file:
            reader = csv.reader(file, delimiter=' ')
            # Skip the header
            next(reader)
            for row in reader:
                # last character is digit ?
                if row[0][-1].isdigit(): 
                    gloss = row[0][:-1]
                else:
                    gloss = row[0]
                if gloss not in self.glossClass_dict:
                    self.glossClass_dict[gloss] = []
                self.glossClass_dict[gloss].append(row[1])

        for signstate, classlabels in self.glossClass_dict.items():
            for classlabel in classlabels:
                self.reversed_glossClass_dict[classlabel] = signstate

    # train.alignment to python dict
    #
    # features/fullFrame-210x260px/train/01April_2010_Thursday_heute_default-0/1/01April_2010_Thursday_heute.avi_pid0_fn000027-0.png 3693
    # 
    # 798990 train.alignment
    def make_master_dict(self):

        num = 0
        with open(self.TRAIN_ALIGNMENT, 'r') as file:
            for line in file:
                #if num > 300:
                #    break
                line_glossClass = line.split()
                if len(line_glossClass) == 2:
                    id_file=line_glossClass[0].split('/')
                    if len(id_file) != 6:
                        print("Something wrong in train.alignment")
                        break
                    num += 1
                    #print(id_file[3] + "   " + id_file[5] + "   " + line_glossClass[1])
                    #
                    # to make me understand this code later
                    #

                    id         = id_file[3]
                    filename   = id_file[5]
                    classlabel = line_glossClass[1]
                    signstate  = self.reversed_glossClass_dict[classlabel]

                    if id not in self.master_dict:
                        annotation_list = self.train_corpus_dict[id]['annotation_list']
                        self.master_dict[id] = {'annotation' : annotation_list, 'files' : []}
                    self.master_dict[id]['files'].append([filename, classlabel, signstate])
                else:
                    print("Something wrong in train.alignment")
                    break

        #print(self.master_dict['01April_2010_Thursday_heute_default-0'])

    # 조잡해 보이지만 잘 작동한다.
    def insert_annotation_index(self, annotation_list, files_list):
        tmp_annotation_list = annotation_list.copy()

        prev_signstate = ""
        for afile in files_list:
            if afile[2] == "si":
                afile.append('-1')
            else:
                #print(tmp_annotation_list)
                index = tmp_annotation_list.index(afile[2])
                original_index = annotation_list.index(afile[2])
                afile.append(index)

                if prev_signstate:
                    if prev_signstate != afile[2]:
                        #del tmp_annotation_list[0]
                        prev_index = tmp_annotation_list.index(prev_signstate)
                        tmp_annotation_list[prev_index] = ""
                        prev_signstate = afile[2]
                else:
                    prev_signstate = afile[2]


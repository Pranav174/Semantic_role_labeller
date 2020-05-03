from ssfAPI import *
import pickle

class Parser():
    def __init__(self):
        self.sentences = []
        self.data_folders = ['Urdu_Propbank_pre_release_version_0.005/Data/ComplexPredicates','Urdu_Propbank_pre_release_version_0.005/Data/SimplePredicates']
        self.out_path = 'processed_data.dat'

    def parse_folder(self, data_folder):
        print(f"Parsing {data_folder}...")
        
        counter = 1
        fileList = folderWalk(data_folder)
        newFileList = []
        
        for fileName in fileList :
            xFileName = fileName.split('/')[-1]
            if xFileName == 'err.txt' or xFileName.split('.')[-1] in ['comments','bak'] or xFileName[:4] == 'task' :
                continue
            else :
                newFileList.append(fileName)
        for fileName in newFileList :
            d = Document(fileName)
            for sentence in d.nodeList:
                has_arg = False
                for chunk in sentence.nodeList:
                    if chunk.parentPBRelation != 'root':
                        has_arg = True
                        break
                if has_arg:
                    self.sentences.append(sentence)
                print(f"\rParsed: {counter}", end='')
                counter += 1
        print()
    
    def parse(self):
        for folder in self.data_folders:
            self.parse_folder(folder)
        
        print(f"\nWriting to {self.out_path}...")
        with open(self.out_path, "wb") as f:
            pickle.dump(self.sentences, f, protocol=-1)  
        print("Done!")

if __name__ == "__main__":
    parser = Parser()
    parser.parse()

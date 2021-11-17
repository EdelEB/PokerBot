import os;

class WeightStorage(object):

    @staticmethod
    def store(dic, id_num):
        file = open("bot"+str(id_num)+"_weights"+".txt", 'w');

        for element in dic:
            string = element+"--"+str(dic[element])+"\n";
            file.write(string);
        file.close();

    @staticmethod
    def retrieve(id_num):
        dic = {};
        file = file = open("bot"+str(id_num)+"_weights"+".txt", 'r');
        for line in file:
            tup = line.strip().split("--"); # scenario:(fold_threshold,raise_threshold)
            dic[tup[0]] = tup[1];
        file.close();
        os.remove("bot"+str(id_num)+"_weights"+".txt");
        return dic;


def test():
    dic = {
        "1:2:1" : (200,400),
        "2:1:2" : (250,450)
    }
    WeightStorage.store(dic, 8);

    dic = WeightStorage.retrieve(8);
    print(dic);

#test();
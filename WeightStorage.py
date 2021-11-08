import os;

class WeightStorage(object):

    @staticmethod
    def store(dic, id_num):
        file = open("bot"+id_num+"_weights"+".txt", 'w');

        for element in dic:
            string = element+":"+dic[element]+"\n";
            file.write(string);
        file.close();

    @staticmethod
    def retrieve(id_num):
        dic = {};
        file = file = open("bot"+id_num+"_weights"+".txt", 'r');
        for line in file:
            tup = line.split(":"); # scenario:(fold_threshold,raise_threshold)
            dic[tup[0]] = tup[1];
        file.close();
        os.remove("bot"+id_num+"_weights"+".txt");
        return dic;


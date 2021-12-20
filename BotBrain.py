
class BotBrain():
    def __init__(self, filename):
        self.file = filename;
        self.dic = {};
        self.retrieve_weights();
        self.ADJUSTER = 5; # determines how much the weights are modified each hand

    def __del__(self):
        self.store_weights(self.dic);
        print(f"Data stored in {self.file}");

    def adjust_weights(self, winner, pending):  # Win/True || Loss/False
        for tup in pending:
            key = tup[0];
            move = tup[1];
            if winner:
                if self.dic[key][0] > 0:
                    self.dic[key][0] = self.dic[key][0] - self.ADJUSTER
                    self.dic[key][1] = self.dic[key][1] - self.ADJUSTER;
            else:
                if False: # move == 'c':
                    if self.dic[key][1] - self.dic[key][0] > self.ADJUSTER * 2 - 1:
                        self.dic[key][0] = self.dic[key][0] + self.ADJUSTER;
                        self.dic[key][1] = self.dic[key][1] + self.ADJUSTER;
                    else:
                        self.dic[key][0] = self.dic[key][0] + self.ADJUSTER;
                        self.dic[key][1] = self.dic[key][1] - self.ADJUSTER;
                else:
                    if self.dic[key][0] < 600:
                        self.dic[key][0] = self.dic[key][0] + self.ADJUSTER;
                        self.dic[key][1] = self.dic[key][1] + self.ADJUSTER;

    def store_weights(self, dic):
        with open(self.file, 'w') as file:
            for key in dic:
                string = f"{key}--{dic[key][0]},{dic[key][1]}\n";
                file.write(string);
                file.truncate();

    def retrieve_weights(self):
        dic = {};

        with open(self.file, 'r') as file:
            for line in file:
                tup = line.strip().split("--");  # key :[fold_threshold,raise_threshold]
                temp = tup[1].split(',');
                if len(temp) > 1 :
                    temp[0], temp[1] = int(temp[0]), int(temp[1]);
                dic[tup[0]] = temp;

        self.dic = dic;
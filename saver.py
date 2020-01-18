import os, pickle

class Saver:
    def __init__(self):
        self.out = 'data/save.dat'

    def save(self, data):
        f = open(self.out, mode='wb+')
        pickle.dump(data, f)
        f.close()
        pass

    def load(self):
        if os.path.isfile(self.out):
            f = open(self.out, mode='rb')
            t = pickle.load(f)
            f.close()
            return t
            pass
        else:
            return None

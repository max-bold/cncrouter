import numpy as np

class myclass:
    def __init__(self):
        self.val=np.asarray((1,2,3))
    
    def __repr__(self):
        return 'repr'
    
    def __str__(self):
        return 'str'
inst=myclass()
print(f'{str(inst)=}')
print(f'{repr(inst)=}')
print(f'{inst=}')
print(f'{inst.val.tolist()=}')
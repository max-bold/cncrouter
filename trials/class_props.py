class T:
    def __init__(self) -> None:
        self.x=0

    @property
    def val(self):
        self.x+=1
        return self.x

a=T()

for i in range(10):
    print(a.val)


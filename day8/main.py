import itertools

BLACK = 0
WHITE = 1
TRANSPARENT = 2

class Image():
    def __init__(self, width, height, data):
        super().__init__()
        self.width = width
        self.height = height
        self.layers = self.get_layers([int(x) for x in data])

    def get_layers(self, data):
        layer_len = self.width * self.height
        return [
            [x[1] for x in group[1]] for group in
            itertools.groupby(enumerate(data), key=lambda x: x[0]//layer_len)
        ]

    def checksum(self):
        layer = min(self.layers, key=lambda layer: layer.count(0))
        return layer.count(1) * layer.count(2)

    def render(self):
        img = [
            next(color for color in layers if color != TRANSPARENT) for layers in
            zip(*self.layers)
        ]
        buffer = ""
        for i, char in enumerate(img):
            if char == 1:
                buffer += "X"
            else:
                buffer += " "
            if (i + 1) % self.width == 0:
                buffer += "\n"
        return buffer

if __name__ == "__main__":
    with open('input') as f:
        data = f.read().strip()
        img = Image(25, 6, data)
        print("Checksum is: {}".format(img.checksum()))
        print(img.render())
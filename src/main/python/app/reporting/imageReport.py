class ImageReport:
    def __init__(self, png_path):
        self.png_path = png_path

    def save_graph_as_png(self, fig):
        fig.savefig(self.png_path)

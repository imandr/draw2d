class Scene(object):
    
    def __init__(self):
        self.Named = {}
        self.Unnamed = []
        
    def add(self, g, label=None, at=None, rotation=None, scale=None):
        if label is None:
            self.Unnamed.append(g)
        else:
            self.Named[label] = g
        if at is not None:  g.move_to(*at)
        if rotation is not None:    g.rotate_to(rotation)
        if scale is not None:   g.scale_to(*scale)
        return self
            
    def __getitem__(self, label):
        return self.Named[label]
        
    def render(self, surface, transform=None):
        if transform is None:
            c = self.Transform
        else:
            c = transform * self.Transform
        for g in self.Unnamed + list(self.Named.values()):
            if not g.Hidden:
                print("rendering:", g)
                g.render(surface, c)

    def remove_all(self):
        self.Named = {}
        self.Unnamed = []
    
    clear = remove_all

    def remove(self, label):
        return self.Named.pop(label, None)

    def remove_transient(self):
        self.Unnamed = [s for s in self.Unnamed if not s.Transient]
        self.Named = {label:s for label, s in self.Named.items() if not s.Transient}
        for s in self.Unnamed + list(self.Named.values()):
            if isinstance(s, Scene):
                s.remove_transient()


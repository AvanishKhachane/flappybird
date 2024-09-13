from pygame import image, transform, mask, font


class show:
    def __init__(self):
        pass

    def object(self, obj, x, y, tf=None, part=None, screen=None):
        if tf or tf is None:
            if part:
                if type(part) == tuple:
                    obj.set_colorkey((0, 0, 0))
                    screen.blit(obj, (x, y), part)
                elif type(part) == bool:
                    obj.set_colorkey((0, 0, 0))
                    screen.blit(obj, (x, y))
            else:
                screen.blit(obj, (x, y))

    def text(self, font_family, font_size, text, x, y, screen, tf=None, rgb=None):
        if tf is None: tf = True
        if rgb is None: rgb = [0, 0, 0]
        fonte = font.Font(font_family, font_size)
        fonte_render = fonte.render(str(text), tf, (rgb[0], rgb[1], rgb[2]))
        if tf: screen.blit(fonte_render, (x, y))


class sprites:
    def __init__(self, sprite_surface, size, x, y, screen, pos=None):
        self.screen = screen
        size = [str(size).split("x")[0], str(size).split("x")[1]]
        size = [int(size[0]), int(size[1])]
        self.size = size
        sprite_surface = image.load(sprite_surface)
        sprite_surface = transform.scale(sprite_surface, size)
        self.surface = sprite_surface
        self.x = x
        self.y = y
        if pos is None:
            pos = (x, y)
        else:
            x, y = pos
        self.pos = pos
        self.surface_mask = mask.from_surface(sprite_surface)
        self.ofst = ()

    def show(self, x=None, y=None, size=None, tf=None, part=None):
        if x is None: x = self.x - self.size[0]/2
        if y is None: y = self.y - self.size[1]/2
        if size is None:
            size = self.size
            if type(size) is list: size = f"{size[0]}x{size[1]}"
        show.object(None, self.surface, x, y, tf, part, self.screen)

    def collision(self, other_sprite, offset=None):
        ofst = ()
        if offset is None:
            ofst = (self.x + self.size[0] / 2 - (other_sprite.x + other_sprite.size[0] / 2), self.y + self.size[1] / 2 - (other_sprite.y + other_sprite.size[1] / 2))
        else:
            ofst = offset
        self.ofst = ofst
        return self.surface_mask.overlap(other_sprite.surface_mask, ofst)

    def rotate(self, angle):
        orig_rect = self.surface.get_rect()
        rot_image = transform.rotate(self.surface, angle)
        rot_rect = orig_rect
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect)
        self.surface = rot_image

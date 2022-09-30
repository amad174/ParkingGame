import pygame, math, os




def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


class PlayerCar:
    def __init__(self, start_pos):
        self.img = scale_image(pygame.image.load(os.path.join('assets', 'GreenCar.png')),0.08)
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.max_vel = 4
        self.vel = 0
        self.rotation_vel = 4
        self.angle = 0
        self.x, self.y = start_pos
        self.acceleration = 0.1 

    #car drawing updates here
    def draw(self,win):
        rotated_img = pygame.transform.rotate(self.img, self.angle)
        self.rect = rotated_img.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_img, self.rect.topleft)

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians)* self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration , 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-x),int(self.y-y))
        collisionIntersect = mask.overlap(car_mask, offset)
        return collisionIntersect
        
    def move_player(self, win):
        self.draw(win)
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_w] or keys[pygame.K_s]:
            if keys[pygame.K_a]:
                self.angle += self.rotation_vel
            if keys[pygame.K_d]:
                self.angle -= self.rotation_vel
            
        if keys[pygame.K_w]:
            moved = True
            #increase forward speed
            self.vel  = min(self.vel + self.acceleration, self.max_vel)
            self.move()

        if not moved :
            self.reduce_speed()

        if keys[pygame.K_s]:
            #decrease speed
            self.vel  = min(self.vel - self.acceleration, -self.max_vel/2)
            self.move()

import pygame

class Car(pygame.sprite.Sprite):
	def __init__(self):
		self.image = pygame.image.load('Car.png')
		self.rect = self.image.get_rect(center = (640,360))
		self.angle = 0
		self.rotation_speed = 1.8
		self.direction = 0
		self.forward = pygame.math.Vector2(0,-1)

	def set_rotation(self):
		if self.direction == 1:
			self.angle -= self.rotation_speed
		if self.direction == -1:
			self.angle += self.rotation_speed

		self.image = pygame.transform.rotozoom(self.original_image,self.angle,0.25)
		self.rect = self.image.get_rect(center = self.rect.center)

	def get_rotation(self):
		if self.direction == 1:
			self.forward.rotate_ip(self.rotation_speed)
		if self.direction == -1:
			self.forward.rotate_ip(-self.rotation_speed)

	def accelerate(self):
		if self.active:
			self.rect.center += self.forward * 5

	def update(self):
		self.set_rotation()
		self.get_rotation()
		self.accelerate()
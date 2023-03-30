# Import and initialize the pygame library
import pygame
import random
import numpy as np

# Define a Person object by extending pygame.sprite.Sprite

class Person:
    def __init__(self, world_size):
        self.x, self.y = random.randint(0,world_size), random.randint(0,world_size)
        self.infected = False
        self.exposed = False
        self.immune = False
        self.dead = False
        self.days_exposed = 0
        self.days_infected = 0
    def update(self, world_size):
        rand_num = random.randint(1,4)
        #if person is dead don't move
        if not self.dead:
            vel = random.randint(0,10)
        else:
            vel = 0
        if rand_num == 1:
            if self.x < world_size:  
                self.x += vel
        if rand_num == 2: 
            if self.x > 0:
                self.x -= vel
        if rand_num == 3:
            if self.y < world_size:
                self.y += vel
        if rand_num == 4:
            if self.y > 0:
                self.y -= vel

pygame.init()
#world_size
world_size = 500
# Set up the drawing window
screen = pygame.display.set_mode([500, 500])
fps = 30
fpsClock = pygame.time.Clock()
red = (255,0,0)
blue = (0, 0, 250)
orange = (255,128,0)
purple = (128,0,128)
black = (0,0,0)


#number of people
n = 1000
#survival chance 
survival_rate = 20

"""
    Randomly decide to recover or to die
    if random.randint(0,100) > survival_rate:
        turn to purple
    else 
        turn to black

"""

# Instantiate 1000 persons and 1 infected person
persons = [Person(world_size) for i in range(n)]
rand_index = random.randint(0,n-1)
infected = [rand_index]

# Run until the user asks to quit
running = True
first_iteration = True

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the background with white
    screen.fill((255, 255, 255))
    
    for i, person in enumerate(persons):
        #initialize colors during 1st run
        if first_iteration:
            if rand_index == i:    
                pygame.draw.circle(screen, red, (person.x, person.y), 2, 1)
                person.infected = True
                person.days_infected += 1
            else:
                pygame.draw.circle(screen, blue, (person.x, person.y), 2, 1)
            first_iteration = False
        #after that change colors according to the following conditions
        else:
            # if not infected or not immune calculate distance to infected guys around
            if person.infected == False and person.immune==False and person.dead==False:
                distances = []
                p_coord = np.array([person.x, person.y])  
                for each in infected:
                    infected_coord = np.array([persons[each].x, persons[each].y])
                    distances.append(np.linalg.norm(np.array(infected_coord) - p_coord))     
                
                dist = sum(distances)/len(distances) 
                # if they are far from infected keep them blue
                if dist >= 50:
                    pygame.draw.circle(screen, blue, (person.x, person.y), 2, 1)
                
                else:
                    #if not infected turn to exposed and start counting days
                    if person.exposed == False and person.infected == False:
                        pygame.draw.circle(screen, orange, (person.x, person.y), 2, 1)
                        person.days_exposed += 1
                        person.exposed = True
                    #if exposed longer than 2 days turn to infected and start counting days
                    if person.exposed == True:
                        if person.days_exposed > 2:
                            person.exposed = False
                            person.days_exposed = 0 
                            person.infected = True
                            if i not in infected:
                                infected.append(i)
                            pygame.draw.circle(screen, red, (person.x, person.y), 2, 1)
                            person.days_infected +=1
                        else:
                            pygame.draw.circle(screen, orange, (person.x, person.y), 2, 1)
                            person.days_exposed += 1                    

            """when person infected check if it's been like that for longer than 21 days, 
            if yes turn to immune or dead with 80% survival rate"""
            if person.infected == True:

                if person.days_infected > 21:
                    #decide randomly to survive or to die
                    person.infected = False
                    person.days_infected = 0
                    if random.randint(0,100) > survival_rate:
                        pygame.draw.circle(screen, purple, (person.x, person.y), 2, 1)
                        person.immune = True
                    else: 
                        pygame.draw.circle(screen, black, (person.x, person.y), 2, 1)
                        person.dead = True
                    
                    if i in infected:
                        infected.remove(i)
                else:    
                    pygame.draw.circle(screen, red, (person.x, person.y), 2, 1)
                    person.days_infected +=1
            """If person immune keep them purple"""
            if person.immune == True:
                pygame.draw.circle(screen, purple, (person.x, person.y), 2, 1)
            if person.dead == True:
                pygame.draw.circle(screen, black, (person.x, person.y), 2, 1)
        #update persons' location
        person.update(world_size)
    print(len(infected))        
    pygame.display.update()
    fpsClock.tick(fps)
# Done! Time to quit.
pygame.quit()
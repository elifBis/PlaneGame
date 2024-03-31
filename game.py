import pygame
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import math
import random
import functions

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Game")
playerImg = pygame.image.load('plane.png')
background = pygame.image.load('background.jpg')
player_width, player_height = playerImg.get_rect().size
playerX = 200
playerY = 480
playerX_change = 0
playerY_change = 0

font = pygame.font.Font(None, 32)

# We are going to initialize an HandDetector from CVZone package.
#The "detector" object will help us to use features of HandDetector class.
# You can find more information in detail from here: https://github.com/cvzone/cvzone?tab=readme-ov-file#hand-tracking-module
detector = HandDetector(detectionCon=0.8, maxHands=1)


time.sleep(2.0)

video = cv2.VideoCapture(0)

# Nokta sınıfı
class Point:
    def __init__(self):
        self.x = random.randint(50, 550)
        self.y = random.randint(50, 550)
        self.visible = True

    def draw(self):
        if self.visible:
            screen.blit(red_icon, (self.x - 12, self.y - 12)) 
# Oyuncu çizme fonksiyonu
def player(x, y):
    screen.blit(playerImg, (x, y))

# Nokta listesi
points = [Point() for _ in range(5)]  

score = 0
start_time = time.time()
best_time = float('inf')  

red_icon = pygame.image.load('parachutist.png')

best_time_text = font.render('', True, (255, 255, 255))

while True:
    ret, frame = video.read()
    hands, img = detector.findHands(frame)
    cv2.rectangle(img, (640, 480), (400, 425), (50, 50, 255), -2)

    current_time = time.time()
    elapsed_time = current_time - start_time

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_text = f"Time: {minutes:02d}:{seconds:02d}"


    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        x1, y1 = lmList[5][:2]
        x2, y2 = lmList[17][:2]
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        

        fingerUp = detector.fingersUp(hand)

        # if fingerUp == [0, 0, 0, 0, 0]:
        #     cv2.putText(frame, 'Ilerle', (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        #     if 20 <= distance <= 40:
        #         playerY_change = -0.5
        #     elif 40 < distance <= 70:
        #         playerY_change = -1
        #     elif 70 < distance <= 100:
        #         playerY_change = -2
        # else:
        #     playerY_change = 0


        if fingerUp == [0, 0, 0, 0, 0]:
            playerY_change = functions.move_player('forward', distance, playerY_change)
        if fingerUp == [0, 1, 1, 0, 0]:
            playerX_change = functions.move_player('left', distance, playerX_change )
        elif fingerUp == [0, 1, 0, 0, 0]:
            playerX_change = functions.move_player('right', distance, playerX_change )
        else:
            playerX_change = 0



        # if fingerUp == [0, 1, 1, 0, 0]:
        #     cv2.putText(frame, 'Sol', (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        #     if 20 <= distance <= 40:
        #         playerX_change = -0.5
        #     elif 40 < distance <= 70:
        #         playerX_change = -1
        #     elif 70 < distance <= 100:
        #         playerX_change = -2
        # elif fingerUp == [0, 1, 0, 0, 0]:
        #     cv2.putText(frame, 'Sag', (440, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        #     if 20 <= distance <= 40:
        #         playerX_change = +0.5
        #     elif 40 < distance <= 70:
        #         playerX_change = +1
        #     elif 70 < distance <= 100:
        #         playerX_change = +2
        # else:
        #     playerX_change = 0  

        for point in points:
            distance = math.sqrt((point.x - playerX)**2 + (point.y - playerY)**2)
            if distance < 25 and point.visible:
                point.visible = False
                score += 1

        if score == len(points):
            if elapsed_time < best_time:
                best_time = elapsed_time
            score_text = font.render(f'Oyun bitti!', True, (255, 255, 255))
            best_time_text = font.render(f'Bitirme Süresi: {int(best_time // 60):02d}:{int(best_time % 60):02d}', True, (255, 255, 255))
            screen.blit(score_text, (200, 250))
            screen.blit(best_time_text, (200, 300))
            pygame.display.flip()
            pygame.time.wait(3000)  
            break

    screen.fill((0, 0, 0))
    playerY += playerY_change
    playerX += playerX_change

    if playerX <= -player_width:  
        playerX = 600
    elif playerX >= 600: 
        playerX = -player_width
    if playerY <= -player_height:  
        playerY = 600
    elif playerY >= 600:  
        playerY = -player_height

    screen.blit(background, (0, 0))
    for point in points:
        point.draw()    
        
    player(playerX, playerY)

    # Puanı ekrana yazdırma
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 50))
    # Zamanı ekrana yazdırma
    timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", False, (255, 255, 255))
    screen.blit(timer_text, (200, 10))

    pygame.display.flip()  

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

import pygame
import os
import SpaceShip



WIDTH, HEIGHT = 900, 500
FPS = 30
MAX_BULLETS = 5

WHITE =(255,255,255)
BORDERCOLOR = WHITE
BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)


SHIPSCALE = (60,60)
SHIP_PATH = os.path.join("Assets","ship.png")



SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.jpg')), (WIDTH, HEIGHT))



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")



def DrawWindow()->None:
    WIN.blit(SPACE,(0,0)) #BLIT SPACE ON WIN AT 0,0
    pygame.draw.rect(WIN,BORDERCOLOR,BORDER)
    ship1.Update(ship2)
    ship2.Update(ship1)

    pygame.display.update();





def main():
    global ship1
    global ship2

    ship1 = SpaceShip.Ship(SHIP_PATH,SHIPSCALE,(30,30), 1) #ship
    ship2 = SpaceShip.Ship(SHIP_PATH,SHIPSCALE,(500,200), -1) #ship2
    ship2.SetButton() #change button 

    # set position of heath point
    ship1.Health.SetPosition(10,10)
    ship2.Health.SetPosition(WIDTH - 130,10)
    
    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break;
            
            if event.type == pygame.KEYDOWN:
                if event.key == ship1.buttons.get("SHOOTINGBOTTON") and len(ship1.bullets) < MAX_BULLETS:
                    ship1.FireBullets()
                if event.key == ship2.buttons.get("SHOOTINGBOTTON") and len(ship2.bullets) < MAX_BULLETS:
                        ship2.FireBullets()



        if SpaceShip.GameOver():
            run = False
            SpaceShip.isGameOver = False
            break;
        keysPressed = pygame.key.get_pressed() # bool and pressed button tuple
        ship1.HandleMovements(keysPressed)
        ship2.HandleMovements(keysPressed)
        DrawWindow();

        

    main()
        

if __name__ =="__main__":
    SpaceShip.SetGameWindow(WIN,(WIDTH, HEIGHT))
    main()
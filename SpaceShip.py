
import pygame
import os

pygame.mixer.init()

SHOOTSOUND = pygame.mixer.Sound(os.path.join("Assets",("bullet.mp3")))
COllITIONSOUND = pygame.mixer.Sound(os.path.join("Assets",("explosion.mp3")))



isGameOver = False
SPEED = 5
BULLETCOLOR = (255,0,0)
BULLETSPEED = 10
FONTCOLOR = (255,255,255)

def GameOver()->bool:
    return isGameOver

DEFAULT_BOTTON = {"UP" : pygame.K_UP,
                        "DOWN" : pygame.K_DOWN,
                        "SHOOTINGBOTTON" : pygame.K_RSHIFT}



SECONDRY_BOTTON = {"UP" : pygame.K_w,
                   "DOWN" : pygame.K_s,
                   "SHOOTINGBOTTON" : pygame.K_LSHIFT}
# gameWindow:pygame.display
# gameWindowSize =(0,0);
# HIT = pygame.USEREVENT

def SetGameWindow(gameWin:pygame.display,gameWinSize:tuple):
    global gameWindow
    global gameWindowSize
    gameWindow = gameWin;
    gameWindowSize = gameWinSize;
    # print(gameWindowSize)
 


pygame.font.init()
# pygame.mixer.init()
HEALTH_FONT = pygame.font.SysFont('comicsans',20)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

class Text:
    def __init__(self,text:str,pos:tuple = (0,0),Font:pygame.font= HEALTH_FONT,fontColor:tuple= FONTCOLOR):
        self.text = text;
        self.Font = Font
        self.xFont, self.yFont = 0,0;
        self.fontColor = FONTCOLOR
        
    def SetPosition(self,x:int,y:int):
        self.xFont, self.yFont = x,y

    def SetFont(self,textFont:pygame.font):
        self.Font = textFont
    
    def Display(self):
        txt = self.Font.render(self.text ,1,FONTCOLOR)
        gameWindow.blit(txt,(self.xFont,self.yFont))

    def DisplayFont(self,health:int):

        txt = self.Font.render(self.text +str(health) ,1,FONTCOLOR)
        gameWindow.blit(txt,(self.xFont,self.yFont))


    

class Ship:
    def __del__(self):
      print ("ship gets destroyed");
    
    def __init__(self,spaceShip:str,spaceShipScale:tuple,spaceShipPos:tuple,direction:int = 1):
        """
        gameWindow:pygame.display
        spaceShip:str
        spaceShipScaletuple
        spaceShipPos:tuple  
        direction:bool
        """ 
        self.spaceShip = pygame.transform.rotate(  #rotate
                            pygame.transform.scale(  #scale down
                            pygame.image.load(spaceShip),spaceShipScale),direction*90);
        self.shipWidth,self.shipHeight = spaceShipScale
        self.xAxis,self.yAxis = spaceShipPos
        self.bullets = []
        self.direction = direction
        self.Health = Text("HEALTH :")
        self.healthPoint = 100;
        self.buttons = {"UP" : pygame.K_UP,
                        "DOWN" : pygame.K_DOWN,
                        "SHOOTINGBOTTON" : pygame.K_RSHIFT}
        
        
    def HandleMovements(self,keysPressed):
        if keysPressed[self.buttons.get("UP")] and self.yAxis >0:
            self.yAxis -= SPEED
        if keysPressed[self.buttons.get("DOWN")] and (self.yAxis + self.shipWidth < gameWindowSize[1]):
            self.yAxis += SPEED
        
    def SetButton(self):
        self.buttons =SECONDRY_BOTTON


    def HandleHits(self):
        self.healthPoint -= 5
        print(self.healthPoint)
        if self.healthPoint <= 0:
            self.showWinningScreen()
    
    def showWinningScreen(self):
        # gameWindow.fill((0,0,0))
        global isGameOver
        isGameOver = True
        gameOver = Text("Game Over")
        gameOver.SetFont(WINNER_FONT)
        gameOver.SetPosition(200,100)
        gameOver.Display()

        pygame.display.update()
        pygame.time.delay(5000)

    def HandleBullets(self,otherShip:"Ship"):
        for bullet in self.bullets:
            bullet.x += self.direction * BULLETSPEED
            pygame.draw.rect(gameWindow,BULLETCOLOR,bullet)
            print(bullet.x);

            if otherShip.Collition(bullet):
                COllITIONSOUND.play()
                otherShip.HandleHits();
                self.bullets.remove(bullet)

            if 0 > bullet.x or bullet.x > 900:
                self.bullets.remove(bullet)
                # print("removed")

    def Collition(self,bullet)->bool:    
        return ( bullet.x < self.xAxis +self.shipWidth and
                bullet.x +bullet.w > self.xAxis and
                bullet.y < self.yAxis + self.shipHeight and
                bullet.y + bullet.w > self.yAxis
                )
    
    def FireBullets(self)->None:
        bullet = pygame.Rect(self.xAxis+self.shipWidth//2,self.yAxis+self.shipHeight//2,10,5)
        self.bullets.append(bullet)
        self._bulletSound();
    
        # pass

    def _bulletSound(self):
        SHOOTSOUND.play()

    def Update(self,otherShip):
        self.HandleBullets(otherShip)
        self._ShowSpaceShip()

    def _ShowSpaceShip(self):
        self.Health.DisplayFont(self.healthPoint);  
        gameWindow.blit(self.spaceShip,(self.xAxis,self.yAxis))
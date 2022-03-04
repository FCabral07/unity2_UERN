# This is a Hangman Game, this version is a hybrid version, with words and explication in Portuguese, but the code is
# all in English. A full english version is on development.
# Created by: Felipe Cabral.

# Importando as bibliotecas que vou usar no jogo

from timeit import default_timer as timer

import pygame
import random
import sys

# Iniciando a biblioteca pygame e definindo ajustes da tela

fps = 60
pygame.init()
width = 1280
height = 720
Display = pygame.display.set_mode((1280, 720))

# Definindo cores, imagens, sons e fontes que usarei no jogo

black = (0, 0, 0)
white = (255, 255, 255)
lightred = (255, 165, 145)
darklightred = (255, 97, 81)
lightblue = (126, 178, 255)
darklightblue = (42, 129, 255)
lightgrey = (192, 192, 192)
aquamarine = (69, 139, 116)
orange = (255, 69, 0)
wine = (114, 47, 55)

image = pygame.image.load("images/background.png")
bg_Music = pygame.mixer.Sound("images/back.wav")
bg_Music.play(loops=-1)
bg_Music.set_volume(0.035)
Font = pygame.font.SysFont("Cour", 50)
Font2 = pygame.font.Font("images/font.ttf", 20)


def button(word, x, y, w, h, ic, ac, action=None):  # Botões que usarei no jogo
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    buttonText = pygame.font.SysFont("Cour", 30)
    buttonTextSurf = buttonText.render(word, True, white)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(buttonTextSurf, buttonTextRect)


def endGame():  # Criando a tela do final do jogo
    end = timer()
    print("Time it took: ", end - start)
    timeTaken = (end - start)
    message = "Time taken: " + str(round(timeTaken)) + "s"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Limpando a tela para exibir as informações
        screen.blit(image, (0, 0))

        # Criando os botões de sair ou não do jogo
        button("Yes", (width / 2) - 50, 480, 100, 50, darklightred, lightred, quitGame)
        button("No", (width / 2) - 50, 540, 100, 50, darklightred, lightred, hangman)

        # Texto da tela
        largeText = pygame.font.SysFont("comicsansms", 100)
        TextSurf = largeText.render("End Game?", True, darklightred)
        TextRect = TextSurf.get_rect()
        TextRect.center = (width / 2, height / 2)
        screen.blit(TextSurf, TextRect)

        textSurf = largeText.render(message, True, darklightred)
        textRect = textSurf.get_rect()
        textRect.center = (width / 2, 200)
        screen.blit(textSurf, textRect)

        # Atualizando a tela
        pygame.display.update()
        clock.tick(fps)  # Faz com que o jogo nunca rode a mais que o número de fps por segundo


def quitGame():  # Função chamada quando acaba o jogo e pergunta se o jogador quer continuar
    pygame.quit()
    sys.exit()


def placeLetter(letter):  # Criando a tela para aparecerem as letras.
    global pick, pickSplit
    space = 10
    wordSpace = 0
    while wordSpace < len(pick):
        text = pygame.font.SysFont('Cour', 60)
        if letter in pickSplit[wordSpace]:
            textSurf = text.render(letter, True, aquamarine)
            textRect = textSurf.get_rect()
            textRect.center = ((150 + space), 200)
            screen.blit(textSurf, textRect)
        wordSpace += 1
        space += 60

    # Atualizando a tela
    pygame.display.update()
    clock.tick(fps)  # Faz com que o jogo nunca rode a mais que o número de fps por segundo


def textBoxLetter(letter):  # Criando o espaço onded ficarão as letras erradas.
    global textBoxSpace, textBoxNumber
    if textBoxNumber <= 5:
        text = pygame.font.Font("freesansbold.ttf", 40)
        textSurf = text.render(letter, True, orange)
        textRect = textSurf.get_rect()
        textRect.center = ((105 + textBoxSpace), 350)
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 10:
        text = pygame.font.Font("freesansbold.ttf", 40)
        textSurf = text.render(letter, True, orange)
        textRect = textSurf.get_rect()
        textRect.center = ((105 + textBoxSpace), 400)
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 15:
        text = pygame.font.Font("freesansbold.ttf", 40)
        textSurf = text.render(letter, True, orange)
        textRect = textSurf.get_rect()
        textRect.center = ((105 + textBoxSpace), 450)
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 20:
        text = pygame.font.Font("freesansbold.ttf", 40)
        textSurf = text.render(letter, True, orange)
        textRect = textSurf.get_rect()
        textRect.center = ((105 + textBoxSpace), 500)
        screen.blit(textSurf, textRect)

    # Atualizando a tela
    pygame.display.update()
    clock.tick(fps)  # Faz com que o jogo nunca rode a mais que o número de fps por segundo


def hangman():  # Tela do jogo
    global textBoxSpace, textBoxNumber
    textBoxSpace = 5
    textBoxNumber = 0
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Definindo a tela de fundo e seus aspectos
        screen.blit(image, (0, 0))

        textBoxSpace = 5

        Display.blit(pygame.font.Font("images/font.ttf", 40).render("HANGMAN", True, white), (20, 20))
        Display.blit(Font2.render("by Felipe Cabral", True, aquamarine), (60, 60))
        Display.blit(Font.render("Level Difficulty", True, aquamarine), ((width / 1.5), (height / 10)))

        # Criando os botões de dificuldade
        button("Hard", 900, 330, 150, 100, aquamarine, lightgrey, Hard)
        # button("Insane", 900, 435, 150, 100, aquamarine, lightgrey, Insane)
        #  ^ Preferi deixar a categoria insane de fora visto que seria muito dificil encaixar as palavras na tela.
        button("Easy", 900, 120, 150, 100, aquamarine, lightgrey, Easy)
        button("Medium", 900, 225, 150, 100, aquamarine, lightgrey, Medium)

        # Criando o bonequinho da forca que estará no menu iniciável.
        pygame.draw.line(Display, aquamarine, (220, 470), (500, 470), 8)  # baseline
        pygame.draw.line(Display, aquamarine, (300, 150), (300, 470), 8)  # stick1
        pygame.draw.line(Display, aquamarine, (300, 150), (470, 150), 8)  # stick2
        pygame.draw.line(Display, aquamarine, (390, 210), (390, 150), 8)  # rope
        pygame.draw.circle(Display, aquamarine, (390, 250), 40, 8)  # head
        pygame.draw.line(Display, aquamarine, (390, 290), (390, 390), 8)  # body
        pygame.draw.line(Display, aquamarine, (390, 310), (340, 350), 10)  # lefthand
        pygame.draw.line(Display, aquamarine, (450, 350), (390, 310), 10)  # righthand
        pygame.draw.line(Display, aquamarine, (390, 390), (340, 440), 10)  # leftleg
        pygame.draw.line(Display, aquamarine, (450, 440), (390, 390), 10)  # rightleg

        # Atualizando a tela
        pygame.display.update()
        clock.tick(fps)  # Faz com que o jogo nunca rode a mais que o número de fps por segundo


def hangmanGame(catagory, title):  # Tela após o menu, a forma do jogo
    global pause, pick, pickSplit, textBoxSpace, textBoxNumber, start, chances  # score
    start = timer()
    end = timer()
    chances = 20
    # score = (end - start)*100
    pick = random.choice(catagory)
    pickSplit = [pick[i:i + 1] for i in range(0, len(pick), 1)]

    screen.blit(image, (0, 0))

    wordSpace = 0
    space = 10
    while wordSpace < len(pick):
        text = pygame.font.Font("freesansbold.ttf", 40)
        textSurf1 = text.render("_", True, aquamarine)
        textRect1 = textSurf1.get_rect()
        textRect1.center = ((150 + space), 200)
        screen.blit(textSurf1, textRect1)
        space = space + 60
        wordSpace += 1

    guesses = ''
    gamePlay = True
    while gamePlay == True:
        guessLett = ''

        if textBoxNumber == 5:
            textBoxSpace = 5
        if textBoxNumber == 10:
            textBoxSpace = 5
        if textBoxNumber == 15:
            textBoxSpace = 5

        # Criando o quadrado de chances no canto superior direito da tela no jogo
        pygame.draw.rect(screen, black, [850, 20, 200, 20])
        text = pygame.font.Font("freesansbold.ttf", 20)
        textSurf = text.render(("Chances: %s" % chances), False, darklightred)
        textRect = textSurf.get_rect()
        textRect.topright = (1000, 20)
        screen.blit(textSurf, textRect)

        # Criando o título no canto superior de qual dificuldade está sendo jogada.
        textTitle = pygame.font.Font("freesansbold.ttf", 40)
        textTitleSurf = textTitle.render(title, True, lightgrey)
        textTitleRect = textTitleSurf.get_rect()
        textTitleRect.center = ((width / 2), 50)
        screen.blit(textTitleSurf, textTitleRect)

        pygame.draw.rect(screen, lightgrey, [100, 300, 250, 250], 2)

        # Criando o boneco da forca a cada vez que errar uma palavra.
        if chances == 19:
            pygame.draw.rect(screen, orange, [450, 550, 100, 10])
            #  = score//2
        elif chances == 18:
            pygame.draw.rect(screen, orange, [550, 550, 100, 10])
            #  = score//2
        elif chances == 17:
            pygame.draw.rect(screen, orange, [650, 550, 100, 10])
            #  = score//2
        elif chances == 16:
            pygame.draw.rect(screen, orange, [500, 450, 10, 100])
            #  = score//2
        elif chances == 15:
            pygame.draw.rect(screen, orange, [500, 350, 10, 100])
            #  = score//2
        elif chances == 14:
            pygame.draw.rect(screen, orange, [500, 250, 10, 100])
            #  = score//2
        elif chances == 13:
            pygame.draw.rect(screen, orange, [500, 250, 150, 10])
            #  = score//2
        elif chances == 12:
            pygame.draw.rect(screen, orange, [600, 250, 100, 10])
            #  = score//2
        elif chances == 11:
            pygame.draw.rect(screen, orange, [600, 250, 10, 50])
            #  = score//2
        elif chances == 10:
            pygame.draw.line(screen, orange, [505, 505], [550, 550], 10)
            #  = score//2
        elif chances == 9:
            pygame.draw.line(screen, orange, [550, 250], [505, 295], 10)
            #  = score//2
        elif chances == 8:
            pygame.draw.line(screen, orange, [505, 505], [460, 550], 10)
            #  = score//2
        elif chances == 7:
            pygame.draw.circle(screen, orange, [605, 325], 30)
            #  = score//2
        elif chances == 6:
            pygame.draw.rect(screen, orange, [600, 350, 10, 60])
            #  = score//2
        elif chances == 5:
            pygame.draw.rect(screen, orange, [600, 410, 10, 60])
            #  = score//2
        elif chances == 4:
            pygame.draw.line(screen, orange, [605, 375], [550, 395], 10)
            #  = score//2
        elif chances == 3:
            pygame.draw.line(screen, orange, [605, 375], [650, 395], 10)
            #  = score//2
        elif chances == 2:
            pygame.draw.line(screen, orange, [605, 465], [550, 485], 10)
            #  = score//2
        elif chances == 1:
            pygame.draw.line(screen, orange, [605, 465], [650, 485], 10)
            #  = score//2

        button("Back", 50, 50, 100, 50, black, lightgrey, hangman)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Criando os eventos que acontecem a cada evento do teclado.
            if event.type == pygame.KEYDOWN:
                failed = 0
                print("Failed", failed)
                print("Chance", chances)

                if event.key == pygame.K_SPACE:
                    pause()

                if event.key == pygame.K_ESCAPE:
                    gamePlay = False

                if event.key == pygame.K_a:
                    # letra a
                    guessLett = guessLett + 'a'
                    guesses += guessLett
                    print("letter a guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('a')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('a')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_b:
                    # letra b
                    guessLett = guessLett + 'b'
                    guesses += guessLett
                    print("letter b guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('b')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('b')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_c:
                    # letra c
                    guessLett = guessLett + 'c'
                    guesses += guessLett
                    print("letter c guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('c')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('c')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_d:
                    # letra d
                    guessLett = guessLett + 'd'
                    guesses += guessLett
                    print("letter d guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('d')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('d')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_e:
                    # letra e
                    guessLett = guessLett + 'e'
                    guesses += guessLett
                    print("letter e guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('e')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('e')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_f:
                    # letra f
                    guessLett = guessLett + 'f'
                    guesses += guessLett
                    print("letter f guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('f')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('f')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_g:
                    # letra g
                    guessLett = guessLett + 'g'
                    guesses += guessLett
                    print("letter g guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('g')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('g')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_h:
                    # letra h
                    guessLett = guessLett + 'h'
                    guesses += guessLett
                    print("letter h guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('h')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('h')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_i:
                    # letra i
                    guessLett = guessLett + 'i'
                    guesses += guessLett
                    print("letter i guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('i')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('i')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_j:
                    # letra j
                    guessLett = guessLett + 'j'
                    guesses += guessLett
                    print("letter j guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('j')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('j')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_k:
                    # letra k
                    guessLett = guessLett + 'k'
                    guesses += guessLett
                    print("letter k guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('k')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('k')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_l:
                    # letra l
                    guessLett = guessLett + 'l'
                    guesses += guessLett
                    print("letter l guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('l')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('l')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_m:
                    # letra m
                    guessLett = guessLett + 'm'
                    guesses += guessLett
                    print("letter m guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('m')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('m')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_n:
                    # letra n
                    guessLett = guessLett + 'n'
                    guesses += guessLett
                    print("letter n guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('n')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('n')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_o:
                    # letra o
                    guessLett = guessLett + 'o'
                    guesses += guessLett
                    print("letter o guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('o')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('o')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_p:
                    # letra p
                    guessLett = guessLett + 'p'
                    guesses += guessLett
                    print("letter p guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('p')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('p')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_q:
                    # letra q
                    guessLett = guessLett + 'q'
                    guesses += guessLett
                    print("letter q guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('q')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('q')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_r:
                    # letra r
                    guessLett = guessLett + 'r'
                    guesses += guessLett
                    print("letter r guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('r')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('r')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_s:
                    # letra s
                    guessLett = guessLett + 's'
                    guesses += guessLett
                    print("letter s guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('s')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('s')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_t:
                    # letra t
                    guessLett = guessLett + 't'
                    guesses += guessLett
                    print("letter t guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('t')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('t')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_u:
                    # letra u
                    guessLett = guessLett + 'u'
                    guesses += guessLett
                    print("letter u guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1
                    if guessLett in pick:
                        placeLetter('u')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('u')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_v:
                    # letra v
                    guessLett = guessLett + 'v'
                    guesses += guessLett
                    print("letter v guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('v')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('v')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_w:
                    # letra w
                    guessLett = guessLett + 'w'
                    guesses += guessLett
                    print("letter w guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('w')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('w')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_x:
                    # letra x
                    guessLett = guessLett + 'x'
                    guesses += guessLett
                    print("letter x guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1
                    if guessLett in pick:
                        placeLetter('x')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('x')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_y:
                    # letra y
                    guessLett = guessLett + 'y'
                    guesses += guessLett
                    print("letter y guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('y')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('y')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

                if event.key == pygame.K_z:
                    # letra z
                    guessLett = guessLett + 'z'
                    guesses += guessLett
                    print("letter z guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('z')

                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        # print(score)
                        endGame()

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('z')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was", pick)
                        # print(score)
                        endGame()

        pygame.display.update()
        clock.tick(fps)

    pygame.display.update()
    clock.tick(fps)


def Easy():  # Categoria fácil
    easy = ['amarelo', 'ave', 'celular', 'felipe', 'parque', 'meia', 'geleia', 'branco', 'tigre', 'penguim', 'girar',
            'panda', 'cerveja', 'batata', 'jazz', 'gato', 'juiz', 'anzol', 'cavalo', 'spray', 'ziper',
            'webcam', 'mouse', 'python', 'java', 'chocolate', 'dormir']
    print("easy")
    title = "Easy Difficulty"
    hangmanGame(easy, title)


def Medium():  # Categoria média
    medium = ['sintetizador', 'nebulizador', 'desfibrilador', 'dromedario', 'endocrinologista', 'vertiginoso', 'axioma',
              'pizzaiolo', 'jenipapo', 'oftalmologista', 'ambulancia', 'reportagem', 'imbu', 'esparadrapo', 'flamengo',
              'amendoim', 'caatinga', 'catapora', 'mexerica', 'groselha', 'campinense', 'jabuticaba', 'embarcacao']
    print("medium")
    title = "Medium Difficulty"
    hangmanGame(medium, title)


def Hard():  # Categoria dificil
    hard = ['alfarroba', 'ciriguela', 'pachorrento', 'sobrepujar', 'quimera', 'sumidade', 'vacancia', 'tergiversar',
            'ananases', 'empedernido', 'idiossincrasia', 'rubicundo', 'homizio', 'pudico', 'oboe', 'xilofone', 'xequere'
        , 'bergamota', 'saguaraji', 'pirilampo', 'turismologo', 'vicissitude', 'ictericia', 'criptomoeda', ]
    print("hard")
    title = "Hard Difficulty"
    hangmanGame(hard, title)


# def Insane():  # categoria insana
#    insane = ['pneumoultramicroscopicossilicovulcanoconiose', 'paraclorobenzilpirrolidinonetilbenzimidazol',
#              'piperidinoetoxicarbometoxibenzofenona', 'dimetilaminofenildimetilpirazolona',
#              'hipopotomonstrosesquipedaliofobia']
#    print("insane")
#    title = "Insane Difficulty"
#    hangmanGame(insane, title)


def main():  # Arquivo main, que chama o jogo.
    global clock, screen, play
    play = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hangman Game")

    while True:
        hangman()


if __name__ == '__main__':  # Roda o jogo
    main()

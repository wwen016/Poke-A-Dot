from tkinter import *
from tkinter import messagebox
import numpy as np
import pygame
# ---------------------------- CONSTANTS ------------------------------- #

FONT_NAME = "Helvetica Neue"
PHNM = 6041234567 # need to make some kinda input for this
NAME = "Maki"
WIDTH = 1000
HEIGHT = 800
COUNT = 0
BOTNUM = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
BALLNUM = 10
BALLCOL = []
for b in np.arange(BALLNUM):
    BALLCOL.append(np.random.randint(50, 256, size=3))

# initial positions, velocities
POSX = WIDTH * np.linspace(0.1, 0.9, BALLNUM)
POSY = HEIGHT * np.random.rand(BALLNUM)
VY = 0.5

# ---------------------------- INFORMATION------------------------------- #
def show_info():
    messagebox.showinfo(title="Info", message="By practicing clicking on the dots in that are in your contact's "
                                              "phone number, you will improve the connection between the brain "
                                              "and physical movements.")

# ---------------------------- INPUT PHONE NUMBER------------------------------- #
def add_more():
    messagebox.askquestion(title="Confirm Save", message="Number saved. Would you like to add more?")

def input():
    #Create a Toplevel window
    top = Toplevel()
    top.geometry("450x100")

    #Labels
    name_label = Label(top, text="Enter a name: ", font=(FONT_NAME, 15))
    name_label.grid(row=0, column=0)

    number_label = Label(top, text="Enter their phone number: ", font=(FONT_NAME, 15))
    number_label.grid(row=1, column=0)

    #Create an Entry Widget in the Toplevel window
    name_entry = Entry(top, width=25)
    name_entry.grid(row=0, column=1)

    number_entry = Entry(top, width=25)
    number_entry.grid(row=1, column=1)

    #BUTTON
    input_button = Button(top, text="Save", command=add_more)
    input_button.grid(row=2, column=0)

    done_button = Button(top, text="Done", command=top.destroy)
    done_button.grid(row=2, column=1)

# ---------------------------- GAME FUNCTIONALITY ------------------------------- #
def update():
    """
    moves balls down, if they go past the screen move
    them back to the top
    """
    global POSX, POSY, VY
    for p in np.arange(len(POSY)):
        if POSY[p] + VY >= HEIGHT:
            POSY[p] = 0
        else:
            POSY[p] += VY

def render(screen):
    """
    renders balls
    """

    # draw balls
    for b in np.arange(BALLNUM):
        font = pygame.font.SysFont(None, 42)
        img = font.render(str(b), True, (0, 0, 0))
        pygame.draw.circle(screen, BALLCOL[b], (POSX[b], POSY[b]), 50)
        screen.blit(img, (POSX[b] - 8, POSY[b] - 14))
    font2 = pygame.font.SysFont(None, 80)
    img2 = font2.render("".join(BOTNUM), True, (0, 0, 0))
    img3 = font2.render(NAME, True, (0, 0, 0))
    screen.blit(img2, (WIDTH / 2 - 180, HEIGHT - 180))
    screen.blit(img3,(WIDTH / 2 - 90, HEIGHT - 110))
    pygame.display.update()

def run_game():
    """
    runs poke-a-dot game.
    """
    global BOTNUM, COUNT
    ph_number = "{0}".format(PHNM)
    # initialize game
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    # run game
    running = True
    while running:

        pygame.mouse.set_visible(True)

        # white bg
        screen.fill((255, 255, 255))

        if ph_number == "":
            font3 = pygame.font.SysFont(None, 150)
            font4 = pygame.font.SysFont(None, 50)
            img = font3.render("Good Job!", True, (0, 0, 0))
            img2 = font4.render("+ 15 myelin. press space to restart.", True, (0,128,0))
            screen.blit(img, (WIDTH/5+25, HEIGHT/2 - 100))
            screen.blit(img2, (WIDTH / 7 + 60, HEIGHT / 2))
            pygame.display.update()
        else:
            # number we want to be clicked:
            num = ph_number[0]
            pos = [[x, y] for x, y in zip(POSX, POSY)]
            circ = pos[int(num)]

        for event in pygame.event.get():
            # close game
            if event.type == pygame.QUIT:
                running = False
            # check if right num clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # math lmfao
                sqx = (x - circ[0]) ** 2
                sqy = (y - circ[1]) ** 2
                if (sqx + sqy) < 2500:
                    # place num on screen
                    BOTNUM[COUNT] = num
                    render(screen)
                    # remove first number
                    ph_number = ph_number[1:]
                    COUNT += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("space")
                    BOTNUM = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
                    ph_number = str(PHNM)
                    COUNT = 0
        if ph_number != "":
            update()
            render(screen)

# ---------------------------- START GUI ------------------------------- #
window = Tk()
window.title("Poke-A-Dot")
window.config(bg="#f5f6f5")

# Image
logo = Canvas(width=400, height=400, bg="#f5f6f5", highlightthickness=0)
cursor_img = PhotoImage(file="cursor.png")
logo.create_image(200, 200, image=cursor_img)
logo.grid(row=1, column=1)

#Labels
title_label = Label(text="Poke-A-Dot", bg="#f7b844", font=(FONT_NAME, 50, "bold"), width=20)
title_label.grid(row=0, column=0, columnspan=3)

# Button
start_img = PhotoImage(file="start.png")
start_button = Button(text="START", image=start_img, command=run_game)
start_button.grid(row=2, column=1)

add_img = PhotoImage(file="add_button.png")
add_button = Button(text="ADD", image=add_img, command=input)
add_button.grid(row=3, column=1)

back_img = PhotoImage(file="back.png")
back_button = Button(text="BACK", image=back_img)
back_button.grid(row=2, column=0, padx=(40, 0))

help_button = Button(highlightthickness=0, command=show_info)
help_img = PhotoImage(file="help.png")
help_button.config(image=help_img)
help_button.grid(row=2, column=2, padx=(0, 40))

# Keep window on screen
window.mainloop()

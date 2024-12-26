import pygame
import cowsay
from time import sleep, time
from pickle import load, dump
from random import choice
from datetime import datetime
from math import floor 
import sys

user = input("Enter your username : ")
time_disp = datetime.now()
start_time = time()

cowsay.turtle(f"Hello {user}! \nWelcome to Human Vs A.I. TicTacToe Game :)")
sleep(1)

with open("info.dat", "ab") as file:
    pass

blue = {"bg" : (178, 171, 140), "fore" : (71, 89, 126)}
#green = {"bg" : (172, 216, 170), "fore" : (19, 117, 71)}
green = {"bg" : (66, 17, 60), "fore" : (55, 9, 38)}
on_hover = (44, 4, 28)
on_hover_text = (216,191,216)



board = [ [[], [], []], [[], [], []], [[], [], []] ]
l = ["11", "12", "13", "21", "22", "23", "31", "32", "33"]

def reset() :
    global board
    global l 
    board = [ [[], [], []], [[], [], []], [[], [], []] ]
    l = ["11", "12", "13", "21", "22", "23", "31", "32", "33"] 

def winn(board):

    uw = (user + " wins")
    aw = "A.I. wins"
    o = ["O", "O", "O"]
    x = ["X", "X", "X"]
    for i in range(3) :
        if board[i] == o :
            return uw
        elif board[i] == x :
            return aw
    for i in range(3) :
        if [board[0][i], board[1][i], board[2][i]] == o :
            return uw
        elif [board[0][i], board[1][i], board[2][i]] == x :
            return aw
    if [board[0][0], board[1][1], board[2][2]] == o :
        return uw 
    elif [board[0][0], board[1][1], board[2][2]] == x :
        return aw
    if [board[0][2], board[1][1], board[2][0]] == o :
        return uw 
    elif [board[0][2], board[1][1], board[2][0]] == x :
        return aw
    
    return False

def tie_check(board) :
    c = True
    for i in board :
        for j in i :
            if j == [] :
                c = False
    if c and not(winn(board)) :
        return "True"
    else :
        return "No"

def utility(board) :
    if winn(board) ==  (user + " wins"):
        return -1
    elif winn(board) == ("A.I. wins") :
        return 1
    if tie_check(board) == "True" :                    
        return 0

def valid_pos(board) :
    index = []
    for i in range(3) :
        for j in range(3) :
            if board[i][j]  == [] :
                index.append([i,j])
    return index
    

def copy_board(old) :
    new = []
    for i in range(len(old)) :
        new.append([])
    for i in range(len(old)) :
        new[i] = old[i].copy()
    return new
        

def minmax(board, depth) :   

    final_scores = []

    if winn(board) or (tie_check(board) == "True"):
        return utility(board)
    else :
        depth += 1
        v_pos = valid_pos(board)
        for i in v_pos :
            new_board = copy_board(board)
            if (depth%2 != 0) :
                new_board[i[0]][i[1]] = "X"
            elif (depth%2 == 0) :
                new_board[i[0]][i[1]] = "O"
            score = minmax(new_board, depth) 
            final_scores.append(score)

    if depth == 1:
        return final_scores
    elif (depth%2 != 0) and (depth != 1):
        return max(final_scores)
    elif depth%2 == 0:
        return min(final_scores)

def move_pos(score_list, val_pos) :
    for i in range(len(score_list)):
        if score_list[i] == max(score_list):
            break
    return val_pos[i]

click = ""

def ai_move2(l) :  #impossible
    first = 0
    first_dict = {"11": 22, "12": 11, "13": 22, "21": 11, "22": 11, "23": 13, "31": 22, "32": 12, "33": 22}
    for i in l :
        if i == "" :
            first += 1
    if first == 1 :
        move = str(first_dict[click])
        for i in range(len(l)) :
            if l[i] == move :
                l[i] = ""
        row = int(move[0]) - 1
        col = int(move[1]) - 1
        board[row][col] = "X"
        return move
    else :
        inp = ""
        score_list = minmax(board, 0)
        val_pos = valid_pos(board)
        move = move_pos(score_list, val_pos)
        inp = str(move[0]+1) + str(move[1]+1)
        
        row = move[0]
        col = move[1]
        board[row][col] = "X"

        for i in range(len(l)) :
            if l[i] == inp :
                l[i]= ""

        return inp

def ai_move1(l) :
    global board
    move = ""
    while move == "" :
        move = choice(l)
        
    row = int(move[0]) - 1
    col = int(move[1]) - 1
    board[row][col] = "X"
    
    for i in range(len(l)) :
        if l[i] == move :
            l[i] = ""
            
    return move

mode_ch = ""

def database() :

    notin = False
    
    with open("info.dat", "rb+") as file :
        
        # record format : {name: "username", curr_win : u_wins, curr_lose: ai_wins, totalW: "", totalL: "", for_board : {easy: easy_dict, medium: medum_dict, hard: hard_dict}}
        while True :
            try :
                pos = file.tell()
                rec = load(file)
                if rec["name"].lower() == user.lower() :
                    rec["curr_win"] = u_wins
                    rec["curr_lose"] = ai_wins
                    x = int(rec["totalW"] + u_wins)
                    rec["totalW"] = x
                    y = int(rec["totalL"] + ai_wins)
                    rec["totalL"] = y
                    rec["for_board"]["easy"]["wins"] += easy_lst["wins"]
                    rec["for_board"]["medium"]["wins"] += medium_lst["wins"]
                    rec["for_board"]["hard"]["wins"] += hard_lst["wins"]
                    rec["for_board"]["easy"]["loses"] += easy_lst["loses"]
                    rec["for_board"]["medium"]["loses"] += medium_lst["loses"]
                    rec["for_board"]["hard"]["loses"] += hard_lst["loses"]
                    file.seek(pos)
                    dump(rec, file)
                    return rec
            except :
                rec = {"name": user, "curr_win" : u_wins, "curr_lose": ai_wins, "totalW": u_wins, "totalL": ai_wins, "for_board": {"easy": easy_lst, "medium": medium_lst, "hard": hard_lst}}
                notin = True
                break
                
    if notin : 
        with open("info.dat", "ab+") as file :
            dump(rec, file)
            return rec
        
def leader_display() :
    with open("info.dat", "rb+") as file :
        final_dict = {}
        try :
            while True :
                rec = load(file)
                total = rec["totalW"] + rec["totalL"]
                final_dict[rec["name"]] = [total, rec["for_board"]]
        except :
            pass

        leaders = {}
        all_scores = [final_dict[i][0] for i in final_dict]
        all_scores = sorted(all_scores)
        if len(all_scores) >= 3 :
            count = 3
        else :
            count = len(all_scores)
        for i in range(count) :
            check = all_scores.pop()
            for record in final_dict :
                if final_dict[record][0] == check :
                    leaders[record] = final_dict[record]
        return leaders

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("TicTacToe")
#icon = pygame.image.load("logo.png")
#pygame.display.set_icon(icon)


class button :
    
    def __init__(self, color, x, y, width, height, tag, text = "", text_col = (255, 255, 255)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.tag = tag
        self.text_col = text_col


    def draw(self,win):
        #Call this method to draw the button on the screen
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('yellowtail', 30)
            text = font.render(self.text, 1, self.text_col)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))  #centers the text in the button

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def onClick(self, newtext) :
        self.text = newtext

class back_to_mode(button) :

    def __init__(self, color, x, y, width, height, tag, text, text_col = (255, 255, 255)):
        super().__init__(color, x, y, width, height, tag, text=text, text_col=text_col)

    def onClick(self):
        global u_wins
        global ai_wins
        global count_rec
        global tie_count
        global easy_lst
        global medium_lst
        global hard_lst
        u_wins = 0
        ai_wins = 0
        count_rec = 0
        tie_count = 0
        easy_lst = {"wins" : 0, "loses" : 0}
        medium_lst = {"wins" : 0, "loses" : 0}
        hard_lst = {"wins" : 0, "loses" : 0}
        main()

class leader_board(button) :

    def __init__(self, color, x, y, width, height, tag, text, text_col = (255, 255, 255)):
        super().__init__(color, x, y, width, height, tag, text=text, text_col=text_col)
    
    def onClick(self):
        data = leader_display()
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        for players in data :
            first = "Wins : " + str(data[players][1]["easy"]["wins"]) + ", Loses : " + str(data[players][1]["easy"]["loses"])
            second = "Wins : " + str(data[players][1]["medium"]["wins"]) + ", Loses : " + str(data[players][1]["medium"]["loses"])
            third = "Wins : " + str(data[players][1]["hard"]["wins"]) + ", Loses : " + str(data[players][1]["hard"]["loses"])
            print(f"{players} :\n   Total Conclusive Games Played = {data[players][0]}\n   Easy Mode :- {first}\n   Medium Mode :- {second}\n   Impossible :- {third}")
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        print()


easy = button(green["fore"], 45, 235, 60, 33, "1", "Easy")
med = button(green["fore"], 200, 235, 95, 33, "2", "Medium")
imp = button(green["fore"], 350, 235, 125, 33, "3", "Impossible")
mode_list = [easy, med, imp]

mode_button = back_to_mode(green["fore"], 30, 400, 70, 33, "mode-page", "Modes")
leaderboard = leader_board(green["fore"], 340, 400, 130, 33, "leader", "LeaderBoard")
leader_for_mode = leader_board(green["fore"], 182.5, 400, 130, 33, "leader", "LeaderBoard")
    

def mode() :
    win.fill(green["bg"])
    font = pygame.font.SysFont('arvo', 30)
    text = font.render("Choose a Mode", 1, (255, 255, 255))
    win.blit(text, (180, 150))
    easy.draw(win)
    med.draw(win)
    imp.draw(win)
    leader_for_mode.draw(win)



u_wins = 0
ai_wins = 0
count_rec = 0
tie_count = 0
easy_lst = {"wins" : 0, "loses" : 0}
medium_lst = {"wins" : 0, "loses" : 0}
hard_lst = {"wins" : 0, "loses" : 0}



def main() :
    
    global u_wins
    global ai_wins
    global click
    global tie_count
    global mode_ch
    global easy_lst
    global medium_lst
    global hard_lst
    global mode_button
    global dont_hurt_database
    
         
    def redraw_window() :
        win.fill(green["bg"])
        movebutton11.draw(win)
        movebutton12.draw(win)
        movebutton13.draw(win)
        movebutton21.draw(win)
        movebutton22.draw(win)
        movebutton23.draw(win)
        movebutton31.draw(win)
        movebutton32.draw(win)
        movebutton33.draw(win)
        if tie_check(board) == "True":
            font = pygame.font.SysFont('arvo', 30)
            text = font.render("It's a Tie", 1, (255, 255, 255))
            win.blit(text, (225, 400))
            cont.draw(win)
            close.draw(win)
            
        if winn(board) :
            font = pygame.font.SysFont('arvo', 30)
            text = font.render(winn(board), 1, (255, 255, 255))
            win.blit(text, (200, 390))
            cont.draw(win)
            close.draw(win)
            
    def redraw_final() :
        global count_rec
        global data
        global hour
        global mint
        global sec
        win.fill(green["bg"])
        if dont_hurt_database == 0 :
            data = database()
            total_time = time() - start_time
            hour = floor(total_time // 3600)
            mint = floor(total_time // 60)
            if mint >= 60 :
                mint -= (hour*60)
            sec = floor(total_time)
            if sec >= 3600 :
                sec -= (hour*3600)
            if sec >= 60 :
                sec -= (mint*60)
        line1 = f'No. of times you won in this round: {data["curr_win"]}'
        line2 = f'No. of times A.I. won in this round: {data["curr_lose"]}'
        line3 = f'Total no. of times you have won: {data["totalW"]}'
        line4 = f'Total no. of times A.I. has won: {data["totalL"]}'
        ties = f'No. of ties: {tie_count}'
        
        time_play = f"Time played : {hour}:{mint}:{sec}"
        show_time = f"Time of login : {time_disp.hour}:{time_disp.minute}:{time_disp.second}"
        font = pygame.font.SysFont('arvo', 30)
        text1 = font.render(line1, 1, (255, 255, 255))
        text2 = font.render(line2, 1, (255, 255, 255))
        text3 = font.render(line3, 1, (255, 255, 255))
        text4 = font.render(line4, 1, (255, 255, 255))
        tiess = font.render(ties, 1, (255, 255, 255))
        show_times = font.render(show_time, 1, (255, 255, 255))
        show_dur = font.render(time_play, 1, (255, 255, 255))
        win.blit(text1, (90, 120))
        win.blit(text2, (90, 150))
        win.blit(tiess, (90, 180))
        win.blit(text3, (90, 210))
        win.blit(text4, (90, 240))
        win.blit(show_times, (90, 270))
        win.blit(show_dur, (90, 300))
        mode_button.draw(win)
        leaderboard.draw(win)
        count_rec += 1
            

    movebutton11 = button(green["fore"], 145, 165, 50, 30, "11")
    movebutton12 = button(green["fore"], 225, 165, 50, 30, "12")
    movebutton13 = button(green["fore"], 305, 165, 50, 30, "13")
    movebutton21 = button(green["fore"], 145, 225, 50, 30, "21")
    movebutton22 = button(green["fore"], 225, 225, 50, 30, "22")
    movebutton23 = button(green["fore"], 305, 225, 50, 30, "23")
    movebutton31 = button(green["fore"], 145, 285, 50, 30, "31")
    movebutton32 = button(green["fore"], 225, 285, 50, 30, "32")
    movebutton33 = button(green["fore"], 305, 285, 50, 30, "33")
    cont = button(green["fore"], 10, 450, 105, 41, "", "Continue")
    close = button(green["fore"], 410, 450, 75, 41, "", "Exit")
    but_list = [movebutton11, movebutton12, movebutton13, movebutton21, movebutton22, movebutton23, movebutton31, movebutton32, movebutton33]
    exit_list = [cont, close]

    run = True
    closed = False
    count = 0
    mode_ch = ""
    med_count = 1
    dont_hurt_database = 0



    while run :

        if mode_ch == "" :

            for i in mode_list :
                pos = pygame.mouse.get_pos()
                
                if leader_for_mode.isOver(pos) :
                    leader_for_mode.color = on_hover
                    leader_for_mode.text_col = on_hover_text
                else :
                    leader_for_mode.color = green["fore"]
                    leader_for_mode.text_col = (255, 255, 255)

                if i.isOver(pos) :
                    i.color = on_hover
                    i.text_col = on_hover_text
                else :
                    i.color = green["fore"] 
                    i.text_col = (255, 255, 255)
            
            
            mode()
            pygame.display.update()

            
            for event in pygame.event.get() :

                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT :
                    run = False
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN :
                    
                    if easy.isOver(pos) :
                        mode_ch = easy.tag

                    if med.isOver(pos) :
                        mode_ch = med.tag

                    if imp.isOver(pos) :
                        mode_ch = imp.tag
                    
                    if leader_for_mode.isOver(pos) :
                        leader_for_mode.onClick()
                
        
        else : 
        
            while closed :

                redraw_final()

                dont_hurt_database += 1

                pygame.display.update()

                pos = pygame.mouse.get_pos()

                if mode_button.isOver(pos) :
                    mode_button.color = on_hover
                    mode_button.text_col = on_hover_text
                else :
                    mode_button.color = green["fore"]
                    mode_button.text_col = (255, 255, 255)

                if leaderboard.isOver(pos) :
                    leaderboard.color = on_hover
                    leaderboard.text_col = on_hover_text
                else :
                    leaderboard.color = green["fore"]
                    leaderboard.text_col = (255, 255, 255)

                for event in pygame.event.get() :
                    pos = pygame.mouse.get_pos()
                
                    if event.type == pygame.QUIT :
                        run = False
                        pygame.quit()
                        sys.exit()

                    
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if mode_button.isOver(pos) :
                            closed = False
                            reset()
                            mode_button.onClick()
                        if leaderboard.isOver(pos) :
                            leaderboard.onClick()

            else :
                redraw_window()
                
            pygame.display.update()


            if (click != "") :
                if (len(valid_pos(board)) > 1) and (not winn(board)) and (tie_check(board) == "No"):
                    if mode_ch == "1" :
                        ai = ai_move1(l)
                    elif mode_ch == "2" :
                        if med_count%2 != 0 :
                            ai = ai_move2(l)
                            med_count += 1
                        else :
                            ai = ai_move1(l)
                            med_count += 1
                    elif mode_ch == "3" :
                        ai = ai_move2(l)
                    for i in range(len(but_list)) :
                        if but_list[i].tag == ai :
                            but_list[i].onClick("X")

            click = ""

            for j in [but_list, exit_list] :
                for i in j :
                    pos = pygame.mouse.get_pos()
                    if i.isOver(pos) :
                        i.color = on_hover
                        i.text_col = on_hover_text
                    else :
                        i.color = green["fore"]
                        i.text_col = (255, 255, 255)


            for event in pygame.event.get() :

                pos = pygame.mouse.get_pos()
                
                if event.type == pygame.QUIT :
                    run = False
                    pygame.quit()

                    
                if event.type == pygame.MOUSEBUTTONDOWN :

                    if (winn(board) == False) and (tie_check(board) != "True") : 
                    
                        for ele in but_list :
                            if ele.tag in l :
                                if ele.isOver(pos) :
                                    ele.onClick("O")
                                    click = ele.tag
                                
     
                    if (tie_check(board) == "True") or winn(board) :
                        if cont.isOver(pos) :
                            reset()
                            main()

                        if close.isOver(pos) :
                            closed = True
                            
            if count_rec == 1:        
                run = False
                                                    
            
            if (click != "") :

                row = int(click[0]) - 1
                col = int(click[1]) - 1
                board[row][col] = "O"

                for i in range(len(l)) :
                    if l[i] == click :
                        l[i] = ""
                            
            if (not closed) :
                if winn(board) :
                    if count == 0  :
                        if winn(board) == user + " wins" :
                            u_wins += 1
                            if mode_ch == "1" :
                                easy_lst["wins"] += 1
                            elif mode_ch == "2" :
                                medium_lst["wins"] += 1
                            elif mode_ch == "3" :
                                hard_lst["wins"] += 1
                        elif winn(board) == "A.I. wins" :
                            ai_wins += 1
                            if mode_ch == "1" :
                                easy_lst["loses"] += 1
                            elif mode_ch == "2" :
                                medium_lst["loses"] += 1
                            elif mode_ch == "3" :
                                hard_lst["loses"] += 1
                        count += 1

                if tie_check(board) == "True":
                    if count == 0 :
                        count += 1
                        tie_count += 1                  


exc = True

if __name__ == "__main__" :
    main()

    while exc :
        
        for event in pygame.event.get() :
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT :
                exc = False
                pygame.quit()

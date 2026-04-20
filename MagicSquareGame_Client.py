import socket

def start_server():
    s = socket.socket()
    s.bind(("0.0.0.0", 9999))
    s.listen(1)
    print("Waiting for connection...")
    conn, addr = s.accept()
    print("Connected to", addr)
    return conn

def start_client():
    s = socket.socket()
    s.connect(("localhost", 9999))
    print("Connected to server")
    return s

def get_move(conn, my_turn):
    if my_turn:
        pos = int(input("Enter position: ")) - 1
        num = int(input("Enter number: "))
        conn.send(f"{pos},{num}".encode())
    else:
        print("Waiting for opponent...")
        data = conn.recv(1024).decode()
        pos, num = map(int, data.split(","))
    return pos, num

def ShowGrid(grid,n):
    x=0
    print()
    for i in range(n):
        for j in range(n):
            if grid[x]=="":
                print("  .  ",end=" ")
            else:
                print(grid[x],end=" ")
            x+=1
        print("\n")


def WinCondition(grid,n):

    #rows
    for i in range(n):
        total=0
        player=""
        same=True
        empty=False

        for j in range(n):
            cell=grid[i*n+j]

            if cell=="":
                empty=True
                break

            cellparts=cell.split("_")

            if player=="":
                player=cellparts[0]
            elif player!=cellparts[0]:
                same=False

            total+=int(cellparts[1])

        if total==15 and same==True and empty==False:
            return True

    #columns
    for j in range(n):
        total=0
        player=""
        same=True
        empty=False

        for i in range(n):
            cell=grid[i*n+j]

            if cell=="":
                empty=True
                break

            cellparts=cell.split("_")

            if player=="":
                player=cellparts[0]
            elif player!=cellparts[0]:
                same=False

            total+=int(cellparts[1])

        if total==15 and same==True and empty==False:
            return True

    #diagonal 1
    total=0
    player=""
    same=True
    empty=False

    for i in range(n):
        cell=grid[i*n+i]

        if cell=="":
            empty=True
            break

        cellparts=cell.split("_")

        if player=="":
            player=cellparts[0]
        elif player!=cellparts[0]:
            same=False

        total+=int(cellparts[1])

    if total==15 and same==True and empty==False:
        return True

    #diagonal 2
    total=0
    player=""
    same=True
    empty=False

    for i in range(n):
        cell=grid[i*n+(n-1-i)]

        if cell=="":
            empty=True
            break

        cellparts=cell.split("_")

        if player=="":
            player=cellparts[0]
        elif player!=cellparts[0]:
            same=False

        total+=int(cellparts[1])

    if total==15 and same==True and empty==False:
        return True

    return False

def Play(conn, is_host):
    if is_host:
        n = int(input("Enter grid size: "))
        conn.send(str(n).encode())
    else:
        n = int(conn.recv(1024).decode())

    grid=[]
    for i in range(n*n):
        grid.append("")
    usednos=[]
    player=1

    while True:
        ShowGrid(grid,n)
        print("Player",player)

        my_turn = (player == 1 and is_host) or (player == 2 and not is_host)
        pos, num = get_move(conn, my_turn)

        if pos<0 or pos>=n*n:
            print("Wrong position")
            continue

        if grid[pos]!="":
            print("Already filled")
            continue

        if num in usednos:
            print("Number used")
            continue

        grid[pos]="U"+str(player)+"_"+str(num)
        usednos.append(num)

        #win
        if WinCondition(grid,n):
            ShowGrid(grid,n)
            print("Player",player,"wins!")
            break

        #draw
        if "" not in grid:
            ShowGrid(grid,n)
            print("Draw!")
            break

        #pc
        if player==1:
            player=2
        else:
            player=1


conn = start_client()
Play(conn, False)

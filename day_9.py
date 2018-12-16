def day9():
    from collections import deque

    nplayer = 435
    last_marble_worth = 71184 * 100  # remove the *100 for part 1

    playerscores = [0] * nplayer
    player = -1

    marblecircle = deque([])

    for marblenr in range(last_marble_worth + 1):
        player = (player + 1) % nplayer
        if (marblenr % 23) == 0 and (marblenr != 0):
            playerscores[player] += marblenr
            marblecircle.rotate(7)
            playerscores[player] += marblecircle.pop()
            marblecircle.rotate(-1)
        else:
            marblecircle.rotate(-1)
            marblecircle.append(marblenr)

    print(max(playerscores))



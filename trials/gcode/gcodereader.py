import numpy as np

np.set_printoptions(suppress=True, precision=2, floatmode="fixed")
file = open(r"trials\gcode\3DBenchy_0.2mm_PLA_MEGA0_1h48m.gcode")

absmove = True
absextrude = True
currentpos = np.zeros(4, float)
queue = []
speed = 0
i = 0
for line in file:
    line = line.split(";")[0]
    line = line.rstrip()
    if line:
        line = line.split(" ")
        match line[0]:
            case "G0" | "G1":
                newpos = np.zeros(4, float)
                if absmove:
                    newpos[:3] = currentpos[:3]
                if absextrude:
                    newpos[3] = currentpos[3]
                for param in line[1:]:
                    match param[0]:
                        case "X":
                            newpos[0] = float(param[1:])
                        case "Y":
                            newpos[1] = float(param[1:])
                        case "Z":
                            newpos[2] = float(param[1:])
                        case "E":
                            newpos[3] = float(param[1:])
                        case "F":
                            speed = float(param[1:])
                        case _:
                            raise ValueError(f"Unknown parameter in command {line}")
                move = np.zeros(5, float)
                if absmove:
                    move[:3] = newpos[:3] - currentpos[:3]
                    currentpos[:3] = newpos[:3]
                else:
                    move[:3] = newpos[:3]
                    currentpos[:3] += newpos[:3]
                if absextrude:
                    move[3] = newpos[3] - currentpos[3]
                    currentpos[3] = newpos[3]
                else:
                    move[3] = newpos[3]
                    currentpos[3] += newpos[3]
                move[4] = speed
                if any(move[0:4]):
                    queue.append(move)
            case "G2":
                pass
            case "G3":
                pass
            case "G21":
                pass
            case "G28":
                move = np.zeros(5, float)
                move[4] = 6000
                if len(line) == 1:
                    move[:3] = -currentpos[:3]
                    currentpos[:3] = [0, 0, 0]
                else:
                    for param in line[1:]:
                        match param[0]:
                            case "X":
                                move[0] = -currentpos[0] + float(param[1:])
                                currentpos[0] = float(param[1:])
                            case "Y":
                                move[1] = -currentpos[1] + float(param[1:])
                                currentpos[1] = float(param[1:])
                            case "Z":
                                move[2] = -currentpos[2] + float(param[1:])
                                currentpos[2] = float(param[1:])
                if any(move[:3]):
                    queue.append(move)
            case "G90":
                absmove = True
                absextrude = True
            case "G91":
                absmove = False
                absextrude = False
            case "G92":
                for param in line[1:]:
                    match param[0]:
                        case "X":
                            currentpos[0] = float(param[1:])
                        case "Y":
                            currentpos[1] = float(param[1:])
                        case "Z":
                            currentpos[2] = float(param[1:])
                        case "E":
                            currentpos[3] = float(param[1:])
                        case _:
                            raise ValueError(f"Unknown parameter in command {line}")
            case "M82":
                absextrude = True
            case "M83":
                absextrude = False
            case "M84":
                pass
            case "M104":
                pass
            case "M106":
                pass
            case "M107":
                pass
            case "M109":
                pass
            case "M117":
                # print(" ".join(line[1:]))
                pass
            case "M190":
                pass
            case "M300":
                pass
            case _:
                raise ValueError(f"Unknown command {line[0]}")
pos = np.zeros(4, float)
for move in queue:
    pos += move[:4]
    # print(move)
print(pos)

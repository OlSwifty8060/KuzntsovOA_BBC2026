
import random

SIZE = 5
ROOM_TYPES = ["пусто", "сундук", "монстр", "ловушка", "портал"]
LOOT = ["золото", "зелье", "меч", "щит", "карта"]
ICONS = {"пусто": "⬜️", "сундук": "📦", "монстр": "👹", "ловушка": "⚠️",
         "портал": "🌀", "ключ": "🔑", "старт": "🏁", "выход": "🚪"}


def generate_maze(size):
    maze = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append({"type": random.choice(ROOM_TYPES), "visited": False})
        maze.append(row)

    maze[0][0]["type"] = "старт"
    maze[size - 1][size - 1]["type"] = "выход"

    # ключ в случайную комнату
    while True:
        kx = random.randint(0, size - 1)
        ky = random.randint(0, size - 1)
        if maze[kx][ky]["type"] != "старт" and maze[kx][ky]["type"] != "выход":
            maze[kx][ky]["type"] = "ключ"
            break

    return maze


def show_map(maze, pos, reveal=False):
    for i in range(len(maze)):
        line = ""
        for j in range(len(maze[i])):
            room = maze[i][j]
            if [i, j] == pos:
                line = line + "🧍"
            elif room["visited"] or reveal:
                line = line + ICONS[room["type"]]
            else:
                line = line + "❓"
        print(line)


def drink_potion(state):
    if "зелье" in state["inv"]:
        state["inv"].remove("зелье")
        state["hp"] = state["hp"] + 30
        if state["hp"] > 100:
            state["hp"] = 100
        print("+30 HP")
        return True
    else:
        print("Нет зелья!")
        return False


def fight(state):
    monster_hp = random.randint(20, 40)
    print("Монстр! У него", monster_hp, "HP")

    while monster_hp > 0 and state["hp"] > 0:
        print("Монстр:", monster_hp, "HP | Вы:", state["hp"], "HP")
        action = input("1 - атака, 2 - зелье, 3 - бежать: ")

        if action == "1":
            dmg = random.randint(5, 15)
            if "меч" in state["inv"]:
                dmg = dmg + 5
            monster_hp = monster_hp - dmg
            print("Вы нанесли", dmg, "урона")
        elif action == "2":
            drink_potion(state)
        elif action == "3":
            if random.random() < 0.5:
                print("Вы сбежали!")
                return
            else:
                print("Не удалось сбежать!")
        else:
            continue

        if monster_hp > 0:
            hit = random.randint(5, 12)
            if "щит" in state["inv"]:
                hit = hit - 3
                if hit < 1:
                    hit = 1
            state["hp"] = state["hp"] - hit
            print("Монстр бьёт на", hit)

    if state["hp"] > 0:
        print("Монстр побеждён! Выпало: золото")
        state["inv"].append("золото")


def enter_room(maze, state):
    x = state["pos"][0]
    y = state["pos"][1]
    room = maze[x][y]

    if room["visited"] == True:
        return
    room["visited"] = True
    kind = room["type"]
    print("\n>>> Комната:", kind)

    if kind == "сундук":
        count = random.randint(1, 3)
        items = random.sample(LOOT, count)
        print("В сундуке:", items)
        for item in items:
            state["inv"].append(item)
    elif kind == "ключ":
        print("Вы нашли ключ!")
        state["inv"].append("ключ")
    elif kind == "ловушка":
        dmg = random.randint(10, 25)
        if "щит" in state["inv"]:
            dmg = dmg // 2
            print("Щит смягчил удар!")
        state["hp"] = state["hp"] - dmg
        print("Ловушка! -", dmg, "HP")
    elif kind == "монстр":
        fight(state)
    elif kind == "портал":
        state["pos"] = [random.randrange(SIZE), random.randrange(SIZE)]
        print("Портал телепортировал вас!")
        enter_room(maze, state)


def inventory_menu(state):
    while True:
        print("\nИнвентарь:", state["inv"])
        c = input("1 - сортировать, 2 - выбросить, 3 - выпить зелье, 0 - назад: ")

        if c == "1":
            state["inv"].sort()
        elif c == "2":
            name = input("Что выбросить? ")
            if name in state["inv"]:
                state["inv"].remove(name)
            else:
                print("Нет такого предмета")
        elif c == "3":
            drink_potion(state)
        elif c == "0":
            return


def main():
    maze = generate_maze(SIZE)
    state = {"hp": 100, "inv": [], "pos": [0, 0]}
    maze[0][0]["visited"] = True

    print("Найдите ключ 🔑 и выйдите через дверь 🚪!")

    while True:
        print()
        show_map(maze, state["pos"])
        print("HP:", state["hp"], "| Инвентарь:", len(state["inv"]), "предм.")

        cmd = input("w/a/s/d - идти, i - инвентарь, m - карта (если есть), q - выйти: ")
        cmd = cmd.lower()

        if cmd == "q":
            print("Выход из игры.")
            return
        elif cmd == "i":
            inventory_menu(state)
            continue
        elif cmd == "m":
            if "карта" in state["inv"]:
                show_map(maze, state["pos"], True)
            else:
                print("У вас нет карты!")
            continue

        # движение
        if cmd == "w":
            dx = -1
            dy = 0
        elif cmd == "s":
            dx = 1
            dy = 0
        elif cmd == "a":
            dx = 0
            dy = -1
        elif cmd == "d":
            dx = 0
            dy = 1
        else:
            print("Неизвестная команда")
            continue

        nx = state["pos"][0] + dx
        ny = state["pos"][1] + dy

        if nx < 0 or nx >= SIZE or ny < 0 or ny >= SIZE:
            print("Там стена!")
            continue

        state["pos"] = [nx, ny]
        enter_room(maze, state)

        if state["hp"] <= 0:
            print("\nВы погибли... GAME OVER 💀")
            return

        x = state["pos"][0]
        y = state["pos"][1]
        if maze[x][y]["type"] == "выход":
            if "ключ" in state["inv"]:
                gold = state["inv"].count("золото")
                print("\nВы открыли дверь и сбежали! 🎉 Золота:", gold)
                return
            else:
                print("Дверь заперта. Найдите ключ!")



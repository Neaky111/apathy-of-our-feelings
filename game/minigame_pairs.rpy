init python:
    successfully_init = False

    game_pairs_win = False

    card_image_width = 128 # Ширина изображения
    card_image_height = 128 # Высота изображения

    card_xzoom = card_image_width / 2000.0 # Увеличение изображения по оси x
    card_yzoom = card_image_height / 2000.0 # Увеличение изображения по оси y

    card_in_row = 2 # Количество карточек в строке
    card_in_col = 2 # Количество карточек в столбце

    dir_card_images = "images/pair_cards" # Папка с изображениями карточек
    shirt_card_name = "card_shirt"

    card_margin = 4 # Отступы между карточками

    can_click = True

    all_card_list = []
    card_list = []

    wait = 0.5

    max_time = 60

    for file in renpy.list_files():
        if file.startswith(dir_card_images + "/" + "card_") and file.endswith(".png"):
            name = file[len(dir_card_images) + 1:-4]
            renpy.image("card " + name, file)
            if name != shirt_card_name:
                all_card_list.append(name)

    def init_cards():
        global card_list

        renpy.random.shuffle(all_card_list)
        selected_cards = all_card_list[:(card_in_row * card_in_col) / 2]

        if len(selected_cards) < (card_in_row * card_in_col) / 2:
            print("error init cards")

        card_list = selected_cards + selected_cards
        renpy.random.shuffle(card_list)

    def setup():
        init_cards()

label game_pairs:
    $ setup()

    $ cards = []
    $ pair_timer = max_time
    
    python:
        for i in range (0, len(card_list) ):
            cards.append({"c_number": i, "c_value": card_list[i], "c_chosen": False})

    show screen game_pairs_screen

    label game_pairs_loop:
        $ can_click = True
        $ turned_cards_numbers = []
        $ turned_cards_values = []
        $ turns_left = 2

        label turns_loop:
            if turns_left > 0:
                $ result = ui.interact()
                $ pair_timer = pair_timer
                $ turned_cards_numbers.append (cards[result]["c_number"])
                $ turned_cards_values.append (cards[result]["c_value"])
                $ turns_left -= 1
                jump turns_loop
        $ can_click = False
        if turned_cards_values.count(turned_cards_values[0]) != len(turned_cards_values):
            $ renpy.pause (wait, hard = True)
            python:
                for i in range (0, len(turned_cards_numbers) ):
                    cards[turned_cards_numbers[i]]["c_chosen"] = False
        else:
            $ renpy.pause (wait, hard = True)
            python: 
                for i in range (0, len(turned_cards_numbers) ):
                    cards[turned_cards_numbers[i]]["c_value"] = cards[turned_cards_numbers[i]]["c_value"]
                for j in cards:
                    if j["c_chosen"] == False:
                        renpy.jump ("game_pairs_loop")
                renpy.jump ("pair_game_win")
        jump game_pairs_loop

label pair_game_win:
    hide screen game_pairs_screen
    $ renpy.pause (0.1, hard = True)
    centered "Нихуя крутой!"
    $ game_pairs_win = True
    return
    

label pair_game_lose:
    hide screen game_pairs_screen
    $ renpy.pause (0.1, hard = True)
    centered "Нихуя не крутой!"
    $ game_pairs_win = False
    return

screen game_pairs_screen:

    timer 1.0 action If (pair_timer > 1, SetVariable("pair_timer", pair_timer - 1), Jump("pair_game_lose") ) repeat True

    grid card_in_row card_in_col:
        align (.5, .5)
        for card in cards:
            button:
                left_padding card_margin
                right_padding card_margin
                top_padding card_margin
                bottom_padding card_margin
                background None
                if card["c_chosen"]:
                    add "card " + card["c_value"] xzoom card_xzoom yzoom card_yzoom
                else:
                    add "card card_shirt" xzoom card_xzoom yzoom card_yzoom
            
                action If(
                    (card["c_chosen"] or not can_click), 
                    true = None, 
                    false = [SetDict(cards[card["c_number"]], "c_chosen", True), Return(card["c_number"])]
                )
    
    text str(pair_timer) xalign .2 yalign 0.2 size 30
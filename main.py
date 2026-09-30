import os
import sys
from pathlib import Path


# Quand le jeu est compilé en .exe,
# on utilise le dossier de l'exécutable
# comme dossier de travail.
if getattr(sys, "frozen", False):
    os.chdir(
        Path(sys.executable).resolve().parent
    )

import pygame
try:
    from admin import AdminPanel

    ADMIN_AVAILABLE = True

except ImportError:

    ADMIN_AVAILABLE = False
from multiplayer.hub_multiplayer import HubMultiplayer
from network.client import NetworkClient
from network.config import SERVER_URL
from games.uno.uno_online import UnoOnline
from multiplayer.lobby import MultiplayerLobby
from player import Player
from mainmenu import MainMenu
from hub import Hub
from stats import StatsManager
from profiles import Profile
from friends import FriendsMenu
from friend_profile import FriendProfile
from arcade import Arcade
from games.uno.uno_game import UnoGame
from progression import ProgressionManager
# --------------------------------
# INITIALISATION
# --------------------------------

pygame.init()


WIDTH = 1280
HEIGHT = 720
FPS = 60


screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption(
    "Game Hub"
)


game_surface = pygame.Surface(
    (WIDTH, HEIGHT)
)


clock = pygame.time.Clock()

font = pygame.font.Font(
    None,
    40
)

hub_network_timer = 0.0

HUB_NETWORK_RATE = 0.10
# --------------------------------
# OBJETS
# --------------------------------
stats = StatsManager()
character_id = (
    stats.data
    .get("profile", {})
    .get(
        "character",
        "pink_girl"
    )
)

player = Player(
    640,
    360,
    character_id
)


main_menu = MainMenu()

hub = Hub(player)


progression = ProgressionManager(
    stats
)
if ADMIN_AVAILABLE:

    admin_panel = AdminPanel(
        stats,
        progression
    )

else:

    admin_panel = None
profile = Profile(
    stats,
    progression
)

friends_menu = FriendsMenu()

friend_profile = FriendProfile()

arcade = Arcade(stats)

uno_game = UnoGame(progression)

# --------------------------------
# ETAT DU JEU
# --------------------------------
active_game = None
state = "main_menu"
return_state = "main_menu"
running = True

player_name = (
    stats.data
    .get(
        "profile",
        {}
    )
    .get(
        "display_name",
        "Player"
    )
)
profile_data = stats.data.get(
    "profile",
    {}
)

player_name = profile_data.get(
    "display_name",
    "Player"
)

player_character = profile_data.get(
    "character",
    "pink_girl"
)
network_client = NetworkClient(
    SERVER_URL,
    player_name,
    player_character
)

network_client.start()
hub_multiplayer = HubMultiplayer(
    network_client
)
uno_online = UnoOnline(
    network_client
)
multiplayer_lobby = (
    MultiplayerLobby(
        network_client
    )
)
# --------------------------------
# POSITION SOURIS
# --------------------------------
def get_player_network_data(
    player
):

    if hasattr(
        player,
        "x"
    ):

        x = player.x
        y = player.y

    else:

        x = player.position.x
        y = player.position.y


    direction = getattr(
        player,
        "direction",
        "down"
    )


    movement_state = getattr(
        player,
        "state",
        "idle"
    )


    return (
        x,
        y,
        direction,
        movement_state
    )
def get_game_mouse_pos():

    mouse_x, mouse_y = (
        pygame.mouse.get_pos()
    )

    window_width, window_height = (
        screen.get_size()
    )


    game_x = (
        mouse_x
        * WIDTH
        / window_width
    )

    game_y = (
        mouse_y
        * HEIGHT
        / window_height
    )


    return (
        game_x,
        game_y
    )


# --------------------------------
# ECRAN TEMPORAIRE
# --------------------------------

def draw_placeholder(
    screen,
    title
):

    screen.fill("#171923")


    title_text = font.render(
        title,
        True,
        "white"
    )

    title_rect = (
        title_text.get_rect(
            center=(640, 300)
        )
    )

    screen.blit(
        title_text,
        title_rect
    )


    back_text = font.render(
        "ESC pour revenir",
        True,
        "#aaaaaa"
    )

    back_rect = (
        back_text.get_rect(
            center=(640, 380)
        )
    )

    screen.blit(
        back_text,
        back_rect
    )


# --------------------------------
# BOUCLE PRINCIPALE
# --------------------------------

while running:

    dt = clock.tick(FPS) / 1000

    network_events = network_client.update()
    if state == "uno_online":

        uno_online.update(
            dt
        )
    for network_event in network_events:
        if (
            network_event.get("type")
            == "game_ended"
        ):

            state = "multiplayer"
        if (
            network_event.get("type")
            == "uno_restarted"
        ):

            state = "uno_online"
        if (
            network_event.get("type")
            == "game_started"
            and network_event.get("game")
            == "uno"
        ):

            state = "uno_online"

    stats.update()


    mouse_pos = (
        get_game_mouse_pos()
    )


    # --------------------------------
    # EVENTS
    # --------------------------------

    for event in pygame.event.get():
        if (
            event.type == pygame.KEYDOWN
            and event.key in (pygame.K_F10, pygame.K_l)
            and admin_panel is not None
        ):

            admin_panel.toggle()

            continue
        if (
            admin_panel is not None
            and admin_panel.open
        ):

            admin_panel.handle_event(
                event,
                mouse_pos
            )

            continue
        if event.type == pygame.QUIT:

            running = False


        # --------------------------------
        # MAIN MENU
        # --------------------------------
        if state == "hub":
            hub_multiplayer.update(
                dt
            )
            hub_network_timer += dt

            if (
                hub_network_timer
                >= HUB_NETWORK_RATE
            ):

                hub_network_timer = 0.0
                x, y, direction, movement_state = (
                    get_player_network_data(
                        player
                    )
                )


                network_client.send_hub_position(
                    x,
                    y,
                    direction,
                    movement_state
                )
        if state == "main_menu":

            action = (
                main_menu.handle_event(
                    event,
                    mouse_pos
                )
            )
            if action == "multiplayer":

                state = "multiplayer"

            elif action == "play":

                state = "hub"

                x, y, _, _ = (
                    get_player_network_data(
                        player
                    )
                )

                network_client.enter_hub(
                    x,
                    y
                )
                

            elif action == "profile":

                return_state = "main_menu"

                state = "profile"


            elif action == "friends":

                return_state = "main_menu"

                state = "friends"


            elif action == "options":

                return_state = "main_menu"

                state = "options"


            elif action == "quit":

                running = False
        elif state == "uno_online":

            result = uno_online.handle_event(
                event,
                mouse_pos
            )

            if result == "back":
                network_client.leave_hub()
                state = "multiplayer"
        elif state == "uno":
        
                uno_game.handle_event(
                    event,
                    mouse_pos
                )

        # --------------------------------
        # HUB
        # --------------------------------

        elif state == "hub":

            action = hub.handle_event(event)
                            
            if action is not None:
            
                return_state = "hub"
            
                state = action

        elif state == "arcade":

            result = arcade.handle_event(
                event,
                mouse_pos
            )

            if (
                result is not None
                and result["action"] == "launch_game"
            ):

                game_id = result["game_id"]

                stats.start_game(
                    game_id
                )

                if game_id == "uno":

                    uno_game.reset_game()

                    state = "uno"

                else:

                    active_game = result["game"]

                    state = "mini_game"

        elif state == "multiplayer":

            result = multiplayer_lobby.handle_event(
                event,
                mouse_pos
            )

            if result == "back":
                network_client.leave_hub()
                state = "main_menu"
        elif state == "profile":

            profile.handle_event(
                event,
                mouse_pos
            )

        elif state == "friends":

            result = friends_menu.handle_event(
                event,
                mouse_pos
            )

            if result is not None:

                # -------------------------
                # PROFIL D'UN AMI
                # -------------------------

                if result["action"] == "friend_profile":

                    friend_profile.set_friend(
                        result["friend"]
                    )

                    state = "friend_profile"

                # -------------------------
                # REJOINDRE
                # -------------------------

                elif result["action"] == "join_friend":

                    friend = result["friend"]

                    print(
                        f"On rejoint {friend['display_name']}"
                    )

        elif state == "friend_profile":

            friend_profile.handle_event(
                event,
                mouse_pos
            )
        # --------------------------------
        # ESC
        # --------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                # Depuis un sous-menu
                # on retourne au hub
                if state == "mini_game":

                    stats.stop_game()

                    active_game = None

                    state = "arcade"

                elif state == "uno":
                
                    stats.stop_game()
                
                    state = "arcade"

                elif state == "friend_profile":

                    state = "friends"

                elif state in [
                    "profile",
                    "friends",
                    "arcade",
                    "options"
                ]:

                    state = return_state

                
                # Depuis le hub
                # on retourne au menu principal

                elif state == "hub":
                    network_client.leave_hub()
                    state = "main_menu"


    # --------------------------------
    # TOUCHES
    # --------------------------------

    keys = pygame.key.get_pressed()


    # --------------------------------
    # UPDATE
    # --------------------------------

    if state == "hub":

        hub.update(
            keys,
            dt
        )

    elif state == "uno":

        uno_game.update()

    if (
        profile.character_changed
        is not None
    ):

        new_character = (
            profile.character_changed
        )

        player.set_character(
            new_character
        )

        network_client.update_character(
            new_character
        )
        
        profile.character_changed = None
    # --------------------------------
    # DRAW
    # --------------------------------

    if state == "main_menu":

        main_menu.draw(
            game_surface,
            mouse_pos
        )
    elif state == "uno_online":

        uno_online.draw(
            game_surface,
            mouse_pos
        )
    elif state == "multiplayer":

        multiplayer_lobby.draw(
            game_surface,
            mouse_pos
        )
    
    elif state == "hub":

        hub.draw(
            game_surface
        )
        hub_multiplayer.draw(
            game_surface
        )
        player.draw(
            game_surface
        )

    elif state == "profile":


        profile.draw(
            game_surface,
            mouse_pos
        )


    elif state == "friends":

        friends_menu.draw(
            game_surface,
            mouse_pos
        )

    elif state == "friend_profile":

        friend_profile.draw(
            game_surface,
            mouse_pos
        )

    elif state == "arcade":

        arcade.draw(
            game_surface,
            mouse_pos
        )

    
    elif state == "uno":

        uno_game.draw(
            game_surface,
            mouse_pos
        )
    elif state == "options":

        draw_placeholder(
            game_surface,
            "OPTIONS"
        )

    elif state == "mini_game":

        game_surface.fill(
            "#0d0f15"
        )

        if active_game is not None:

            game_title = font.render(
                active_game["name"],
                True,
                "white"
            )

            title_rect = game_title.get_rect(
                center=(640, 280)
            )

            game_surface.blit(
                game_title,
                title_rect
            )

            placeholder = font.render(
                "JEU PLACEHOLDER",
                True,
                "#888888"
            )

            placeholder_rect = (
                placeholder.get_rect(
                    center=(640, 350)
                )
            )

            game_surface.blit(
                placeholder,
                placeholder_rect
            )

            game_time = font.render(
                stats.get_game_playtime_text(
                    active_game["id"]
                ),
                True,
                "#5f78ff"
            )

            time_rect = game_time.get_rect(
                center=(640, 410)
            )

            game_surface.blit(
                game_time,
                time_rect
            )

            esc_text = font.render(
                "ESC - Retour a l'Arcade",
                True,
                "#777777"
            )

            esc_rect = esc_text.get_rect(
                center=(640, 500)
            )

            game_surface.blit(
                esc_text,
                esc_rect
            )

    # --------------------------------
    # TEMPS DE JEU
    # --------------------------------

    playtime_text = font.render(
        f"Temps : {stats.get_playtime_text()}",
        True,
        "white"
    )

    game_surface.blit(
        playtime_text,
        (10, 10)
    )

    if admin_panel is not None:

        admin_panel.draw(
            game_surface,
            mouse_pos
        )


    # --------------------------------
    # ADAPTATION FENETRE
    # --------------------------------

    scaled_surface = (
        pygame.transform.scale(
            game_surface,
            screen.get_size()
        )
    )

    screen.blit(
        scaled_surface,
        (0, 0)
    )

    pygame.display.flip()


# --------------------------------
# SAUVEGARDE
# --------------------------------
network_client.stop()

stats.close()

pygame.quit()
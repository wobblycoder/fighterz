import configparser
import pygame
import sys

from artwork import Artwork
from colors import RED, BLUE
from fighter import Fighter, makeDemoFighter
from missile import Missile
import tests
import utils
from world import World


class Game:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.done = False
        self.paused = False
        self.should_draw_sensors = False
        self.show_platform_info = False
        self.full_screen = False
        self.icon_scale = 1.0
        self.screen = None
        self.screen_size = [1024, 786]
        self.world = None
        self.selectedPlayer = None
        self.selectedId = None

        self.initialScore = dict()
        self.currentScore = dict()

        self.read_configuration()
        self.initialize_game_engine()
        self.load_graphics()
        self.create_game_world()

        if len(sys.argv) > 1:
            self.setup_test()
        else:
            self.setup_demo()

    def mainloop(self):
        ticks = 0
        self.clock = pygame.time.Clock()
        self.initialScore = self.compute_scores()

        while not self.done:
            self.handle_events()
            self.draw_everything()
            if not self.paused:
                self.world.update(ticks / 1000.0)
                ticks = self.clock.tick(50)
        pygame.quit()

    def draw_everything(self) -> None:
        self.draw_background()
        self.draw_fighters()
        self.draw_missiles()
        self.draw_all_explosions()
        self.draw_selection()
        self.draw_score()
        self.draw_platform_info_panel()

        pygame.display.flip()

    def read_configuration(self):
        self.config.read("fighterz.ini")
        self.load_screen_settings()
        self.load_options()

    def load_screen_settings(self):
        if self.config.has_option("Screen", "width"):
            self.screen_size[0] = self.config.getint("Screen", "width")

        if self.config.has_option("Screen", "height"):
            self.screen_size[1] = self.config.getint("Screen", "height")

        if self.config.has_option("Screen", "fullScreen"):
            self.full_screen = self.config.getboolean("Screen", "fullScreen")

        if self.config.has_option("Screen", "iconScale"):
            self.icon_scale = self.config.getfloat("Screen", "iconScale")

    def load_options(self):
        self.should_draw_sensors = self.config.getboolean("Options",
                                                          "drawSensors")

    def initialize_game_engine(self):
        pygame.init()

        if self.full_screen:
            self.screen = pygame.display.set_mode(self.screen_size,
                                                  pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

        pygame.display.set_caption('Fighters!')

    def load_graphics(self):
        self.art = Artwork(scale=self.icon_scale,
                           screenWidth=self.screen_size[0],
                           screenHeight=self.screen_size[1])

        icons = self.config.items("Icons")

        for icon in icons:
            self.art.loadImage(icon[0], icon[1])

        chosen_background = self.config.get("Backgrounds", "choice")

        self.art.loadBackground(
            "background",
            self.config.get("Backgrounds", chosen_background)
        )

        Fighter.imagesByForce = {
            BLUE: self.art.assets["bluefighter"],
            RED: self.art.assets["redfighter"]
        }

        Missile.imagesByForce = {
            BLUE: self.art.assets["bluemissile"],
            RED: self.art.assets["redmissile"]
        }

    def create_game_world(self):
        maxWorldX = 1000.0
        maxWorldY = maxWorldX * self.screen_size[1] / self.screen_size[0]
        self.world = World([maxWorldX, maxWorldY])

    def setup_demo(self):

        if (self.config.has_option("Demo", "enabled") and
                self.config.getboolean("Demo", "enabled")):

            redQty = self.config.getint("Demo", "red.qty")
            blueQty = self.config.getint("Demo", "blue.qty")

            for i in range(redQty):
                self.world.addPlayer(makeDemoFighter(RED,
                                                     self.config,
                                                     self.world))

            for j in range(blueQty):
                self.world.addPlayer(makeDemoFighter(BLUE,
                                                     self.config,
                                                     self.world))

    def setup_test(self):
        try:
            testFunction = getattr(tests, sys.argv[-1])
            self.world.addPlayers(testFunction())
        except Exception:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                near_player, near_id = self.find_nearest_player(event.pos)
                self.selectedPlayer = near_player
                self.selectedId = near_id
            elif event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.key == pygame.K_s:
                    self.should_draw_sensors = not self.should_draw_sensors
                if event.key == pygame.K_r:
                    self.create_game_world()
                    self.setup_demo()

                if event.key in [pygame.K_p, pygame.K_SPACE]:
                    self.paused = not self.paused
                    if not self.paused:
                        self.clock = pygame.time.Clock()
                if event.key == pygame.K_i:
                    self.show_platform_info = not self.show_platform_info

    def find_nearest_player(self, eventPos):
        ids = list(self.world.players.keys())
        p1 = self.world.players[ids[0]]
        sx, sy = self.translate_coords(p1.x, p1.y)
        nearestDistance = utils.compute_distance(
            eventPos[0], eventPos[1], sx, sy)
        closest = p1
        closestId = ids[0]

        for playerId in ids[1:]:
            p = self.world.players[playerId]
            sx, sy = self.translate_coords(p.x, p.y)
            d = utils.compute_distance(eventPos[0], eventPos[1], sx, sy)
            if d < nearestDistance:
                closest = p
                closestId = playerId
                nearestDistance = d

        if nearestDistance < 64 and closest.state != "DEAD":
            return closest, closestId

        return None, None

    def draw_background(self):
        self.screen.blit(self.art.assets["background"], [0, 0])

    def draw_fighters(self):
        for playerId in self.world.players:
            player = self.world.players[playerId]
            if player.state != "DEAD":
                self.draw_player(player)

    def draw_missiles(self):
        for missileId in self.world.weapons:
            missile = self.world.weapons[missileId]
            if missile.state != "DEAD":
                self.draw_player(missile)

    def draw_all_explosions(self):
        for explosionNumber in self.world.explosions:
            explosion = self.world.explosions[explosionNumber]
            self.draw_single_explosion(explosion)

    def draw_single_explosion(self, explosion):
        imageName = "explosion" + str(explosion["phase"] % 9)
        image = self.art.assets[imageName]
        px, py = self.translate_coords(explosion["x"], explosion["y"])
        blitx = px - image.get_width() / 2
        blity = py - image.get_height() / 2
        self.screen.blit(image, [blitx, blity])

    def draw_player(self, player):
        image = player.image
        px, py = self.translate_coords(player.x, player.y)
        blitx = px - image.get_width() / 2
        blity = py - image.get_height() / 2
        if self.should_draw_sensors:
            self.draw_sensors(player)

        rotatedImage = self.rotate_image(image, player.heading)
        self.screen.blit(rotatedImage, [blitx, blity])

    def draw_sensors(self, player):
        has_search_results = hasattr(player, "searchResults")

        if has_search_results:
            px, py = self.translate_coords(player.x, player.y)
            detections = filter(lambda res: self.is_live_detection(res),
                                player.searchResults)

            for d in detections:
                tgt = self.world.players[d["targetId"]]
                dx, dy = self.translate_coords(tgt.x, tgt.y)
                pygame.draw.line(self.screen,
                                 player.force,
                                 [px, py + 1],
                                 [dx, dy + 1],
                                 5)

    def draw_selection(self):
        """
        Highlights the currently selected player
        """
        sp = self.selectedPlayer
        if sp is not None and sp.state != "ALIVE":
            self.selectedPlayer = None
            return

        if sp is not None:
            px, py = self.translate_coords(sp.x, sp.y)
            pygame.draw.circle(self.screen,
                               (0, 255, 0, 128),
                               (int(px), int(py)),
                               int(sp.image.get_width() / 2),
                               2)

    def draw_score(self):
        self.currentScore = self.compute_scores()

        try:

            redScore = self.currentScore[RED] / self.initialScore[RED]
            blueScore = self.currentScore[BLUE] / self.initialScore[BLUE]

            pygame.draw.rect(self.screen,
                             (0, 0, 0, 0),
                             (4, 4, 214, 66))

            pygame.draw.rect(self.screen,
                             (225, 225, 255, 255),
                             (10, 10, int(200 * blueScore), 22),
                             2)

            pygame.draw.rect(self.screen,
                             (0, 0, 255, 255),
                             (12, 12, int(200 * blueScore), 22))

            pygame.draw.rect(self.screen,
                             (225, 225, 255, 255),
                             (10, 38, int(200 * redScore), 22),
                             2)

            pygame.draw.rect(self.screen,
                             (255, 0, 0, 255),
                             (12, 40, int(200 * redScore), 22))

        except ZeroDivisionError:
            pass

    def draw_platform_info_panel(self):

        if not self.show_platform_info:
            return

        pygame.draw.rect(self.screen, (224, 224, 224, 64), (4, 80, 400, 272))
        pygame.draw.rect(self.screen, (214, 214, 214, 64), (6, 82, 396, 268))
        pygame.draw.rect(self.screen, (204, 204, 204, 64), (8, 84, 392, 264))
        pygame.draw.rect(self.screen, (194, 194, 194, 64), (10, 86, 388, 260))
        pygame.draw.rect(self.screen, (0, 0, 0, 64), (12, 88, 384, 256), 1)

        font = pygame.font.Font('freesansbold.ttf', 24)

        playerid = "??"
        if self.selectedPlayer is not None:
            playerid = str(self.selectedId)

            textColor = self.selectedPlayer.force
            textSurface = font.render(
                "Player {0}".format(playerid), True, textColor)
            textRect = textSurface.get_rect()
            textRect.center = (202, 108)
            self.screen.blit(textSurface, textRect)

            textSurface = font.render("heading {0}".format(
                int(self.selectedPlayer.heading)), True, textColor)
            textRect = textSurface.get_rect()
            textRect.center = (202, 144)
            self.screen.blit(textSurface, textRect)

            textSurface = font.render("speed {0}".format(
                int(self.selectedPlayer.speed)), True, textColor)
            textRect = textSurface.get_rect()
            textRect.center = (202, 180)
            self.screen.blit(textSurface, textRect)

            textSurface = font.render("(x,y) = ({0:.2f},{1:.2f})".format(
                self.selectedPlayer.x, self.selectedPlayer.y), True, textColor)
            textRect = textSurface.get_rect()
            textRect.center = (202, 216)
            self.screen.blit(textSurface, textRect)

    def rotate_image(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def compute_scores(self):
        score = {RED: 0, BLUE: 0}
        for playerId in self.world.players:
            p = self.world.players[playerId]
            if not p.state == "DEAD":
                score[p.force] += 1
        return score

    def translate_coords(self, x, y):
        sx, sy = utils.tx_world_to_screen(x, y, self.world, self.screen_size)
        return sx, sy

    def is_alive(self, player_id):
        return player_id in self.world.players

    def is_live_detection(self, res):
        return res["detected"] and self.is_alive(res["targetId"])


if __name__ == "__main__":
    game = Game()
    game.mainloop()

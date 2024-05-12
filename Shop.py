from maze_settings import *
import pygame_menu


def Back():
    from MainMenu import StartMenu
    return StartMenu()


class Shop:
    def __init__(self):
        self.frame_UP = None
        self.frame = None
        self.frame_hp = None
        self.menu = pygame_menu.Menu("Магазин", maze_settings.Width, maze_settings.Height,
                                     theme=maze_settings.Settings_Theme)

        self.Buy_Hp_Count = 0
        self.screen = maze_settings.screen

    def Show_Shop(self):
        self.frame_UP = self.menu.add.frame_h(maze_settings.Width // 2, 50,
                                              background_color=(150, 50, 50),
                                              padding=0, )

        self.frame_UP.pack(self.menu.add.image('Sprite/money/money.png', scale=(0.4, 0.4)))
        self.frame_UP.pack(self.menu.add.label(f'{maze_settings.Shop_Money}', label_id="Total_money"))
        self.frame = self.menu.add.frame_v(maze_settings.Width // 2, maze_settings.Height // 2,
                                           background_color=(50, 50, 50),
                                           padding=0, )

        self.frame_hp = self.menu.add.frame_h(maze_settings.Width // 2, 60,
                                              background_color=(20, 120, 50),
                                              padding=0, )
        self.frame.pack(self.frame_hp)
        self.frame_hp.pack(self.menu.add.label('5'))
        self.frame_hp.pack(self.menu.add.image('Sprite/money/money.png', scale=(0.5, 0.5)))
        self.frame_hp.pack(self.menu.add.label('+ здоровье'))
        self.frame_hp.pack(self.menu.add.button('купить', self.Buy_Hp), margin=(5, 5), align=pygame_menu.locals.ALIGN_RIGHT)

        self.menu.add.button("Назад", Back)

        self.menu.mainloop(self.screen)

    def Buy_Hp(self):
        if self.Buy_Hp_Count <= 3 and maze_settings.Shop_Money >= 5:
            maze_settings.Player_hp += 1
            maze_settings.Shop_Money -= 5
            self.Buy_Hp_Count += 1
        self.menu.remove_widget("Total_money")
        self.frame_UP.pack(self.menu.add.label(f'{maze_settings.Shop_Money}', label_id="Total_money"))


if __name__ == "__main__":
    ShopObj = Shop()
    ShopObj.Show_Shop()

from guipyg.gui_style import style

style_dict = {}
theme_dict = {}

default = style.Style()
style_dict[default.style_name] = default

my_first_style = style.Style()
my_first_style.style_name = "my_first_style"
my_first_style.corner_rounding = 4
my_first_style.margin_top = 5
my_first_style.margin_left = 10
my_first_style.border_thickness = 4
my_first_style.background_color = (150, 150, 150)
my_first_style.has_border = True
my_first_style.drop_shadow_alpha = 200
my_first_style.border_color = (1, 1, 1, my_first_style.drop_shadow_alpha)
my_first_style.has_drop_shadow = True
my_first_style.drop_shadow_bottom = 8
my_first_style.drop_shadow_right = 8
my_first_style.drop_shadow_color = (0, 0, 0)
style_dict[my_first_style.style_name] = my_first_style
# theme_dict["element_group"] = my_first_style

my_button_style = style.Style()
my_button_style.style_name = "my_button_style"
my_button_style.border_color = (1, 1, 1)
my_button_style.border_thickness = 2
my_button_style.corner_rounding = 4
my_button_style.has_border = True
my_button_style.background_color = (100, 100, 100)
style_dict[my_button_style.style_name] = my_button_style
# theme_dict["element"] = my_button_style

my_theme = style.Theme("my_theme", my_first_style, my_button_style)
theme_dict[my_theme.theme_name] = my_theme

blue_menu = style.Style()
blue_menu.style_name = "blue_menu"
blue_menu.has_border = True
blue_menu.border_thickness = 2
blue_menu.border_color = (1, 1, 1)
blue_menu.background_color = (100, 140, 200)
blue_menu.margin_top = 10
blue_menu.margin_right = 4
# blue_menu.alpha = 125
style_dict[blue_menu.style_name] = blue_menu

blue_button = style.Style()
blue_button.style_name = "blue_button"
blue_button.has_border = True
blue_button.border_thickness = 2
# blue_button.corner_rounding = 2
blue_button.background_color = (80, 110, 150)
blue_button.border_color = (0, 10, 40)
style_dict[blue_button.style_name] = blue_button

blue_theme = style.Theme("blue_theme", blue_menu, blue_button)
theme_dict[blue_theme.theme_name] = blue_theme

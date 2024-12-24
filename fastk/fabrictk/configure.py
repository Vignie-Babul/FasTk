from fabrictk import system_colors

import copy


__all__ = ('Configure')


class Configure:
	system_accent_colors = system_colors.get_system_accent_colors()
	colors = {
		'white': '#ffffff',  # fg title bar
		'grey_1': '#e8e8e8', # fg primary text
		'grey_2': '#9e9e9e', # fg secondary text
		'grey_3': '#5B5B5B', # fg placeholder
		'grey_4': '#595959', # bg button press
		'grey_5': '#404040', # bg button hover/enter
		'grey_6': '#303030', # bg entry
		'grey_7': '#1f1f1f', # bg window
		'grey_8': '#0a0a0a', # bg title bar
		'red_1': '#f16f7a',  # bg title bar exit button press
		'red_2': '#e81123',  # bg title bar exit button hover/enter
		'enter': system_accent_colors[3], # hover/enter
		'active': system_accent_colors[2], # press
		'default': system_accent_colors[4],
	}
	background_color = colors['grey_7']

	general_font = 'Consolas'
	general = {
		'borderwidth': 0,
		'font': ('Concolas', 13),
		'relief': 'flat',
		'takefocus': False,
	}
	button = {
		'activebackground': colors['active'],
		'activeforeground': colors['grey_1'],
		'background': colors['default'],
		'disabledforeground': colors['grey_1'],
		'foreground': colors['grey_1'],
		'overrelief': 'flat',
	}
	button_enterbackground = colors['enter']

	entry = {
		'background': colors['grey_6'],
		'width': 14,
	}
	entry_no_placeholder = {
		'foreground': colors['grey_1'],
	}
	entry_placeholder = {
		'foreground': colors['grey_3'],
	}

	cursor_keys = (
		'Left', 'Right',
		'KP_Left', 'KP_Right',
		'BackSpace',
	)

	label = {
		'background': colors['grey_7'],
	}
	label_primary = {
		'foreground': colors['grey_1'],
	}
	label_secondary = {
		'foreground': colors['grey_2'],
	}

	title_bar = {
		'widget': {
			'background': colors['grey_8'],
			'foreground': colors['white']
		},
		'close_button': {
			'enter': colors['red_2'],
			'press': colors['red_1'],
		},
		'button': {
			'enter': colors['grey_5'],
			'press': colors['grey_4'],
		},
		'buttons_symbols': {
			'minimize': '—',
			'expand': '🗖',
			'collapse': '🗗',
			'close': '🞨',
		}
	}

	hyperlink = {
		'background': colors['grey_7'],
		'foreground': colors['enter'],
	}

	@staticmethod
	def add_kwargs(kwargs: dict, widget_args: dict) -> dict:
		widget_args_kwargs = copy.deepcopy(widget_args)
		short_names = {
			'bg': 'background',
			'bd': 'borderwidth',
			'fg': 'foreground',
		}

		for key, value in kwargs.items():
			if key in short_names:
				key = short_names[key]

			widget_args_kwargs[key] = value

		return widget_args_kwargs

	@staticmethod
	def get_root_win_size(master):
		'''Convert 'WIDTHxHEIGHT+X+Y' -> (WIDTH, HEIGHT)'''

		master.update_idletasks()
		size = master.winfo_geometry().split('+')[0].split('x')
		size = tuple(
			map(int, size)
		)
		return size
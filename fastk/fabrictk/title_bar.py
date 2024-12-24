from fabrictk import configure, button

import ctypes
import tkinter as tk


__all__ = ('TitleBar')


class TitleBar(tk.Frame):
	def __init__(
		self,
		master,
		title_text=None,
		background=configure.Configure.title_bar['widget']['background'],
		foreground=configure.Configure.title_bar['widget']['foreground'],
		height=32,
		general_button=configure.Configure.title_bar['button'],
		close_button=configure.Configure.title_bar['close_button'],
		buttons_symbols=configure.Configure.title_bar['buttons_symbols']
	) -> None:

		super().__init__(master, background=background)

		self._master = master
		self._title_text = title_text
		if title_text is None:
			self._title_text = self._master.title()
		self._background = background
		self._foreground = foreground
		self._height = height
		self._general_button = general_button
		self._close_button = close_button
		self._buttons_symbols = buttons_symbols

		# root window configure
		self._master.overrideredirect(True)
		self._master.after(10, lambda: _set_task_bar_integration(root_window=self._master))

		self._master_size = configure.Configure.get_root_win_size(master=self._master)
		self._master_size_title_bar = [self._master_size[0], self._master_size[1] + self._height]
		self._master.geometry('{0}x{1}'.format(*self._master_size_title_bar))

		self._buttons_width = 46
		self._half_height = self._height / 2

		self._buttons_frame_width = self._buttons_width * 3
		self._title_frame_width = self._master_size[0] - self._buttons_frame_width

		self._is_pressed = False
		self._is_entered = False

		self._is_minimized = False

		self._master.bind('<Button-1>', self._get_window_position)
		self._master.bind('<B1-Motion>', self._move_window)

		self._master.bind('<FocusIn>', self._deminimize)

		self.__create_widgets()
		self._place_in_root_window()

	def __create_widgets(self) -> None:
		self._create_buttons_frame()
		self._create_title_frame()

		self._bind_flag_events()

		self._create_title()
		self._create_buttons()

	def _create_title_frame(self) -> None:
		self._title_frame = tk.Frame(self, background=self._background)
		self._title_frame.place(
			height=self._height,
			width=self._title_frame_width,
			y=self._half_height,
			anchor='w',
		)

	def _create_buttons_frame(self) -> None:
		self._buttons_frame = tk.Frame(self, background=self._background)
		self._buttons_frame.place(
			height=self._height,
			width=self._buttons_frame_width,
			x=self._title_frame_width,
			y=self._half_height,
			anchor='w',
		)

	def _bind_flag_events(self) -> None:
		self._title_frame.bind('<ButtonPress-1>', self._on_press)
		self._title_frame.bind('<ButtonRelease-1>', self._on_release)
		self._title_frame.bind('<Enter>', self._on_enter)
		self._title_frame.bind('<Leave>', self._on_leave)

	def _create_title(self) -> None:
		self._title = tk.Label(
			self._title_frame,
			text=self._title_text,
			background=self._background,
			foreground=self._foreground,
		)
		self._title.place(
			x=12,
			y=self._half_height,
			anchor='w',
		)

	def _create_buttons(self) -> None:
		self._minimize_button = button.Button(
			self._buttons_frame,
			text=self._buttons_symbols['minimize'],
			command=self._minimize,
			font=('Segoe UI', 7),
			foreground=self._foreground,
			background=self._background,
			enterbackground=self._general_button['enter'],
			activebackground=self._general_button['press'],
		)

		self._expand_button = button.Button(
			self._buttons_frame,
			text=self._buttons_symbols['expand'],
			command=lambda: print(True),
			font=('Segoe UI', 10),
			foreground=self._foreground,
			background=self._background,
			enterbackground=self._general_button['enter'],
			activebackground=self._general_button['press'],
		)

		self._close_button_ = button.Button(
			self._buttons_frame,
			text=self._buttons_symbols['close'],
			command=self.quit,
			font=('Segoe UI', 13),
			foreground=self._foreground,
			background=self._background,
			enterbackground=self._close_button['enter'],
			activebackground=self._close_button['press'],
		)

		# place buttons
		self.buttons = [
			self._minimize_button,
			self._expand_button,
			self._close_button_
		]

		for button_, index in zip(self.buttons, range(3)):
			button_.place(
				height=self._height,
				width=self._buttons_width,
				x=self._buttons_width * index,
				y=self._half_height,
				anchor='w',
			)

	def _place_in_root_window(self) -> None:
		self.place(
			height=32,
			relwidth=1,
			y=16,
			anchor='w',
		)

	def _on_press(self, event=None) -> None:
		if self._is_entered:
			self._is_pressed = True

	def _on_release(self, event=None) -> None:
		self._is_pressed = False

	def _on_enter(self, event=None) -> None:
		self._is_entered = True

	def _on_leave(self, event=None) -> None:
		self._is_entered = False

	def _get_window_position(self, event=None) -> None:
		self.x_win = self._master.winfo_x() - event.x_root
		self.y_win = self._master.winfo_y() - event.y_root

	def _move_window(self, event=None) -> None:
		x_win = event.x_root + self.x_win
		y_win = event.y_root + self.y_win

		if self._is_entered or self._is_pressed:
			self._master.geometry(f'+{x_win}+{y_win}')

	def _minimize(self) -> None:
		self._is_minimized = True
		self._master.attributes('-alpha', 0)

	def _deminimize(self, event=None) -> None:
		if self._is_minimized:
			self._master.focus()
			self._master.attributes('-alpha', 1)
			self._is_minimized = False


def _set_task_bar_integration(root_window: tk.Tk)  -> None:
	GWL_EXSTYLE = -20
	WS_EX_APPWINDOW = 0x00040000
	WS_EX_TOOLWINDOW = 0x00000080

	hwnd = ctypes.windll.user32.GetParent(root_window.winfo_id())
	stylew = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
	stylew = stylew & ~WS_EX_TOOLWINDOW
	stylew = stylew | WS_EX_APPWINDOW
	result = ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

	root_window.wm_withdraw()
	root_window.after(10, lambda: root_window.wm_deiconify())
from fabrictk import configure

import tkinter as tk


__all__ = ('Button')


class Button(tk.Button):
	def __init__(
		self,
		master,
		enterbackground=configure.Configure.button_enterbackground,
		**kwargs
	) -> None:

		super().__init__(master, **kwargs)

		self._enterbackground = enterbackground
		if 'command' in kwargs:
			self._command = kwargs['command']
		else:
			self._command = None

		self._general_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.general
		)
		self._button_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.button
		)

		self.configure(**self._general_configure)
		self.configure(**self._button_configure)

		self._is_entered = False

		self.bind('<ButtonPress-1>', self._on_press)
		self.bind('<ButtonRelease-1>', self._on_release)
		self.bind('<Enter>', self._on_enter)
		self.bind('<Leave>', self._on_leave)

		self.configure(state='disabled')

	def _on_press(self, event=None) -> None:
		if self._is_entered:
			self.configure(bg=self._button_configure['activebackground'])

	def _on_release(self, event=None) -> None:
		if self._is_entered:
			self.configure(bg=self._enterbackground)

			if self._command is not None:
				self._command()

	def _on_enter(self, event=None) -> None:
		self._is_entered = True
		self.configure(bg=self._enterbackground)

	def _on_leave(self, event=None) -> None:
		self._is_entered = False
		self.configure(bg=self._button_configure['background'])
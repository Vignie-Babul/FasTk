from . import configure

import tkinter as tk


__all__ = ('Hyperlink')


class Hyperlink(tk.Label):
	def __init__(self, master, text='', command=None, **kwargs) -> None:
		super().__init__(master, text=text, **kwargs)

		self._command = command

		self._underline_font = (*configure.Configure.general['font'], 'underline')
		self._default_font = configure.Configure.general['font']

		self._general_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.general
		)
		self._hyperlink_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.hyperlink
		)

		self.configure({**self._general_configure, **self._hyperlink_configure})

		self._is_entered = False

		self.bind('<ButtonRelease-1>', self._on_release)
		self.bind('<Enter>', self._on_enter)
		self.bind('<Leave>', self._on_leave)

	def _on_release(self, event=None) -> None:
		if self._is_entered:
			if self._command is not None:
				self._command()

	def _on_enter(self, event=None) -> None:
		self._is_entered = True
		self.configure(font=self._underline_font, cursor='hand2')

	def _on_leave(self, event=None) -> None:
		self._is_entered = False
		self.configure(font=self._default_font, cursor='')
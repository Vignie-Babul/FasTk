from fabrictk import configure

import tkinter as tk


__all__ = ('Entry')


class Entry(tk.Entry):
	def __init__(self, master, placeholder='', password: bool | None = None, **kwargs) -> None:
		super().__init__(master, **kwargs)

		self._placeholder = placeholder

		self._password = password
		if self._password is not None:
			if isinstance(self._password, str):
				self._password_show = {'show': self._password}
				self._password = True
			else:
				self._password_show = {'show': '•'}

		self._general_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.general
		)
		self._entry_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.entry
		)

		self._entry_no_placeholder_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.entry_no_placeholder
		)
		self._entry_placeholder_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.entry_placeholder
		)

		self.configure({**self._general_configure, **self._entry_configure})

		self.bind('<FocusIn>', self._on_focus_in)
		self.bind('<FocusOut>', self._on_focus_out)
		self.bind('<KeyPress>', self._on_key_press)

		# placeholder initialization
		self._add_placeholder()

	def _configure_placeholder(self):
		self.configure(**self._entry_placeholder_configure)
		if self._password:
			self.configure(show='')

	def _configure_no_placeholder(self):
		self.configure(**self._entry_no_placeholder_configure)
		if self._password:
			self.configure(**self._password_show)

	def _add_placeholder(self) -> None:
		if (self.get() != self._placeholder) or (not self.get()):
			self.insert(0, self._placeholder)
			self._configure_placeholder()

	def _remove_placeholder(self) -> None:
		if self.get() == self._placeholder:
			self.delete(0, tk.END)
			self._configure_no_placeholder()

	def _ignore_cursor_keys(self) -> None:
		for cursor_key in configure.Configure.cursor_keys:
			self.bind(f'<{cursor_key}>', self.icursor(0))

	def _unignore_cursor_keys(self) -> None:
		for cursor_key in configure.Configure.cursor_keys:
			self.unbind(f'<{cursor_key}>')

	def _on_focus_in(self, event=None) -> None:
		if self.get() == self._placeholder:
			self.icursor(0)
			self._ignore_cursor_keys()
			self._configure_placeholder()
		else:
			self._unignore_cursor_keys()

	def _on_focus_out(self, event=None) -> None:
		if not self.get():
			self._add_placeholder()

	def _on_key_press(self, event=None) -> None:
		if self.get() == self._placeholder:
			if event.keysym in configure.Configure.cursor_keys:
				self._ignore_cursor_keys()
				self._add_placeholder()
			else:
				self._remove_placeholder()
				self._unignore_cursor_keys()
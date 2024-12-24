from fabrictk import configure

import tkinter as tk


__all__ = ('Label')


class Label(tk.Label):
	def __init__(self, master, secondary=False, **kwargs):
		super().__init__(master, **kwargs)

		self._general_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.general
		)
		self._label_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.label
		)

		self._label_primary_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.label_primary
		)
		self._label_secondary_configure = configure.Configure.add_kwargs(
			kwargs=kwargs,
			widget_args=configure.Configure.label_secondary
		)

		self.configure(
			{
				**self._general_configure,
				**self._label_configure,
				**self._label_primary_configure
			}
		)
		if secondary:
			self.configure(**self._label_secondary_configure)
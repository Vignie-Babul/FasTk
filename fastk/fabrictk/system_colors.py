import winreg


__all__ = ('get_system_accent_colors')


def _get_colors_value(value_name: str) -> str:
	path = 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Accent'

	key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
	value, _ = winreg.QueryValueEx(key, value_name)
	winreg.CloseKey(key)

	return value

def get_system_accent_colors() -> list[hex]:
	values_names = ['AccentPalette', 'AccentColorMenu', 'StartColorMenu']

	accent_palette = _get_colors_value(value_name=values_names[0])
	accent_palette = ' '.join(f'{byte:02x}' for byte in accent_palette).split()
	palette = [
		f'#{accent_palette[i]}{accent_palette[i+1]}{accent_palette[i+2]}' for i in range(0, 25, 4)
	]

	for value_name in values_names[1:]:
		menu_color_hex = f'{_get_colors_value(value_name=value_name):02x}'
		menu_color = f'#{menu_color_hex[2:]}'
		palette.append(menu_color)

	return palette
:: remove build directories
@RD /S /Q build
@RD /S /Q dist

:: run pyinstaller with provided options
pyinstaller plenoptisign\gui\gui_app.py^
	--onefile^
	--noconsole^
	--name=plenoptisign^
	--icon=plenoptisign\gui\misc\circlecompass_1055093.ico
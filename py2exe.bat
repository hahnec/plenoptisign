:: remove build directories
@RD /S /Q build
@RD /S /Q dist

:: run pyinstaller with provided options
pyinstaller plenoptisign\gui\gui_app.py^
	--onefile^
	--noconsole^
	--name=plenoptisign^
	--icon=plenoptisign\gui\misc\circlecompass_1055093.ico^
    --add-data=.\docs\build\html\;.\docs\build\html\^
    --add-data=plenoptisign\gui\misc\circlecompass_1055093.ico;.\misc\

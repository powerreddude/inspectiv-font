all: build/InspectivIcons.ttf build/InspectivIcons.otf build/InspectivIcons.woff 

build/InspectivIcons.%:
	./src/generate_font.py -i ./src/glyphs -o ./build -n "Inspectiv Icons"


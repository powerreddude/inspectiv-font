all: build/Inspectiv.ttf build/Inspectiv.eot build/Inspectiv.svg build/Inspectiv\ Mac.ttf

tmp/Inspectiv%: 
	 birdfont-export -o tmp ./src/Inspectiv.bf && ls -rt1 tmp/ | sed "s/^ //" | xargs -I '{}' cp 'tmp/\ {}' 'tmp/{}' 

build/Inspectiv%: tmp/Inspectiv% 
	cp '$<' '$@'

clean: 
	rm -rf ./tmp/*


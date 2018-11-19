# Label Key
*This is a palette plugin for the [Glyphs font editor](http://glyphsapp.com/).*
  
It adds a new palette to the sidebar displaying a user defined key for Glyphs' colour labelling. 

<img src="https://github.com/RobertPratley/labelKey/blob/master/labelKeyExample.png" width="350"/>

### How to use

The plugin requires a labelkey.txt file stored in either ~/Library/Application Support/Glyphs/info/ or the same directory as the current Glyphs source file. Preference is given to the latter allowing for the sharing of the labelkey.txt file with glyphs source files to retain labelling information between project contributors. 

The labelkey.txt file requires the formatting `colorName=meaning`, with each key on a newline and with no space surrounding the '='. The order of the key will follow the order specified in the text file. An example, with the defined colorNames is given below. 

```
red=Red
orange=Orange
brown=Brown
yellow=Yellow
lightGreen=Light green
darkGreen=Dark green
lightBlue=Light blue
darkBlue=Dark blue
purple=Purple
magenta=Magenta
lightGray=Light Gray
charcoal=Charcoal
```

*Thanks to Georg Seifert for helping with bug fixing.*

### License

Copyright 2017 Robert Pratley (@RobertPratley).
Based on sample code by Yanone (@yanone) and Georg Seifert (@schriftgestalt).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.

# Iceberglist

### Tasks
- validating xml file
	+ validating form (xml)
	+ validating structure (xsd file)
- extracting elements with attributes from xml file
	+ writing generic "Widget" class
	+ creating "Widget" classes for each element including its attributes
	+ validating elements
	+ validating attributes of each element
- creating mockup file from xml file
	+ todo
- creating class file from xml file
	+ todo
- pyIf
- creating a way to style (eg.) all "label" widgets


### for future releases
- Positioning of widgets is very simple at the moment. For example, it is not possible to put two widgets next to each other.
- Idea: Per default, if anything is changed, everything gets refreshed. BUT you can also reference certain items, eg.:
	Lets say there is a button A and it changes the color of label B. Button A could have a reference (pyLink="labelA") while label A has a reference id (pyRef="labelA"). Now, if button A invokes a change (because of a press) ONLY every object linked to it (and the objects linked to the child, and so on) get refreshed. OTHERWISE, if an object does not have any linked objects AND was not invoked to change by reference, everything (all widgets) get refreshed. This takes more time (since everything is reloaded), but guarantees that every change is visible.
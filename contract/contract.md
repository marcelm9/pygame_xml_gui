# Better GUI development in Pygame: PyXG (Pygame XML GUI)

#### The goal of this project is to simplify the process of GUI creation in Pygame. Until now, GUI creation in Pygame has been a very tedious task compared to GUI creation in other languages like HTML. This project aims at reducing the time and effort that goes into great UIs by combining xml-like formatting with custom elements and attributes, all in a Python environment.
&nbsp;

### Example use case: Creating a list of entity positions
The goal is to not only display the positions, but also
to make it possible to edit them. Because of this, the
structure of each line (/position) should look like this:

<table>
	<tr>
		<td> Position
		</td>
		<td> Entity name
		</td>
		<td> Change (position)
		</td>
		<td> Round (to int)
		</td>
		<td> Delete
		</td>
	</tr>
</table>

The code for this UI should look like this:
```xml
<canvas pySize="500x500" pySource="data.py" pyStyle="dark">
	<style>
		<all size="26"/>
		<label font="consolas"/>
	</style>
	<label> Entity positions </label>
	<list pyMoving="True" pyAxis="horizontal">
		<list-item pyFor="e in entities">
			<label pyWidth="20"> {{ e.position }} </label>
			<label pyWidth="20"> {{ e.name }} </label>
			<button pyWidth="20"> Change </button>
			<button pyWidth="20"> Round </button>
			<button pyWidth="20"> Delete </button>
		</list-item>
	</list>
</canvas>
```

&nbsp;
### Elements
Name | Info
-|-
canvas | toplevel element
style | -
all | only in "style" element, specifies style for elements "label" and "button"
label | -
button | -
list | -
list-item | only in "list" element

&nbsp;
### Attributes
Name | Description | Elements
-|-|-
pySize | size of the canvas (has to be set) | canvas
pySource | data source for canvas | canvas
pyStyle | sets the style of the file to a preset (_multiple shall be created during development_) | canvas
pyStylePath | sets the style of the file to the style specified in the given file | canvas
pyMoving | makes widget scrollable | label-list, button-list
pyClick | action on click | button
pyIf | if statement | -
pyFor | for statement | label-list-item, button-list-item
pyW | width of the element (in percent of the width of the parent element) | -

&nbsp;
### Default values for attributes
Name | Default value
-|-
pySize | -
pySource | -
pyStyle | -
pyStylePath | -
pyMoving | -
pyClick | -
pyIf | -
pyFor | -
pyW | -
pyAxis | "horizontal"

&nbsp;
### How the project will be used
First, the developer will create a python file and store any variables that should be accessible during the testing of the UI. Then, the developer starts writing the xml file. To create mockup UI from the xml file, the command "pyxg_xml_to_mockup _path_to_xml_file_" can be used. This file is instantly launchable as a standalone GUI, just to see how the GUI of the XML file looks for now. After the finishing touches on the xml file, the command "pyxg_xml_to_class _path_to_xml_file_" can be used to create a python class that is insertable into any pygame project.

&nbsp;
### Commands
Name | Use case
-|-
pyxg_xml_to_mockup | create a mockup of the ui that can be instantly launched
pyxg_xml_to_class | create a GUI class that can be used in any pygame project
pyxg_validate_xml | validate an xml file

&nbsp;
### Hints
- While writing the xml file, you can test out your code with example data by giving the canvas a "pySource" attribute. In the given file you can create variables which will then be used in the xml file.
- Variables of the source file can be referenced in the xml file. For example, you can create a list of entities and create a label for each entity by using a list and a list-item with the attribute "pyFor".

&nbsp;
### Further ideas
- Maybe add references?
	+ eg.:
```xml
<label pyRef="title"> Hello world! </label>
```
- Maybe create xsd file for better error highlighting?
- Maybe add a way to reference a style file?
- Maybe create some standard color schemes?
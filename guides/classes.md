# Formatting of the classes file
The classes file exists to make the design of UIs easier. It should be a `json` file, and can contain multiple different styles for widgets. The topmost keys can be the names of widgets, to make such widgets automatically adapt the given style. In the following example, all widgets of type `label` will automatically have blue text, unless they have an attribute `pyStyle` that overrides the textcolor.

```json
{
    "label": {
        "tc": [0, 0, 255]
    }
}
```

It is also possible to define new styles, called `classes`. These `classes` work very similar to html classes, and can be given to widgets via the `pyClass` attribute. In the following (simplified) example, a new style named 'style1' is created and then assigned to a `label` widget. Multiple `classes` can be assigned to one widget by separating the `class` names with whitespaces.

```json
{
    "style1": {
        "bgc": [0, 255, 0]
    },

    "style2": {
        "bw": 1,
        "bc": [255, 0, 0]
    }
}
```
```xml
<canvas>
    <label pyClass="style1"> Hello world! </label>
    <label pyClass="style1 style2"> Hello world 2! </label>
</canvas>
```


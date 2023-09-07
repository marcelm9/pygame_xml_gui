class Widget:
    def __init__(self, name, attributes: dict, content):
        self.name = name
        self.attributes = attributes
        self.content = content

        self.__info = {}

    def set_width(self, width):
        self.__info["force_width"] = width

    def set_height(self, height):
        self.__info["force_height"] = height

    def __repr__(self) -> str:
        return f"widget (name: {self.name}, attributes: {dict(self.attributes)}, content: {self.content})"
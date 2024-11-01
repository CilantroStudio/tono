from tono.lib.base import TonoToolFormatter


class ToolFormatter(TonoToolFormatter):
    def format(self, parsed_doc):
        tool = {
            "type": "function",
            "function": {
                "name": parsed_doc.name,
                "description": f"{parsed_doc.short_description} {parsed_doc.long_description}",
            },
        }

        if parsed_doc.params:
            tool["function"]["parameters"] = {
                "type": "object",
                "properties": {
                    param.arg_name: {
                        "type": param.type_name,
                        "description": param.description,
                    }
                    for param in parsed_doc.params
                },
                "required": parsed_doc.required,
                "additionalProperties": False,
            }

            for param in parsed_doc.params:
                if param.enum:
                    tool["function"]["parameters"]["properties"][param.arg_name][
                        "enum"
                    ] = param.enum

        return tool

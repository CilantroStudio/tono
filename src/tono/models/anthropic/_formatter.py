from tono.lib.base import TonoToolFormatter


class ToolFormatter(TonoToolFormatter):
    def format(self, parsed_doc):
        tool = {
            "name": parsed_doc.name,
            "description": f"{parsed_doc.short_description} {parsed_doc.long_description}",
        }

        if parsed_doc.params:
            tool["input_schema"] = {
                "type": "object",
                "properties": {
                    param.arg_name: {
                        "type": param.type_name,
                        "description": param.description,
                    }
                    for param in parsed_doc.params
                },
                "required": parsed_doc.required,
            }

            for param in parsed_doc.params:
                if param.enum:
                    tool["input_schema"]["properties"][param.arg_name]["enum"] = (
                        param.enum
                    )

        return tool

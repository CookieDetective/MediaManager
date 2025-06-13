from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel

def write_report(filename, html):
    with open(filename, 'w') as f:
        f.write(html)

class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str

#We use structured tool because the Tool class can only receive functions that have a single argument.
#Tools with multiple arguments need StructuredTool
write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool when someone asks for a report",
    func=write_report,
    args_schema=WriteReportArgsSchema
)
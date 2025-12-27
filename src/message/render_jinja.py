from jinja2 import Environment, FileSystemLoader


def jinja_render(
    financials_result: list[dict], template: str, repository: str = "src/message/templates/"
) -> str:
    environment = Environment(
        loader=FileSystemLoader(repository), keep_trailing_newline=False
    )
    template = environment.get_template(template)

    return template.render(
        financials_result=financials_result,
    )

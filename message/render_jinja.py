from jinja2 import Environment, FileSystemLoader


def daily_earning(financials_result: list[dict]) -> str:
    environment = Environment(loader=FileSystemLoader("message/templates/"), keep_trailing_newline=False)
    template = environment.get_template("earning.jinja")

    return template.render(
        financials_result=financials_result,
    )

def month_over_month(financials_result: list[dict]) -> str:
    environment = Environment(loader=FileSystemLoader("message/templates/"), keep_trailing_newline=False)
    template = environment.get_template("mom.jinja")

    return template.render(
        financials_result=financials_result,
    )

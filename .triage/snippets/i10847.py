class CustomErrReportingClass:
    pass


class CustomErrOne(CustomErrReportingClass):
    pass


class CustomErrTwo(CustomErrReportingClass):
    pass


class SpecialException1(Exception):
    pass


class SpecialException2(Exception):
    pass


def fetch_result() -> str:
    return "ok"


def report_error(_e: CustomErrReportingClass) -> None:
    pass


def run() -> None:
    result: str | None = None
    err: CustomErrReportingClass

    try:
        result = fetch_result()
    except SpecialException1:
        err = CustomErrOne()
    except SpecialException2:
        err = CustomErrTwo()

    if not result:
        report_error(err)

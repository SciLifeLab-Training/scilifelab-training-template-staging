from datetime import date, datetime


def _parse_date(value):

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    return datetime.strptime(
        str(value),
        "%Y-%m-%d",
    ).date()


def _format_date(value):

    return _parse_date(value).strftime("%-d %B %Y")


def render_registration(registration):

    if not registration.get("enabled"):
        return ""

    opening_date = registration.get("opening_date")
    closing_date = registration.get("closing_date")
    after_closing = registration.get("after_closing", "hide")

    if not opening_date:
        return ""

    today = date.today()

    opening_date = _parse_date(opening_date)

    if closing_date:
        closing_date = _parse_date(closing_date)

    # --------------------------------------------------
    # Registration has not opened yet
    # --------------------------------------------------

    if today < opening_date:

        formatted_date = _format_date(opening_date)

        return f"""
<div class="course-registration">

<div class="course-registration-content">

<div class="course-registration-title">
Registration opens soon
</div>

<div class="course-registration-message">
Registration for this training opens on {formatted_date}.
</div>

</div>

</div>
""".strip()

    # --------------------------------------------------
    # Registration is open
    # --------------------------------------------------

    if closing_date is None or today <= closing_date:

        url = registration.get("url")

        if not url:
            return ""

        formatted_date = (
            _format_date(closing_date)
            if closing_date
            else None
        )

        cost = registration.get("cost") or {}

        amount = cost.get("amount")
        currency = cost.get("currency")
        note = cost.get("note")

        details_html = []

        if formatted_date:
            details_html.append(
                '<div class="course-registration-deadline">'
                f'Register by {formatted_date}.'
                '</div>'
            )

        if amount is not None and currency:
            details_html.append(
                '<div class="course-registration-fee">'
                f'Cost: {amount} {currency}'
                '</div>'
            )

        if note:
            details_html.append(
                '<div class="course-registration-note">'
                f'{note}'
                '</div>'
            )

        details_html = "\n".join(details_html)

        return f"""
<div class="course-registration">

<div class="course-registration-content">

<div class="course-registration-title">
Registration is open
</div>

{details_html}

</div>

<a
    class="course-registration-button"
    href="{url}">
    Register for this training →
</a>

</div>
""".strip()

    # --------------------------------------------------
    # Registration has closed
    # --------------------------------------------------

    if after_closing == "hide":
        return ""

    return """
<div class="course-registration">

<div class="course-registration-content">

<div class="course-registration-title">
Registration is closed
</div>

<div class="course-registration-message">
Registration for this training is now closed.
</div>

<div class="course-registration-note">
For questions or more information, please contact the training team.
</div>

</div>

</div>
""".strip()
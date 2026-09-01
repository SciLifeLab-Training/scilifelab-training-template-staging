document.addEventListener("DOMContentLoaded", function () {

    const schedule = document.querySelector(".course-schedule");

    if (!schedule) {
        return;
    }

    const buttons = schedule.querySelectorAll(
        ".course-schedule-day-link"
    );

    const days = schedule.querySelectorAll(
        ".course-schedule-day"
    );

    if (!buttons.length || !days.length) {
        return;
    }

    function showDay(dayId) {

        days.forEach(function (day) {

            day.classList.toggle(
                "is-active",
                day.id === dayId
            );

        });

        buttons.forEach(function (button) {

            button.classList.toggle(
                "is-active",
                button.dataset.day === dayId
            );

        });

    }

    buttons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            event.preventDefault();

            showDay(button.dataset.day);

        });

    });

    showDay(days[0].id);

});
document.addEventListener("DOMContentLoaded", function () {

    // ==================================================================
    // Schedule day navigation
    // ==================================================================

    const schedule = document.querySelector(".course-schedule");

    if (schedule) {

        const buttons = schedule.querySelectorAll(
            ".course-schedule-day-link"
        );

        const days = schedule.querySelectorAll(
            ".course-schedule-day"
        );

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

        if (days.length) {
            showDay(days[0].id);
        }

    }


    // ==================================================================
    // Upcoming event
    // ==================================================================

    const upcoming = document.querySelector(".course-upcoming");

    if (!upcoming) {
        return;
    }

    const events = JSON.parse(
        upcoming.dataset.events
    );

    const card = upcoming.querySelector(
        ".course-upcoming-card"
    );

    const dayGroup = upcoming.querySelector(
        ".course-upcoming-weekday"
    );

    const dayNumber = upcoming.querySelector(
        ".course-upcoming-date"
    );

    const month = upcoming.querySelector(
        ".course-upcoming-month"
    );

    const time = upcoming.querySelector(
        ".course-upcoming-time"
    );

    const type = upcoming.querySelector(
        ".course-upcoming-type"
    );

    const title = upcoming.querySelector(
        ".course-upcoming-title"
    );

    const speaker = upcoming.querySelector(
        ".course-upcoming-speaker"
    );

    const location = upcoming.querySelector(
        ".course-upcoming-location"
    );

    const countdown = upcoming.querySelector(
        ".course-upcoming-countdown"
    );


    // ------------------------------------------------------------------
    // Month abbreviations
    // ------------------------------------------------------------------

    const MONTHS = [
        "JAN", "FEB", "MAR", "APR",
        "MAY", "JUN", "JUL", "AUG",
        "SEP", "OCT", "NOV", "DEC"
    ];


    // ------------------------------------------------------------------
    // Find the next relevant event
    //
    // An event remains the upcoming event until its END time.
    // This means that while an event is currently happening, it
    // remains displayed.
    // ------------------------------------------------------------------

    function getUpcomingEvent() {

        const now = new Date();

        return events.find(function (event) {

            const end = new Date(event.end);

            return end > now;

        });

    }


    // ------------------------------------------------------------------
    // Format countdown
    // ------------------------------------------------------------------

    function formatCountdown(event) {

        const now = new Date();
        const start = new Date(event.start);
        const end = new Date(event.end);

        // Event is currently happening.
        if (now >= start && now < end) {

            const remaining = end - now;

            const totalMinutes = Math.ceil(
                remaining / 60000
            );

            const hours = Math.floor(
                totalMinutes / 60
            );

            const minutes = totalMinutes % 60;

            if (hours > 0 && minutes > 0) {
                return `Ends in ${hours}h ${minutes}m`;
            }

            if (hours > 0) {
                return `Ends in ${hours}h`;
            }

            return `Ends in ${minutes}m`;
        }


        // Event has not started yet.
        const remaining = start - now;

        const totalMinutes = Math.ceil(
            remaining / 60000
        );

        const days = Math.floor(
            totalMinutes / (60 * 24)
        );

        const hours = Math.floor(
            (totalMinutes % (60 * 24)) / 60
        );

        const minutes = totalMinutes % 60;


        if (days > 0) {

            if (hours > 0) {
                return `Starts in ${days}d ${hours}h`;
            }

            return `Starts in ${days}d`;
        }

        if (hours > 0) {

            if (minutes > 0) {
                return `Starts in ${hours}h ${minutes}m`;
            }

            return `Starts in ${hours}h`;
        }

        if (minutes > 0) {
            return `Starts in ${minutes}m`;
        }

        return "Starting now";
    }


    // ------------------------------------------------------------------
    // Display an event
    // ------------------------------------------------------------------

    function showUpcomingEvent(event) {

        const start = new Date(event.start);
        const end = new Date(event.end);

        const group = event.group.toUpperCase();

        const day = start.getDate()
            .toString()
            .padStart(2, "0");

        const monthName = MONTHS[start.getMonth()];

        const startTime = start.toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false
            }
        );

        const endTime = end.toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false
            }
        );


        // Day information

        dayGroup.textContent = group;
        dayNumber.textContent = day;
        month.textContent = monthName;


        // Time

        time.textContent =
            `${startTime}–${endTime}`;


        // Event type

        const eventTypeClass =
            event.type
                .toLowerCase()
                .replace(/_/g, "-");

        type.textContent =
            event.type
                .replace(/_/g, " ")
                .replace(/\b\w/g, function (letter) {
                    return letter.toUpperCase();
                });

        type.className =
            `course-upcoming-type course-type-${eventTypeClass}`;

    // ------------------------------------------------------------------
    // Title
    // ------------------------------------------------------------------

    if (event.content) {

        title.innerHTML =
            `<a href="${event.content}">${event.title}</a>`;

    } else {

        title.textContent = event.title;

    }

        // Speaker

        if (event.people && event.people.length) {

            speaker.innerHTML =
                `<i class="bi bi-person"></i>` +
                event.people.join(", ");

            speaker.style.display = "";

        } else {

            speaker.innerHTML = "";
            speaker.style.display = "none";

        }


        // Location

        if (event.location) {

            location.innerHTML =
                `<i class="bi bi-geo-alt"></i>` +
                event.location;

            location.style.display = "";

        } else {

            location.innerHTML = "";
            location.style.display = "none";

        }


        // Countdown

        countdown.textContent =
            formatCountdown(event);
    }


    // ------------------------------------------------------------------
    // Update upcoming event
    // ------------------------------------------------------------------

    function updateUpcoming() {

        const event = getUpcomingEvent();

        if (!event) {

            const section = document.querySelector(
                ".course-upcoming-section"
            );

            if (section) {

                section.remove(); 
                };

            return;

        }

        showUpcomingEvent(event);
    }


    // ------------------------------------------------------------------
    // Initial update
    // ------------------------------------------------------------------

    updateUpcoming();


    // ------------------------------------------------------------------
    // Keep countdown updated
    //
    // Checking every second means the card will automatically switch
    // to the next event when the current event ends.
    // ------------------------------------------------------------------

    setInterval(
        updateUpcoming,
        1000
    );

});

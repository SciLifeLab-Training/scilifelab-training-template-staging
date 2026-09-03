# TEMPLATE_SPEC.md

# SciLifeLab Course Website Template Specification

**Version:** 1.0  
**Status:** Architecture Frozen

---

# 1. Purpose

The SciLifeLab Course Website Template provides a reusable framework for creating FAIR, maintainable, and consistent course websites using **Quarto** and **GitHub Pages**.

The template is designed to support a broad range of educational formats, including:

- Self-paced online courses
- Instructor-led workshops
- Hybrid courses
- Multi-day events
- Modular learning resources

The template emphasizes:

- Single source of truth
- FAIR metadata
- Minimal duplication
- Consistent user experience
- Flexible course content


## 1.1 Glossary

| Term      | Meaning                           |
| --------- | --------------------------------- |
| Course    | The educational offering          |
| Event     | A scheduled item in the programme |
| Content   | Learning material in `content/`   |
| Page      | A top-level website page          |
| Component | A reusable section of a page      |


---

# 2. Design Principles

The template follows five guiding principles.

## 2.1 Single Source of Truth

Every piece of information exists in only one place.

| Information | Source |
|------------|--------|
| Course metadata | `course.yml` |
| Website configuration | `website.yml` |
| People | `team.yml` |
| Programme and timetable | `schedule.yml` |
| Learning material | `content/` |

---

## 2.2 Derive Whenever Possible

Users should never manually maintain information that can be generated automatically.

Examples include:

- Navigation
- Quick links
- Registration button
- Team preview
- Citation
- Schedule grouping (Day 1, Day 2, etc.)

---

## 2.3 Separate Metadata from Content

Metadata is stored in YAML files.

Course material is written as Quarto documents.

This allows instructors complete freedom when designing learning materials while maintaining a consistent website structure.

---

## 2.4 Opinionated Core, Flexible Content

Every course website shares the same backbone:

- Home
- Course content
- Syllabus

Additional pages are optional.

Course content itself is intentionally unrestricted.

---

## 2.5 Progressive Complexity

A minimal course should require only the mandatory metadata.

Additional functionality can be enabled through optional pages and metadata without increasing complexity for simple courses.

---

# 3. Repository Structure

```text
.github/

_sections/
│
├── components/
│     navbar.qmd
│     footer.qmd
│
│     welcome.qmd
│     announcements.qmd
│     upcoming.qmd
│     quick-links.qmd
│     team-preview.qmd
│
└── pages/
      schedule.qmd
      syllabus.qmd
      practical.qmd
      precourse.qmd
      resources.qmd
      faq.qmd
      team.qmd

_generated/

content/
    index.qmd

data/
    course.yml
    website.yml
    schedule.yml
    team.yml

img/
scripts/
js/
includes/

index.qmd
_quarto.yml
styles.css
README.md
```

---

# 4. Data Files

The template uses four YAML configuration files.

| File | Purpose |
|------|---------|
| `course.yml` | Course metadata and educational metadata |
| `website.yml` | Website configuration and behaviour |
| `team.yml` | People and roles |
| `schedule.yml` | Programme and timetable |

---

# 5. course.yml

`course.yml` stores all metadata describing the course itself.

It is intended to support:

- Website generation
- FAIR metadata
- README generation
- Future citation generation
- Future repository metadata

## Schema

```yaml
course:

  # Identity
  title:
  subtitle:
  abstract:
  description:

  # Delivery
  start_date:
  end_date:
  duration:
  format:
  location:
  language:

  # Educational
  target_audience:
  expertise_level:

  prerequisites:
    knowledge:
    technical:

  learning_outcomes:

  topics:

  # Contact
  contact_email:

reuse:

  keywords:

  content_provider:

  licence:

  doi:

  version:

  lifecycle:

  created:

  published:

  revised:
```

## Mandatory Fields

- `title`
- `description`
- `duration`
- `format`
- `language`
- `target_audience`
- `expertise_level`
- `prerequisites.knowledge`
- `prerequisites.technical`
- `learning_outcomes`
- `topics`
- `contact_email`
- `keywords`
- `content_provider`
- `licence`

---

# 6. website.yml

`website.yml` controls website behaviour and configuration.

It does **not** describe the course.

## Core Pages

The following pages are always present:

- Home
- Course content
- Syllabus

## Optional Pages

- Schedule
- Practical information
- Pre-course
- Resources
- FAQ
- Team

## Schema

```yaml
navigation:
  content_label: Course content

pages:
  schedule: true
  practical: true
  precourse: false
  resources: false
  faq: false
  team_page: false

homepage:
  announcements: true
  upcoming: true

registration:
  enabled: false
  label: Register now
  url:
```

---

# 7. team.yml

`team.yml` contains all people associated with the course.

It serves as the single source of truth for:

- Homepage team preview
- Team page
- README authors and contributors
- Future citation generation
- Future FAIR metadata

## Schema

```yaml
team:

  - name:

    roles:
      - Course lead
      - Author
      - Instructor
      - Teaching assistant
      - Contributor
      - Reviewer
      - Developer

    job_title:

    affiliation:

    email:

    orcid:

    linkedin:

    github:

    image:
```

## Supported Roles

- Course lead
- Author
- Instructor
- Teaching assistant
- Contributor
- Reviewer
- Developer

A person may have multiple roles.

---

# 8. schedule.yml

`schedule.yml` contains all time-based events associated with the course.

It does **not** describe the course content.

Course structure belongs in the `content/` directory.

## Schema

```yaml
events:

  - title:

    type:

    group:

    start:

    end:

    all_day: false

    location:

    people:

    description:

    content: 
```

`content:` is an optional reference to the corresponding learning material in the content/ directory. It is used to link Schedule events to course content and does

## Supported Event Types

- lecture
- workshop
- practical
- discussion
- webinar
- assessment
- deadline
- social
- break
- lunch
- other

## Grouping

The `group` field is optional.

### Default behaviour

If `group` is omitted:

- Events are sorted by their start time.
- Events are grouped automatically by date.
- The Schedule page displays headings such as:

```text
Day 1
Monday 12 October 2026

Day 2
Tuesday 13 October 2026
```

### Custom grouping

If `group` is provided, events are grouped using that value instead.

Examples include:

- Workshop Day 1
- Week 1
- Module 1

---

# 9. Content Organization

The `content/` directory contains the actual learning material.

Unlike the YAML files, the content structure is intentionally flexible.

Recommendations:

- Keep `index.qmd` as the landing page for the course material.
- Organize additional pages in whatever way best suits the course.
- Use Quarto cross-references or links to guide learners.
- Group related pages into folders if the course becomes large.

The template does not prescribe a particular pedagogical structure.

For example, a course may be organized by:

- Modules
- Lectures
- Practicals
- Assignments
- Topics

or any other structure appropriate for the course.

---

# 10. Component Responsibilities

## Navbar - MANDATORY

**Purpose**

Provide site-wide branding, navigation, and access to course registration.

### Data dependencies

| Source | Fields |
|--------|--------|
| `course.yml` | `course.title` |
| `website.yml` | `navigation.content_label` |
| `website.yml` | `pages.*` |
| `website.yml` | `registration.enabled` |
| `website.yml` | `registration.label` |
| `website.yml` | `registration.url` |

### Behaviour

- Always display the SciLifeLab logo.
- Always display the course title.
- Always display links to:
  - Home
  - Course content
  - Syllabus
- Display optional navigation items according to `website.pages`.
- Display the registration button only if `registration.enabled` is `true`.
- Use `navigation.content_label` as the label for the Course content page.

### Output

The navbar contains:

- SciLifeLab logo
- Course title
- Navigation menu
- Optional registration button

## Welcome - MANDATORY

**Purpose**

Introduce the course by presenting its title and key delivery information.

### Data dependencies

| Source | Fields |
|--------|--------|
| `course.yml` | `course.title` |
| `course.yml` | `course.subtitle` *(optional)* |
| `course.yml` | `course.start_date` |
| `course.yml` | `course.end_date` |
| `course.yml` | `course.location` |

### Behaviour

- Display the course title prominently.
- Display the course subtitle if provided.
- Display the course dates if available.
- Display the course location if available.

### Output

The generated header of the Welcome section contains:

- Course title
- Optional subtitle
- Course dates
- Course location

## Upcoming - OPTIONAL

**Purpose**

Highlight the next upcoming scheduled event for the course.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `homepage.upcoming` |
| `schedule.yml` | `events.title` |
| `schedule.yml` | `events.start` |
| `schedule.yml` | `events.end` |
| `schedule.yml` | `events.location` |
| `schedule.yml` | `events.people` |

### Behaviour

- Display the component only if `homepage.upcoming` is `true`.
- Identify the next upcoming event based on the current date and time.
- Ignore events that have already ended.
- Display only a single event.
- If no future events exist, hide the component.
- Ignore events that have already ended.

### Output

The Upcoming component displays:

- Event date
- Event time
- Event title
- People
- Location

## Quick Links - MANDATORY

**Purpose**

Provide prominent navigation cards linking to the main sections of the course website.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `pages.*` |
| `website.yml` | `navigation.content_label` |

### Behaviour

- Display the component on the homepage.
- Always display cards for:
  - Course content
  - Syllabus
- Display optional cards only if the corresponding page is enabled in `website.yml`.
- Each card links to its corresponding page.
- The title of the Course content card uses `navigation.content_label`.

### Author editable

The following are edited directly in `quick-links.qmd`:

- Card descriptions
- Call-to-action text
- Icons
- Card layout and styling

### Output

The Quick Links component displays a responsive grid of navigation cards for all available course sections.


## Announcements - OPTIONAL

**Purpose**

Communicate important information and updates to course participants.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `homepage.announcements` |

### Behaviour

- Display the component only if `homepage.announcements` is `true`.
- The component content is authored directly in `announcements.qmd`.
- Support one or more announcements.
- Announcements are displayed in the order they appear in the file.

### Author editable

The following are edited directly in `announcements.qmd`:

- Announcement dates
- Announcement text
- Links
- Formatting

### Output

A list of course announcements, each containing:

- Date
- Announcement text


## Team Preview - MANDATORY

**Purpose**

Introduce the course team by highlighting a small selection of members and providing a link to the full team page.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `pages.team_page` |
| `team.yml` | `team.name` |
| `team.yml` | `team.roles` |
| `team.yml` | `team.affiliation` |
| `team.yml` | `team.image` |

### Behaviour

- Display up to three team members.
- Team members are displayed in the order they appear in `team.yml`.
- Display the first role listed for each team member.
- Display a "View full team" button if the Team page is enabled.
- Hide the button if the Team page is disabled.

### Output

Each team member card displays:

- Profile image
- Name
- Primary course role
- Affiliation

The component includes an optional **View full team** button linking to the Team page.

## Footer - MANDATORY

**Purpose**

Provide attribution, licensing information, and links related to the course website.

### Data dependencies

None.

### Behaviour

- Display the standard SciLifeLab Training footer on every page.
- Include licensing information.
- Include attribution to the SciLifeLab Training Hub.
- Include a link to the course GitHub repository.
- The footer is identical for all course websites.

### Author editable

The footer content is maintained directly in `footer.qmd`.

### Output

The footer contains:

- Attribution
- License information
- GitHub link

## Schedule OPTIONAL

**Purpose**

Present the course programme as a chronological timetable of scheduled events and, where available, direct learners to the corresponding course content.

### Data dependencies

| Source | Fields |
|--------|--------|
| `schedule.yml` | `events.title` |
| `schedule.yml` | `events.content` |
| `schedule.yml` | `events.type` |
| `schedule.yml` | `events.group` |
| `schedule.yml` | `events.start` |
| `schedule.yml` | `events.end` |
| `schedule.yml` | `events.all_day` |
| `schedule.yml` | `events.location` |
| `schedule.yml` | `events.people` |
| `schedule.yml` | `events.description` |

### Behaviour

- Display all events in chronological order.
- Group events by `group` if one or more events define a group.
- Otherwise, group events automatically by date.
- Display event times unless `all_day` is `true`.
- Display a visual badge indicating the event type.
- Display the event location if provided.
- Display associated people if provided.
- Display the event description if provided.
- Link the event title to the corresponding course content page if `content` is provided.

### Author editable

The Schedule page layout and styling are maintained in `schedule.qmd`.

### Output

The Schedule page displays a chronological timetable of course events.

Each event includes:

- Date
- Start time
- End time
- Event type badge
- Event title *(linked to the corresponding course content page when available)*
- Location *(optional)*
- People *(optional)*
- Description *(optional)*

## Syllabus - MANDATORY

**Purpose**

Provide a structured overview of the course, including its educational objectives, delivery, and key metadata.

### Data dependencies

| Source | Fields |
|--------|--------|
| `course.yml` | `course.title` |
| `course.yml` | `course.subtitle` |
| `course.yml` | `course.description` |
| `course.yml` | `course.learning_outcomes` |
| `course.yml` | `course.prerequisites.knowledge` |
| `course.yml` | `course.prerequisites.technical` |
| `course.yml` | `course.language` |
| `course.yml` | `course.format` |
| `course.yml` | `course.duration` |
| `course.yml` | `course.target_audience` |
| `course.yml` | `course.expertise_level` |
| `course.yml` | `course.topics` |
| `course.yml` | `course.contact_email` |
| `course.yml` | `reuse.licence` |

### Behaviour

- Present course information in a structured layout.
- Display optional fields only if they are provided.
- Preserve the order of learning outcomes and topics as defined in `course.yml`.

### Author editable

None.

The Syllabus page is generated entirely from `course.yml`.

### Output

The Syllabus page contains:

- Course title
- Subtitle *(optional)*
- Course description
- Learning outcomes
- Prerequisites
  - Knowledge prerequisites
  - Technical prerequisites
- Target audience
- Expertise level
- Language
- Format
- Duration
- Topics
- Contact information
- License

## Team - OPTIONAL

**Purpose**

Introduce the course team and provide information about the people involved in developing and delivering the course.

### Data dependencies

| Source | Fields |
|--------|--------|
| `team.yml` | All fields |

### Behaviour

- Display all team members in the order they appear in `team.yml`.
- Display all roles associated with each team member.
- Display only fields that are provided.

### Output

Each team member profile may include:

- Profile image
- Name
- Course roles
- Job title
- Affiliation
- Email
- ORCID
- GitHub
- LinkedIn

## Practical Information - OPTIONAL

**Purpose**

Provide logistical information to course participants.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `pages.practical` |

### Behaviour

- Display the page only if enabled.

### Author editable

The page content is maintained directly in `practical.qmd`.

## Pre-course - OPTIONAL

**Purpose**

Provide instructions and preparation material before the course begins.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `pages.precourse` |

### Behaviour

- Display the page only if enabled.

### Author editable

The page content is maintained directly in `precourse.qmd`.

## Resources - OPTIONAL

**Purpose**

Provide additional learning resources related to the course.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `pages.resources` |

### Behaviour

- Display the page only if enabled.

### Author editable

The page content is maintained directly in `resources.qmd`.

## FAQ - OPTIONAL

**Purpose**

Provide answers to frequently asked questions.

### Data dependencies

| Source | Fields |
|--------|--------|
| `website.yml` | `pages.faq` |

### Behaviour

- Display the page only if enabled.

### Author editable

The page content is maintained directly in `faq.qmd`.


---

# 11. Rendering Architecture

The course website is built using a three-layer architecture that separates data, rendering logic, and presentation.

## 11.1 Authored Content

Website structure, page composition, and editable course content are maintained as Quarto documents.

These include:

```text
index.qmd

_sections/
    components/
    pages/

content/
```

Course authors edit these files to:

- write course material;
- customize homepage text;
- provide practical information;
- add pre-course instructions;
- create FAQs and resource lists; and
- control the overall page layout.

Quarto files contain presentation and composition only.

They do not contain data processing, rendering logic, or Python code.

---

## 11.2 Data and Rendered Components

Structured course information is maintained in the YAML configuration files:

```text
data/
    course.yml
    website.yml
    team.yml
    schedule.yml
```

During the Quarto pre-render step, the Python renderer:

- validates the YAML files;
- checks internal consistency;
- transforms structured data into reusable Quarto fragments; and
- writes those fragments to `_generated/`.

For example:

```text
_generated/
    navbar.qmd
    quick-links.qmd
    upcoming.qmd
    team-preview.qmd
    schedule.qmd
    syllabus.qmd
```

Generated files are implementation artifacts.

They should never be edited manually, as they are recreated every time the renderer runs.

---

## 11.3 Presentation

The authored Quarto pages assemble the website by including the generated components where required.

For example:

```text
index.qmd
    ├── welcome.qmd
    ├── announcements.qmd
    ├── quick-links.qmd
    └── footer.qmd
```

Individual components include the generated fragments they require.

This keeps the authored Quarto files simple, readable, and focused entirely on presentation.

---

# 12. Render Flow

The website is rendered as part of the Quarto build process.

The render sequence is:

1. `quarto render` starts.
2. Quarto runs the course renderer as a pre-render step.
3. The renderer reads and validates:
   - `course.yml`
   - `website.yml`
   - `team.yml`
   - `schedule.yml`
4. The renderer generates reusable Quarto fragments in `_generated/`.
5. The authored pages in `_sections/` include the generated fragments.
6. `index.qmd` assembles the complete website.
7. Quarto renders the final HTML site.
8. The rendered website is written to `_site/`.

The relationship between the main components is therefore:

```text
course.yml ────────┐
website.yml ───────┤
team.yml ──────────┤
schedule.yml ──────┘
        │
        ▼
scripts/render_course.py
        │
        ▼
_generated/*.qmd
        │
        ▼
_sections/*.qmd
        │
        ▼
index.qmd
        │
        ▼
_site/

styles.css ───────────────────────────────────────────────►
```

---

# 13. Rendering Responsibilities

The renderer is responsible for:

- validating all YAML configuration files;
- checking required fields and data types;
- validating relationships between data files;
- verifying references (for example, that `events.content` refers to existing course content);
- transforming structured data into reusable Quarto fragments;
- generating navigation;
- generating homepage components;
- generating timetable and team components;
- generating the syllabus page;
- generating future repository artifacts such as citations or metadata.

The renderer does **not** generate complete pages.

Overall page composition remains the responsibility of the authored Quarto files.

This architecture maintains a clear separation of responsibilities:

| Layer | Responsibility |
|--------|----------------|
| YAML | Structured course data |
| Python | Validation and rendering |
| Quarto | Composition and presentation |
| CSS | Styling and responsive behaviour |

---

# 12. Architecture Summary

The template consists of five independent components:

| Component | Responsibility |
|-----------|----------------|
| `course.yml` | What is this course? |
| `website.yml` | How should the website behave? |
| `team.yml` | Who created and delivers the course? |
| `schedule.yml` | When do events happen? |
| `content/` | What do learners study? |

Each component has a single responsibility and acts as the authoritative source for its respective information.

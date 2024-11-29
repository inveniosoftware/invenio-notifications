..
    Copyright (C) 2023 CERN.
    Copyright (C) 2024 Graz University of Technology.

    Invenio-Notifications is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======


Version 1.0.0 (release 2024-12-10)

- setup: bump major dependencies

Version 0.6.1 (release 2024-11-30)

- setup: change to reusable workflows
- setup: pin dependencies
- i18n:push translations

Version 0.6.0 (released 2024-06-04)

- dependencies: bump invenio-records-resources

Version 0.5.0 (released 2024-03-22)

- init: move menu and breadcrumb into finalize_app
  (removes before_first_request deprecation)
- Fix transifex config


Version 0.4.0 (released 2023-10-06)

- backends: set email reply to field
- generators: add conditional recipient generator

Version 0.3.0 (released 2023-08-30)

- backends: strip html tags for plain text mail
- i18n: remove gettext call for backend only messages
- i18n: add transifex config

Version 0.2.1 (released 2023-07-12)

- force locale when rendering template in task

Version 0.2.0 (released 2023-06-06)

- views: register notification settings menu
- backends: render template fully once to establish context

Version 0.1.1 (released 2023-05-05)

- remove type hints

Version 0.1.0 (released 2023-05-04)

- Initial public release.

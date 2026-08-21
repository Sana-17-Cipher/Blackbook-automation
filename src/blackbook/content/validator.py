def validate_project(project):
    errors = []
    warnings = []

    if not project.title:
        errors.append("Project title is missing.")

    if not project.student_name:
        errors.append("Student name is missing.")

    if not project.uid:
        errors.append("UID is missing.")

    if not project.chapters:
        errors.append("No chapters found.")

    for chapter in project.chapters:

        if not chapter.title:
            errors.append(
                f"Chapter {chapter.number} has no title."
            )

        if not chapter.sections:
            warnings.append(
                f"Chapter {chapter.number} has no sections."
            )

        for section in chapter.sections:

            if not section.content.strip():
                warnings.append(
                    f"Section '{section.title}' has no content."
                )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
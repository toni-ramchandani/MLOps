name: Pull Request
description: Create a pull request
title: "[PR] "

body:
  - type: markdown
    attributes:
      value: |
        ## Pull Request Template

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe your changes
    validations:
      required: true

  - type: textarea
    id: related
    attributes:
      label: Related Issues
      description: "Closes #(issue number)"

  - type: textarea
    id: testing
    attributes:
      label: Testing
      description: How was this tested?
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: Code follows style guidelines
          required: true
        - label: Tests added/updated
          required: true
        - label: Documentation updated
          required: true
        - label: No breaking changes
          required: true

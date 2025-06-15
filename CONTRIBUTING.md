# Contributing to Raspberry Pi Weather Station

Thank you for considering contributing to the Raspberry Pi Weather Station project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers understand your report, reproduce the issue, and find related reports.

Before creating bug reports, please check the issue tracker as you might find that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples.
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem.
* **If the problem is related to performance or memory**, include a CPU profile capture with your report.
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples.
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of the project which the suggestion is related to.
* **Explain why this enhancement would be useful** to most users.
* **List some other applications where this enhancement exists.**
* **Specify which version of the project you're using.**
* **Specify the name and version of the OS you're using.**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Python style guides
* Include tests when adding new features
* Update documentation when changing the API

## Development Process

### Setting Up Development Environment

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/rpi-weather-station.git`
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment:
   * On Unix/macOS: `source .venv/bin/activate`
   * On Windows: `.venv\Scripts\activate`
5. Install development dependencies: `pip install -r requirements/local.txt`
6. Create a branch for your changes: `git checkout -b feature/your-feature-name`

### Code Style

This project uses Ruff for code formatting and linting. Before submitting your code, please run:

```bash
make format
```

### Testing

All new code should include tests. Run the tests with:

```bash
make test
```

## Documentation

Documentation is a crucial part of this project. Please update the documentation when you change or add features.

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

* `bug` - Issues that are bugs
* `documentation` - Issues or PRs related to documentation
* `enhancement` - Issues that are feature requests or PRs that add new features
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested

## Thank You!

Your contributions to open source, large or small, make projects like this possible. Thank you for taking the time to contribute.
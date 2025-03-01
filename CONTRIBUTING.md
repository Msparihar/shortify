# Contributing to Shortify

We love your input! We want to make contributing to Shortify as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issue tracker](https://github.com/yourusername/shortify/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/shortify/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Process

1. Clone the repo
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests and linting
5. Commit your changes
6. Push to your fork
7. Create a Pull Request

### Backend Development

1. Install dependencies:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run tests:

   ```bash
   pytest
   ```

3. Check code style:

   ```bash
   black .
   isort .
   flake8
   ```

### Frontend Development

1. Install dependencies:

   ```bash
   cd frontend
   pnpm install
   ```

2. Run tests:

   ```bash
   pnpm test
   ```

3. Check code style:

   ```bash
   pnpm lint
   ```

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Use Black for formatting
- Use isort for import sorting
- Maximum line length: 88 characters (Black default)

### TypeScript/JavaScript

- Use ESLint configuration
- Use Prettier for formatting
- Follow React best practices
- Use TypeScript for type safety

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

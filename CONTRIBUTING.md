# Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your bug report or contribution.

## How to Contribute

### 1. Fork the Repository

[fork](https://help.github.com/articles/fork-a-repo/) the repository on GitHub and clone it to your local machine.

```bash
git clone https://github.com/infraspecdev/bentoml-template
```

### 2. Create a Branch

Create a new branch for your feature or bug fix. Use a descriptive name for your branch.

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

Make the necessary changes to the codebase. Ensure your changes adhere to the project's coding standards.

### 4. Test Your Changes

Test your changes thoroughly to ensure they work as expected. If possible, add tests to verify the functionality. <p>
#### Checklists for contributions
- [ ] `pytest`

### 5. Commit Your Changes

Commit your changes with a descriptive commit message.

```bash
git add .
git commit -m "Add feature: Description of your feature"
```

### 6. Push Your Changes

Push your changes to your forked repository.

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

Github has documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

To generate changelog, Pull Requests or Commits must have semantic and must follow conventional specs below:

- `feat:` for new features
- `fix:` for bug fixes
- `improvement:` for enhancements
- `docs:` for documentation and examples
- `refactor:` for code refactoring
- `test:` for tests
- `ci:` for CI purpose
- `chore:` for chores stuff

The `chore` prefix skipped during changelog generation. It can be used for `chore: update changelog` commit message by example.

## Code Style

Please ensure your code follows the existing coding style and conventions.

## Reporting Issues

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check existing open, or recently closed, issues to make sure somebody else hasn't already
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A reproducible test case or series of steps
* The version of our code being used
* Any modifications you've made relevant to the bug
* Anything unusual about your environment or deployment

## Thank You!

Thank you for contributing to `bentoml-template` ! Your support is greatly appreciated.

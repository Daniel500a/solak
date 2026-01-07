# Contributing to Solak

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Daniel500a/solak.git
cd solak
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

Run all tests:
```bash
python -m unittest test_region_finder.py -v
```

Run a specific test:
```bash
python -m unittest test_region_finder.TestRegionFinder.test_find_region_from_images_exact_match
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write comprehensive docstrings for all public methods
- Keep functions focused and single-purpose

## Adding New Features

1. Create tests for your new feature
2. Implement the feature
3. Ensure all tests pass
4. Update documentation
5. Submit a pull request

## Testing Your Changes

Before submitting, make sure:
- All unit tests pass
- The example script runs successfully
- Documentation is updated
- No security vulnerabilities are introduced

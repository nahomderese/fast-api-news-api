# Tests for SWEN AI Pipeline

This directory contains comprehensive tests for the SWEN AI Pipeline project.

## Test Structure

```
tests/
├── services/
│   └── test_brave_search_service.py  # Tests for BraveSearchService
└── README.md
```

## Running Tests

### Prerequisites

1. Install the testing dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you're in the project root directory.

### Running the BraveSearchService Tests

You can run the tests in several ways:

#### Option 1: Using the test runner script
```bash
python run_tests.py
```

#### Option 2: Using pytest directly
```bash
# Run all tests
pytest tests/services/test_brave_search_service.py -v

# Run specific test methods
pytest tests/services/test_brave_search_service.py::TestBraveSearchService::test_search_images_success -v

# Run with coverage (if pytest-cov is installed)
pytest tests/services/test_brave_search_service.py --cov=swen_ai_pipeline.services.brave_search_service
```

#### Option 3: Using the Makefile (if available)
```bash
make test
```

## Test Coverage

The `test_brave_search_service.py` file includes comprehensive tests for:

### BraveSearchService.search_images()
- ✅ Successful image search with proper response parsing
- ✅ Custom parameters (count, country)
- ✅ No results handling
- ✅ Missing properties in response
- ✅ HTTP errors
- ✅ General exceptions
- ✅ Missing API key

### BraveSearchService.search_videos()
- ✅ Successful video search with proper response parsing
- ✅ Custom parameters (count, country)
- ✅ No results handling
- ✅ Missing fields in response
- ✅ HTTP errors
- ✅ General exceptions
- ✅ Missing API key

### BraveSearchService.discover_media()
- ✅ Successful media discovery
- ✅ No results handling

### Service Initialization
- ✅ Proper initialization with API key
- ✅ Initialization without API key

### Integration-style Tests
- ✅ Mocked httpx responses for realistic testing

## Test Features

- **Async Testing**: Uses `pytest-asyncio` for testing async methods
- **Mocking**: Comprehensive mocking of external dependencies (httpx, settings)
- **Fixtures**: Reusable test fixtures for common test data
- **Error Handling**: Tests for various error conditions
- **Edge Cases**: Tests for missing data and malformed responses
- **Parameter Testing**: Tests for different parameter combinations

## Notes

- Tests use mocked HTTP responses to avoid making real API calls
- All tests are isolated and don't depend on external services
- Tests cover both success and failure scenarios
- The test suite is designed to be fast and reliable

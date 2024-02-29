# Python Loki Logger

Welcome to the `python-loki-logger` project! This open-source Python package simplifies the process of pushing logs to Grafana Loki, offering a seamless integration to enhance your logging capabilities and gain valuable insights.

## Features

- **Easy Integration**: Simple and intuitive API to integrate with your existing projects.
- **Customizable Severity Levels**: Tailor your logging experience with customizable severity levels.
- **Authentication Support**: Built-in authentication support for secure log pushing.
- **Well-Structured Code**: Clean, well-organized codebase following best practices.

## Getting Started

### Installation

You can install the `python-loki-logger` package using pip:

```bash
pip install python-loki-logger
```

### Example Usage

```python
from python_loki_logger import LokiLogger

# Instantiate the logger
logger = LokiLogger(baseUrl="https://your-loki-instance.com")

# Log an error message
logger.error("Something went wrong!")

# Log an info message with additional labels
logger.info("Application started successfully", labels={"app": "my-app"})
```

## Contribute

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests on our [GitHub repository](https://github.com/your-repo/python-loki-logger).

## Conclusion

Elevate your logging game with `python-loki-logger`. Explore the package, provide feedback, and contribute to its continuous improvement. Thank you for your support, and happy logging!

---

Thank you for exploring `python-loki-logger`. Let's make logging to Grafana Loki a breeze together!

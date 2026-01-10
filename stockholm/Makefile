all: setup

setup:
	@echo "Installing dependencies..."
	@pip3 install cryptography>=41.0.0 2>/dev/null || pip install cryptography>=41.0.0
	@chmod +x stockholm
	@echo "Setup complete. Run with: ./stockholm <key>"

clean:
	@echo "Nothing to clean"

.PHONY: all setup clean

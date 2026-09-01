import sys
import os

# Add src/ to the path so tests can import modules like
# `from weather_tool import get_weather` regardless of which
# directory pytest is invoked from.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
#!/usr/bin/env python3


from prometheus_client import start_http_server, Gauge
import subprocess
import time

# Define the metric
locked_hint_metric = Gauge('screen_unlocked', 'Screen unlock status as boolean (1: unlocked, 0: locked)')

def fetch_locked_hint():
	try:
		# Run the command and capture the output
		result = subprocess.run(['loginctl', 'show-session', '2'], capture_output=True, text=True)
		output = result.stdout

		# Parse the output to find the "LockedHint" line
		for line in output.splitlines():
			if line.startswith("LockedHint="):
				# Extract the value and convert it to boolean
				locked_hint_value = line.split('=')[1].strip()
				return 1 if locked_hint_value == "no" else 0
	except Exception as e:
		print(f"Error fetching LockedHint: {e}")
	return 0

if __name__ == '__main__':
	# Start the HTTP server to expose the metrics
	start_http_server(8000)
	print("Custom metrics exporter running on port 8000")

	while True:
		# Fetch the metric value
		locked_hint = fetch_locked_hint()
		print(locked_hint)

		# Set the gauge to the fetched metric value
		locked_hint_metric.set(locked_hint)

		# Sleep for a bit before fetching the metric again
		time.sleep(5)

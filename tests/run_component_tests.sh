#!/bin/bash
HARNESS=simple_app_harness

# Build and start Container Under Test (CUT) and test harness
docker-compose up -d --build

# Pass stdout of test harness to stdout of this process
docker logs -f $HARNESS

# Retrieve exit code of the test harness in order for this script to return the same code
TEST_HARNESS_EXIT_CODE=$(docker wait $HARNESS)

# If test harness was run with `rmi` option then tear down build docker images
if [ "$1" = "rmi" ]; then
	docker-compose down --rmi local -v
else
	docker-compose down
fi

# Return exit code of the test harness
exit $TEST_HARNESS_EXIT_CODE

"""Module contains component tests for simple_app service/container."""


def test_basic_consul_templating(simple_app):
	"""Verify changes in consul configuration cause simple_app to update and use latest values."""
	simple_app.write_service_input('hello')
	assert simple_app.read_service_output() == 'hello'

	simple_app.consul_set('zmq_message_suffix', ' world!')

	# Sleep for arbitrary amount of time otherwise next write and read will occur before
	# consul-template restarts service
	import time;time.sleep(5)

	simple_app.write_service_input('hello')
	assert simple_app.read_service_output() == 'hello world!'

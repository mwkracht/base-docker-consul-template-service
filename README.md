# Migrating Legacy App into Microservice/Distributed System Deployment

This project is intended to serve as an example of how to migrate an existing legacy application into a container-based microservices distributed system.

In this project `src/simple_app` serves as the legacy application which reads a static configuration file at startup and whose configuration cannot change at run-time (thus requiring a service restart to consume a new configuration). In a container-based distributed system we assume that there exists some key-value store (in this case consul) for storing configuration values. In order to hook our legacy application into this system we need to containerize the application and also adapt its static configuration file assumption to the dynamic key-value configuration store.

That's where [consul-template](https://github.com/hashicorp/consul-template) comes in. We package the `simple_app` application along with a consul-template process in the `simple_app` container. The consul-template process will generate a new configuration file anytime `simple_app` configuration keys change within the consul key-value store. After the new configuration file is generated consul-template will restart `simple_app` using supervisorctl.

#### Drawbacks

Of course there are many other options for tying an application into a key-value store like consul: The consul-template service could be run outside of the same container as the application, you may have higher level orchestration tools which take care of the config templating, or your application could be refactored to directly pull and update from the key-value store itself.

The main drawback to this approach is that multiple services must be run in a single container (simple_app and consul-template). This is done using supervisord which is [not an uncommon approach for the problem of running multiple services in a single container](https://docs.docker.com/config/containers/multi-service_container/). The issue with running multiple services mostly revolves around logging but in this case the consul-template and application services should mostly be running/logging at separate times. In the end, the logging issue did not outweigh the benefits of having a single image for the application where templating and configuration would melt into the black box that is the single image.

#### Testing

`simple_app` provides its own set of unit tests which are run (along with linting) using tox in the base simple_app directory: `src/simple_app`.

There are also component tests which test the simple_app container. The setup for these tests is defined in a docker-compose file in `tests` directory. The simple_app container is setup along with a consul container and another container which is running the actual component tests. This allows for running tests against the actual container ( not just the simple_app source code) which is important in a deployment model where the docker image is the deployed component.

Currently there are only component tests for verifying that the config templating setup correctly responds to changes in consul key-value store. These are provided mostly as examples and would be extended for a more complicated application.

To run the component tests, run `tests/run_component_tests.sh`.
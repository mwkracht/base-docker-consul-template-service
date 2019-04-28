# This denotes the start of the configuration section for Consul. All values
# contained in this section pertain to Consul. More information about this
# file can be found at https://github.com/hashicorp/consul-template

template {
  source = "/etc/simple_app/simple_app.yaml.ctmpl"
  destination = "/etc/simple_app/simple_app.yaml"
  command = "/usr/bin/supervisorctl restart simple_app"
}

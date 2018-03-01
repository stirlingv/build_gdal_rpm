VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/centos-6.7"
  config.vm.provision :shell, path: "bootstrap.sh"
  config.vm.network :private_network, ip: "192.168.99.110"
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--name", "ggdal-centos", "--memory", "4000"]
  end
end
#!/bin/bash
git clone https://github.com/pedrogazquez/appBares.git
cd appBares/VAGRANT-baresquesada/
vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
vagrant up --provider=azure
vagrant provision 

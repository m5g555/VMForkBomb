# Intended to be run on a debian
# To start this it will prob need a currently installed psutil and numpy

import sys, os, psutil, numpy

passwrd = "SUDO PASSWORD ON CURRENT MACHINE AND FOR ALL FORKED MACHINES"
memoryForVM = (psutil.virtual_memory.available)/3
storageForVM = (psutil.disk_usage.free)/3
storageForVMInMB = numpy.floor(storageForVM/1048576)

def installModules():
    os.system('''
    su -
    {password}
    apt install python3-psutil
    apt install python3-numpy
'''.format(password=passwrd))

def installVB():
    os.system('''su -
                {password}
                echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-2016.gpg] https://download.virtualbox.org/virtualbox/debian <mydist> contrib" >> /etc/apt/sources.list
                apt update
                wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc | sudo gpg --yes --output /usr/share/keyrings/oracle-virtualbox-2016.gpg --dearmor
                apt update
                apt install virtualbox-7.0
              '''.format(password = passwrd))

def createDebianVM(num):
    os.system('''
        VBoxManage createvm --name Fork{id} --ostype Debian --register
        VBoxManage modifyvm Fork{id} --memory{memory} --bridgeadapter1 msk1 --nic1 bridged
        VBoxManage storagectl Fork{id} --name "SATA Controller" --add sata --controller IntelAhci
        VBoxManage storageattach Fork{id} --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium VirtualBox\ VMs/Fork{id}/Fork{id}.vdi
        VBoxManage modifyhd VMs/Fork{id}/Fork{id}.vdi --resize{storage}
        '''.format(id = num, memory=memoryForVM, storage=storageForVMInMB))
    

def __main__():
    installModules()
    for x in range(0,2):
        createDebianVM(x)
        runFileOnVM(x)

echo "Starting auto-deployment..."

echo "\n[server]" >> hosts
var="$(python connect.py | grep -Po '(\d{1,3}\.){3}\d{1,3}')"
echo "$var"
echo "$var" >> hosts

export var

#ansible-playbook -i hosts -u ubuntu --key-file=~/demokey tasks/volume.yml
ansible-playbook -i hosts -u ubuntu --key-file=~/demokey tasks/transferfile.yml
ansible-playbook -i hosts -u ubuntu --key-file=~/demokey tasks/harvest.yml
ansible-playbook -i hosts -u ubuntu --key-file=~/demokey tasks/apache2.yml
ansible-playbook -i hosts -u ubuntu --key-file=~/demokey tasks/couchnode.yml
#ansible-playbook -i hosts -u ubuntu --key-file=~/demokey runthis1.yml

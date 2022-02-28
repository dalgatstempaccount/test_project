apt install -y python3
apt install -y python3-pip 
apt install -y python3-pytest

pip install -r requirements.txt

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt -y install ./google-chrome-stable_current_amd64.deb
# balle_pico
Ball-E's control interface with Raspberry Pi Pico(2) and uPython 

## Usage
0. (**One-Time**) Install dependencies and grant user permission to access Pico
  ```console
  sudo apt install python3-pip
  pip install rshell
  sudo usermod -aG dialout $USER
  ```

  > [!TIP]
  > Reboot computer to gain access.

1. Download and dive into the repository.

  ```console
  cd ~  # use $HOME as an example
  git clone https://github.com/UCAEngineeringPhysics/balle_pico.git
  cd ~/balle_pico
  ```

2. Upload motion and perception controller 

  ```console
  rshell cp -r upython_scripts/mobile_base /pyboard/
  rshell cp -r upython_scripts/perception /pyboard/
  ```

3. Set up automatic communication using [`pico_interface.py`](./upython_scripts/pico_interface.py).

  ```console
  rshell cp upython_scripts/pico_interface.py /pyboard/main.py
  ```

  > [!TIP]
  > A hard reset (unplug Pico then plug it back) is required to activate `main.py`.

> [!NOTE]
> If you are completely new to Pico or MicroPython, please follow the official [guide](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/) to get started.

## Test

Run [`computer_usb_messenger.py`](/tests/computer_usb_messenger.py) on a desktop/laptop/SBC to test USB communication.

```console
cd ~/homer_pico/
python3 tests/computer_usb_messenger.py
```

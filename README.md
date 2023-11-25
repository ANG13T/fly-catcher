<p align="center">
  <img width="200" src="https://github.com/ANG13T/fly-catcher/blob/main/assets/logo.png" alt="Fly Catcher logo" />
</p>
<h1 align="center" style="font-size:50px !important;">Fly Catcher</h1>
<p align="center">
  <i>Fly Catcher monitors for malicious ADS-B signals in the 1090MHz frequency to detect for aircraft spoofing</i>
   <br/><br/>
  <b><a href="#features-️">Learn More</a></b> | <b><a href="#build-it-yourself-️">Build Guide</a></b> | <b><a href="#detecting-for-spoofing-">Getting Started</a></b> | <b><a href="#watch-it-in-action-">Video</a></b> | <b><a href="https://github.com/ANG13T/fly-catcher/blob/main/assets/project_report.pdf">Research Paper</a></b>
  <br/><br/>
</p>

<details>
  <summary><b>Table of Contents</b></summary>
  <p>
  
- **Getting Started**
  - [✈️ Features](#features-️)
  - [⚡ Demo Gallery](#demo-gallery-️)
  - [⚙️ Build it Yourself](#build-it-yourself-️)
  - [🚀 Getting Started](#detecting-for-spoofing-)
  - [🔎 Detecting for Spoofing](#detecting-for-spoofing-)
- **Learning More**
  - [🎥 Watch it in Action](#watch-it-in-action-)
  - [🔬 Read the Research Paper](https://github.com/ANG13T/fly-catcher/blob/main/assets/project_report.pdf)
  - [📄 Read the Article](#article)
- **Community**
  - [✨ Contributing](#contributing-)
  - [🏆 Special Thanks & Credits](#special-thanks--credits-)
  - [💜 Support](#support-)
  - [📜 License](https://github.com/ANG13T/fly-catcher/blob/main/LICENSE)
    
  </p>
</details>

## Features ✈️
- 🔎  Detecting spoofed ADS-B messages
- 📡  Logging messages on the 1090 MHz frequency
- ✈️  Mapping and visualizing ADS-B messages
- ⚙️  A portable Raspberry-Pi based device
- ⚡️  An accurate neural network classifier
- 🔨  3D printable case with small form factor
- 📻  Compatible with the FlightAware SDR

## Demo Gallery ⚡️

<table>
  <tr>
    <td valign="top"><img src="https://github.com/ANG13T/fly-catcher/blob/main/assets/display_1.png?raw=true" alt="Gallery Image" height="180" width="250"> <h4 align="center">Picture of the completed build</h4></td>
    <td valign="top"><img src="https://github.com/ANG13T/fly-catcher/blob/main/assets/display_2.png?raw=true" alt="Gallery Image" height="180" width="250"> <h4 align="center">Device shown with the SportCruiser</h4></td>
    <td valign="top"><img src="https://github.com/ANG13T/fly-catcher/blob/main/assets/display_3.png?raw=true" alt="Gallery Image" height="180" width="250"> <h4 align="center">Display shown on the TFT Screen</h4></td>
  </tr>
</table>

## Watch it in Action 🎥
Watch the video overview of Fly Catcher on YouTube

## Build it Yourself ⚙️

###  Materials List
- 1090MHz Rubber Ducky Antenna
- Raspberry Pi 3B
- FlightAware Pro Stick Plus SDR
- 3.5 in TFT Screen
- Portable Battery Charger
- USB-C to Micro USB Cable
- [Custom 3D Printed Case](https://github.com/ANG13T/fly-catcher/blob/main/fabrication/Device_Case.f3d)
- SD Card
- Rasbian Operating System
- 4x 3/32 Screws
- Python and Pip on Raspberry Pi

<img src="https://github.com/ANG13T/fly-catcher/blob/main/assets/materials.png?raw=true" alt="Folium Map" width="400" />

### Constructing the Device
1. Install the Rasbian operating system to the Raspberry Pi with the SD Card
2. Connect the Flight Aware SDR to the Raspberry Pi using the Micro USB cable
3. Connect the 1090 MHz antenna to the Flight Aware SDR
4. Configure the 3.5-inch TFT Screen to the Raspberry Pi
5. Place the Device into the 3D Printed Case
6. Ensure Python and Pip are installed on the Raspberry Pi
7. Install dump-1090 FlightAware library on the Raspberry Pi to receive ADS-B
information

#### The following tutorial is very helpful for getting dump-1090 installed on the Pi
[https://www.stuffaboutcode.com/2015/11/raspberry-pi-piaware-aircraft-radar.html](https://www.stuffaboutcode.com/2015/11/raspberry-pi-piaware-aircraft-radar.html)

### Running the Radar Code

Clone the Repository on the Pi
```
git clone https://github.com/ANG13T/fly-catcher.git
```

Run the Program
```
python3 fly-catcher/device-rpi/piawareradar.py longitude latitude
```
Replace longitude and latitude with your [geo-coordinates](https://www.gps-coordinates.net/)

## Detecting for Spoofing 🔎

### Download the Jupyter Notebook
```
git clone https://github.com/ANG13T/fly-catcher.git
cd notebook
jupyter notebook
```
Install [Jupyter Notebook](https://jupyter.org/install) if you do not have it

### Open up the localhost server at `http://localhost:8888`

### Download JSON Flight Logs from Device
Visit the IP address of the Raspberry Pi device followed by the path `/data/aircraft.json`
For example, `192.168.1.114:8080/data/aircraft.json`

<img src="https://github.com/ANG13T/fly-catcher/blob/main/assets/flight_log_screenshot.png?raw=true" alt="Folium Map" width="400" />

### Open `Fly_Catcher.ipynb` and Run the Notebook

<img src="https://github.com/ANG13T/fly-catcher/blob/main/assets/folium_map.png?raw=true" alt="Folium Map" width="400" />

## Research Paper 🔬
To get a more in-depth and technical overview of Fly Catcher, you can refer to this [research paper](https://github.com/ANG13T/fly-catcher/blob/main/assets/project_report.pdf).

## Future Improvements 🚀
- Enhanced UI features on the radar screen 
- Deep learning techniques such as RNNs and LSTM networks
- Incorporating reinforcement learning techniques
- Differentiate spoofing attacks (ie. GPS spoofing, aircraft masquerading, etc)

## Contributing ✨
Fly Catcher is open to any contributions. Please fork the repository and make a pull request with the features or fixes you want to implement.

## Special Thanks & Credits 🏆
The Fly Catcher leveraged on previous ADS-B works and references included below

- [Pi Aware Radar by Martin O'Hanlon](http://www.stuffaboutcode.com/2015/11/raspberry-pi-piaware-aircraft-radar.html)
- [Reference dump1090 README](https://github.com/SDRplay/dump1090/blob/master/README-json.md)
- [Data Samples from ADSB Exchange](https://www.adsbexchange.com/data-samples/)
- [IEEE Research on ADS-B Signals](https://ieeexplore.ieee.org/document/9377975)

## Support 💜
If you enjoyed Fly Catcher, please consider becoming a sponsor in order to fund my future projects.

To check out my other works, visit my [GitHub profile](github.com/ANG13T).

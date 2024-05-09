## Content Steering for Adaptive Video Streaming over the Edge-Cloud Continuum: A Hands-on Experience 

This repository was created to host the materials for the NOMS'24 tutorial.

### Abstract

Video streaming is among the most used Internet applications nowadays, with many big techs competing for a share in a billion-dollar market size. The demands of these video streaming products require the careful utilization of computing resources strategically placed close to the end users to deliver high-quality experience services. New technologies such as 6G and edge-cloud continuum infrastructures have been investigated to supply these increasing computing resource demands. These technologies are envisioned to be combined to provide fast and reliable data transfer for extremely high volumes of data. The edge-cloud continuum, particularly, also enables service placement mobility from the cloud data centers placed on the core of the network all the way to the edge devices closer to the end-users. However, network management to support seamless service mobility and timely and precise computing resource allocation to maintain high-quality service experiences is extremely complex. As a way forward, in this scenario, the concept known as zero-touch network, where there is no need for human interaction to (re)configure networked systems and the network itself, has gained popularity. In the video streaming application domain, the combination of Content Steering architecture, part of the Dynamic Adaptive Streaming over HTTP (DASH) protocol, and container orchestrator technologies would allow strategies for autonomous video streaming services placement throughout the continuum with minimal human involvement and maximum computing resources exploitation. In this context,  this tutorial offers a hands-on experience with state-of-the-art technology that supports content steering for adaptive video streaming on the edge-cloud continuum. We present the latest technology, architectures, and tools that enable the creation and autonomous management of adaptive video streaming applications on the continuum, leveraging the hierarchy of computing resources to provide high-quality experiences to end-users. Our tutorial provides both a theoretical and practical experience for the participants who will have access to a small edge-cloud virtual testbed to explore strategies for steering requests to video content to services placed throughout the computing continuum. We will also lay down current challenges and future opportunities for research in this area.


## Prerequisites:

- [mkcert](https://github.com/FiloSottile/mkcert)
- [docker](https://www.docker.com/)

## VirtualBox VM:

We provide a fully configured VirtualBox VM with all the necessary software for you to download and explore our tutorial's testbed. You can download the pre-configured VM in the following link: https://drive.google.com/file/d/1mCB585muebdJIN6yXbioIoD1762svy3T/view?usp=sharing

To use the VM, you'll need VirtualBox installed on your system. For more information on how to install VirtualBox or how to import a VM image, please refer to: https://www.virtualbox.org/

## Configure Environment Tutorial:


## 1. Clone the Tutorial Repository
First, clone the tutorial repository from GitHub using Git:

```shell
git clone https://github.com/robertovrf/content-steering-tutorial
```

## 2. Set Up Local Streaming Service

### 2.1 Set Up Local Custom Domains and Certificates 
Edit your local hosts file located at /etc/hosts to assign local custom domain names for streaming and steering services. Then, run the script create_certs.sh to generate certificates and enable HTTPS in localhost:

```shell
./create_certs.sh <streaming-domain> <steering-domain>
```

### 2.1 Download DASH Video Dataset

Download a DASH video from the mmsys dataset and save it to the designated folder named dataset. The dataset offers various codec options such as AV1, AVC, HEVC, and VVC. You can use wget or any other method to download the video.


### 2.2 Start Local Streaming Service

Run the script create_streaming.sh to initiate the regional streaming setup where the streaming services will run:

```shell
./starting_streaming.sh
```

You can now verify if the local video streaming is operational. Access the [dash.js](https://reference.dashif.org/dash.js/latest/samples/dash-if-reference-player/index.html) player and attempt to load the manifest using the following URL format:

```shell
https://streaming-service/<streaming path>/manifest.mpd
```

Replace <streaming-service> with your streaming domain and <streaming-path> with the path to your video.


## References

- [mmsys22 Dataset](https://doi.org/10.1145/3524273.3532889) 
Babak Taraghi, Hadi Amirpour, and Christian Timmerer. 2022. Multi-codec ultra high definition 8K MPEG-DASH dataset. In Proceedings of the 13th ACM Multimedia Systems Conference (MMSys '22). Association for Computing Machinery, New York, NY, USA, 216–220. 

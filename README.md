## Content Steering for Adaptive Video Streaming over the Edge-Cloud Continuum: A Hands-on Experience 

This repository was created to host the material for the NOMS'24 tutorial.

### Abstract

Video streaming is among the most used Internet applications nowadays, with many big techs competing for a share in a billion-dollar market size. The demands of these video streaming products require the careful utilization of computing resources strategically placed close to the end users to deliver high-quality experience services. New technologies such as 6G and edge-cloud continuum infrastructures have been investigated to supply these increasing computing resource demands. These technologies are envisioned to be combined to provide fast and reliable data transfer for extremely high volumes of data. The edge-cloud continuum, particularly, also enables service placement mobility from the cloud data centers placed on the core of the network all the way to the edge devices closer to the end-users. However, network management to support seamless service mobility and timely and precise computing resource allocation to maintain high-quality service experiences is extremely complex. As a way forward, in this scenario, the concept known as zero-touch network, where there is no need for human interaction to (re)configure networked systems and the network itself, has gained popularity. In the video streaming application domain, the combination of Content Steering architecture, part of the Dynamic Adaptive Streaming over HTTP (DASH) protocol, and container orchestrator technologies would allow strategies for autonomous video streaming services placement throughout the continuum with minimal human involvement and maximum computing resources exploitation. In this context,  this tutorial offers a hands-on experience with the state-of-the-art technology that supports content steering for adaptive video streaming on the edge-cloud continuum. We present the latest technology, architectures, and tools that enable the creation and autonomous management of adaptive video streaming applications on the continuum, leveraging the hierarchy of computing resources to provide high-quality experiences to end-users. Our tutorial provides both a theoretical and practical experience for the participants who will have access to a small edge-cloud virtual testbed to explore strategies for steering requests to video content to services placed throughout the computing continuum. We will also lay down current challenges and future opportunities for research in this area.


### Slides Outline

1. Introduction
2. DASH
  - What is DASH?
  - How does it work?
  - Introducing the Content Steering Architecture
  - dash.js
3. Containers
  - Introduction
  - Kernel-level Virtualization
  - Docker Image creation: 
    - Resource Availability
    - Network Configuration
4. Container-orchestrators
  - Introduction
  - Container lifetime cycle
  - Kubernetes:
    - Introduction
    - Deployment Creation
5. Video Streaming Application: Putting it all together
  - Architecture
  - Deployment
  - Service Mobility and Adaptation
6. Current Challenges and Future Opportunities


### Practical Exercises

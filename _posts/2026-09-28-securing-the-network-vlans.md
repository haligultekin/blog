---
layout: post
title: "Securing the Network: VLAN Segmentation"
date: 2026-09-28 10:00:00 +0000
categories: homelab security
tags: [security, network, vlan]
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=80"
---
When building a homelab, flattening your network (putting all devices on the same subnet) is a security risk. If a smart light bulb gets compromised, you don't want it having direct access to your backup NAS.

### The Solution: VLANs
Virtual Local Area Networks (VLANs) allow you to logically separate your network traffic using a managed switch and a capable router/firewall. 

In my setup, I use strict segmentation:
* **IoT Network:** For smart home devices. This network has no access to other local devices and restricted internet access.
* **Server Network:** For my homelab servers.
* **Trusted Network:** For my personal laptops and phones.
* **Guest Network:** Isolated internet access for visitors.

By configuring strict firewall rules between these VLANs, I ensure that my critical infrastructure remains secure even if another part of the network is exposed.

---
layout: post
title: "The Heart of the Homelab: A Deep Dive into My Architecture"
date: 2026-09-24 10:00:00 +0000
categories: homelab architecture
tags: [homelab, server, infrastructure, hardware]
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=80"
---

Welcome to the beating heart of my digital life! If you are new to the world of homelabs, you might be wondering why anyone would want a rack of blinking servers humming away in a closet. For me, it started as a simple desire to self-host a few files. Over time, it evolved into an obsession with digital sovereignty, learning enterprise-grade IT skills, and automating my entire vintage reselling business. 

In this post, I want to take you through the high-level architecture of my setup. Building a reliable homelab is less about buying the most expensive hardware and more about designing a system that is resilient, low-power, and highly automated.

### The Philosophy: Separation of Concerns

When you first start out, it is tempting to install everything onto a single, massive operating system. You install your hypervisor, your storage array, and your Docker engine all on one machine. While this works, it creates a single point of failure. If that machine needs a reboot, your entire network goes dark.

Instead, I have adopted a strict separation of concerns across three distinct layers.

### Layer 1: The Gateway

The edge of my network is protected by a dedicated hardware firewall. This device does exactly one thing: route traffic and secure the perimeter. It handles my strict VLAN segmentation, blocking malicious incoming traffic, and providing secure WireGuard VPN access so I can securely connect to my servers from my phone when I am sourcing vintage denim at flea markets. By keeping the firewall on dedicated hardware, I can reboot my compute nodes without losing internet access for the rest of the house.

### Layer 2: The Compute Nodes

The actual processing power of my lab comes from a cluster of small form-factor PCs. These "micro nodes" run my hypervisor (Proxmox). Instead of one massive server, having multiple small servers allows me to pool their resources. If one node experiences a hardware failure, the hypervisor automatically shifts the virtual machines to a surviving node. This high availability ensures that my AI models, Telegram bots, and reselling scripts never experience downtime. 

### Layer 3: The Storage Array

Compute is useless without data. My storage array is a heavily fortified, dedicated NAS (Network Attached Storage) system. This system is loaded with high-capacity NAS-rated hard drives running in a redundant ZFS pool. If a drive fails, the system continues operating normally while alerting me to swap it out. This array serves as the central repository for all my container volumes, automated backups, and extensive media library. The compute nodes access this storage over a high-speed internal network, meaning the compute nodes themselves are completely stateless.

### The Result

By adhering to this three-tier architecture, maintaining the lab becomes a joy rather than a chore. Upgrading hardware, patching software, or recovering from a hardware failure is completely modular. Over the next few posts, we will dive deeper into the specific software that brings this hardware to life!

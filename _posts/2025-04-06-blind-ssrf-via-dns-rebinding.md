---
title: "Blind SSRF via DNS Rebinding"
date: 2025-04-06
layout: post
---

<body>
<div class="container">
<header>
<h1>Blind SSRF via DNS Rebinding</h1>
</header>
<p><strong>Blind SSRF via DNS rebinding</strong> is a technique where an attacker leverages a server’s backend URL-fetching functionality and uses DNS tricks to pivot into internal systems. The DNS rebinding part works by resolving an attacker-controlled domain (e.g., <code>payload.rbndr.us</code>) to a public IP on the first lookup, and then switching to an internal IP (e.g., <code>127.0.0.1</code> or <code>192.168.x.x</code>) once the DNS cache expires. This bypasses network-layer protections like IP whitelisting or NAT boundaries.</p>
<p>The "blind" part refers to the lack of direct response from the vulnerable server. The attacker infers internal access by monitoring side channels — such as response timing, status codes, or connection failures.</p>
<p>In this case, while testing the endpoint <code>https://api.target.com/vendor/v3/external_registry</code>, I supplied a rebinding payload in the <code>endpoint</code> parameter and used timing analysis to enumerate internal IPs. The results indicated the server made backend requests and likely resolved internal addresses.</p>
<h2>Steps to Reproduce</h2>
<ol>
<li>Capture a request to: <code>https://api.target.com/vendor/v3/external_registry</code></li>
<li>Generate a payload using: <a href="https://lock.cmpxchg8b.com/rebinder.html" target="_blank">https://lock.cmpxchg8b.com/rebinder.html</a><br/>
                Example: <code>7f000001.ac14000a.rbndr.us</code></li>
<li>Insert the payload into the <code>endpoint</code> parameter of the POST body.</li>
<li>Send the request to Burp Intruder. Use the “Positions” tab to select two characters from the rebinding subdomain.</li>
<li>Under “Payloads”, use numbers 01–154, representing <code>192.168.0.1</code> through <code>192.168.0.153</code>.</li>
<li>Launch the attack and monitor the “Response Completed” time. Increased latency suggests the server resolved or connected to internal targets.</li>
</ol>
<img alt="Intruder Result Screenshot" src="/assets/images/writeup/intruder.png"/>
<p align="center">response timings</p>
<img alt="Payload Screenshot" src="/assets/images/writeup/payload.png"/>
<p align="center">rebinding payloads</p>
<h2>Impact</h2>
<p>This vulnerability allowed internal IP enumeration via DNS rebinding and blind SSRF behavior. Although no response data was leaked, the ability to interact with internal infrastructure is a stepping stone to more serious attacks — especially when combined with metadata service access or open ports on internal services.</p>
<h2>Timeline</h2>
<ul>
<li>March 28, 2022 – Initial report submitted</li>
<li>March 30, 2022 – First response from program; 192.168.0.0/24 not in use</li>
<li>March 31, 2022 – Retested using Class A IPs; consistent timing anomalies observed</li>
<li>April 1, 2022 – Report accepted and bounty awarded</li>
</ul>
<footer>
            Thanks, <br/> Anand
        </footer>
</div>
</body>

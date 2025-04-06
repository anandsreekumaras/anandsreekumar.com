---
title: "Remote Code Execution via Dependency Confusion"
date: 2025-04-06
layout: post
---

<body>
<div class="container">
<header>
<h1>Remote Code Execution via Dependency Confusion</h1>
</header>
<p>The following write-up details how I discovered a dependency confusion vulnerability on a HackerOne private program, leading to remote code execution.</p>
<p>Let's refer to the organization as <strong>orgxyz</strong>.</p>
<p>While running fuff on one of orgxyz's subdomains, I stumbled upon a disclosed <code>package-lock.json</code> file, specifically <code>engineering.orgxyz.com/package-lock.json</code>.</p>
<img alt="Package Lock File" src="/assets/images/writeup/pkglck.png"/>
<p>The file contained over 100 packages, sparking the idea to test for dependency confusion.</p>
<p><i>What is dependency confusion? <p>Dependency confusion, also known as "substitution attacks," is a sneaky tactic hackers use to trick developers. They upload malicious code to public libraries, pretending it's a trusted internal one. When developers use these libraries, they accidentally download the harmful code. It's like getting fake medicine instead of the real thing. </p> <a href="https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610">Read more...</a></i></p>
<p>Thus, the challenge was to identify missing NPM packages. Fortunately, the <code>package-lock.json</code> included NPM registry URLs, prompting me to ping each URL to detect missing packages.</p>
<img alt="urls" src="/assets/images/writeup/regurls.png"/>
<p>I sought assistance from ChatGPT to obtain a Bash script that would provide the status code after visiting each URL. A 404 status code indicated a missing package, notably <strong>orgxyz-css-1.0.4.tgz</strong>.</p>
<p>Hosting the package <strong>orgxyz-css-1.0.4</strong> on NPM with a higher version could potentially lead to an internal application or server within orgxyz inadvertently executing my code.</p>
<h2>Next steps:</h2>
<ol>
<li>Create an account on npmjs.com.</li>
<li>Develop an <code>index.js</code> script to send a ping back to a canary token or Burp collaborator URL if executed.</li>
<img alt="index.js file" src="/assets/images/writeup/indexjs.png"/>
<li>Compose a <code>package.json</code> specifying the missing package name. Ensure to use a higher package version for automatic pull.</li>
<img alt="Package.json" src="/assets/images/writeup/pkgjson.png"/>
<li>Publish the package and await triggered canary tokens.</li>
<li>About three hours later, I received an email notification confirming the execution of my code on orgxyz's system.</li>
<img alt="Canary Token Triggered" src="/assets/images/writeup/cantoken.png"/>
<li>Next morning, I decided to compose another <code>index.js</code> file to execute system commands and extract information, forwarding them to a Burp collaborator URL.</li>
<li>Uploaded the new <code>index.js</code> and monitored responses on my Burp collaborator. Ping backs with command execution outputs were received approximately an hour later.</li>
<img alt="Canary Token Triggered" src="/assets/images/writeup/collaburl2.png"/>
<li>Upon verifying all details, report the vulnerability to the private program. Draft the report and send it once the issue is resolved, resulting in a bounty award.</li>
<!-- <img src="/assets/images/writeup/h1pgm.png" alt="Bounty Awarded"> -->
</ol>
<h2>Timeline:</h2>
<ul>
<li>March 10, 2024 - Discovery of missing package</li>
<li>March 14, 2024 - Reporting the issue via HackerOne after reproducing the bug</li>
<li>March 23, 2024 - Issue resolution and bounty award</li>
</ul>
</div><br/>
<p style="text-align: center;">Thanks, <br/> Anand</p>
</body>

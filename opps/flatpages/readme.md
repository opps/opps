
Flatpage
========

Flatpages are used to give life to simple pages like:

 - About
 - Company profile

Or any information that doesn't need Channel, Container or any kind of relationship.
It is commonly defined as "Static Page" on others CMS.

Templating
----------

To create/extend a Flatpage template you must create a file named with the same slug as the Flatpage object.

Let's imagine I created a page called *About* with slug *about* and another named *Our Team* with slug *our-team*:

    .../templates/flatpages/about.html
    .../templates/flatpages/our-team.html

And accessed by /page/about.html and /page/our-team.html


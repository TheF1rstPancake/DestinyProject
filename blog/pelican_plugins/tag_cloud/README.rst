tag_cloud
=========

This plugin generates a tag-cloud.

Settings
--------

================================================    =====================================================
Setting name (followed by default value)            What does it do?
================================================    =====================================================
``TAG_CLOUD_STEPS = 4``                             Count of different font sizes in the tag
                                                    cloud.
``TAG_CLOUD_MAX_ITEMS = 100``                       Maximum number of tags in the cloud.
``TAG_CLOUD_SORTING = 'random'``                    The tag cloud ordering scheme.  Valid values:
                                                    random, alphabetically, alphabetically-rev, size and
                                                    size-rev
================================================    =====================================================

The default theme does not include a tag cloud, but it is pretty easy to add one::

    <ul class="tagcloud">
        {% for tag in tag_cloud %}
            <li class="tag-{{ tag.1 }}"><a href="{{ SITEURL }}/{{ tag.0.url }}">{{ tag.0 }}</a></li>
        {% endfor %}
    </ul>

You should then also define CSS styles with appropriate classes (tag-1 to tag-N,
where N matches ``TAG_CLOUD_STEPS``), tag-1 being the most frequent, and
define a ``ul.tagcloud`` class with appropriate list-style to create the cloud.
For example::

    ul.tagcloud {
      list-style: none;
        padding: 0;
    }

    ul.tagcloud li {
        display: inline-block;
    }

    li.tag-1 {
        font-size: 150%;
    }

    li.tag-2 {
        font-size: 120%;
    }

    ...

By default the tags in the cloud are sorted randomly, but if you prefers to have it alphabetically use the `alphabetically` (ascending) and `alphabetically-rev` (descending). Also is possible to sort the tags by it's size (number of articles with this specific tag) using the values `size` (ascending) and `size-rev` (descending).
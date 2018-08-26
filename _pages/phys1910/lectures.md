---
layout: page
title: PHYS 1910 Lectures
---

Here you can find an archive of lecture recordings for the PHYS 1910 course, which you can find out more about [here]( {{ site.url }}{{ site.baseurl }}/phys1910/about/ ).

<div class="lectures-years" id="lectures-years">
    {% for year in site.data.phys1910.lectures %}
    {%- capture year_no_spaces -%}
        {{ year.year | remove: " " }}
    {%- endcapture -%}
    {% if year.year == site.data.phys1910.current-year %}
        {% assign expanded = true %}
    {% else %} 
        {% assign expanded = false %}
    {% endif %}
    {% include collapse-list-heading.html
       heading=year.year
       target-id=year_no_spaces
       heading-type='h1'
       expanded=expanded
    %}
    <div class="recordings collapse {% if year.year == site.data.phys1910.current-year %} show {% endif %}" id="{{ year_no_spaces }}" aria-labelledby="{{ year_no_spaces }}" data-parent="#lectures-years">
        {% if year.recordings %}
        {% for recording in year.recordings %}
            <div class="collapse-list-heading collapsed" data-toggle="collapse" data-target="#{{ recording.id }}" aria-expanded="false" aria-controls="{{ recording.id }}">
                <h3>
                    <a class="recording-info"> 
                        {{ recording.speaker }} - {{ recording.title }} 
                    </a>
                </h3>
            </div>
            <div class="recording-container collapse" id="{{ recording.id }}" aria-labelledby="{{ recording.id }}">
                {% if recording.slides %}
                <h4>
                    Slides can be found <a href="{{ recording.slides }}">here</a>.
                </h4>
                {% endif %}
                <iframe class="recording-video" src="https://uva.hosted.panopto.com/Panopto/Pages/Embed.aspx?id={{ recording.id }}&v=1" frameborder="0" allowfullscreen allow="autoplay">
                </iframe>
            </div>
        {% endfor %}
        {% else %}
            <p> Oops...doesn't look like there are any videos for {{ year.year }}. Try checking out the archive of previous years' videos below. </p>
        {% endif %}
    </div>
    {% endfor %}
</div>
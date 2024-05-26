---
theme: cotton
title: Birds of Briggs Terrace
toc: false
---

<style type="text/css">
  ul#birdBadges {
    list-style-type: none;
    padding: 0px;
  }
  ul#birdBadges li {
    height 240px;
    width: 120px;
    display: inline-block;
    vertical-align: top;
    text-align: center;
    margin: 5px;
  }
  img.birdBadge {
    height: 120px;
    width: 120px;
    border-radius: 60px;
  }
  span.comName {
    font-size: 11px;
    display: block;
  }
  span.sciName {
    font-size: 11px;
    font-style: italic;
    display: block;
  }
  span.firstTimeDetected {
    font-size: 11px;
    display: block;
  }
</style>

# Birds of Briggs Terrace

Our hobby is tracking the birds that visit our yard. This page is a report of the detections we've heard so far! Each "detection" is made by a small outdoor microphone. A bird with more 
detections spent more time in our yard than bird with less.


```js
const detectionsByDayL365 = FileAttachment("data/detectionsByDayL365.csv").csv({typed: true});
const detectionsByHourOfDayL365 = FileAttachment("data/detectionsByHourOfDayL365.csv").csv({typed: true});
const detectionsNewBirds = FileAttachment("data/detectionsNewBirds.csv").csv({typed: true});
```

```js
const top_birds_colors = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(detectionsByDayL365, (D) => -d3.sum(D, d => d.detections_cnt), (d) => d.comName).filter((d) => d !== "Other"),
    unknown: "#AAA",
    scheme: "Set2"
  }
});
```

```js
function detectionsByDayL365Timeline(data, {width} = {}) {
  return Plot.plot({
    title: "Top birds over the past year (starting Feb 2024)",
    width,
    height: 300,
    y: {grid: true, label: "Detections"},
    x: {grid: true, label: "Date", tickFormat: "%b %d"},
    color: {...top_birds_colors, legend: true},
    marks: [
      Plot.areaY(data, Plot.groupX(
        {y: "sum"},
        {x: "time", y: "detections_cnt_7dma", fill: "comName", interval: "day", tip: true, curve: "bump-x"}
      ))
    ]
  });
}


function detectionsByHourOfDayL365Chart(data, {width} = {}) {
  return Plot.plot({
    title: "Birds by hour of the day",
    width,
    height: 300,
    y: {grid: true, label: "Detections"},
    x: {grid: true, label: "Hour of the day", tickFormat: (d) => String(((d-0.5) % 12) + 1) + (d < 11 ? "AM" : "PM")},
    color: {...top_birds_colors, legend: true},
    marks: [
      Plot.barY(data, Plot.binX(
        {y: "sum"},
        {x: "hour_of_day", y: "detections_cnt", fill: "comName", tip: true, interval: 1}
      ))
    ]
  });
}

```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => detectionsByDayL365Timeline(detectionsByDayL365, {width}))}
  </div>
  <div class="card" style="height: 397px; overflow-y: auto;">
    <h2>Birds by date of detection</h2>
    <ul id="birdBadges"></ul>
  </div>
</div>

```js
var formatBirdBadgeTime = d3.utcFormat("%B %d, %Y")
d3
.select("#birdBadges")
.selectAll("li")
.data(detectionsNewBirds)
.enter()
  .append('li')
  .html(d => ( 
    "<img class='birdBadge' src='https://s3.amazonaws.com/briggsbirds.com/bird-image-store/" + d.sciName + ".jpg' />" +
    "<span class='comName'>" + d.comName + "</span>" + 
    "<span class='sciName'>(" + d.sciName + ")</span>" + 
    "<span class='firstTimeDetected'>" + formatBirdBadgeTime(d.first_time_detected) + "</span>"
  ));
```


<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => detectionsByHourOfDayL365Chart(detectionsByHourOfDayL365, {width}))}
  </div>
</div>

## How it's done

In our yard, there is a microphone hooked into a small computer (a *[Raspberry Pi](https://www.raspberrypi.com/)*) which is running a citizen science model named *[BirdNET](https://birdnet.cornell.edu/)*. Each time a bird is recognized by this model, it's tallied above.

Tech used to make this project work:
1. *[Raspberry Pi 4B](https://www.raspberrypi.com/):* the computer running the local detection model
2. *[BirdNET](https://birdnet.cornell.edu/):* the detection model developed by Cornell University and Chemnitz University researchers.
3. *[BirdNET-Pi](https://github.com/mcguirepr89/BirdNET-Pi):* a collection of scripts used to serve the BirdNET model on a RaspberryPi (a _huge_ amount of work done here by other folks)
4. *AWS Timestream:* for logging bird detections
5. *[Briggs-Freebird](https://github.com/janmtl/briggs-freebird/):* the code for the site you're reading, built with the *[Observable Framework](https://observablehq.com/framework/)* and rebuilt every three hours using _Github Actions_.

## On Privacy

Typically, folks running this software also contribute data to *[Birdweather.com](https://www.birdweather.com/)* but contributing a birdweather station would require us to submit the audio recordings associated with each bird detection. While BirdNET has privacy filters in place to never send sounds recognized as human speech — we felt that we didn't want to risk a false negative getting through. Thus, for our own privacy and the privacy of our neighbors, the audio data associated with bird detections is _never_ logged online and is otherwise regularly purged from the Raspberry Pi in our yard.

---
theme: cotton
title: Birds of Briggs Terrace
toc: false
---

# Birds of Briggs Terrace

Our hobby is tracking the birds that visit our yard. This page is a report of the detections we've heard so far! Each "detection" is made by a small outdoor microphone. A bird with more 
detections spent more time in our yard than bird with less.


```js
const detectionsByDayL365 = FileAttachment("data/detectionsByDayL365.csv").csv({typed: true});
const detectionsByHourL7 = FileAttachment("data/detectionsByHourL7.csv").csv({typed: true});
const detectionsTopKL28 = FileAttachment("data/detectionsTopKL28.csv").csv({typed: true});
const detectionsByHourOfDayL365 = FileAttachment("data/detectionsByHourOfDayL365.csv").csv({typed: true});
```

```js
const top_birds_colors = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(detectionsByHourL7, (D) => -d3.sum(D, d => d.detections_cnt), (d) => d.comName).filter((d) => d !== "Other"),
    unknown: "var(--theme-foreground-muted)",
    scheme: "Set2"
  }
});
```

```js
function detectionsByDayL365Timeline(data, {width} = {}) {
  return Plot.plot({
    title: "Top 10 birds over the past year (starting Feb 2024)",
    width,
    height: 300,
    y: {grid: true, label: "Detections"},
    x: {grid: true, label: "Date", tickFormat: "%b %d"},
    color: {...top_birds_colors, legend: true},
    marks: [
      Plot.rectY(data, Plot.binX(
        {y: "sum"},
        {x: "time", y: "detections_cnt", fill: "comName", interval: "day", tip: true}
      ))
    ]
  });
}

function detectionsByHourL7Timeline(data, {width} = {}) {
  return Plot.plot({
    title: "Birds by hour over the past week",
    width,
    height: 300,
    y: {grid: true, label: "Detections"},
    x: {grid: true, label: "Date", tickFormat: "%b %d"},
    color: {...top_birds_colors, legend: true},
    marks: [
      Plot.rectY(data, Plot.binX(
        {y: "sum"},
        {x: "time", y: "detections_cnt", fill: "comName", interval: "hour", tip: true}
      ))
    ]
  });
}

function bumpChart(data, {x = "time", y = "sum_rank", z = "comName", interval = "day", width} = {}) {
  const num_lookback_days = Math.floor(width / 100)
  const filtered_data = data.filter((d) => d.num_days_back < num_lookback_days)
  const rank = Plot.stackY2({x, z, order: y, reverse: true});
  const [xmin, xmax] = d3.extent(Plot.valueof(filtered_data, x));
  return Plot.plot({
    title: "Top birds over the past two week",
    width,
    x: {
      [width < 480 ? "insetRight" : "inset"]: 120,
      label: null,
      grid: true,
      interval: "day"
    },
    y: {
      axis: null,
      inset: 20,
      reverse: true
    },
    color: {
      scheme: "spectral"
    },
    marks: [
      Plot.lineY(filtered_data, Plot.binX({x: "first", y: "first", filter: null}, {
        ...rank,
        stroke: z,
        strokeWidth: 24,
        curve: "bump-x",
        sort: {color: "y", reduce: "first"},
        interval,
        render: halo({stroke: "var(--theme-background-alt)", strokeWidth: 27})
      })),
      Plot.text(filtered_data, {
        ...rank,
        text: rank.y,
        fill: "black",
        stroke: z,
        channels: {"Common name": "comName", "Scientific name": "sciName", "Detections": (d) => String(d.detections_cnt)},
        tip: {format: {y: null, text: null}}
      }),
      width < 480 ? null : Plot.text(filtered_data, {
        ...rank,
        filter: (d) => d[x] <= xmin,
        text: z,
        dx: -20,
        textAnchor: "end"
      }),
      Plot.text(filtered_data, {
        ...rank,
        filter: (d) => d[x] >= xmax,
        text: z,
        dx: 20,
        textAnchor: "start"
      })
    ]
  })
}

function halo({stroke = "currentColor", strokeWidth = 3} = {}) {
  return (index, scales, values, dimensions, context, next) => {
    const g = next(index, scales, values, dimensions, context);
    for (const path of [...g.childNodes]) {
      const clone = path.cloneNode(true);
      clone.setAttribute("stroke", stroke);
      clone.setAttribute("stroke-width", strokeWidth);
      path.parentNode.insertBefore(clone, path);
    }
    return g;
  };
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
  <div class="card">
    ${resize((width) => detectionsByHourL7Timeline(detectionsByHourL7, {width}))}
  </div>
</div>
<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => bumpChart(detectionsTopKL28, {width}))}
  </div>
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

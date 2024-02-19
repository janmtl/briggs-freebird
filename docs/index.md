---
theme: cotton
title: Birds of Briggs Terrace
toc: false
---

# Birds of Briggs Terrace

<!-- Load and transform the data -->

```js
const detectionsByDayL365 = FileAttachment("data/detectionsByDayL365.csv").csv({typed: true});
const detectionsByHourL7 = FileAttachment("data/detectionsByHourL7.csv").csv({typed: true});
const detectionsTopKL28 = FileAttachment("data/detectionsTopKL28.csv").csv({typed: true});
const detectionsByHourOfDayL365 = FileAttachment("data/detectionsByHourOfDayL365.csv").csv({typed: true});
```

<!-- A shared color scale for consistency, sorted by the number of detections -->

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

<!-- Plot of bird detections -->

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
  const rank = Plot.stackY2({x, z, order: y, reverse: true});
  const [xmin, xmax] = d3.extent(Plot.valueof(data, x));
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
      Plot.lineY(data, Plot.binX({x: "first", y: "first", filter: null}, {
        ...rank,
        stroke: z,
        strokeWidth: 24,
        curve: "bump-x",
        sort: {color: "y", reduce: "first"},
        interval,
        render: halo({stroke: "var(--theme-background-alt)", strokeWidth: 27})
      })),
      Plot.text(data, {
        ...rank,
        text: rank.y,
        fill: "black",
        stroke: z,
        channels: {"Common name": "comName", "Scientific name": "sciName", "Detections": (d) => String(d.detections_cnt)},
        tip: {format: {y: null, text: null}}
      }),
      width < 480 ? null : Plot.text(data, {
        ...rank,
        filter: (d) => d[x] <= xmin,
        text: z,
        dx: -20,
        textAnchor: "end"
      }),
      Plot.text(data, {
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

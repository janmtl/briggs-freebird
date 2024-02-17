---
theme: cotton
title: Birds of Briggs Terrace
toc: false
---

# Birds of Briggs Terrace

<!-- Load and transform the data -->

```js
const birds = FileAttachment("data/unload_results.csv").csv({typed: true});
```

<!-- A shared color scale for consistency, sorted by the number of detections -->

```js
const color = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(birds, (D) => -D.length, (d) => d.comName).filter((d) => d !== "Other"),
    unknown: "var(--theme-foreground-muted)"
  }
});
```

<!-- Plot of bird detections -->

```js
function detectionTimeline(data, {width} = {}) {
  return Plot.plot({
    title: "Detections over days",
    width,
    height: 300,
    y: {grid: true, label: "Detections"},
    color: {...color, legend: true},
    marks: [
      Plot.rectY(data, Plot.binX({y: "sum"}, {x: "time", y: "detections_cnt", fill: "comName", interval: "hour", tip: true}))
    ]
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => detectionTimeline(birds, {width}))}
  </div>
</div>

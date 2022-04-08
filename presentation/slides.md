---
theme: apple-basic
layout: intro-image-right
image: /modularity.svg
---

# Community detection in large open-source projects

## Analyzing scikit-learn contribution graph

<div class="absolute bottom-10">
  <span class="font-700">
    German Arutyunov 08.04.2022
  </span>
</div>

<style>
.slidev-layout h1 + h2 {
    margin-top: 1.5rem;
}
</style>

---
layout: two-cols
class: my-auto
---

<template v-slot:default>

# GitHub Data

* Pull requests: 990
* Reviews: 18905
* Comments: 29077
* Contributors: 509

</template>

<template v-slot:right>

# Graph summary

* Directional homogeneous unweighted graph with self loops
* Nodes: 503
* Edges: 3182

</template>

---
layout: two-cols
---

<template v-slot:default>

# Communication

```mermaid
sequenceDiagram
    Author->>Reviewer #1: Review my PR
    Author->>Reviewer #2: Review my PR
    Reviewer #1->>Author: LGTM
    Reviewer #2->>Reviewer #1: This line is wrong!
    Reviewer #2->>Reviewer #2: NVM! All good!
    Reviewer #1->>Reviewer #2: :)
    Reviewer #2->>Author: LGTM
```

</template>

<template v-slot:right>

# Resulting Graph

```mermaid
graph TD
    B[Reviewer #1] -->|Review| A[Author]
    C[Reviewer #2] -->|Review| A
    C -->|Comment| B
    C -->|Reply| C
    B -->|Reply| C
```

</template>

<style>
.col-left .mermaid {
    margin-top: -4rem;
}

h1 {
    text-align: center;
}

.col-right .mermaid {
    margin-left: 6rem;
    margin-top: 4rem;
}
</style>

---
class: my-auto
---

# Hypothesis

* H1: High clustering coefficient
* H2: Hubs with high degrees and centralities
* H3: Short average path length
* H4: Power-law like distribution
* H5: Few tight communities

---
layout: two-cols
---

<template v-slot:default>

# Clustering coefficient

<img src="/clustering-plot.svg"/>

Average clustering coefficient: 0.77

</template>

<template v-slot:right>

<img src="/clustering.svg"/>

</template>

---
layout: two-cols
---

<template v-slot:default>

# Betweenness centrality and shortest paths

<img src="/path-length-plot.svg"/>

Average path length: 2.48

</template>

<template v-slot:right>

<img src="/betweenness.svg"/>

</template>

---
layout: two-cols
---

<template v-slot:default>

# Power law?

<img src="/degree-plot.svg"/>

</template>

<template v-slot:right>

<img src="/degree.svg"/>

</template>

---
layout: two-cols
---

<template v-slot:default>

# Who are the hubs?

<img src="/contributors.gif"/>

</template>

<template v-slot:right>

<img src="/hits.svg"/>

</template>

<style>
.col-left img {
    margin-top: 6rem;
    margin-left: -1rem;
}
</style>

---
layout: image-right
image: /barabasi-albert.svg
---

# Barabasi & Albert Model

* Nodes: 503
* Edges: 3163

<br>

| Metrics          | Real | BA   |
|------------------|------|------|
| Avg. clustering  | 0.77 | 0.06 |
 | Modularity       | 0.29 | 0.26 |
| Avg. path length | 2.56 | 2.78 |
| Diameter         | 6    | 4    |
| Radius           | 3    | 3    |

---
layout: image-right
image: /modularity.svg
---

# Community detection

* Method: Louvain
* Number of communities: 8
* Modularity: 0.291

---
layout: statement
---

# Thank you for your attention!

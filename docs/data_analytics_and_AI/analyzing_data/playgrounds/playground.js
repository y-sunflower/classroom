(function () {
  "use strict";

  const modelName = document.body.dataset.model;
  const WIDTH = 760;
  const HEIGHT = modelName === "linear" ? 370 : 350;
  const PLOT =
    modelName === "linear"
      ? { left: 72, top: 14, right: 14, bottom: 52 }
      : { left: 44, top: 14, right: 14, bottom: 30 };
  const plotWidth = WIDTH - PLOT.left - PLOT.right;
  const plotHeight = HEIGHT - PLOT.top - PLOT.bottom;
  const canvas = document.getElementById("chart");
  const context = canvas.getContext("2d");
  const plotWrap = canvas.parentElement;
  const controls = Array.from(document.querySelectorAll(".control input"));
  const fitButton = document.getElementById("fit-button");
  const status = document.getElementById("model-status");
  const detail = document.getElementById("chart-detail");
  const sampleCount = document.getElementById("sample-count");
  const sampleOutput = document.getElementById("sample-output");
  const scoreStat = document.getElementById("score-stat");
  const scoreOutput = document.getElementById("score-output");
  const hint = document.getElementById("hint");
  const range =
    modelName === "linear"
      ? { xMin: 15, xMax: 85, yMin: 0, yMax: 600 }
      : { xMin: -1.5, xMax: 2.5, yMin: -1.25, yMax: 1.6 };
  let points = [];
  let model = null;
  let boundary = null;
  let query = null;
  let resizeObserver = null;
  let probabilityTooltip = null;

  if (modelName !== "linear") {
    probabilityTooltip = document.createElement("div");
    probabilityTooltip.className = "probability-tooltip";
    probabilityTooltip.setAttribute("role", "tooltip");
    probabilityTooltip.hidden = true;
    plotWrap.classList.add("probability-enabled");
    plotWrap.appendChild(probabilityTooltip);
  }

  function hideProbabilityTooltip() {
    if (probabilityTooltip) probabilityTooltip.hidden = true;
  }

  function showProbabilityTooltip(event) {
    if (!model || !boundary || !probabilityTooltip) {
      hideProbabilityTooltip();
      return;
    }
    const bounds = canvas.getBoundingClientRect();
    const pixelX = ((event.clientX - bounds.left) / bounds.width) * WIDTH;
    const pixelY = ((event.clientY - bounds.top) / bounds.height) * HEIGHT;
    if (
      pixelX < PLOT.left ||
      pixelX > PLOT.left + plotWidth ||
      pixelY < PLOT.top ||
      pixelY > PLOT.top + plotHeight
    ) {
      hideProbabilityTooltip();
      return;
    }

    const column = Math.min(
      boundary.columns - 1,
      Math.floor(((pixelX - PLOT.left) / plotWidth) * boundary.columns),
    );
    const row = Math.min(
      boundary.rows - 1,
      Math.floor(((pixelY - PLOT.top) / plotHeight) * boundary.rows),
    );
    const pClass1 = Math.round(
      boundary.values[row * boundary.columns + column] * 100,
    );
    const pClass2 = 100 - pClass1;
    probabilityTooltip.textContent =
      "Class 1: " + pClass1 + "% · Class 2: " + pClass2 + "%";
    probabilityTooltip.hidden = false;

    const wrapBounds = plotWrap.getBoundingClientRect();
    let left = event.clientX - wrapBounds.left + 10;
    let top =
      event.clientY - wrapBounds.top - probabilityTooltip.offsetHeight - 10;
    if (top < 5) top = event.clientY - wrapBounds.top + 12;
    if (left + probabilityTooltip.offsetWidth > wrapBounds.width - 5) {
      left =
        event.clientX - wrapBounds.left - probabilityTooltip.offsetWidth - 10;
    }
    left = Math.max(
      5,
      Math.min(left, wrapBounds.width - probabilityTooltip.offsetWidth - 5),
    );
    top = Math.max(
      5,
      Math.min(top, wrapBounds.height - probabilityTooltip.offsetHeight - 5),
    );
    probabilityTooltip.style.left = left + "px";
    probabilityTooltip.style.top = top + "px";
  }

  function seededRandom(seed) {
    let state = seed >>> 0;
    return function () {
      state = (1664525 * state + 1013904223) >>> 0;
      return state / 4294967296;
    };
  }

  function normalRandom(random) {
    const u = Math.max(random(), 0.000001);
    const v = Math.max(random(), 0.000001);
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function value(id, fallback) {
    const input = document.getElementById(id);
    return input ? Number(input.value) : fallback;
  }

  function setOutputs() {
    controls.forEach(function (input) {
      const output = document.getElementById(input.id + "-value");
      if (!output) return;
      const suffix = input.dataset.suffix || "";
      output.value = input.value + suffix;
      output.textContent = input.value + suffix;
    });
    sampleOutput.value = sampleCount.value;
    sampleOutput.textContent = sampleCount.value;
  }

  function makeRegressionData() {
    const count = Number(sampleCount.value);
    const noise = value("noise", 60);
    const random = seededRandom(2026 + count * 13 + Math.round(noise));
    points = [];
    for (let i = 0; i < count; i += 1) {
      const x = 18 + random() * 62;
      const y = 80 + 5.5 * (x - 18) + normalRandom(random) * noise;
      points.push({ x: x, y: y });
    }
  }

  function makeMoonData() {
    const count = Number(sampleCount.value);
    const random = seededRandom(749 + count * 17);
    const half = Math.ceil(count / 2);
    points = [];
    for (let i = 0; i < count; i += 1) {
      const label = i < half ? 0 : 1;
      const angle = random() * Math.PI;
      const bend = 0.13 * normalRandom(random);
      const wobble = 0.13 * normalRandom(random);
      const x =
        label === 0 ? Math.cos(angle) + bend : 1 - Math.cos(angle) + bend;
      const y =
        label === 0
          ? Math.sin(angle) + wobble
          : 0.45 - Math.sin(angle) + wobble;
      points.push({ x: x, y: y, label: label });
    }
    for (let i = points.length - 1; i > 0; i -= 1) {
      const j = Math.floor(random() * (i + 1));
      const current = points[i];
      points[i] = points[j];
      points[j] = current;
    }
  }

  function prepareData() {
    if (modelName === "linear") makeRegressionData();
    else makeMoonData();
    invalidateModel();
  }

  function invalidateModel() {
    model = null;
    boundary = null;
    hideProbabilityTooltip();
    scoreOutput.textContent = "—";
    scoreStat.hidden = true;
    fitButton.disabled = false;
    fitButton.innerHTML =
      'Fit model <span class="arrow" aria-hidden="true">↗</span>';
    status.textContent = "Ready to fit";
    detail.textContent =
      modelName === "linear"
        ? "Each dot is one example"
        : "The background will show the model’s decision regions";
    hint.textContent =
      modelName === "knn"
        ? "Change a setting, fit the model, then click the chart to try a new example."
        : "Change a setting, fit again, and compare the pattern. The score describes the examples used to fit.";
    draw();
  }

  function fitRegression() {
    let meanX = 0;
    let meanY = 0;
    points.forEach(function (point) {
      meanX += point.x;
      meanY += point.y;
    });
    meanX /= points.length;
    meanY /= points.length;
    let covariance = 0;
    let variance = 0;
    points.forEach(function (point) {
      covariance += (point.x - meanX) * (point.y - meanY);
      variance += (point.x - meanX) * (point.x - meanX);
    });
    const penalty = 0;
    const slope = covariance / (variance + penalty * points.length * 0.08);
    const intercept = meanY - slope * meanX;
    return { slope: slope, intercept: intercept };
  }

  function sigmoid(input) {
    if (input < -30) return 0;
    if (input > 30) return 1;
    return 1 / (1 + Math.exp(-input));
  }

  function fitLogistic() {
    const regularization = 5;
    const lambda = 0.015 / regularization;
    let weights = [0, 0, 0];
    const rate = 0.09;
    for (let iteration = 0; iteration < 700; iteration += 1) {
      const gradient = [0, 0, 0];
      points.forEach(function (point) {
        const prediction = sigmoid(
          weights[0] + weights[1] * point.x + weights[2] * point.y,
        );
        const error = prediction - point.label;
        gradient[0] += error;
        gradient[1] += error * point.x;
        gradient[2] += error * point.y;
      });
      weights[0] -= (rate * gradient[0]) / points.length;
      weights[1] -= rate * (gradient[1] / points.length + lambda * weights[1]);
      weights[2] -= rate * (gradient[2] / points.length + lambda * weights[2]);
    }
    return { weights: weights, threshold: value("threshold", 50) / 100 };
  }

  function gini(zeros, ones) {
    const total = zeros + ones;
    if (total === 0) return 0;
    const zeroRate = zeros / total;
    const oneRate = ones / total;
    return 1 - zeroRate * zeroRate - oneRate * oneRate;
  }

  function fitTree(training, maxDepth, minLeaf, randomFeature) {
    function build(rows, depth) {
      let positive = 0;
      rows.forEach(function (point) {
        positive += point.label;
      });
      const probability = positive / rows.length;
      if (
        depth >= maxDepth ||
        rows.length < minLeaf * 2 ||
        probability === 0 ||
        probability === 1
      ) {
        return { probability: probability };
      }

      const features = randomFeature === null ? [0, 1] : [randomFeature()];
      let best = null;
      features.forEach(function (feature) {
        const sorted = rows.slice().sort(function (a, b) {
          return feature === 0 ? a.x - b.x : a.y - b.y;
        });
        let leftPositive = 0;
        for (let index = 0; index < sorted.length - 1; index += 1) {
          leftPositive += sorted[index].label;
          const leftSize = index + 1;
          const rightSize = sorted.length - leftSize;
          if (leftSize < minLeaf || rightSize < minLeaf) continue;
          const currentValue =
            feature === 0 ? sorted[index].x : sorted[index].y;
          const nextValue =
            feature === 0 ? sorted[index + 1].x : sorted[index + 1].y;
          if (currentValue === nextValue) continue;
          const leftGini = gini(leftSize - leftPositive, leftPositive);
          const rightPositive = positive - leftPositive;
          const rightGini = gini(rightSize - rightPositive, rightPositive);
          const score = leftSize * leftGini + rightSize * rightGini;
          if (!best || score < best.score) {
            best = {
              score: score,
              feature: feature,
              threshold: (currentValue + nextValue) / 2,
            };
          }
        }
      });
      if (!best) return { probability: probability };
      const left = [];
      const right = [];
      rows.forEach(function (point) {
        const coordinate = best.feature === 0 ? point.x : point.y;
        (coordinate <= best.threshold ? left : right).push(point);
      });
      if (left.length < minLeaf || right.length < minLeaf)
        return { probability: probability };
      return {
        feature: best.feature,
        threshold: best.threshold,
        left: build(left, depth + 1),
        right: build(right, depth + 1),
      };
    }
    return build(training, 0);
  }

  function fitDecisionTree() {
    return fitTree(points, value("depth", 4), value("leaf", 5), null);
  }

  function fitRandomForest() {
    const count = value("trees", 12);
    const depth = value("forest-depth", 4);
    const random = seededRandom(
      8411 + count * 71 + depth * 313 + points.length,
    );
    const forest = [];
    for (let tree = 0; tree < count; tree += 1) {
      const sample = [];
      for (let index = 0; index < points.length; index += 1) {
        sample.push(points[Math.floor(random() * points.length)]);
      }
      forest.push(
        fitTree(sample, depth, 4, function () {
          return Math.floor(random() * 2);
        }),
      );
    }
    return forest;
  }

  function predictTree(tree, x, y) {
    let node = tree;
    while (typeof node.probability !== "number") {
      const coordinate = node.feature === 0 ? x : y;
      node = coordinate <= node.threshold ? node.left : node.right;
    }
    return node.probability;
  }

  function neighborPredictions(x, y, count, includeDetails) {
    const distances = points.map(function (point, index) {
      const dx = point.x - x;
      const dy = point.y - y;
      return { index: index, distance: dx * dx + dy * dy };
    });
    distances.sort(function (a, b) {
      return a.distance - b.distance;
    });
    const nearest = distances.slice(0, Math.min(count, distances.length));
    let positive = 0;
    nearest.forEach(function (item) {
      positive += points[item.index].label;
    });
    return includeDetails
      ? { probability: positive / nearest.length, nearest: nearest }
      : positive / nearest.length;
  }

  function probabilityAt(x, y) {
    if (modelName === "logistic") {
      const weights = model.weights;
      return sigmoid(weights[0] + weights[1] * x + weights[2] * y);
    }
    if (modelName === "tree") return predictTree(model, x, y);
    if (modelName === "forest") {
      let total = 0;
      model.forEach(function (tree) {
        total += predictTree(tree, x, y);
      });
      return total / model.length;
    }
    return neighborPredictions(x, y, value("neighbors", 7), false);
  }

  function chartX(x) {
    return (
      PLOT.left + ((x - range.xMin) / (range.xMax - range.xMin)) * plotWidth
    );
  }

  function chartY(y) {
    return (
      PLOT.top + ((range.yMax - y) / (range.yMax - range.yMin)) * plotHeight
    );
  }

  function domainX(pixel) {
    return (
      range.xMin + ((pixel - PLOT.left) / plotWidth) * (range.xMax - range.xMin)
    );
  }

  function domainY(pixel) {
    return (
      range.yMax - ((pixel - PLOT.top) / plotHeight) * (range.yMax - range.yMin)
    );
  }

  function resizeCanvas() {
    const ratio = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
    const bounds = canvas.getBoundingClientRect();
    canvas.width = Math.round(bounds.width * ratio);
    canvas.height = Math.round(bounds.height * ratio);
    context.setTransform(
      canvas.width / WIDTH,
      0,
      0,
      canvas.height / HEIGHT,
      0,
      0,
    );
    draw();
  }

  function drawGrid() {
    context.fillStyle = "#fff";
    context.fillRect(0, 0, WIDTH, HEIGHT);
    context.strokeStyle = "#eef2f7";
    context.lineWidth = 1;
    context.fillStyle = "#7b8798";
    context.font = "10px Inter, ui-sans-serif, system-ui, sans-serif";
    context.textAlign = "center";
    context.textBaseline = "top";
    for (let i = 0; i <= 4; i += 1) {
      const x = PLOT.left + (plotWidth * i) / 4;
      const y = PLOT.top + (plotHeight * i) / 4;
      context.beginPath();
      context.moveTo(x, PLOT.top);
      context.lineTo(x, PLOT.top + plotHeight);
      context.stroke();
      context.beginPath();
      context.moveTo(PLOT.left, y);
      context.lineTo(PLOT.left + plotWidth, y);
      context.stroke();
      const xValue = range.xMin + ((range.xMax - range.xMin) * i) / 4;
      const yValue = range.yMax - ((range.yMax - range.yMin) * i) / 4;
      context.fillText(
        xValue.toFixed(modelName === "linear" ? 0 : 1),
        x,
        modelName === "linear" ? HEIGHT - 31 : HEIGHT - 19,
      );
      context.textAlign = "right";
      context.textBaseline = "middle";
      context.fillText(
        modelName === "linear"
          ? "€" + yValue.toFixed(0)
          : yValue.toFixed(1),
        PLOT.left - 7,
        y,
      );
      context.textAlign = "center";
      context.textBaseline = "top";
    }
    if (modelName === "linear") {
      context.fillStyle = "#64748b";
      context.font = "11px Inter, ui-sans-serif, system-ui, sans-serif";
      context.textAlign = "center";
      context.textBaseline = "bottom";
      context.fillText("Age (years)", PLOT.left + plotWidth / 2, HEIGHT - 3);
      context.save();
      context.translate(15, PLOT.top + plotHeight / 2);
      context.rotate(-Math.PI / 2);
      context.fillText("Monthly spend (€ / month)", 0, 0);
      context.restore();
    }
  }

  function drawClassificationBackground(alpha) {
    if (!boundary) return;
    const columns = boundary.columns;
    const rows = boundary.rows;
    const cellWidth = plotWidth / columns;
    const cellHeight = plotHeight / rows;
    context.save();
    context.globalAlpha = alpha;
    for (let row = 0; row < rows; row += 1) {
      for (let column = 0; column < columns; column += 1) {
        const probability = boundary.values[row * columns + column];
        const threshold = modelName === "logistic" ? model.threshold : 0.5;
        const strong = Math.abs(probability - threshold);
        const color = probability >= threshold ? "49, 92, 206" : "232, 135, 90";
        context.fillStyle =
          "rgba(" + color + ", " + (0.08 + strong * 0.23) + ")";
        context.fillRect(
          PLOT.left + column * cellWidth,
          PLOT.top + row * cellHeight,
          cellWidth + 1,
          cellHeight + 1,
        );
      }
    }
    context.restore();
  }

  function drawRegression() {
    drawGrid();
    if (model) {
      context.strokeStyle = "#315cce";
      context.lineWidth = 3;
      context.beginPath();
      context.moveTo(
        chartX(range.xMin),
        chartY(model.intercept + model.slope * range.xMin),
      );
      context.lineTo(
        chartX(range.xMax),
        chartY(model.intercept + model.slope * range.xMax),
      );
      context.stroke();
    }
    points.forEach(function (point) {
      context.beginPath();
      context.arc(chartX(point.x), chartY(point.y), 3.7, 0, Math.PI * 2);
      context.fillStyle = "#e8875a";
      context.fill();
      context.strokeStyle = "#fff";
      context.lineWidth = 1;
      context.stroke();
    });
  }

  function drawClassification(alpha) {
    drawGrid();
    drawClassificationBackground(alpha === undefined ? 1 : alpha);
    points.forEach(function (point) {
      context.beginPath();
      context.arc(chartX(point.x), chartY(point.y), 3.8, 0, Math.PI * 2);
      context.fillStyle = point.label === 1 ? "#315cce" : "#e8875a";
      context.fill();
      context.strokeStyle = "#fff";
      context.lineWidth = 1;
      context.stroke();
    });
    if (query) {
      context.beginPath();
      context.arc(chartX(query.x), chartY(query.y), 7, 0, Math.PI * 2);
      context.fillStyle = "#fff";
      context.fill();
      context.strokeStyle = "#172033";
      context.lineWidth = 2;
      context.stroke();
      context.beginPath();
      context.moveTo(chartX(query.x) - 11, chartY(query.y));
      context.lineTo(chartX(query.x) + 11, chartY(query.y));
      context.moveTo(chartX(query.x), chartY(query.y) - 11);
      context.lineTo(chartX(query.x), chartY(query.y) + 11);
      context.stroke();
    }
  }

  function draw() {
    if (!canvas.width) return;
    if (modelName === "linear") drawRegression();
    else drawClassification();
  }

  function buildBoundary() {
    const columns = 58;
    const rows = 28;
    const values = [];
    for (let row = 0; row < rows; row += 1) {
      const y = range.yMax - ((row + 0.5) / rows) * (range.yMax - range.yMin);
      for (let column = 0; column < columns; column += 1) {
        const x =
          range.xMin + ((column + 0.5) / columns) * (range.xMax - range.xMin);
        values.push(probabilityAt(x, y));
      }
    }
    boundary = { columns: columns, rows: rows, values: values };
  }

  function trainingScore() {
    if (modelName === "linear") {
      const mean =
        points.reduce(function (sum, point) {
          return sum + point.y;
        }, 0) / points.length;
      const total = points.reduce(function (sum, point) {
        return sum + Math.pow(point.y - mean, 2);
      }, 0);
      const residual = points.reduce(function (sum, point) {
        const estimate = model.intercept + model.slope * point.x;
        return sum + Math.pow(point.y - estimate, 2);
      }, 0);
      return total === 0 ? 0 : 1 - residual / total;
    }
    let correct = 0;
    points.forEach(function (point) {
      const prediction = probabilityAt(point.x, point.y);
      const threshold = modelName === "logistic" ? model.threshold : 0.5;
      if ((prediction >= threshold ? 1 : 0) === point.label) correct += 1;
    });
    return correct / points.length;
  }

  function showQueryPrediction() {
    if (!query || modelName !== "knn" || !model) return;
    const result = neighborPredictions(
      query.x,
      query.y,
      value("neighbors", 7),
      true,
    );
    const pClass1 = Math.round(result.probability * 100);
    const pClass2 = 100 - pClass1;
    detail.textContent =
      "Class 1: " +
      pClass1 +
      "% · Class 2: " +
      pClass2 +
      "% of its nearest examples.";
  }

  function fit() {
    if (fitButton.disabled) return;
    hideProbabilityTooltip();
    fitButton.disabled = true;
    status.textContent = "Fitting the model…";
    detail.textContent =
      modelName === "linear"
        ? "Finding a line that follows the examples"
        : "Finding a pattern in the examples";
    hint.textContent = "The model is learning from the sample.";
    window.setTimeout(function () {
      if (modelName === "linear") model = fitRegression();
      if (modelName === "logistic") model = fitLogistic();
      if (modelName === "tree") model = fitDecisionTree();
      if (modelName === "forest") model = fitRandomForest();
      if (modelName === "knn") model = { trained: true };
      if (modelName !== "linear") buildBoundary();
      const score = trainingScore();
      const fittedModel = model;
      scoreStat.hidden = false;
      scoreOutput.textContent =
        modelName === "linear"
          ? Math.max(-1, score).toFixed(2)
          : Math.round(score * 100) + "%";
      status.textContent = "Model fitted";
      detail.textContent =
        modelName === "linear"
          ? "The blue line is the fitted estimate"
          : "The shaded regions show the model’s predictions";
      hint.textContent =
        "This fit score uses the same examples the model learned from. Test on new examples before making decisions.";
      fitButton.disabled = false;
      fitButton.innerHTML =
        'Fit again <span class="arrow" aria-hidden="true">↗</span>';
      let start = 0;
      function reveal(timestamp) {
        if (!start) start = timestamp;
        const progress = Math.min(1, (timestamp - start) / 420);
        drawClassification(progress);
        if (progress < 1) window.requestAnimationFrame(reveal);
        else showQueryPrediction();
      }
      if (modelName === "linear") {
        const meanY =
          points.reduce(function (sum, point) {
            return sum + point.y;
          }, 0) / points.length;
        function revealLine(timestamp) {
          if (!start) start = timestamp;
          const progress = Math.min(1, (timestamp - start) / 420);
          model = {
            slope: fittedModel.slope * progress,
            intercept: meanY + (fittedModel.intercept - meanY) * progress,
          };
          draw();
          if (progress < 1) window.requestAnimationFrame(revealLine);
          else model = fittedModel;
        }
        window.requestAnimationFrame(revealLine);
      } else {
        window.requestAnimationFrame(reveal);
      }
      showQueryPrediction();
    }, 140);
  }

  function onControlChange(event) {
    setOutputs();
    if (
      event.target === sampleCount ||
      (modelName === "linear" && event.target.id === "noise")
    ) {
      if (modelName === "linear") makeRegressionData();
      else makeMoonData();
    }
    invalidateModel();
  }

  controls.forEach(function (input) {
    input.addEventListener("input", onControlChange);
  });
  fitButton.addEventListener("click", fit);
  if (probabilityTooltip) {
    canvas.addEventListener("pointermove", showProbabilityTooltip);
    canvas.addEventListener("pointerleave", hideProbabilityTooltip);
  }
  canvas.addEventListener("click", function (event) {
    if (modelName !== "knn") return;
    const bounds = canvas.getBoundingClientRect();
    const pixelX = ((event.clientX - bounds.left) / bounds.width) * WIDTH;
    const pixelY = ((event.clientY - bounds.top) / bounds.height) * HEIGHT;
    if (
      pixelX < PLOT.left ||
      pixelX > PLOT.left + plotWidth ||
      pixelY < PLOT.top ||
      pixelY > PLOT.top + plotHeight
    )
      return;
    query = { x: domainX(pixelX), y: domainY(pixelY) };
    draw();
    if (model) showQueryPrediction();
    else detail.textContent = "Fit the model to classify your new point.";
  });

  setOutputs();
  prepareData();
  if (window.ResizeObserver) {
    resizeObserver = new ResizeObserver(resizeCanvas);
    resizeObserver.observe(canvas);
  } else {
    window.addEventListener("resize", resizeCanvas);
  }
  resizeCanvas();
})();

import { useEffect, useRef } from "react";
import Plotly from "plotly.js-dist-min";

function lineTraces(plotData) {
  const traces = [
    {
      x: plotData.x,
      y: plotData.y,
      mode: "lines",
      type: "scatter",
      name: "Function",
      line: { color: "#2563eb", width: 3 },
    },
  ];

  if (plotData.critical_x) {
    traces.push({
      x: plotData.critical_x,
      y: plotData.critical_y,
      mode: "markers",
      type: "scatter",
      name: "Critical Points",
      marker: { size: 10, color: "#f97316" },
    });
  }

  if (plotData.extrema) {
    traces.push({
      x: plotData.extrema.map((point) => point.x),
      y: plotData.extrema.map((point) => point.y),
      mode: "markers",
      type: "scatter",
      name: "Extrema",
      marker: { size: 10, color: "#16a34a" },
    });
  }

  if (plotData.inflections) {
    traces.push({
      x: plotData.inflections.map((point) => point.x),
      y: plotData.inflections.map((point) => point.y),
      mode: "markers",
      type: "scatter",
      name: "Inflection Points",
      marker: { size: 10, color: "#9333ea" },
    });
  }

  return traces;
}

function tracesFor(plotResponse) {
  const plotData = plotResponse.plot_data || {};

  if (plotResponse.plot_type === "line") return lineTraces(plotData);
  if (plotResponse.plot_type === "scatter") return [{ x: plotData.x, y: plotData.y, mode: "markers", type: "scatter", marker: { color: "#2563eb", size: 8 } }];
  if (plotResponse.plot_type === "histogram") return [{ x: plotData.data, type: "histogram", nbinsx: plotData.bins, marker: { color: "#2563eb" } }];
  if (plotResponse.plot_type === "boxplot") return [{ y: plotData.data, type: "box", marker: { color: "#2563eb" } }];
  if (plotResponse.plot_type === "vector") {
    return (plotData.vectors || []).map((vector, index) => ({
      x: [0, vector[0]],
      y: [0, vector[1]],
      mode: "lines+markers",
      type: "scatter",
      name: `Vector ${index + 1}`,
      line: { width: 3 },
    }));
  }

  return [];
}

function layoutFor(plotType) {
  return {
    title: {
      text: plotType ? `${plotType[0].toUpperCase()}${plotType.slice(1)} Plot` : "Plot",
      font: { size: 16 },
    },
    autosize: true,
    margin: { l: 52, r: 24, t: 52, b: 44 },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "#ffffff",
    xaxis: { title: "X", zeroline: true, gridcolor: "#e5e7eb" },
    yaxis: { title: "Y", zeroline: true, gridcolor: "#e5e7eb" },
    showlegend: true,
  };
}

export function PlotDisplay({ plot }) {
  const plotRef = useRef(null);

  useEffect(() => {
    if (!plot || !plotRef.current) return undefined;

    const traces = tracesFor(plot);
    if (traces.length > 0) {
      Plotly.newPlot(plotRef.current, traces, layoutFor(plot.plot_type), { responsive: true, displaylogo: false });
    }

    return () => {
      if (plotRef.current) Plotly.purge(plotRef.current);
    };
  }, [plot]);

  if (!plot) {
    return <div className="empty-state">Plots and graph output will appear here after a plotting operation.</div>;
  }

  if (!plot.plot_data && plot.png) {
    return <img className="plot-image" src={`data:image/png;base64,${plot.png}`} alt="Generated plot" />;
  }

  return <div ref={plotRef} className="plot-canvas" aria-label="Generated plot" />;
}

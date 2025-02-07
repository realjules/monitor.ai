window.mountChainlitWidget({
  chainlitServer: "http://localhost:8000",
});

window.addEventListener("chainlit-call-fn", (e) => {
  const { name, args, callback } = e.detail;
  
  if (name === "update_medical_dashboard") {
    // Update confidence display
    dash_clientside.set_props("confidence-display", {
      children: `Confidence: ${args.confidence_level}`
    });

    // Update finding display
    if (args.prediction && args.prediction.finding) {
      dash_clientside.set_props("finding-display", {
        children: `Finding: ${args.prediction.finding}`
      });
    }

    // Update location display
    if (args.prediction && args.prediction.location) {
      dash_clientside.set_props("location-display", {
        children: `Location: ${args.prediction.location}`
      });
    }

    // Update measurements graph if measurements exist
    if (args.prediction && args.prediction.measurements) {
      // You'll need to implement the graph update logic based on your measurement data structure
      // dash_clientside.set_props("measurements-graph", {...});
    }

    callback("Dashboard updated successfully");
  }
});
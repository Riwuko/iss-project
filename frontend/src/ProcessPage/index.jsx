import React from "react";

import ProcessType from "./processContainer/ProcessType";
import ProcessConfig from "./processContainer/ProcessConfig";
import ProcessController from "./controllerContainer/ProcessController";
import ProcessChart from "./processContainer/ProcessChart";

const ProcessPage = () => {
  return (
    
    <>
      <div className="left-charts-container">
        <h1>Inteligent Control Systems: Process Simulation Project</h1>
        <ProcessType />
        <ProcessController/>
        <ProcessConfig/>
      </div>
      <div className="right-charts-container">
      <ProcessChart/>
      </div>
    </>
  );
};

export default ProcessPage;

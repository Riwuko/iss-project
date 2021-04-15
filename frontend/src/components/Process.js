import React, { useState, useEffect } from "react";

import ProcessType from "./ProcessType";
import ProcessConfig from "./ProcessConfig";
import ProcessController from "./ProcessController";
import ProcessChart from "./ProcessChart";

const Process = () => {
  const [processType, setProcessType] = useState();
  const [processControlValue, setProcessControlValue] = useState();
  const [controllerType, setControllerType] = useState();
  const [simulationConfig, setSimulationConfig] = useState({});
  const [controllerConfig, setControllerConfig] = useState({});
  

  const handleProcessTypeChange = (process, controlValue) => {
    setProcessType(process);
    setProcessControlValue(controlValue);
  };

  const handleSimulationConfigChange = config => {
    setSimulationConfig(config);
  };

  const handleControllerTypeChange = controller => {
    setControllerType(controller);
  };

  const handleControllerConfigChange = config => {
    setControllerConfig(config);
  };
  

  return (
    <>
      <div className="left-charts-container">
        <h1>Inteligent Control Systems: Process Simulation Project</h1>
        <ProcessType 
          onProcessChange={handleProcessTypeChange} 
          />
        <ProcessController 
          stepsCount={simulationConfig.t_steps}
          controlValue={processControlValue}
          onControllerTypeChange={handleControllerTypeChange}
          onControllerConfigChange={handleControllerConfigChange}
        />
        <ProcessConfig
          processType={processType}
          onConfigChange={handleSimulationConfigChange}
        />
      </div>
      
        <ProcessChart
          controlValue={processControlValue}
          processType={processType}
          controllerType={controllerType}
          controllerConfig={controllerConfig}
          simulationConfig={simulationConfig}
          />

    </>
  );
};

export default Process;

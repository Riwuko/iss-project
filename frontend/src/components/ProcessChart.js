import React, { useState, useEffect } from "react";
import { getProcess } from "../services/process";

import Navbar from "../components/Navbar";
import ProcessConfig from "../components/ProcessConfig";
import Chart from "../components/Chart";

const ProcessChart = () => {
  const [simulationResults, setSimulationResults] = useState([]);
  const [processType, setProcessType] = useState();
  const [simulationConfig, setSimulationConfig] = useState({});

  const handleProcessTypeChange = (process) => {
    setProcessType(process);
  };

  const handleButtonChange = (config) => {
    setSimulationConfig(config);
  };

  useEffect(() => {
    console.log(processType, simulationConfig);
    if (processType) {
      getProcess(processType, simulationConfig).then((items) => {
        setSimulationResults(items);
      });
    }
  }, [processType, simulationConfig]);

  return (
    <>
      <div className="left-charts-container">
        <h1>Inteligent Control Systems: Process Simulation Project</h1>
        <Navbar onChange={handleProcessTypeChange} />
        <ProcessConfig
          processType={processType}
          onButtonChange={handleButtonChange}
        />
      </div>
      <div className="right-charts-container">
        {simulationResults.map((item) => {
          return (
            <div>
              <Chart
                labels={item.times}
                label={item.name}
                data={item.results}
                title={item.title}
              />
            </div>
          );
        })}
      </div>
    </>
  );
};

export default ProcessChart;

import React, { useState, useEffect } from "react";
import { getProcess } from "../services/processService";

import Chart from "./Chart";


const separateData = (items, controlValueName) => {
  const isInput = ([name,]) => name.includes("input");
  const isControlValue = ([name,]) => name.includes(controlValueName)
  const isSetPoint = ([name,]) => name.includes("set_points")


  const [, controlValue] = Object.entries(items).find(isControlValue)
  const inputValves = Object.entries(items).filter(isInput).map(([, item]) => item);
  const results = Object.entries(items).filter(entry => !(isControlValue(entry) || isInput(entry) || isSetPoint(entry))).map(([, item]) => item);
  const setPoints = Object.entries(items).filter(entry => isSetPoint(entry)).map(([,item]) => item);
  return [ controlValue, inputValves, results, setPoints ];
}

const ProcessChart = props => {
    const [controlValueData, setControlValueData] = useState();
    const [simulationResults, setSimulationResults] = useState([]);
    const [inputValvesData, setInputValvesData] = useState([]);
    const [setPointsData, setSetPointsData] = useState();

    useEffect(async () => {
      const items = await getProcess(props.processType, props.simulationConfig, props.controllerType, props.controllerConfig);

      if(props.controlValue) {
        const [ controlValue, inputValvesData, simulationResults, setPoints] = separateData(items, props.controlValue);
        setControlValueData(controlValue);
        setSimulationResults(simulationResults);
        setInputValvesData(inputValvesData);
        setSetPointsData(...setPoints);
      }
    }, [props.processType, props.simulationConfig, props.controllerType, props.controllerConfig]);


    const prepareInputsData = () => {
        let title;
        let labels;
        const inputs = inputValvesData.map((property) => {  
            title = property.title;
            labels = property.times;
            return {label: property.name, fill: false, data: property.results};
        });
        return(
              <Chart
                labels={labels}
                title={title}
                datasets={inputs}
              />
        )
    };

    const prepareControlValueData = () => {
      const controlValueDataSet = [] 
      if (setPointsData)
        controlValueDataSet.push({
          label: "set points",
          fill: false,
          data: setPointsData.values
        })
      controlValueDataSet.push({
        label: controlValueData?.name,
        data: controlValueData?.results
      })
      return(
            <Chart
              labels={controlValueData?.times}
              title={controlValueData?.name}
              datasets={controlValueDataSet}
            />
      )
    };

    return (
        <div className="right-charts-container">
          <div>
          {prepareControlValueData()}
          </div>
        {simulationResults.map(property => {  
          return(
            <div>
              <Chart
                labels={property.times}
                title={property.title}
                datasets={[{label: property.name, data:property.results}]}
              />
            </div>
        )
        })}
        <div>
            {prepareInputsData()}
        </div>

    </div>

  );
};

export default ProcessChart;

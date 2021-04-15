import React, { useEffect, useState } from "react";
import { getControllerList } from "../services/processService";
import ProcessControllerConfig from "./ProcessControllerConfig";

const ProcessController = props => {
  const [controllers, setControllers] = useState([]);
  const [controllerType, setControllerType] = useState();


  useEffect(() => {
    getControllerList().then((items) => {
      setControllers(items);
    });
  }, []);

  const handleControllerTypeChange = (event) => {
    setControllerType(event.target.value);
    props.onControllerTypeChange(event.target.value);
  }

  const handleControllerConfigChange = (config) => {
    props.onControllerConfigChange(config);
  }

  const generateSelectOptions = () => {
    return(
      <select className="select-wide-grayed" onChange={handleControllerTypeChange} >
      <option value="" selected >No controller</option>
      {controllers.map((item) => (
        <option key={item.model_slug} value={item.model_slug}>
          {item.model_name.toUpperCase()}
        </option>
      ))}
    </select>
    )
  }

  return (
    <div className="controller-container">
     {generateSelectOptions()}
      <ProcessControllerConfig
          stepsCount={props.stepsCount}
          controlValue={props.controlValue}
          controllerType={controllerType}
          onConfigChange={handleControllerConfigChange}
        />
    </div>
  );
};

export default ProcessController;

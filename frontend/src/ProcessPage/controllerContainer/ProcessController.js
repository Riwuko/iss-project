import React, { useEffect, useState } from "react";
import { getControllerList } from "../../services/processService";
import ProcessControllerConfig from "./ProcessControllerConfig";
import ProcessControllerTuner from "../tunerContainer/ProcessControllerTuner";
import SelectOptions from "../sharedComponents/SelectOptions";

import { useActionDispatcher } from "../actions";

const ProcessController = () => {
  const [controllers, setControllers] = useState([]);
  const { setControllerType } = useActionDispatcher();


  useEffect(() => {
    getControllerList().then((items) => {
      setControllers(items);
    });
  }, []);

  const handleControllerTypeChange = (controller) => {
    setControllerType(controller);
  };


  return (
    <div className="controller-container">
      <SelectOptions 
        items={controllers} 
        handleChange={handleControllerTypeChange} 
        defaultValue={"No controller"}/>
      <ProcessControllerTuner />
      <ProcessControllerConfig/>
    </div>
  );
};



export default ProcessController;

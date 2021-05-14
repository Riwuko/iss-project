import React, { useEffect, useState } from "react";
import { getTunerList } from "../services/processService";

const ProcessControllerTuner = (props) => {
  const [tuners, setTuners] = useState([]);
  const [currentValue, setCurrentValue] = useState();

  const controllerType = props.controllerType;

  useEffect(() => {
    getTunerList().then((items) => {
      setTuners(items);
    });
  }, []);

  const handleTunerTypeChange = (event) => {
    const value = event.target.checked ? event.target.value : "";
    setCurrentValue(value);
    props.onTunerTypeChange(value);
  };

  return (
    <div className="tuner-container">
      Add tuning method:
      {!!controllerType && (
        tuners.map((item) => (
          <div>
            <input
              type="checkbox"
              key={item.model_slug}
              checked={item.model_slug === currentValue}
              value={item.model_slug}
              onClick={handleTunerTypeChange}
            />
            {item.model_name.toUpperCase()}
          </div>
        ))
      )}
    </div>
  );
};


export default ProcessControllerTuner;

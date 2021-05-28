import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { getTunerList } from "../../services/processService";
import { useActionDispatcher } from "../actions";
import { selectTunerType, selectControllerType } from "../selectors";
import ProcessControllerTunerConfig from "./ProcessControllerTunerConfig";

const ProcessControllerTuner = () => {
  const [tuners, setTuners] = useState([]);
  const tunerType = useSelector(selectTunerType);
  const { setTunerType } = useActionDispatcher();
  const controllerType = useSelector(selectControllerType);

  useEffect(() => {
    getTunerList().then((items) => {
      setTuners(items);
    });
  }, []);

  const handleTunerTypeChange = (event) => {
    const value = event.target.checked ? event.target.value : "";
    setTunerType(value);
  };

  return (
  <div>{
      controllerType && 
        tuners.map((item, i) => (
          <div className='tuner-container' key={i}>
            <div>Add tuning method:</div>
            <div>
              <input
                type="checkbox"
                key={item.model_slug}
                checked={item.model_slug === tunerType}
                value={item.model_slug}
                onChange={handleTunerTypeChange}
              />
              {item.model_name.toUpperCase()}
            </div>
          </div>
        ))
    }
    <ProcessControllerTunerConfig />
    </div>
      ) 
};


export default ProcessControllerTuner;

import React, { useEffect } from "react";
import { useSelector } from "react-redux";

import { getTunerConfig } from "../../services/processService";
import { selectTunerConfig, selectTunerType } from "../selectors";

import SliderField from "../../shared/SliderField";

import { useActionDispatcher } from "../actions";

const ProcessControllerConfig = () => {
  const tunerConfig = useSelector(selectTunerConfig);
  const tunerType = useSelector(selectTunerType)
  const { setTunerConfig } = useActionDispatcher();


  useEffect(() => {
    if (tunerType) 
      getTunerConfig().then((items) => {
        setTunerConfig(items);
      });
  }, [setTunerConfig, tunerType]);


  const handleSliderChange = (fieldId, value) => {
    const newConfig = tunerConfig;
    newConfig[fieldId] = value;
    setTunerConfig({ ...newConfig })
  };

  return ( 
    <div> {tunerType && 
      <form>
        <SliderField
          label="amplification factor"
          name="amplification_factor"
          defaultValue={tunerConfig?.amplification_factor || 1}
          step={0.1}
          max={40}
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="oscillation period"
          name="oscillation_period"
          defaultValue={tunerConfig?.oscillation_period || 1}
          step={0.1}
          max={40}
          fieldChanged={handleSliderChange}
        />
      </form>
    }</div>
    );

}

export default ProcessControllerConfig;

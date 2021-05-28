import React, { useEffect } from "react";
import { useSelector } from "react-redux";

import { getControllerConfig } from "../../services/processService";
import { selectProcessConfig, selectControllerType, selectControllerConfig, selectControlValueName } from "../selectors";

import SliderField from "../../shared/SliderField";

import { useActionDispatcher } from "../actions";

const ProcessControllerConfig = () => {
  const controllerType = useSelector(selectControllerType);
  const controllerConfig = useSelector(selectControllerConfig);
  const { setControllerConfig } = useActionDispatcher();
  const  processConfig = useSelector(selectProcessConfig);
  const stepsCount = processConfig?.steps_count;
  const simulationTime = processConfig?.simulation_time;
  const setPoints = controllerConfig?.set_points;

  useEffect(() => {
    if (simulationTime && stepsCount)
      getControllerConfig(stepsCount, simulationTime).then((items) => {
        setControllerConfig(items);
      });
  }, [stepsCount, simulationTime, controllerType, setControllerConfig]);

  

  const handleSliderChange = (fieldId, value) => {
    const newConfig = controllerConfig;
    newConfig[fieldId] = value;
    setControllerConfig({ ...newConfig })
  };

  
  const controllerForm = {
    pid: [<PControllerConfig handleSliderChange={handleSliderChange} key="P"/>, 
      <IControllerConfig handleSliderChange={handleSliderChange} key="I"/>, 
      <DControllerConfig handleSliderChange={handleSliderChange} key="D"/>],
  };


    return ( 
    <div> {controllerType && 
      <form>
        {setPoints?.map((item, index) => {
          return( 
            <SetPointsSliderField
              item={item}
              index={index}
              key={index}
              stepsCount={stepsCount}
            />
        )
        })}
        <SliderField
          label="minimum input valve open [%]"
          name="min_value"
          defaultValue={0}
          max={100}
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="maximum input valve open [%]"
          name="max_value"
          defaultValue={100}
          min={controllerConfig?.min_value}
          max={100}
          fieldChanged={handleSliderChange}
        />
        {controllerForm[controllerType]}
      </form>
    }</div>
    );

};

const SetPointsSliderField = ({index, item, stepsCount}) => {
  const controlValueName = useSelector(selectControlValueName);
  const controllerConfig = useSelector(selectControllerConfig);
  const { setControllerConfig } = useActionDispatcher();
  const setPoints = controllerConfig?.set_points;
  const min = index === 0 ? 0 : setPoints[index - 1].range_to;
  const defaultValue = index === 0 ? stepsCount : min;

  const handleAddSetPointsClick = (event) => {
    event.preventDefault();
    const newConfig = controllerConfig;
    newConfig.set_points.push({
      range_to: stepsCount,
      value: 0,
    });
    setControllerConfig({ ...newConfig });
  };

  const handleSetPointsSliderChange = (fieldId, value, index) => {
    const newConfig = controllerConfig;
    newConfig["set_points"][index][fieldId] = parseInt(value);
    setControllerConfig({ ...newConfig })
  };
  
  return (
    <div>
      <div className="row-sliders">
        <SliderField
          label={controlValueName + " set points interval"}
          name="range_to"
          defaultValue={defaultValue}
          index={index}
          min={min}
          max={stepsCount}
          fieldChanged={handleSetPointsSliderChange}
        />
        <SliderField
          label={controlValueName + " set point value"}
          name="value"
          index={index}
          defaultValue={item.value}
          max={100}
          fieldChanged={handleSetPointsSliderChange}
        />
      </div>
      {setPoints.length - 1 === index && (
        <button onClick={handleAddSetPointsClick}>
          Add set points interval
        </button>
      )}
    </div>
  );
};

const PControllerConfig = ({handleSliderChange}) => {
  const controllerConfig = useSelector(selectControllerConfig);
  return (
    <SliderField
      label="Proportional coefficient"
      name="P"
      defaultValue={controllerConfig?.P || 4}
      step={0.1}
      max={20}
      fieldChanged={handleSliderChange}
    />
  );
};
const IControllerConfig = ({handleSliderChange}) => {
  const controllerConfig = useSelector(selectControllerConfig);
  return (
    <SliderField
      label="Integral coefficient"
      name="I"
      defaultValue={controllerConfig?.I || 1}
      step={0.1}
      max={20}
      fieldChanged={handleSliderChange}
    />
  );
};

const DControllerConfig = ({handleSliderChange}) => {
  const controllerConfig = useSelector(selectControllerConfig);
  return (
    <SliderField
      label="Derivative coefficient"
      name="D"
      defaultValue={controllerConfig?.D || 0.2}
      step={0.1}
      max={20}
      fieldChanged={handleSliderChange}
    />
  );
};


export default ProcessControllerConfig;

import React, { useEffect, useState } from "react";
import { getControllerConfig } from "../services/processService";

import SliderField from "./SliderField";

const ProcessControllerConfig = props => {
    const [config, setConfig] = useState({});

    useEffect(() => {
        if (props.stepsCount){
            getControllerConfig(props.stepsCount).then((items) => {
            setConfig(items);
        });
    }}, [props.stepsCount, props.controllerType]);
  
    useEffect(() => {
      props.onConfigChange(config);
    }, [config]);

    const handleAddSetPointsClick = () => {
      let setPoints = config;
      setPoints.set_points.push({
        "range_to": props.stepsCount,
        "value": 0,
        })
      setConfig(setPoints);
      props.onConfigChange({ ...setPoints });
    };

    const handleSetPointsSliderChange = (fieldId, value, index) => {
      setConfig((currentValues) => {
        currentValues['set_points'][index][fieldId] = parseInt(value);
        return { ...currentValues };
      });
    }

    const handleSliderChange = (fieldId, value) => {

        setConfig((currentValues) => {
          currentValues[fieldId] = parseInt(value);
          return { ...currentValues };
        });
      };

    
    const PControllerConfig = () => {
      return (
          <SliderField
              label="Proportional coefficient"
              name="P"
              defaultValue="4"
              step={0.1}
              max={20}
              fieldChanged={handleSliderChange}
            />
      )
    }
    const IControllerConfig = () => {
      return (
          <SliderField
              label="Integral coefficient"
              name="I"
              defaultValue="1"
              step={0.1}
              max={20}
              fieldChanged={handleSliderChange}
            />
      )
    }

    const DControllerConfig = () => {
      return (
          <SliderField
              label="Derivative coefficient"
              name="D"
              defaultValue="0.2"
              step={0.1}
              max={20}
              fieldChanged={handleSliderChange}
            />
      )
    }

    const controllerForm = {
      "pid": [PControllerConfig(), IControllerConfig(), DControllerConfig()],
    } 
    
    const setPointsForm = (index, item) => {
      const min = index===0? 0 : config.set_points[index-1].range_to;
      const defaultValue = index===0? props.stepsCount : min;
      return(
      <div>
        <div className='row-sliders'>
              <SliderField
                label={props.controlValue+" set points interval"}
                name="range_to"
                defaultValue={defaultValue}
                index={index}
                min={min}
                max={props.stepsCount}
                fieldChanged={handleSetPointsSliderChange}
              />
              <SliderField
                label={props.controlValue+" set point value"}
                name="value"
                index={index}
                defaultValue={item.value}
                max="100"
                fieldChanged={handleSetPointsSliderChange}
              />
              </div>
            {config.set_points.length - 1 === index && ( 
              <button onClick={() => handleAddSetPointsClick()} >
                Add set points interval
            </button> ) }
    </div>
      )
    }

    const commonConfigForm = () => {
        if (!!props.controllerType){
        return (
          <form>
            {config?.set_points?.map((item, index) => {
              return setPointsForm(index, item);
        })}
            <SliderField
              label="minimum input valve open [%]"
              name="min_value"
              defaultValue="0"
              max="100"
              fieldChanged={handleSliderChange}
            />
            <SliderField
              label="maximum input valve open [%]"
              name="max_value"
              defaultValue="100"
              min={config.min_value}
              max="100"
              fieldChanged={handleSliderChange}
            />

          {controllerForm[props.controllerType]}

          </form>
        );
      };
    };

    return <div>{commonConfigForm()}</div>;
}

export default ProcessControllerConfig;

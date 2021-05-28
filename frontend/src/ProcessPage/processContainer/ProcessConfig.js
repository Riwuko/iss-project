import React, { useEffect } from "react";
import { useSelector } from "react-redux";

import { getConfig } from "../../services/processService";

import SliderField from "../../shared/SliderField";
import ProcessConcentrationConfig from "./ProcessConcentrationConfig";
import ProcessTankFillingConfig from "./ProcessTankFillingConfig";
import { selectProcessType, selectProcessConfig } from "../selectors";
import { useActionDispatcher } from "../actions";

const ProcessConfig = () => {
  const processType = useSelector(selectProcessType);
  const processConfig = useSelector(selectProcessConfig);
  const { setProcessConfig } = useActionDispatcher();
  const outputValves = processConfig?.valves_config.output_valves;

  useEffect(() => {
    getConfig().then((items) => {
      setProcessConfig(items);
    });
  }, [setProcessConfig]);

  const handleAddInputValveClick = (newValve) => {
    let valvesList = processConfig;
    valvesList.valves_config.input_valves.push(newValve);
    setProcessConfig({ ...valvesList });
  };

  const handleRemoveInputValveClick = (e, index) => {
    e.preventDefault();
    let valvesList = processConfig;
    valvesList.valves_config.input_valves.splice(index, 1);
    setProcessConfig({ ...valvesList });
  };

  const handleSliderChange = (fieldId, value) => {
    const newConfig = processConfig;
    newConfig[fieldId] = value;
    setProcessConfig({ ...newConfig });
    };

  const handleSliderValveChange = (fieldId, value, index, valvesType) => {
    const newConfig = processConfig;
    newConfig["valves_config"][valvesType][index][fieldId] = value;
    setProcessConfig({ ...newConfig });
  };

  
  const processForm = {
    "concentration-model": (
      <ProcessConcentrationConfig
        handleSliderChange={handleSliderChange}   
        handleValveChange={handleSliderValveChange}
        handleAddValve={handleAddInputValveClick}
        handleRemoveValve={handleRemoveInputValveClick}
      />
    ),
    "tank-filling-model": (
      <ProcessTankFillingConfig
        handleValveChange={handleSliderValveChange}
        handleAddValve={handleAddInputValveClick}
        handleRemoveValve={handleRemoveInputValveClick}
      />
    ),
  };

  return <div className="form-wrapper">{
    processConfig && (
      <form>
        <SliderField
          label="tank area [dm²]"
          name="tank_area"
          max={500}
          min={1}
          defaultValue={processConfig.tank_area}
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="simulation time [s]"
          name="simulation_time"
          defaultValue={processConfig.simulation_time}
          max={400}
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="steps count"
          name="steps_count"
          max={200}
          defaultValue={processConfig.steps_count}
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="initial liquid level [dm]"
          name="initial_liquid_level"
          defaultValue={processConfig.initial_liquid_level}
          max={50}
          fieldChanged={handleSliderChange}
        />

        {processForm[processType]}

        {outputValves?.map((item, index) => {
          return (
            <OutputValveForm
            key={index}
            index={index}
            item={item}
            handleChange={handleSliderValveChange}
            />
          )
        })}
      </form>)
  }</div>;
};

const OutputValveForm = ({index, item, handleChange}) => {
  const { processConfig } = useSelector(selectProcessConfig);
  const { setProcessConfig } = useActionDispatcher();
  const outputValves = processConfig?.valves_config.output_valves;
  const newValveElement = {
    valve_capacity: 0,
    valve_open_percent: 0,
  };
  const labels = {
    capacityLabel: "output valve " + index + " capacity [dm³/s]",
    openLabel: "output valve " + index + " open percentage [%]",
  };

  const handleAddOutputValveClick = () => {
    let valvesList = processConfig;
    valvesList?.valves_config.output_valves.push(newValveElement);
    setProcessConfig({ ...valvesList });
  };

  const handleRemoveOutputValveClick = (e, index) => {
    e.preventDefault();
    let valvesList = processConfig;
    valvesList?.valves_config.output_valves.splice(index, 1);
    setProcessConfig({ ...valvesList });
  };

  return (
    <div className="valve-container">
      <div className="row-elements">
        <div className="column-elements">
          <SliderField
            label={labels.capacityLabel}
            index={index}
            name="valve_capacity"
            min={1}
            max={10}
            step={0.5}
            defaultValue={item?.valve_capacity || 0}
            valvesType="output_valves"
            fieldChanged={handleChange}
          />
          <SliderField
            label={labels.openLabel}
            index={index}
            name="valve_open_percent"
            max={100}
            defaultValue={item?.valve_open_percent || 0}
            valvesType="output_valves"
            fieldChanged={handleChange}
          />
        </div>
        {outputValves?.length !== 1 && (
          <button
            className="remove-button"
            onClick={(e) => handleRemoveOutputValveClick(e, index)}
          ></button>
        )}
      </div>
      {outputValves?.length - 1 === index && (
        <button onClick={handleAddOutputValveClick}>
          Add output valve
        </button>
      )}
    </div>
  );
};

export default ProcessConfig;

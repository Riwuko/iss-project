import React, { useEffect, useState } from "react";
import { getConfig } from "../services/processService";

import SliderField from "../components/SliderField";
import ProcessConcentrationConfig from "../components/ProcessConcentrationConfig";
import ProcessTankFillingConfig from "../components/ProcessTankFillingConfig";

const ProcessConfig = (props) => {
  const [config, setConfig] = useState({});
  const newOutputValveElement = {
    valve_capacity: "0",
    valve_open_percent: "0",
  };

  useEffect(() => {
    getConfig().then((items) => {
      setConfig(items);
    });
  }, []);

  useEffect(() => {
    props.onConfigChange(config);
  }, [config]);

  const updateValveList = (valvesList) => {
    setConfig(valvesList);
    props.onConfigChange({ ...valvesList });
  };

  const handleAddInputValveClick = (newValve) => {
    let valvesList = config;
    valvesList.valves_config.input_valves.push(newValve);
    updateValveList(valvesList);
  };

  const handleAddOutputValveClick = (newValve) => {
    let valvesList = config;
    valvesList.valves_config.output_valves.push(newValve);
    updateValveList(valvesList);
  };

  const handleRemoveInputValveClick = (index) => {
    let valvesList = config;
    valvesList.valves_config.input_valves.splice(index, 1);
    updateValveList(valvesList);
  };

  const handleRemoveOutputValveClick = (index) => {
    let valvesList = config;
    valvesList.valves_config.output_valves.splice(index, 1);
    updateValveList(valvesList);
  };

  const handleSliderChange = (fieldId, value) => {
    setConfig((currentValues) => {
      currentValues[fieldId] = value;
      return { ...currentValues };
    });
  };

  const handleSliderValveChange = (fieldId, value, index, valvesType) => {
    setConfig((currentValues) => {
      currentValues["valves_config"][valvesType][index][fieldId] = value;
      return { ...currentValues };
    });
  };

  const outputValveForm = (index, item = null) => {
    const labels = {
      capacityLabel: "output valve " + index + " capacity [dm³/s]",
      openLabel: "output valve " + index + " open percentage [%]",
    };
    return (
      <div className="valve-container">
        <div className="row-elements">
          <div className="column-elements">
            <SliderField
              label={labels.capacityLabel}
              index={index}
              name="valve_capacity"
              min="1"
              max="10"
              step="0.5"
              defaultValue={item ? item.valve_capacity : "0"}
              valvesType="output_valves"
              fieldChanged={handleSliderValveChange}
            />
            <SliderField
              label={labels.openLabel}
              index={index}
              name="valve_open_percent"
              max="100"
              defaultValue={item ? item.valve_open_percent : "0"}
              valvesType="output_valves"
              fieldChanged={handleSliderValveChange}
            />
          </div>
          {config.valves_config.output_valves.length !== 1 && (
            <button
              className="remove-button"
              onClick={() => handleRemoveOutputValveClick(index)}
            ></button>
          )}
        </div>
        {config.valves_config.output_valves.length - 1 === index && (
          <button
            onClick={() => handleAddOutputValveClick(newOutputValveElement)}
          >
            Add output valve
          </button>
        )}
      </div>
    );
  };

  const processForm = {
    "concentration-model": (
      <ProcessConcentrationConfig
        handleInput={setConfig}
        config={config}
        handleSliderChange={handleSliderChange}
        handleSliderValveChange={handleSliderValveChange}
        handleAddInputValve={handleAddInputValveClick}
        handleRemoveInputValve={handleRemoveInputValveClick}
      />
    ),
    "tank-filling-model": (
      <ProcessTankFillingConfig
        handleInput={setConfig}
        config={config}
        handleSliderChange={handleSliderChange}
        handleSliderValveChange={handleSliderValveChange}
        handleAddInputValve={handleAddInputValveClick}
        handleRemoveInputValve={handleRemoveInputValveClick}
      />
    ),
  };

  const commonConfigForm = () => {
    return (
      <form>
        <SliderField
          label="tank area [dm²]"
          name="tank_area"
          max="500"
          min="1"
          defaultValue={config.tank_area}
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="simulation time [s]"
          name="simulation_time"
          defaultValue={config.simulation_time}
          max="400"
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="steps count"
          name="t_steps"
          max="200"
          defaultValue={config.t_steps}
          fieldChanged={handleSliderChange}
        />
        <SliderField
          label="initial liquid level [dm]"
          name="initial_liquid_level"
          defaultValue={config.initial_liquid_level}
          max="50"
          fieldChanged={handleSliderChange}
        />

        {processForm[props.processType]}

        {config?.valves_config?.output_valves?.map((item, index) => {
          return outputValveForm(index, item);
        })}
      </form>
    );
  };

  return <div className="form-wrapper">{commonConfigForm()}</div>;
};

export default ProcessConfig;

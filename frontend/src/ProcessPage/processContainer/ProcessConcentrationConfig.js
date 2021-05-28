import React from "react";
import { useSelector } from "react-redux";

import SliderField from "../../shared/SliderField";
import { selectProcessConfig } from "../selectors";
import { useActionDispatcher } from "../actions";


const ProcessConcentrationConfig = (props) => {
  const processConfig = useSelector(selectProcessConfig);
  const inputValves = processConfig?.valves_config.input_valves

  return (
    <div>
      <SliderField
        label="initial liquid concentration of A [%]"
        name="initial_liquid_concentration_A"
        max={100}
        defaultValue={processConfig?.initial_liquid_concentration_A}
        fieldChanged={props.handleSliderChange}
      />
      {inputValves?.map((item, index) => {
        return (
          <InputValveForm
            key={index}
            index={index}
            item={item}
            inputValves={inputValves}
            handlers={props}
          />
        )
      })}
    </div>
  );
};

const InputValveForm = ({index, item, inputValves, handlers}) => {
  const new_valve_element = {
    valve_capacity: 0,
    valve_open_percent: 0,
    liquid_config: { liquid_concentration_A: 0 },
  };
  const labels = {
    capacityLabel: "input valve " + index + " capacity [dm³/s]",
    openLabel: "input valve " + index + " open percentage [%]",
    concentrationLabel:
      "input valve " + index + " liquid A concentration [%]",
  };
  const processConfig = useSelector(selectProcessConfig);
  const { setProcessConfig } = useActionDispatcher();

  const handleConcentrationValveChange = (fieldId, value, index) => {
    const newConfig = processConfig;
    newConfig["valves_config"]["input_valves"][index]["liquid_config"][fieldId] = value;
    setProcessConfig({ ...newConfig });
  };

  return (
    <div className="valve-container">
      <div className="row-elements">
        <div className="column-elements">
          <SliderField
            label={labels.capacityLabel}
            index={index}
            name="valve_capacity"
            max={10}
            step={0.5}
            min={1}
            defaultValue={item?.valve_capacity || 0}
            fieldChanged={handlers.handleValveChange}
          />
          <SliderField
            label={labels.openLabel}
            index={index}
            name="valve_open_percent"
            max={100}
            defaultValue={item?.valve_open_percent || 0}
            fieldChanged={handlers.handleValveChange}
          />
          <SliderField
            label={labels.concentrationLabel}
            index={index}
            liquid_config={true}
            max={100}
            name="liquid_concentration_A"
            defaultValue={item?.liquid_config?.liquid_concentration_A || 0 }
            fieldChanged={handleConcentrationValveChange}
          />
        </div>
        {inputValves?.length !== 1 && (
          <button
            className="remove-button"
            onClick={(e) => handlers.handleRemoveValve(e, index)}
          ></button>
        )}
      </div>
      {inputValves?.length - 1 === index && (
        <button onClick={() => handlers.handleAddValve(new_valve_element)}>
          Add input valve
        </button>
      )}
    </div>
  );
};

export default ProcessConcentrationConfig;

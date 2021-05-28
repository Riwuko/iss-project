import React from "react";
import { useSelector } from "react-redux";

import SliderField from "../../shared/SliderField";

import { selectProcessConfig } from "../selectors";

const ProcessTankFillingConfig = (props) => {
  const processConfig = useSelector(selectProcessConfig);
  const inputValves = processConfig?.valves_config.input_valves
  
  return (
      inputValves?.map((item, index) => {
        return (
        <InputValveForm
          key={index}
          index={index}
          item={item}
          inputValves={inputValves}
          handlers={props}
        />
        )
      })
  );
};

const InputValveForm = ({ index, item, inputValves, handlers }) => {
  const new_valve_element = { valve_capacity: 0, valve_open_percent: 0 };
  const labels = {
    capacityLabel: "input valve " + index + " capacity [dm³/s]",
    openLabel: "input valve " + index + " open percentage [%]",
  };

  return (
    <div className="valve-container">
      <div className="row-elements">
        <div className="column-elements">
          <SliderField
            label={labels.capacityLabel}
            index={index}
            max={10}
            step={0.5}
            min={1}
            name="valve_capacity"
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

export default ProcessTankFillingConfig;

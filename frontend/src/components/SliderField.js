import React, { useEffect, useState } from "react";

const SliderField = ({
  label,
  fieldChanged,
  name,
  index = null,
  defaultValue = 10,
  min = 0,
  max = 10,
  step = 1,
  valvesType = "input_valves",
}) => {
  const [sliderValue, setSliderValue] = useState(defaultValue);

  useEffect(() => {
    setSliderValue(defaultValue);
  }, [defaultValue]);

  const setSliderValueInput = (e) => {
    setSliderValue(e.target.value);
  };

  return (
    <div className="input-container">
      <label>{label}</label>
      <div>
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={sliderValue}
          onChange={(e) => setSliderValueInput(e)}
          onMouseUp={(e) =>
            fieldChanged(name, e.target.value, index, valvesType)
          }
        />
        <span>{sliderValue}</span>
      </div>
    </div>
  );
};

export default SliderField;

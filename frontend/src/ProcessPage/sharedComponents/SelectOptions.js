import React from "react";

const SelectOptions = ({items, handleChange, defaultValue=""}) => {
    return (
      <select
        className="select-wide-grayed"
        onChange={(e) => handleChange(e.target.value)}
        defaultValue=""
      >

        {defaultValue && <option value="">{defaultValue}</option>}
        {items.map((item) => (
          <option key={item.model_slug} value={item.model_slug}>
            {item.model_name.toUpperCase()}
          </option>
        ))}
      </select>
    );
  };

export default SelectOptions;

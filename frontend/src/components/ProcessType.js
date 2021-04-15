import React, { useEffect, useState } from "react";
import { getList } from "../services/processService";

const ProcessType = props => {
  const [processes, setProcesses] = useState([]);

  const handleProcessChange = event => {
    props.onProcessChange(event.target.value, event.target.selectedOptions[0].getAttribute('control-value'));
  };

  useEffect(() => {
    getList().then((items) => {
        setProcesses(items);
        props.onProcessChange(items[0].model_slug, items[0].control_value);
    });
  }, []);

  return (
    <div className="navbar-container">
      <select className="select-wide" onChange={handleProcessChange}>
        {processes.map((item) => (
          <option key={item.model_slug} value={item.model_slug} control-value={item.control_value}>
            {item.model_name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ProcessType;

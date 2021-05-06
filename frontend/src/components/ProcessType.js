import React, { useEffect, useState } from "react";
import { getList } from "../services/processService";

const findItemBySlug = (items, slug) =>
  items.find((i) => i.model_slug === slug);

const ProcessType = (props) => {
  const [processes, setProcesses] = useState([]);

  const handleProcessChange = (event) => {
    const { model_slug, control_value } = findItemBySlug(
      processes,
      event.target.value
    );

    props.onProcessChange(model_slug, control_value);
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
          <option key={item.model_slug} value={item.model_slug}>
            {item.model_name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ProcessType;

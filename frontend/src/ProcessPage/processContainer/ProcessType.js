import React, { useEffect, useState } from "react";

import { getList } from "../../services/processService";
import { useActionDispatcher } from "../actions";
import SelectOptions from "../sharedComponents/SelectOptions";

const findItemBySlug = (items, slug) =>
  items.find((i) => i.model_slug === slug);


const ProcessType = () => {
  const [processes, setProcesses] = useState([]);
  const { setProcessType } = useActionDispatcher();
  const { setControlValueName } = useActionDispatcher();

  const setProcessAndControlValueName = (processSlug, controlValueName) => {
    setProcessType(processSlug);
    setControlValueName(controlValueName);
  }

  const handleProcessChange = (slug) => {
    const { model_slug, control_value } = findItemBySlug(
      processes,
      slug,
    );
    setProcessAndControlValueName(model_slug, control_value);
  };

  useEffect(() => {
    getList().then((items) => {
      setProcesses(items);
      setProcessAndControlValueName(items[0].model_slug, items[0].control_value);
    });
  }, []);

  return (
    <div className="navbar-container">
      <SelectOptions items={processes} handleChange={handleProcessChange}/>
    </div>
  );
};

export default ProcessType;

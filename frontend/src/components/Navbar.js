import React, { useEffect, useState } from "react";
import { getList } from "../services/process";

const Navbar = (props) => {
  const [processes, setProcesses] = useState([]);

  const handleChange = (event) => {
    props.onChange(event.target.value);
  };

  useEffect(() => {
    let mounted = true;
    getList().then((items) => {
      if (mounted) {
        setProcesses(items);
        props.onChange(items[0].process_slug);
      }
    });
    return () => (mounted = false);
  }, []);

  return (
    <div className="navbar-container">
      <select className="select-wide" onChange={handleChange}>
        {processes.map((item) => (
          <option key={item.process_slug} value={item.process_slug}>
            {item.process_name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default Navbar;

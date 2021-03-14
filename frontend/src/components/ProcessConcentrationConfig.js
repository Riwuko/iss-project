import React from "react";

import SliderField from '../components/SliderField';;

const ProcessConcentrationConfig = (props) => {
    const new_valve_element = {valve_capacity: "0", valve_open_percent: "0", liquid_config: {liquid_concentration_A: 0}}

    const handleSliderConcentrationInputValveChange = (fieldId, value, index) => {
        props.handleInput((currentValues) => {
            currentValues["valves_config"]["input_valves"][index]["liquid_config"][fieldId] = value;
            return {...currentValues};
          });
        };

    const inputValveForm = (index, item=null) => {
        const labels = {
            capacityLabel : "input valve "+index+" capacity [dm³/s]",
            openLabel : "input valve "+index+" open percentage [%]",
            concentrationLabel : "input valve "+index+" liquid A concentration [%]",
          }
        return(
            <div className='valve-container'>
                <div className='row-elements'>
                <div className='column-elements'>
                <SliderField 
                    label={labels.capacityLabel}
                    index={index}
                    name="valve_capacity"
                    max="10"
                    step="0.5"
                    min="1"
                    defaultValue={item ? item.valve_capacity : 0}
                    fieldChanged={props.handleSliderValveChange} />
                <SliderField 
                    label={labels.openLabel}
                    index={index}
                    name="valve_open_percent"
                    max="100"
                    defaultValue={item ? item.valve_open_percent : 0}
                    fieldChanged={props.handleSliderValveChange} />
                <SliderField 
                    label={labels.concentrationLabel}
                    index={index}
                    liquid_config={true}
                    max="100"
                    name="liquid_concentration_A"
                    defaultValue={item ? item.liquid_config.liquid_concentration_A : 0}
                    fieldChanged={handleSliderConcentrationInputValveChange} />
                </div>
                    {props.config.valves_config.input_valves.length !== 1 && <button className='remove-button' onClick={() => props.handleRemoveInputValve(index)}></button>}
                </div>
                    {props.config.valves_config.input_valves.length - 1 === (index) && <button onClick={() => props.handleAddInputValve(new_valve_element)}>Add input valve</button>}

            </div> 
        )
    };

    return(
        <div>
            <SliderField 
                label="initial liquid concentration of A [%]"
                name="initial_liquid_concentration_A"
                max="100"
                defaultValue={props.config.initial_liquid_concentration_A}
                fieldChanged={props.handleSliderChange} />
            {props.config?.valves_config?.input_valves?.map((item, index)=>{
            return (
            inputValveForm(index, item)
            )
            }
            )} 
        </div>
            )};
     export default ProcessConcentrationConfig;

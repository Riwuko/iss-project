import React from "react";

import SliderField from '../components/SliderField';;

const ProcessTankFillingConfig = (props) => {
    const new_valve_element = {valve_capacity: "0", valve_open_percent: "0"};
    

    const inputValveForm = (index, item=null) => {
        const labels = {
            capacityLabel : "input valve "+index+" capacity [dm³/s]",
            openLabel : "input valve "+index+" open percentage [%]",
            }
        return(
            <div className='valve-container'>
                <div className='row-elements'>
                <div className='column-elements'>
                <SliderField 
                    label={labels.capacityLabel}
                    index={index}
                    max="10"
                    step="0.5"
                    min="1"
                    name="valve_capacity"
                    defaultValue={item ? item.valve_capacity : "0"}
                    fieldChanged={props.handleSliderValveChange} />
                <SliderField 
                    label={labels.openLabel}
                    index={index}
                    name="valve_open_percent"
                    max="100"
                    defaultValue={item ? item.valve_open_percent : "0"}
                    fieldChanged={props.handleSliderValveChange} />
                </div>
                    {props.config.valves_config.input_valves.length !== 1 && <button className='remove-button' onClick={() => props.handleRemoveInputValve(index)}></button>}
                    </div>
                    {props.config.valves_config.input_valves.length - 1 === (index) && <button onClick={() => props.handleAddInputValve(new_valve_element)}>Add input valve</button>}
                
            </div>
        )
    }


    return( 
        <div>
          {props.config?.valves_config?.input_valves?.map((item, index)=>{
           return ( 
                inputValveForm(index, item)
            )})}
        </div>
            )   

     };
     
     export default ProcessTankFillingConfig;

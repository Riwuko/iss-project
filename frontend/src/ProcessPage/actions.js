import { useMemo } from "react";
import { useDispatch } from "react-redux";
import { ActionTypes } from "./constants";

export const setProcessType = (processType) => ({ type: ActionTypes.SET_PROCESS_TYPE, payload: processType });

export const setProcessConfig = (processConfig) => ({ type: ActionTypes.SET_PROCESS_CONFIG, payload: processConfig });

export const setControllerType = (controllerType) => ({ type: ActionTypes.SET_CONTROLLER_TYPE, payload: controllerType });

export const setControllerConfig = (controllerConfig) => ({ type: ActionTypes.SET_CONTROLLER_CONFIG, payload: controllerConfig });

export const setTunerType = (tunerType) => ({ type: ActionTypes.SET_TUNER_TYPE, payload: tunerType });

export const setTunerConfig = (tunerConfig) => ({ type: ActionTypes.SET_TUNER_CONFIG, payload: tunerConfig });

export const setControlValueName = (controlValueName) => ({ type: ActionTypes.SET_CONTROL_VALUE_NAME, payload: controlValueName });


export const useActionDispatcher = () => {
  const dispatch = useDispatch();
  return useMemo(() => ({
    setProcessType: (processType) => dispatch(setProcessType(processType)),
    setProcessConfig: (processConfig) => dispatch(setProcessConfig(processConfig)),
    setControllerType: (controllerType) => dispatch(setControllerType(controllerType)),
    setControllerConfig: (controllerConfig) => dispatch(setControllerConfig(controllerConfig)),
    setTunerType: (tunerType) => dispatch(setTunerType(tunerType)),
    setTunerConfig: (tunerConfig) => dispatch(setTunerConfig(tunerConfig)),
    setControlValueName: (controlValueName) => dispatch(setControlValueName(controlValueName)),
  }), [dispatch]);
}

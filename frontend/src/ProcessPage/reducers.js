import { ActionTypes } from "./constants"
const defaultState = {};

export default function processPageReducer (state = defaultState, action) {
    switch (action.type) {
        case ActionTypes.SET_PROCESS_TYPE:
            return { ...state, processType: action.payload };
        case ActionTypes.SET_PROCESS_CONFIG:
            return { ...state, processConfig: action.payload };
        case ActionTypes.SET_CONTROLLER_TYPE:
            return { ...state, controllerType: action.payload };
        case ActionTypes.SET_CONTROLLER_CONFIG:
            return { ...state, controllerConfig: action.payload };
        case ActionTypes.SET_TUNER_TYPE:
            return { ...state, tunerType: action.payload };
        case ActionTypes.SET_TUNER_CONFIG:
            return { ...state, tunerConfig: action.payload };
        case ActionTypes.SET_CONTROL_VALUE_NAME:
            return { ...state, controlValueName: action.payload };
        default:
            return state;
    }
}

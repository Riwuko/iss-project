import { createSelector } from "reselect";

const processPageState = (state) => state.processPage;

export const selectProcessType = createSelector(
    processPageState, 
    (processPage) => processPage.processType
);
  

export const selectProcessConfig = createSelector(
    processPageState,
    (processPage) => processPage.processConfig
);
  

export const selectControllerType = createSelector(
    processPageState,
    (processPage) => processPage.controllerType
);


export const selectControllerConfig = createSelector(
    processPageState,
    (processPage) => processPage.controllerConfig
);

export const selectTunerType = createSelector(
    processPageState,
    (processPage) => processPage.tunerType
);


export const selectControlValueName = createSelector(
    processPageState,
    (processPage) => processPage.controlValueName
);

export const selectTunerConfig = createSelector(
    processPageState,
    (processPage) => processPage.tunerConfig
)

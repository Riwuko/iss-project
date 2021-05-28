import { createStore, combineReducers } from "redux";
import processPage from "./ProcessPage/reducers";

const reducers = combineReducers({ processPage });

export default createStore(reducers, {}, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());

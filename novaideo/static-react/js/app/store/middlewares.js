import thunk from 'redux-thunk';
import promiseMiddleware from 'redux-promise-middleware';

const middlewares = [promiseMiddleware(), thunk];

export default middlewares;
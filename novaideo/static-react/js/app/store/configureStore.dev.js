import { createStore, applyMiddleware, compose } from 'redux';
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = {
  key: 'NovaIdeo',
  storage: storage,
  blacklist: ['i18n', 'network', 'adapters', 'search', 'apps']
};

export default function configureStore(initialState, rootReducer, middlewares) {
  const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose; // eslint-disable-line no-underscore-dangle
  return createStore(persistReducer(persistConfig, rootReducer), initialState, composeEnhancers(applyMiddleware(...middlewares)));
}